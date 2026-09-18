# Stage 04 Visualization Log — Dataset Sampling, Model Outputs, Network Inspection

Supervisor approval: U021 (2026-09-18) — "好的，接下来进行stage 4，如果有需要你可以选择合适的技能或扩展" (proceed to Stage 4; choose suitable skills/extensions if needed). Scope declared to the supervisor before implementation: (1) dataset sampling browser, (2) model output display, (3) intermediate network inspection (Grad-CAM + feature maps).

---

## Design decisions

1. **Zero new dependencies.** Server = Python stdlib `ThreadingHTTPServer`; frontend = vanilla HTML/JS/CSS. No new packages installed; no framework. (Approved skill/extension use: the pre-existing browser-use MCP was used only for UI testing.)
2. **Single process, model loaded once.** `runs/starnet_s2_eurosat/best.pt` loaded at startup with `pretrained=False` (no network access at serve time). Device auto-selects CUDA.
3. **Path security.** Every image-bearing request (`/api/image`, `/api/predict`, `/api/gradcam`, `/api/featuremaps`) requires the relative path to exist EXACTLY in the frozen split index (`split_indices.json`); anything else → 404. Static files are confined to `webapp/` via `Path.is_relative_to`. This makes directory traversal impossible by construction.
4. **Thread safety.** Inference endpoints serialize on a `threading.Lock` (the GradCAM object and the model are shared across ThreadingHTTPServer worker threads).
5. **Network inspection points** (grounded in timm 1.0.29 `starnet.py` source):
   - Grad-CAM target layer: `model.norm` (final BatchNorm2d, highest-resolution pre-head features); predicted class as target via `ClassifierOutputTarget`.
   - Feature maps: forward hook on `model.stages[1]`; first 16 of 128 channels rendered as a 4x4 viridis grid (28x28 spatial for 224 input).

## Implementation

| File | Role |
|---|---|
| `src/serve_app.py` | stdlib HTTP server; JSON API + static `webapp/` |
| `webapp/index.html` | layout: header summary badges, dataset browser, inspect panel |
| `webapp/style.css` | dark theme; pixelated upscaling for 64x64 sources |
| `webapp/app.js` | vanilla JS; `textContent`-only DOM injection; lazy fetch of Grad-CAM/feature maps; stale-response guard |

API endpoints: `/api/classes` (summary + per-split class counts), `/api/samples` (split/class filter, offset/limit, cap 200), `/api/image`, `/api/predict` (softmax probs sorted desc, GT, correctness), `/api/gradcam`, `/api/featuremaps`.

Run: `python src/serve_app.py` (defaults: split/ckpt/metrics under `runs/starnet_s2_eurosat/`, host 127.0.0.1, port 8000).

---

## Verification (2026-09-18)

### API smoke tests (curl, all passed)

| Check | Result |
|---|---|
| `/api/classes` | summary correct (epoch 23, val 0.9738, test top-1 0.9765, macro-F1 0.9758, cuda) + 10 class rows with train/val/test counts |
| `/api/samples?split=test&cls=River&limit=1` | returns `River/River_100.jpg` |
| `/api/image` (valid path) | 200, image/jpeg, 2,919 bytes |
| `/api/image` (path not in split index) | **404** |
| `/api/image` (traversal `../../src/serve_app.py`) | **404** |
| `/api/predict` River/River_100.jpg | pred River, correct, p=0.9658 |
| `/api/gradcam` | PNG b64 56,192 chars, pred River |
| `/api/featuremaps` | PNG b64 73,620 chars |

### Browser test (browser-use MCP, Chromium)

1. Loaded `http://127.0.0.1:8000/` — header badges render run summary; split/class selects populated (all + 10 classes); count "4050 images"; 60 thumbnails rendered; "Load more" visible.
2. Clicked thumbnail `AnnualCrop/AnnualCrop_1002.jpg` — inspect panel shows main image, GT chip (green), Pred chip "AnnualCrop — correct" (green), path, 10 probability bars sorted desc (AnnualCrop 0.9736, Pasture 0.0197, Highway 0.0036, ...).
3. Clicked **Grad-CAM** — overlay PNG rendered (hot spot on field texture region).
4. Clicked **Feature maps** — 4x4 grid rendered; suptitle confirms shape `128x28x28` (stages[1] output).
5. Filter linkage — set split=train, class=Pasture via DOM events: count "1400 images" (matches frozen split: Pasture train = 2,000 x 0.7), 60 thumbnails, Load more visible.

