"""Fine-tune StarNet-S2 on EuroSAT using the frozen stratified split.

Protocol (Stage 02 design): SGD lr=1e-3 momentum=0.9, StepLR(7, 0.1), 25 epochs,
batch 64, native AMP, seed 42. Transfer learning: pretrained ImageNet-1k backbone,
randomly initialized 10-class head.
"""
import argparse
import json
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import timm
import torch
from PIL import Image
from sklearn.metrics import (
    confusion_matrix,
    f1_score,
    precision_recall_fscore_support,
)
from torch.amp import GradScaler, autocast
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from torchvision.transforms import InterpolationMode


class SplitDataset(Dataset):
    def __init__(self, root, relpaths, classes, transform):
        self.root = Path(root)
        self.relpaths = relpaths
        self.class_to_idx = {c: i for i, c in enumerate(classes)}
        self.transform = transform

    def __len__(self):
        return len(self.relpaths)

    def __getitem__(self, i):
        p = self.relpaths[i]
        img = Image.open(self.root / p).convert("RGB")
        return self.transform(img), self.class_to_idx[Path(p).parent.name]


def build_model():
    model = timm.create_model("starnet_s2.in1k", pretrained=True, num_classes=10)
    cfg = timm.data.resolve_model_data_config(model)
    return model, cfg


def make_transform(cfg, train):
    tfs = [transforms.Resize((224, 224), interpolation=InterpolationMode.BILINEAR)]
    if train:
        tfs.append(transforms.RandomHorizontalFlip(0.5))
    tfs += [transforms.ToTensor(), transforms.Normalize(cfg["mean"], cfg["std"])]
    return transforms.Compose(tfs)


