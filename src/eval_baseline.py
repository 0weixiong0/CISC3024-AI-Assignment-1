"""Evaluate the un-fine-tuned model (ImageNet-pretrained backbone + randomly
initialized 10-class head) on the frozen EuroSAT test split — the
"before training" baseline for the transfer-learning ablation.

Read-only evaluation: no training, no downloads (checkpoint is already cached).
The head init is seeded identically to the formal run, so this is exactly the
G4 model at epoch 0.
"""
import argparse
import json
from collections import Counter
from pathlib import Path

import torch
from sklearn.metrics import f1_score
from torch.utils.data import DataLoader

from train_starnet_eurosat import SplitDataset, build_model, evaluate, make_transform


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", default="runs/starnet_s2_eurosat/split_indices.json")
    ap.add_argument("--out", default="runs/starnet_s2_eurosat")
    ap.add_argument("--batch-size", type=int, default=64)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--num-workers", type=int, default=4)
    args = ap.parse_args()

    torch.manual_seed(args.seed)
    device = "cuda"
    split = json.loads(Path(args.split).read_text())
    classes = split["classes"]

    model, cfg = build_model()
    model.to(device).eval()

    test_ds = SplitDataset(split["dataset_root"], split["test"], classes,
                           make_transform(cfg, False))
    loader = DataLoader(test_ds, batch_size=args.batch_size,
                        num_workers=args.num_workers, pin_memory=True)
    preds, gts = evaluate(model, loader, device)
    acc = sum(p == g for p, g in zip(preds, gts)) / len(gts)
    macro_f1 = f1_score(gts, preds, average="macro")

    counts = Counter(Path(p).parent.name for p in split["test"])
    majority = max(counts.values()) / len(split["test"])

    result = {
        "description": ("ImageNet-pretrained starnet_s2.in1k backbone with a randomly "
                        "initialized 10-class head (no fine-tuning), evaluated on the "
                        "frozen test split; identical seed and head init as the formal run"),
        "seed": args.seed,
        "test_top1_acc": round(acc, 4),
        "test_macro_f1": round(macro_f1, 4),
        "majority_class_acc": round(majority, 4),
        "test_class_counts": dict(sorted(counts.items())),
    }
    out = Path(args.out) / "baseline_untrained_head.json"
    out.write_text(json.dumps(result, indent=1))
    print(json.dumps(result, indent=1))


if __name__ == "__main__":
    main()