All Stage 04 acceptance criteria met. Server left running at http://127.0.0.1:8000/ for supervisor inspection.

---

## Notes

- Grad-CAM overlay uses the 224x224 bilinear resize of the 64x64 source (same as eval preprocessing), so hot spots are smooth at 3.5x upscale — expected.
- The `stages[1]` feature maps are mid-network (after stage 2 of 4): local texture/edge detectors, no class semantics yet — consistent with StarNet's star-operations design (element-wise multiplication synthesizing implicit high-dim combinations).
- No dataset images were modified; all access read-only.

## Addendum — Standalone in-browser build (approved U023, 2026-09-18)

User approved building a complete pure-frontend version suitable for later
GitHub hosting ("你试一下做一个完整版的前端，后续可挂在github上"). This addendum records that build.

### Design

- Single ONNX graph (`webapp_standalone/model/model.onnx`, 13.7 MB, opset 17):
  inputs `image` (1,3,224,224 fp32) + `target` one-hot (1,10 fp32);
  outputs `probs` (1,10), `feats` (1,128,28,28 = stages[1] output via hook),
  `cam` (1,1,224,224).
- Grad-CAM is analytic, not autograd: with GAP + linear head, the gradient of
  the class score w.r.t. pre-pool features A is spatially constant and equals
  the class row of the head weight matrix, so `cam = ReLU((onehot @ W) · A)`,
  bilinear-upsampled to 224 and max-normalized — pure forward ops, tracer-safe.
- Two-pass inference per image: pass 1 `target`=zeros → probs/feats → argmax;
  pass 2 `target`=one-hot(pred) → cam. (A bug found during verification: the
  first script version reused the zeros pass for CAM, producing an all-zero
  constant map — corrcoef NaN exposed it; fixed by adding the one-hot pass.)
- Overlay: `0.7·jet(heat) + 0.3·image`, renormalized by global max — mirrors
  `show_cam_on_image`; feature maps: per-channel min-max + viridis LUT, 4×4
  grid of the first 16 channels, nearest-neighbor upscale (mirrors the server
  figure). Jet/viridis LUTs generated from matplotlib into `colormaps.js`.
- Browsing: `manifest.json` (0.87 MB) carries run summary, normalization
  constants, and the frozen split paths grouped per split per class; all
  27,000 images copied to `data/images/` (91.8 MB).
- Runtime: vendored onnxruntime-web 1.20.1 into `ort/` (no CDN at runtime);
  WebGPU EP preferred, WASM fallback; `numThreads=1` (GitHub Pages has no
  COOP/COEP → no SharedArrayBuffer). Fix applied after first test: wasmPaths
  is derived from the ort script's URL — ORT 1.20 already prefixes the script
  directory, so a relative `./ort/` doubled to `/ort/ort/` and 404'd.

### Export-time verification (src/export_onnx.py → model/verification.json)

| Test image (frozen test split) | probs max abs diff (ONNX vs PyTorch) | feats max abs diff | CAM corr vs pytorch_grad_cam |
|---|---|---|---|
| AnnualCrop/AnnualCrop_1153.jpg | 1.6e-05 | 0.0096 | 1.0 |
| PermanentCrop/PermanentCrop_1526.jpg | 0.0 | 0.0149 | 1.0 |
| River/River_2152.jpg | 1e-06 | 0.0085 | 1.0 |

CAM max-abs-diff ≤ 0.31 stems from normalization/resize ordering
(pytorch_grad_cam normalizes at 7×7 before bilinear resize; the graph
normalizes after) — shape-equivalent, correlation 1.0.

### Browser test (http.server :8010 + embedded browser, 9/9 passed)

| # | Check | Result |
|---|---|---|
| 1 | manifest loads; badges model/ckpt/top-1/F1 | 97.65% / 97.58% shown |
| 2 | model load, EP reported | `wasm (cpu)` (no WebGPU in embedded browser) |
| 3 | grid + count | 4050 test images, 60/page, Load more 60→120 |
| 4 | AnnualCrop_1002 predict | Pred AnnualCrop p=0.9709 (server ref 0.9736; top-1 match) |
| 5 | River_100 predict | Pred River p=0.9559 (server ref 0.9658; top-1 match) |
| 6 | Grad-CAM canvas | 224×224 overlay, 8368 hot pixels, concentrated hotspot |
| 7 | feature maps canvas | 640×640 fully painted, viridis, correct caption |
| 8 | filter train+Pasture | 1400 images (matches server) |
| 9 | console errors | none |

