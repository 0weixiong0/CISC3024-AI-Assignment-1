"""Package the frozen EuroSAT split + run metadata into the standalone webapp.

Produces:
  webapp_standalone/data/images/<Class>/<file>.jpg   (27,000 images, mirrored layout)
  webapp_standalone/manifest.json                    (summary, classes, per-split per-class paths)

manifest.json drives the static site: the frontend builds its browser index from
splits[split][class] and fetches images at data/images/<relpath>. Split membership
is frozen (split_indices.json seed) so the standalone site browses exactly the same
train/val/test images as the Python server.
"""
import json
import shutil
from collections import Counter
from pathlib import Path

import timm

ROOT = Path(__file__).resolve().parent.parent
RUN = ROOT / "runs" / "starnet_s2_eurosat"
OUT = ROOT / "webapp_standalone"
IMG_DST = OUT / "data" / "images"


def main():
    split = json.loads((RUN / "split_indices.json").read_text())
    metrics = json.loads((RUN / "metrics.json").read_text())
    root = Path(split["dataset_root"])
    classes = split["classes"]

    cfg = timm.data.resolve_model_data_config(
        timm.create_model("starnet_s2.in1k", pretrained=False, num_classes=10))
    manifest = {
        "summary": {
            "model": "starnet_s2.in1k (fine-tuned)",
            "checkpoint_epoch": metrics["checkpoint_epoch"],
            "checkpoint_val_acc": metrics["checkpoint_val_acc"],
            "test_top1_acc": metrics["test_top1_acc"],
            "test_macro_f1": metrics["test_macro_f1"],
            "per_class_f1": metrics["per_class_f1"],
            "normalization": {"mean": cfg["mean"], "std": cfg["std"]},
            "input_size": [224, 224],
            "dataset": "EuroSAT RGB (27,000 images, 10 classes, 64x64 Sentinel-2 tiles)",
            "split": {"seed": split["seed"], "archive_url": split["archive_url"],
                      "archive_size_mb": split["archive_size_mb"],
                      "counts": {"train": len(split["train"]),
                                 "val": len(split["val"]),
                                 "test": len(split["test"])}},
        },
        "classes": classes,
        "splits": {},
    }

    IMG_DST.mkdir(parents=True, exist_ok=True)
    copied = skipped = missing = 0
    total_bytes = 0
    for s in ("train", "val", "test"):
        by_class = {c: [] for c in classes}
        for rel in split[s]:
            cls = Path(rel).parent.name
            if cls not in by_class:
                raise ValueError(f"unknown class dir {cls!r} in split {s}")
            by_class[cls].append(rel.replace("\\", "/"))
            src = root / rel
            dst = IMG_DST / rel
            if not src.is_file():
                missing += 1
                continue
            if dst.is_file() and dst.stat().st_size == src.stat().st_size:
                skipped += 1
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                copied += 1
            total_bytes += src.stat().st_size
        manifest["splits"][s] = {c: sorted(by_class[c]) for c in classes}

    (OUT / "manifest.json").write_text(json.dumps(manifest, separators=(",", ":")))
    print(json.dumps({
        "images_copied": copied, "already_present": skipped, "missing": missing,
        "total_bytes_mb": round(total_bytes / 1e6, 1),
        "manifest_mb": round((OUT / "manifest.json").stat().st_size / 1e6, 2),
        "counts": {s: {c: len(manifest["splits"][s][c]) for c in classes[:2]} | {}
                   for s in ("train", "val", "test")},
    }, indent=1))


if __name__ == "__main__":
    main()
