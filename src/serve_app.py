"""Stage 04 visualization server for the StarNet-S2 EuroSAT experiment.

Stdlib-only HTTP server (no new dependencies). Serves webapp/ plus a JSON API:
  /api/classes      class list with per-split counts + run summary
  /api/samples      image paths filtered by split/class (validated against frozen split)
  /api/image        dataset image bytes (path must exist in the frozen split index)
  /api/predict      model prediction: top-1, 10-class probabilities, GT, correctness
  /api/gradcam      Grad-CAM overlay PNG (base64) for the predicted class
  /api/featuremaps  stage feature-map grid PNG (base64; query params: layer, start)
Model: runs/starnet_s2_eurosat/best.pt loaded once at startup (no network access).
"""
import argparse
import base64
import io
import json
import mimetypes
import threading
from collections import Counter
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import timm
import torch
from PIL import Image
from torchvision.transforms import InterpolationMode

from train_starnet_eurosat import make_transform

WEBAPP = Path(__file__).resolve().parent.parent / "webapp"
CLASSIFIER_TARGETS = None  # imported lazily (pytorch_grad_cam)


class ApiError(Exception):
    def __init__(self, status, message):
        super().__init__(message)
        self.status = status


class App:
    def __init__(self, split_path, ckpt_path, metrics_path):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.split = json.loads(Path(split_path).read_text())
        self.classes = self.split["classes"]
        self.root = Path(self.split["dataset_root"]).resolve()
        self.by_split = {s: sorted(self.split[s]) for s in ("train", "val", "test")}
        self.valid = {p for paths in self.by_split.values() for p in paths}
        self.by_split_class = {
            (s, c): [p for p in self.by_split[s] if Path(p).parent.name == c]
            for s in self.by_split for c in self.classes
        }

        torch.manual_seed(42)
        self.model = timm.create_model("starnet_s2.in1k", pretrained=False, num_classes=len(self.classes))
        ckpt = torch.load(ckpt_path, map_location=self.device, weights_only=False)
        self.model.load_state_dict(ckpt["model"])
        self.model.to(self.device).eval()
        self.ckpt_meta = {"epoch": ckpt["epoch"], "val_acc": ckpt["val_acc"]}
        self.metrics = json.loads(Path(metrics_path).read_text()) if Path(metrics_path).exists() else {}
        self.cfg = timm.data.resolve_model_data_config(self.model)
        self.eval_tf = make_transform(self.cfg, train=False)
        self.lock = threading.Lock()

        from pytorch_grad_cam import GradCAM
        self.cam = GradCAM(model=self.model, target_layers=[self.model.norm])

    def summary(self):
        s = self.metrics
        return {
            "model": "starnet_s2.in1k (fine-tuned)",
            "checkpoint_epoch": self.ckpt_meta["epoch"],
            "checkpoint_val_acc": self.ckpt_meta["val_acc"],
            "test_top1_acc": s.get("test_top1_acc"),
            "test_macro_f1": s.get("test_macro_f1"),
            "device": self.device,
            "normalization": {"mean": self.cfg["mean"], "std": self.cfg["std"]},
        }

    def classes_info(self):
        rows = []
        for c in self.classes:
            rows.append({
                "name": c,
                "train": len(self.by_split_class[("train", c)]),
                "val": len(self.by_split_class[("val", c)]),
                "test": len(self.by_split_class[("test", c)]),
            })
        return {"summary": self.summary(), "classes": rows}

    def samples(self, split, cls, offset, limit):
        if split not in self.by_split:
            raise ApiError(400, f"unknown split {split!r}")
        if cls == "all":
            items = self.by_split[split]
        elif cls in self.classes:
            items = self.by_split_class[(split, cls)]
        else:
            raise ApiError(400, f"unknown class {cls!r}")
        window = items[offset:offset + limit]
        return {"total": len(items), "offset": offset, "items": window}

    def check_path(self, relpath):
        if relpath not in self.valid:
            raise ApiError(404, "path is not in the frozen split index")
        return relpath

    def load_input(self, relpath):
        img = Image.open(self.root / relpath).convert("RGB")
        x = self.eval_tf(img).unsqueeze(0).to(self.device)
        return img, x

    def predict(self, relpath):
        relpath = self.check_path(relpath)
        img, x = self.load_input(relpath)
        with self.lock, torch.no_grad():
            probs = torch.softmax(self.model(x)[0], dim=0).cpu()
        pred = int(probs.argmax())
        gt = Path(relpath).parent.name
        probs_list = [{"c": c, "p": round(float(p), 4)} for c, p in zip(self.classes, probs)]
        probs_list.sort(key=lambda d: -d["p"])
        return {
            "path": relpath, "gt": gt, "pred": self.classes[pred],
            "correct": self.classes[pred] == gt, "probs": probs_list,
            "checkpoint": self.ckpt_meta,
        }

    def gradcam(self, relpath):
        from pytorch_grad_cam.utils.image import show_cam_on_image
        from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
        relpath = self.check_path(relpath)
        img, x = self.load_input(relpath)
        rgb = np.float32(img.resize((224, 224))) / 255.0
        with self.lock:
            with torch.no_grad():
                pred = int(self.model(x).argmax())
            grayscale = self.cam(input_tensor=x, targets=[ClassifierOutputTarget(pred)])
        overlay = show_cam_on_image(rgb, grayscale[0], use_rgb=True)
        return {"png": png_b64(Image.fromarray(overlay)), "pred": self.classes[pred]}

    def featuremaps(self, relpath, layer=1, start=0):
        if not (0 <= layer < len(self.model.stages)):
            raise ApiError(400, f"layer must be 0-{len(self.model.stages) - 1}")
        relpath = self.check_path(relpath)
        _, x = self.load_input(relpath)
        box = {}
        hook = self.model.stages[layer].register_forward_hook(
            lambda m, i, o: box.update(f=o.detach()))
        with self.lock, torch.no_grad():
            self.model(x)
        hook.remove()
        f = box["f"][0].cpu()
        C, H, W = f.shape
        start = max(0, min(start, C - 1))
        k = min(16, C - start)
        fig, axes = plt.subplots(4, 4, figsize=(6, 6))
        for i, ax in enumerate(axes.flat):
            if i < k:
                ch = f[start + i]
                ch = (ch - ch.min()) / (ch.max() - ch.min() + 1e-8)
                ax.imshow(ch, cmap="viridis")
            ax.axis("off")
        fig.suptitle(
            f"stages[{layer}] channels {start}-{start + k - 1} of {C} ({C}x{H}x{W})",
            fontsize=9)
        buf = io.BytesIO()
        fig.tight_layout()
        fig.savefig(buf, format="png", dpi=110)
        plt.close(fig)
        return {"png": base64.b64encode(buf.getvalue()).decode(),
                "layer": layer, "stages": len(self.model.stages),
                "channels": int(C), "hw": [int(H), int(W)], "start": start}