@torch.no_grad()
def evaluate(model, loader, device):
    model.eval()
    preds, gts = [], []
    for x, y in loader:
        with autocast("cuda"):
            logits = model(x.to(device, non_blocking=True))
        preds += logits.argmax(1).cpu().tolist()
        gts += y.tolist()
    return preds, gts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", default="runs/starnet_s2_eurosat/split_indices.json")
    ap.add_argument("--out", default="runs/starnet_s2_eurosat")
    ap.add_argument("--epochs", type=int, default=25)
    ap.add_argument("--batch-size", type=int, default=64)
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--num-workers", type=int, default=4)
    args = ap.parse_args()

    torch.manual_seed(args.seed)
    device = "cuda"
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    split = json.loads(Path(args.split).read_text())
    classes = split["classes"]
    model, cfg = build_model()
    model.to(device)
    print("normalization:", cfg["mean"], cfg["std"])

    train_ds = SplitDataset(split["dataset_root"], split["train"], classes, make_transform(cfg, True))
    val_ds = SplitDataset(split["dataset_root"], split["val"], classes, make_transform(cfg, False))
    test_ds = SplitDataset(split["dataset_root"], split["test"], classes, make_transform(cfg, False))
    kw = dict(num_workers=args.num_workers, pin_memory=True,
              persistent_workers=args.num_workers > 0)
    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True, **kw)
    val_loader = DataLoader(val_ds, batch_size=args.batch_size, **kw)
    test_loader = DataLoader(test_ds, batch_size=args.batch_size, **kw)

    opt = torch.optim.SGD(model.parameters(), lr=args.lr, momentum=0.9)
    sched = torch.optim.lr_scheduler.StepLR(opt, step_size=7, gamma=0.1)
    scaler = GradScaler("cuda")
    ce = torch.nn.CrossEntropyLoss()

    history_path = out / "history.json"
    history = json.loads(history_path.read_text()) if history_path.exists() else []
    best_val = max((h["val_acc"] for h in history), default=-1.0)

    for ep in range(len(history) + 1, args.epochs + 1):
        model.train()
        t0 = time.time()
        torch.cuda.reset_peak_memory_stats()
        running_loss, seen, correct = 0.0, 0, 0
        for x, y in train_loader:
            x = x.to(device, non_blocking=True)
            y = y.to(device, non_blocking=True)
            opt.zero_grad(set_to_none=True)
            with autocast("cuda"):
                logits = model(x)
                loss = ce(logits, y)
            scaler.scale(loss).backward()
            scaler.step(opt)
            scaler.update()
            running_loss += loss.item() * y.size(0)
            correct += (logits.argmax(1) == y).sum().item()
            seen += y.size(0)

        val_preds, val_gts = evaluate(model, val_loader, device)
        val_acc = sum(p == g for p, g in zip(val_preds, val_gts)) / len(val_gts)
        record = {
            "epoch": ep,
            "train_loss": round(running_loss / seen, 4),
            "train_acc": round(correct / seen, 4),
            "val_acc": round(val_acc, 4),
            "epoch_sec": round(time.time() - t0, 1),
            "peak_vram_gib": round(torch.cuda.max_memory_allocated() / 2**30, 2),
            "lr": opt.param_groups[0]["lr"],
        }
        history.append(record)
        history_path.write_text(json.dumps(history, indent=1))
        print(json.dumps(record))

        if val_acc > best_val:
            best_val = val_acc
            torch.save({"model": model.state_dict(), "classes": classes,
                        "epoch": ep, "val_acc": val_acc}, out / "best.pt")
        sched.step()

    ckpt = torch.load(out / "best.pt", map_location=device, weights_only=False)
    model.load_state_dict(ckpt["model"])
    preds, gts = evaluate(model, test_loader, device)
    acc = sum(p == g for p, g in zip(preds, gts)) / len(gts)
    macro_f1 = f1_score(gts, preds, average="macro")
    _, _, per_f1, _ = precision_recall_fscore_support(
        gts, preds, labels=range(len(classes)), zero_division=0)
    per_class_acc = [
        sum(p == g and g == c for p, g in zip(preds, gts)) / max(1, gts.count(c))
        for c in range(len(classes))
    ]
    cm = confusion_matrix(gts, preds, labels=range(len(classes)))
    metrics = {
        "checkpoint_epoch": ckpt["epoch"],
        "checkpoint_val_acc": ckpt["val_acc"],
        "test_top1_acc": round(acc, 4),
        "test_macro_f1": round(macro_f1, 4),
        "per_class_acc": {c: round(a, 4) for c, a in zip(classes, per_class_acc)},
        "per_class_f1": {c: round(f, 4) for c, f in zip(classes, per_f1)},
        "classes": classes,
        "confusion_matrix": cm.tolist(),
        "history": history,
        "args": vars(args),
    }
    (out / "metrics.json").write_text(json.dumps(metrics, indent=1))
    print(f"TEST top-1 acc {acc:.4f}  macro-F1 {macro_f1:.4f}")

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    eps = [h["epoch"] for h in history]
    axes[0].plot(eps, [h["train_loss"] for h in history])
    axes[0].set_title("train loss"); axes[0].set_xlabel("epoch")
    axes[1].plot(eps, [h["train_acc"] for h in history], label="train")
    axes[1].plot(eps, [h["val_acc"] for h in history], label="val")
    axes[1].set_title("accuracy"); axes[1].legend(); axes[1].set_xlabel("epoch")
    axes[2].plot(eps, [h["epoch_sec"] for h in history])
    axes[2].set_title("seconds / epoch"); axes[2].set_xlabel("epoch")
    fig.tight_layout()
    fig.savefig(out / "curves.png", dpi=150)

    fig, ax = plt.subplots(figsize=(7, 6))
    im = ax.imshow(cm, cmap="Blues")
    ax.set_xticks(range(len(classes))); ax.set_xticklabels(classes, rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(len(classes))); ax.set_yticklabels(classes, fontsize=8)
    for i in range(len(classes)):
        for j in range(len(classes)):
            ax.text(j, i, cm[i, j], ha="center", va="center", fontsize=7,
                    color="white" if cm[i, j] > cm.max() / 2 else "black")
    fig.colorbar(im)
    fig.tight_layout()
    fig.savefig(out / "confusion_matrix.png", dpi=150)
    print(f"artifacts written to {out}")


if __name__ == "__main__":
    main()