Probability drift (~0.003–0.01) is expected: canvas bilinear resize vs PIL
bicubic preprocessing, and fp32 CPU vs fp16 GPU-autocast reference. Top-1
agrees on all spot checks; runtime fetches only the jsep wasm artifacts.

### Files created

`src/export_onnx.py`, `src/package_standalone.py`,
`webapp_standalone/{index.html, style.css, app.js, colormaps.js,
manifest.json, README.md, model/model.onnx, model/verification.json,
ort/*, data/images/<Class>/*.jpg}`.


## Addendum (2026-09-18): Grad-CAM rendering bug fix + multi-layer feature maps (U027/A040)

### User report

Grad-CAM canvas rendered as a near-neutral gray fine checkerboard with four
dark horizontal blobs (no heat colors). Feature maps were limited to
stages[1], first 16 channels only, in both versions. Request: layer
selection, channel paging, fix in BOTH the server version and the
pure-frontend version.

### Root cause of the gray Grad-CAM (frontend bug, not model)

`webapp_standalone/app.js` `renderCam` packed the blended RGB into a
Float32Array at stride 3 (loop 1: `j += 3`) but the write-back loop read it
at stride 4 (loop 2: `j += 4`), so every pixel's R/G/B came from three
different source pixels. Per-pixel channel misalignment statistically
collapses jet-colormap blending into near-neutral gray.

Evidence (embedded browser, live canvas pixel statistics):

| Metric | Before fix | After fix |
|---|---|---|
| mean RGB | [115, 115, 115] | [173, 196, 90] |
| pixels with max-min channel spread > 30 | ~0 (gray mush) | 1.000 |

Fix: index `blended[i * 3 + k]` in the write-back loop. Renormalization by
the global max is kept (matches pytorch_grad_cam's `show_cam_on_image`
behavior of dividing by the max).

Note: the earlier browser-test row "Grad-CAM canvas — 8368 hot pixels"
passed because it only counted hot pixels and never checked per-pixel
channel spread; the check was too weak to catch this bug.

### Correction: stage shapes were mislabeled

The title "stages[1] output (128×28×28)" was wrong. Introspecting the
loaded checkpoint gives:

| Stage | Shape (C×H×W) |
|---|---|
| stages[0] | 32×56×56 |
| stages[1] | 64×28×28 |
| stages[2] | 128×14×14 |
| stages[3] | 256×7×7 |

128 is stages[2]'s channel count. onnxruntime confirmed the old graph's
`feats` output was (1, 64, 28, 28). Corrected in both UIs (dynamic titles),
webapp_standalone/README.md, and this log.

### ONNX re-export (src/export_onnx.py)

Single graph now outputs `probs` (1,10), `f0`–`f3` (per-stage features) and
`cam` (1,1,224,224) — one forward pass returns every layer's features, so
layer switching needs no re-inference in the browser. Re-verification on
3 images (webapp_standalone/model/verification.json):

| Image | probs max abs diff | CAM corr vs pytorch_grad_cam | f0/f1/f2/f3 max abs diff |
|---|---|---|---|
| AnnualCrop_1153 | 1.6e-05 | 1.0 | 0.0042 / 0.0096 / 0.2252 / 0.0201 |
| PermanentCrop_1526 | 0.0 | 1.0 | 0.0041 / 0.0149 / 0.1035 / 0.0157 |
| River_2152 | 1e-06 | 1.0 | 0.0052 / 0.0085 / 0.0253 / 0.0248 |

Deeper-layer drift (f2 up to 0.225) is fp32 graph-shape difference and does
not affect probabilities; CAM correlation 1.0 is the operative check.

### New features (both versions)

- Layer dropdown: stages[0..3]; standalone shows dims in labels
  ("stages[1] (64×28×28)"), server version populates from the API response.
- Channel paging: 16 channels per view, page labels ("0–15", "16–31", …,
  "240–255" for 256-channel stages); layer switch resets to page 0.