def png_b64(img):
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()


class Handler(BaseHTTPRequestHandler):
    app: App = None

    def log_message(self, fmt, *args):
        pass

    def _send(self, status, body, ctype):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj, status=200):
        self._send(status, json.dumps(obj).encode(), "application/json")

    def do_GET(self):
        parsed = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(parsed.query).items()}
        try:
            if parsed.path == "/api/classes":
                self._json(self.app.classes_info())
            elif parsed.path == "/api/samples":
                offset = max(0, int(q.get("offset", 0)))
                limit = min(200, max(1, int(q.get("limit", 60))))
                self._json(self.app.samples(q.get("split", "test"), q.get("cls", "all"), offset, limit))
            elif parsed.path == "/api/image":
                rel = self.app.check_path(q.get("path", ""))
                data = (self.app.root / rel).read_bytes()
                self._send(200, data, "image/jpeg")
            elif parsed.path == "/api/predict":
                self._json(self.app.predict(q.get("path", "")))
            elif parsed.path == "/api/gradcam":
                self._json(self.app.gradcam(q.get("path", "")))
            elif parsed.path == "/api/featuremaps":
                self._json(self.app.featuremaps(
                    q.get("path", ""),
                    layer=int(q.get("layer", 1)),
                    start=int(q.get("start", 0))))
            else:
                self._static(parsed.path)
        except ApiError as e:
            self._json({"error": str(e)}, e.status)
        except (KeyError, ValueError) as e:
            self._json({"error": f"bad request: {e}"}, 400)

    def _static(self, route):
        if route == "/":
            route = "/index.html"
        p = (WEBAPP / route.lstrip("/")).resolve()
        if not (p.is_relative_to(WEBAPP) and p.is_file()):
            self._json({"error": "not found"}, 404)
            return
        ctype = mimetypes.guess_type(str(p))[0] or "application/octet-stream"
        self._send(200, p.read_bytes(), ctype)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", default="runs/starnet_s2_eurosat/split_indices.json")
    ap.add_argument("--ckpt", default="runs/starnet_s2_eurosat/best.pt")
    ap.add_argument("--metrics", default="runs/starnet_s2_eurosat/metrics.json")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8000)
    args = ap.parse_args()

    Handler.app = App(args.split, args.ckpt, args.metrics)
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"serving on http://{args.host}:{args.port}  (device={Handler.app.device})")
    server.serve_forever()


if __name__ == "__main__":
    main()
