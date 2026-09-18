# StarNet-S2 on EuroSAT — In-browser Visualization (Standalone)

A fully static, dependency-free web app that runs the fine-tuned StarNet-S2
EuroSAT classifier **entirely in the browser**: prediction, 10-class
probabilities, genuine Grad-CAM overlays, and intermediate feature maps.
No Python, no backend, no build step — it can be hosted on any static file
server (GitHub Pages, Netlify, nginx) or run locally.

## Layout

| Path | Purpose |
|---|---|
| `index.html`, `style.css`, `app.js` | UI and inference logic (vanilla JS) |
| `model/model.onnx` | Exported single graph: inputs `image` (1,3,224,224) + `target` one-hot (1,10) → outputs `probs` (1,10), `f0`–`f3` (per-stage features: 32×56×56, 64×28×28, 128×14×14, 256×7×7), `cam` (1,1,224,224) |
| `model/verification.json` | Numeric parity evidence vs PyTorch / pytorch_grad_cam at export time |
| `colormaps.js` | Jet and viridis 256-entry LUTs (generated from matplotlib) |
| `ort/` | Vendored onnxruntime-web 1.20.1 (no CDN dependency at runtime) |
| `manifest.json` | Run summary, normalization constants, frozen split paths (per split, per class) |
| `data/images/<Class>/*.jpg` | All 27,000 EuroSAT images of the frozen split (mirrors dataset layout) |

## Run locally

```bash
python -m http.server 8000 -d webapp_standalone
# open http://127.0.0.1:8000/
```

Any static server works. Do **not** open `index.html` via `file://` —
fetching the ONNX model and WASM runtime requires HTTP.

## Deploy to GitHub Pages

1. Create a repository and commit this folder's contents at the repo root
   (or into `docs/` / a `gh-pages` branch).
2. Repo → Settings → Pages → Source: your branch, `/ (root)` → Save.
3. Open `https://<user>.github.io/<repo>/`.

Nothing else is needed: all assets (runtime, model, images) are same-origin
relative paths, so the app works under a subpath like `/repo/`.

## How inference works

- The image is drawn to a 224×224 canvas (bilinear) and normalized with the
  ImageNet mean/std recorded in `manifest.json` — the same constants the
  training pipeline used.
- Two forward passes per image through one ONNX graph:
  1. `target` = zeros → `probs` + `feats`; top-1 = argmax.
  2. `target` = one-hot of the predicted class → `cam`.
- Grad-CAM is computed **analytically inside the graph**: with a
  global-average-pool + linear head, the gradient of the class score w.r.t.
  pre-pool features is spatially constant and equals the class row of the
  head weight matrix, so `cam = ReLU((onehot @ W) · A)` needs no autograd.
  Export-time verification (`model/verification.json`) shows correlation
  1.0 with `pytorch_grad_cam` on test images.
- Overlay blending (`0.7·jet(heat) + 0.3·image`, renormalized) mirrors
  `show_cam_on_image`; feature maps replicate the server's 4×4 viridis grid.

## Notes and known divergences

- **Execution providers**: WebGPU is used when available, otherwise WASM
  (SIMD, single-threaded — GitHub Pages has no COOP/COEP headers, so
  `SharedArrayBuffer` is unavailable and `numThreads` is pinned to 1).
- **Probability drift**: browser preprocessing resizes with canvas bilinear,
  while training/serving used PIL bicubic — top-1 predictions match and
  probabilities differ by ~0.003–0.01 (e.g. AnnualCrop_1002: 0.9709 in
  browser vs 0.9736 from the reference server).
- `ort/ort-wasm-simd-threaded.wasm` + `.mjs` (non-jsep) are fallback
  artifacts; the runtime currently loads the jsep pair.
- Image data provenance: EuroSAT (Sentinel-2, 10 classes, 64×64 RGB),
  split frozen with the seed recorded in `manifest.json` — identical
  membership to the Python reference server in `../webapp`.
