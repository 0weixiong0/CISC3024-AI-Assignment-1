# CISC3024 AI Assignment 1 — StarNet-S2 on EuroSAT

**Pattern Recognition · University of Macau · Fall 2026**

This repository contains the complete implementation of AI Assignment #1 for CISC3024 Pattern Recognition. The assignment requires using AI tools to find a recent Deep CNN or Deep Autoencoder algorithm with a computer vision application, and have the AI implement everything including algorithm search, programming, and report writing.

## Project Overview

**Task**: Satellite scene classification on the EuroSAT dataset (27,000 images, 10 classes)

**Model**: StarNet-S2 (3.7M parameters) — a lightweight star operation network with ImageNet pretraining, fine-tuned on EuroSAT.

**Results**:
- Validation accuracy: **97.38%** (epoch 23)
- Test top-1 accuracy: **97.65%**
- Test macro-F1: **97.58%**

## Repository Structure

```
├── src/                          # Python backend source code
│   ├── train.py                  # Training script (AMP, frozen split, checkpointing)
│   ├── evaluate.py               # Evaluation script (top-1 acc, macro-F1)
│   ├── export_onnx.py            # ONNX export with analytic Grad-CAM
│   └── serve_app.py              # Visualization server (Flask-like)
├── webapp/                       # Server-based web frontend
│   ├── index.html
│   ├── app.js
│   └── style.css
├── webapp_standalone/            # Pure frontend (browser-only ONNX inference)
│   ├── index.html
│   ├── app.js
│   ├── style.css
│   ├── colormaps.js              # Jet/Viridis LUTs
│   ├── model/
│   │   └── model.onnx            # Exported single graph (14MB)
│   ├── ort/                      # onnxruntime-web WASM runtime
│   └── manifest.json             # Frozen train/val/test split
├── research_records/             # Complete research documentation
│   ├── conversation_log.md       # Bilingual supervisor-AI dialogue
│   ├── stage_00_preflight.md     # Environment setup
│   ├── stage_01_*.md             # Literature search & model selection
│   ├── stage_02_experiment_design.md
│   ├── stage_03_experiment_log.md
│   ├── stage_04_visualization_log.md
│   └── stage_05_report_outline.md
└── Requirement.txt               # Original assignment brief
```

## Key Features

### 1. Transfer Learning Pipeline
- AI selected StarNet-S2 from 11 candidates (MobileNetV4, RepViT, EfficientAD, etc.)
- Fine-tuned from ImageNet weights with AMP training
- Frozen train/val/test split (seed 42) for reproducibility

### 2. Analytic Grad-CAM
- Exploits StarNet's GAP + linear head structure
- Gradient computed analytically: `w = onehot @ W_head`
- No autograd needed — fully forward pass
- Verified correlation 1.0 vs pytorch_grad_cam

### 3. Dual Deployment
**Server version** (`webapp/`):
- Python backend with PyTorch inference
- Real-time Grad-CAM and feature map visualization
- Run: `python src/serve_app.py` → http://127.0.0.1:8000

**Standalone version** (`webapp_standalone/`):
- Pure frontend, no backend required
- ONNX inference in browser (WebGPU/WASM)
- Hosted on GitHub Pages: **[Live Demo](https://0weixiong0.github.io/CISC3024-AI-Assignment-1/)**

### 4. Multi-Layer Feature Maps
- Visualize intermediate activations from all 4 stages
- Stage 0: 32×56×56 (shallow edges)
- Stage 1: 64×28×28 (textures)
- Stage 2: 128×14×14 (patterns)
- Stage 3: 256×7×7 (semantic)
- Channel-block paging with viridis colormap

## How to Use

### Server Version (Local)

```bash
# Install dependencies
pip install torch torchvision timm grad-cam matplotlib

# Download model weights (best.pt) and place in runs/starnet_s2_eurosat/
# (Contact author or re-run training)

# Start server
python src/serve_app.py

# Open http://127.0.0.1:8000
```

### Standalone Version (GitHub Pages)

Visit: **https://0weixiong0.github.io/CISC3024-AI-Assignment-1/**

The pure frontend loads model.onnx (14MB) and runs inference entirely in your browser. First inference takes ~5s (WASM initialization), subsequent inferences are fast.

**Note**: The standalone demo does not include the 27,000 dataset images. It uses a manifest.json with relative paths. For full access to the dataset, download EuroSAT separately.

## Grading Criteria Coverage

This repository addresses all 6 grading criteria:

1. **How AI tools found the algorithm**: See `research_records/stage_01_*.md` — systematic literature search across 11 candidates
2. **Algorithm description**: StarNet-S2 architecture with star operation topology
3. **How AI implements it**: Complete pipeline — training, evaluation, ONNX export, dual deployment
4. **Experiment settings and results**: Frozen split, AMP training, 97.65% test accuracy
5. **What you have learnt**: Documented in `research_records/conversation_log.md`
6. **Webpage link of source codes**: This GitHub repository + live demo

## Technical Details

**Model**: StarNet-S2 (`timm.starnet_s2.in1k`)
- Parameters: 3.7M
- Input: 224×224 RGB
- Output: 10 classes (EuroSAT)
- Stages: 4 (with star operation blocks)

**Training**:
- Optimizer: AdamW (lr=3e-4, weight_decay=0.05)
- Scheduler: CosineAnnealingLR (T_max=25)
- Batch size: 64
- Epochs: 25 (best at epoch 23)
- Device: CUDA (AMP enabled)
- Time: ~15 minutes on RTX 3060

**Dataset**: EuroSAT (Helber et al., 2019)
- 27,000 images (64×64 RGB)
- 10 classes: AnnualCrop, Forest, HerbaceousVegetation, Highway, Industrial, Pasture, PermanentCrop, Residential, River, SeaLake
- Split: 18,900 train / 4,050 val / 4,050 test (seed 42)

## Privacy & Security

- **No sensitive data**: Only EuroSAT (public dataset) and source code
- **No API keys or credentials**: All code is self-contained
- **Local-only server**: `serve_app.py` binds to 127.0.0.1 (no external exposure)
- **Standalone frontend**: Pure static site, no server-side execution

## License

This repository is for academic purposes (CISC3024 assignment). EuroSAT dataset is licensed under CC BY 4.0. StarNet model is from timm (Apache 2.0).

## Contact

**Author**: 0weixiong0  
**Email**: look840568428@gmail.com  
**Course**: CISC3024 Pattern Recognition, University of Macau  
**Supervisor**: AI-assisted research workflow (see conversation_log.md)

---

**Submission date**: September 2026  
**Deadline**: 2026-09-20 evening
