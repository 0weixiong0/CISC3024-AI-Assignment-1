"""Export the fine-tuned StarNet-S2 EuroSAT checkpoint to ONNX for in-browser inference.

Single graph:
  inputs : image (1,3,224,224 fp32), target one-hot (1,10 fp32)
  outputs: probs (1,10), f0..f3 (per-stage feature maps:
           stages[0] 32x56x56, stages[1] 64x28x28, stages[2] 128x14x14,
           stages[3] 256x7x7), cam (1,1,224,224)

Grad-CAM weights are analytic: with a global-average-pool + linear head, the
gradient of the class score w.r.t. the pre-pool features is spatially constant
and equals the class row of the head weight matrix, so
  cam = ReLU(sum_k (onehot @ W)[k] * A[k]) / max
matches pytorch_grad_cam's output up to the constant factor that normalization
removes. The script verifies parity against PyTorch and against pytorch_grad_cam.
"""
import json
from pathlib import Path

import numpy as np
import onnxruntime as ort
import timm
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image

from train_starnet_eurosat import make_transform

ROOT = Path(__file__).resolve().parent.parent
RUN = ROOT / "runs" / "starnet_s2_eurosat"
OUT = ROOT / "webapp_standalone"


class OnnxStarNet(nn.Module):
    def __init__(self, m):
        super().__init__()
        self.m = m

    def forward(self, x, onehot):
        boxes = []
        hooks = [s.register_forward_hook(lambda mod, i, o: boxes.append(o.detach()))
                 for s in self.m.stages]
        A = self.m.forward_features(x)
        for h in hooks:
            h.remove()
        pooled = self.m.flatten(self.m.global_pool(A))
        logits = self.m.head(pooled)
        probs = torch.softmax(logits, dim=1)
        w = onehot @ self.m.head.weight
        cam = torch.relu((w.view(1, -1, 1, 1) * A).sum(1, keepdim=True))
        cam = F.interpolate(cam, size=(224, 224), mode="bilinear", align_corners=False)
        denom = torch.max(cam, dim=2, keepdim=True).values
        denom = torch.max(denom, dim=3, keepdim=True).values
        cam = cam / (denom + 1e-8)
        return probs, boxes[0], boxes[1], boxes[2], boxes[3], cam


def main():
    torch.manual_seed(42)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    (OUT / "model").mkdir(parents=True, exist_ok=True)

    model = timm.create_model("starnet_s2.in1k", pretrained=False, num_classes=10)
    ckpt = torch.load(RUN / "best.pt", map_location=device, weights_only=False)
    model.load_state_dict(ckpt["model"])
    model.to(device).eval()
    cfg = timm.data.resolve_model_data_config(model)
    tf = make_transform(cfg, train=False)

    wrapper = OnnxStarNet(model).eval()

    x0 = torch.randn(1, 3, 224, 224, device=device)
    with torch.no_grad():
        probs0 = wrapper(x0, torch.zeros(1, 10, device=device))[0]
        ref0 = torch.softmax(model(x0), dim=1)
    assert torch.allclose(probs0, ref0, atol=1e-5), (probs0 - ref0).abs().max()

    x = torch.zeros(1, 3, 224, 224, device=device)
    onehot = torch.zeros(1, 10, device=device)
    onehot[0, 0] = 1
    onnx_path = OUT / "model" / "model.onnx"
    torch.onnx.export(
        wrapper, (x, onehot), str(onnx_path),
        input_names=["image", "target"],
        output_names=["probs", "f0", "f1", "f2", "f3", "cam"],
        opset_version=17,
        dynamo=False,
    )
    print(f"exported {onnx_path} ({onnx_path.stat().st_size / 1e6:.1f} MB)")

    split = json.loads((RUN / "split_indices.json").read_text())
    root = Path(split["dataset_root"])
    picks = [next(p for p in split["test"] if p.startswith(c + "/"))
             for c in ("AnnualCrop", "PermanentCrop", "River")]

    sess = ort.InferenceSession(str(onnx_path), providers=["CPUExecutionProvider"])
    from pytorch_grad_cam import GradCAM
    from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
    cam_extractor = GradCAM(model=model, target_layers=[model.norm])

    classes = split["classes"]
    report = {"opset": 17, "onnx_mb": round(onnx_path.stat().st_size / 1e6, 2),
              "images": []}
    for rel in picks:
        img = Image.open(root / rel).convert("RGB")
        xt = tf(img).unsqueeze(0).to(device)
        with torch.no_grad():
            ref_probs = torch.softmax(model(xt)[0], 0).cpu().numpy()
        on = sess.run(None, {"image": xt.cpu().numpy(),
                             "target": np.zeros((1, 10), np.float32)})
        on_probs, on_feats = on[0], on[1:5]
        pred = int(ref_probs.argmax())
        tgt = np.zeros((1, 10), np.float32)
        tgt[0, pred] = 1.0
        on_cam = sess.run(None, {"image": xt.cpu().numpy(), "target": tgt})[5]
        with torch.no_grad():
            hb = []
            hh = [s.register_forward_hook(lambda m, i, o: hb.append(o.detach().cpu().numpy()))
                  for s in model.stages]
            model(xt)
            for h in hh:
                h.remove()
        gray = cam_extractor(input_tensor=xt,
                             targets=[ClassifierOutputTarget(pred)])[0]
        corr = float(np.corrcoef(gray.ravel(), on_cam[0, 0].ravel())[0, 1])
        top3 = np.argsort(ref_probs)[::-1][:3]
        rec = {
            "path": rel,
            "pred": classes[pred],
            "ref_top3": [{"c": classes[i], "p": round(float(ref_probs[i]), 4)}
                         for i in top3],
            "probs_max_abs_diff": round(float(np.abs(on_probs[0] - ref_probs).max()), 6),
            "cam_corr_vs_pytorch_grad_cam": round(corr, 4),
            "cam_max_abs_diff": round(float(np.abs(gray - on_cam[0, 0]).max()), 4),
        }
        for k, (onf, ref) in enumerate(zip(on_feats, hb)):
            rec[f"f{k}_shape"] = list(ref.shape[1:])
            rec[f"f{k}_max_abs_diff"] = round(float(np.abs(onf[0] - ref[0]).max()), 6)
        report["images"].append(rec)
        print(json.dumps(rec))
    (OUT / "model" / "verification.json").write_text(json.dumps(report, indent=1))

    from matplotlib import colormaps

    def lut(name):
        cm = colormaps[name]
        return [[int(round(c * 255)) for c in cm(i / 255)[:3]] for i in range(256)]

    (OUT / "colormaps.js").write_text(
        "const JET_LUT=" + json.dumps(lut("jet")) + ";\n"
        "const VIRIDIS_LUT=" + json.dumps(lut("viridis")) + ";\n")
    print("colormaps.js written")


if __name__ == "__main__":
    main()
