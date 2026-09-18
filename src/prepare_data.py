"""Download EuroSAT (RGB) from the official host, verify contents, and freeze a stratified 70/15/15 split.

Official URL and MIT license per the official repository README (github.com/phelber/EuroSAT), fetched 2026-09-18.
"""
import argparse
import json
import urllib.request
import zipfile
from pathlib import Path

from sklearn.model_selection import train_test_split

# Official host first (per official README); fallbacks: Zenodo deposit of the
# EuroSAT authors (record 7711810) and the TorchGeo mirror on Hugging Face.
EUROSAT_URLS = [
    "https://madm.dfki.de/files/sentinel/EuroSAT.zip",
    "https://zenodo.org/records/7711810/files/EuroSAT_RGB.zip?download=1",
    "https://huggingface.co/datasets/torchgeo/eurosat/resolve/main/EuroSAT.zip",
]
EXPECTED_CLASSES = [
    "AnnualCrop", "Forest", "HerbaceousVegetation", "Highway", "Industrial",
    "Pasture", "PermanentCrop", "Residential", "River", "SeaLake",
]


def download(urls, dest: Path) -> str:
    if dest.exists():
        print(f"archive exists: {dest}")
        return "cached"
    errors = []
    for url in urls:
        print(f"trying {url}")
        tmp = dest.with_suffix(".part")
        try:
            with urllib.request.urlopen(url, timeout=60) as r, open(tmp, "wb") as f:
                total = int(r.headers.get("Content-Length", 0))
                done = 0
                while True:
                    chunk = r.read(1 << 20)
                    if not chunk:
                        break
                    f.write(chunk)
                    done += len(chunk)
                    if total:
                        print(f"\r{done / 1e6:.1f}/{total / 1e6:.1f} MB", end="", flush=True)
            print()
            tmp.rename(dest)
            return url
        except Exception as e:
            errors.append(f"{url}: {e}")
            print(f"  failed: {e}")
            if tmp.exists():
                tmp.unlink()
    raise RuntimeError("all download sources failed:\n" + "\n".join(errors))


def extract(zip_path: Path, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    marker = out_dir / ".extracted"
    if not marker.exists():
        print("extracting...")
        with zipfile.ZipFile(zip_path) as z:
            z.extractall(out_dir)
        marker.touch()
    else:
        print("archive already extracted")
    entries = [p for p in out_dir.iterdir() if p.is_dir() and not p.name.startswith(".")]
    if len(entries) == 1 and all((entries[0] / c).is_dir() for c in EXPECTED_CLASSES):
        return entries[0]
    return out_dir


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data")
    ap.add_argument("--out", default="runs/starnet_s2_eurosat/split_indices.json")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    data_dir = Path(args.data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)
    zip_path = data_dir / "EuroSAT.zip"
    used_url = download(EUROSAT_URLS, zip_path)
    size_mb = zip_path.stat().st_size / 1e6
    print(f"archive size: {size_mb:.1f} MB")
    dataset_root = extract(zip_path, data_dir / "EuroSAT")

    classes = []
    relpaths, labels = [], []
    per_class = {}
    for cls in sorted(p.name for p in dataset_root.iterdir() if p.is_dir()):
        files = sorted((dataset_root / cls).glob("*.jpg"))
        classes.append(cls)
        per_class[cls] = len(files)
        for f in files:
            relpaths.append(str(f.relative_to(dataset_root).as_posix()))
            labels.append(len(classes) - 1)
    print("per-class counts:", per_class)
    print("total:", len(relpaths))

    idx_train, idx_rest = train_test_split(
        range(len(relpaths)), test_size=0.30, stratify=labels, random_state=args.seed)
    rest_labels = [labels[i] for i in idx_rest]
    idx_val, idx_test = train_test_split(
        idx_rest, test_size=0.50, stratify=rest_labels, random_state=args.seed)

    split = {
        "classes": classes,
        "seed": args.seed,
        "archive_url": used_url,
        "archive_size_mb": round(size_mb, 1),
        "dataset_root": str(dataset_root),
        "per_class_counts": per_class,
        "train": [relpaths[i] for i in idx_train],
        "val": [relpaths[i] for i in idx_val],
        "test": [relpaths[i] for i in idx_test],
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(split, indent=1))
    print(f"frozen split saved: {out} (train {len(idx_train)} / val {len(idx_val)} / test {len(idx_test)})")


if __name__ == "__main__":
    main()