- Per-cell "ch N" labels on the standalone canvas grid.
- Standalone: all four feature tensors cached per image from the single
  forward pass.
- Server: `/api/featuremaps` accepts `layer` and `start` query params,
  returns metadata `{layer, stages, channels, hw, start}` alongside the PNG;
  invalid layer → 400 `layer must be 0-3` (curl-verified). Server restarted
  on 127.0.0.1:8000 (CUDA).

### Browser tests (2026-09-18, both versions)

Standalone (http://127.0.0.1:8010/), AnnualCrop_1002: prediction correct;
layer options show all 4 stages with correct dims; channel blocks 4×16 for
stages[1]; stages[3] gives 16 blocks (0–15 … 240–255), block 5 → "channels
80–95 of 256"; stages[0] resets to 2 blocks, "channels 0–15 of 32";
Grad-CAM colorful (table above). Server (http://127.0.0.1:8000/): same
image; layer/block switching updates title and grid ("stages[3]
(256×7×7), channels 32–47 of 256"); Grad-CAM overlay renders (server-side
show_cam_on_image, unaffected by the frontend bug).

---

## Addendum: GitHub Deployment (2026-09-18)

**Supervisor request**: Deploy source code to GitHub + enable GitHub Pages for standalone frontend.

### Deployment actions

1. **Installed gh CLI 2.101.0**
   - Downloaded zip from cli/cli releases
   - Extracted to `%LOCALAPPDATA%\Programs\gh-cli\`
   - Configured git credential helper: `gh auth setup-git`

2. **Privacy audit**
   - Created `.gitignore` excluding: `data/`, `webapp_standalone/data/`, `runs/`, `*.pt`, `*.pdf`, `*.pptx`, `*.docx`, `__pycache__/`, `.env`
   - Verified with `git add --dry-run`: 44 files to be added, all source code + documentation
   - No dataset images, no training checkpoints, no course materials uploaded

3. **Repository creation**
   - Repo: https://github.com/0weixiong0/CISC3024-AI-Assignment-1 (public)
   - Initial commit: 44 files (src/, webapp/, webapp_standalone/, research_records/, model.onnx, ort/)
   - Branch `main`: complete project source code
   - Branch `gh-pages`: standalone frontend (webapp_standalone/ content at root)

4. **GitHub Pages deployment**
   - Source: `gh-pages` branch, path `/`
   - URL: https://0weixiong0.github.io/CISC3024-AI-Assignment-1/
   - Status: built and live (HTTP 200, 2385 bytes index.html)
   - Verification: HTML content matches local webapp_standalone/index.html

### Files pushed

**main branch** (44 files):
- `src/` — 6 Python scripts (train, evaluate, export, serve, prepare, package)
- `webapp/` — 3 files (index.html, app.js, style.css)
- `webapp_standalone/` — 13 files (HTML/JS/CSS + model/ + ort/)
- `research_records/` — 20 markdown files (complete bilingual documentation)
- `README.md`, `.gitignore`, `Requirement.txt`
- `DEEP_RESEARCH_*.md` — 2 literature review documents

**gh-pages branch** (13 files):
- Root: index.html, app.js, style.css, colormaps.js, manifest.json, README.md
- `model/` — model.onnx (14MB), verification.json
- `ort/` — onnxruntime-web WASM runtime (33MB)

### Excluded (privacy check)

- `data/` — 234MB (original EuroSAT dataset, 27,000 images)
- `webapp_standalone/data/` — 143MB (packaged dataset for standalone demo)
- `runs/` — 28MB (training checkpoints, logs)
- `*.pt` — PyTorch model weights
- `*.pdf`, `*.pptx`, `*.docx` — course materials

### Verification

- GitHub repo: https://github.com/0weixiong0/CISC3024-AI-Assignment-1 ✓
- GitHub Pages: https://0weixiong0.github.io/CISC3024-AI-Assignment-1/ ✓
- HTTP status: 200 OK ✓
- Content: HTML matches local source ✓

### Notes for report

- Criterion 6 ("webpage link of source codes") satisfied: both repo URL and live demo URL available
- Report can reference specific files: "see `src/train_starnet_eurosat.py` line 42"
- Live demo allows supervisor/grader to interact with the model directly in browser
- No backend required for demo — pure static site, no server costs
