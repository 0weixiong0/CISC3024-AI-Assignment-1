# Stage 02 — Algorithm and Experiment Design: StarNet-S2 Fine-Tuned on EuroSAT

**Date:** 2026-09-18
**Status:** Design approved to be produced (supervisor approved entering Stage 02 on 2026-09-18). All acquisition and execution gates (G1–G4) remain pending — this document authorizes no installation, download, or execution.
**Predecessor evidence:** `DEEP_RESEARCH_STARNET_VS_LSNET_FINAL.md` (final head-to-head, Sections 4–5) and `DEEP_RESEARCH_MODEL_SELECTION.md` (Sections 9–11).

---

## 1. Supervisor decisions recorded on 2026-09-18

1. **Model: StarNet-S2** (the primary recommendation was accepted).
2. **Dataset: EuroSAT** (the primary dataset recommendation was accepted).
3. **Stage 02 approved** — produce the algorithm and experiment plan.

Consequences for the draft three-way design (`DEEP_RESEARCH_STARNET_VS_LSNET_FINAL.md` Section 5): the LSNet-T and LSNet-S arms are **not part of the approved scope**. They are retained in the design only as explicitly optional, time-permitting comparison arms, and may not be run without separate approval. The core deliverable is a single model (StarNet-S2) fine-tuned on EuroSAT under a fully documented protocol.

---

## 2. Algorithm description (grading criterion 2)

### 2.1 The star operation

StarNet (Ma et al., CVPR 2024, "Rewrite the Stars", arXiv 2403.19967) replaces the standard neural element-wise composition with a **multiplicative composition of two linear branches**:

- **Motivating identity (paper Section 3):** the product of two linear transforms, `(W1 X + B1) * (W2 X + B2)`, can be rewritten as a single linear transform `W X + B` acting in a **higher-dimensional implicit feature space** — the product induces exponentially many implicit dimensions.
- **StarNet block mechanism:** `y = f(x) ⊙ g(x)`, where `f` and `g` are depth-wise linear branches, `⊙` is element-wise multiplication, followed by a linear projection.

The single equation and its accompanying diagram (paper Fig. 2) are the core explanatory assets for the report's algorithm-description criterion.

### 2.2 StarNet-S2 specification (verified values only)

| Property | Value | Source |
|---|---|---|
| Params | 3.7M | timm card `starnet_s2.in1k` [62] |
| Compute | 0.5 GMACs (paper prints "547M FLOPs (M)" under a MACs-equivalent convention) | timm card [62]; paper Table 6 |
| Input | 224×224, 3-channel | timm card [62] |
| Pretraining | "Trained on ImageNet-1k by paper authors" (verbatim) | timm card [62] |
| Reported ImageNet-1k top-1 | 74.8% | paper Table 6 |
| License | Apache-2.0 (weights); official repo `ma-xu/Rewrite-the-Stars` | timm card [62] |

Full per-stage config (depths/dims) will be quoted from the paper's architecture table at report-writing time; it is not restated here to avoid transcription errors.

### 2.3 Fine-tuning adaptation (transfer learning — to be disclosed in the report)

- Load `timm/starnet_s2.in1k` pretrained weights; replace the 1,000-class classifier head with a 10-class head (`num_classes=10`).
- This is **transfer learning** (fine-tuning official author-trained ImageNet weights), not training from scratch. The report must state this explicitly, per supervisor guidance of 2026-09-18.

### 2.4 Task formulation: input and output (added 2026-09-18 after supervisor query)

- **Task type: single-label image classification** — each patch carries exactly ONE land-use/land-cover label. This is scene-level recognition, NOT object detection or localization: the model never outputs bounding boxes, segments, or multiple per-image objects.
- **Input:** one Sentinel-2 RGB patch, native 64×64×3, bilinearly resized to 224×224×3, normalized with ImageNet mean/std (per the pretrained model's config).
- **Output:** logits over the 10 classes → softmax probabilities; predicted label = argmax. Example: `{Forest: 0.93, AnnualCrop: 0.03, …}` → "Forest".
- **Output head:** StarNet-S2's original 1,000-class ImageNet head is replaced by a randomly initialized 10-class linear head (`num_classes=10`); the head trains from scratch while the pretrained backbone fine-tunes.
- **Supervision signal:** cross-entropy between predicted class distribution and the folder-derived ground-truth label; correctness is a single label comparison per image (top-1).

---

## 3. Dataset and split (grading criterion 4 — settings)

### 3.1 Dataset: EuroSAT (RGB distribution)

- 27,000 labeled Sentinel-2 patches, 10 land-use/land-cover classes (AnnualCrop, Forest, HerbaceousVegetation, Highway, Industrial, Pasture, PermanentCrop, Residential, River, SeaLake); native 64×64, upscaled to 224×224.
- License: MIT (verified 2026-09-18). Benchmark anchor: authors' own "overall classification accuracy of 98.57%" (Helber et al., IEEE J-STARS 2019).
- **No official train/val/test split** — the repository ships per-class folders only. Exact per-class counts will be counted empirically at download time and recorded.

### 3.2 Split protocol (single fixed split, recorded for reproducibility)

- **Stratified 70/15/15** with `seed = 42`: Train ≈ 18,900 / Validation ≈ 4,050 / Test ≈ 4,050.
- Implementation: per-class file lists → `sklearn.model_selection.train_test_split` twice (first 70/30, then 30 into 15/15), both `stratify=labels`, `random_state=42`.
- The resulting index lists (relative file paths per subset) are written to `runs/starnet_s2_eurosat/split_indices.json` **before training** and never regenerated; every evaluation uses this frozen split.
- *(Engineering choice — EuroSAT literature uses heterogeneous random splits; no canonical split exists to cite.)*

### 3.3 Transforms

- **Train:** `Resize((224,224), bilinear)` → `RandomHorizontalFlip(0.5)` → `ToTensor` → ImageNet normalization (mean/std taken from the timm model's default config at runtime, not hardcoded).
- **Validation/Test:** `Resize((224,224), bilinear)` → `ToTensor` → same normalization.
- Rationale: 64×64 native patches must be geometrically preserved when upscaling; heavy augmentation (RandAugment, mixup, random erasing) is **deferred** — timm documents these for ImageNet-scale recipes [41], and their benefit on a 27k fine-tune is unknown. A light-augmentation bonus arm may be added later only with approval and only if the timeline allows.
- *(Engineering choices; the tutorial-level flip augmentation follows the verified PyTorch transfer-learning protocol [72].)*

---

## 4. Training protocol (grading criterion 4 — settings)

| Item | Value | Status |
|---|---|---|
| Vehicle | **Minimal self-written PyTorch + timm script** (single file: model creation, frozen-split loaders, SGD training loop, AMP, checkpointing) | Deviation from draft — see 4.1 |
| Optimizer | SGD, lr=0.001, momentum=0.9 | Verified tutorial protocol [72] |
| LR schedule | StepLR(step_size=7, gamma=0.1) | Verified tutorial protocol [72] |
| Epochs | 25 | Verified tutorial protocol [72] |
| Batch size | 64 (AMP on) | Pilot-confirmed; OOM → 32 |
| Precision | Native AMP (`torch.amp.autocast('cuda')` + `GradScaler`) | timm default since 0.4.3 [41] |
| Seed | 42 (split, model init shuffling, DataLoader shuffling) | Engineering choice |
| Checkpointing | Best-validation-accuracy checkpoint saved each epoch; final metrics JSON written at test time | Engineering choice |

### 4.1 Deviation from the Stage 02 draft: vehicle

The draft proposed timm's repository `train.py` as the vehicle. Stage 02 selects a **minimal self-written script** instead, because: (a) `train.py` ships only in the repo root and would require cloning `pytorch-image-models` (an extra approval item); (b) a single-model single-dataset run needs only ~150 lines, which is fully explainable in the report and publishable for criterion 6; (c) the assignment rewards documenting *how AI implements the algorithm*, which a readable script serves better. timm's `train.py` remains the fallback if the custom script hits convergence or AMP trouble.

### 4.2 Duration estimate (PROVISIONAL — to be replaced by pilot measurements)

18,900 train images at 224², 3.7M-param model, batch 64, AMP on an RTX 4060 Laptop 8 GiB: **rough epoch-time estimate 1–3 min** ⇒ 25 epochs ≈ **25–75 min total**, plus evaluation and Grad-CAM. These figures are reasoned estimates, **not measurements**; the pilot (G3) will produce real per-epoch timings before any schedule commitment. Per supervisor guidance, no timeline decision relies on these estimates.

---

## 5. Evaluation plan

1. **Metrics (test set, frozen split):** top-1 accuracy; per-class accuracy; macro-F1 and per-class F1 (`sklearn`); 10×10 confusion matrix.
2. **Grad-CAM:** `pytorch-grad-cam` on 2–3 validation/test samples per selected class; target layers specified **by module path** (exact module discovered by printing the model at implementation time; README-guided ViT/Swin precedent [65][66] shows the by-attribute approach for non-CNN blocks). Output: overlay PNGs saved to `runs/starnet_s2_eurosat/gradcam/`.
3. **Compute accounting:** params/GMACs from the timm card [62]; measured wall-clock per epoch; peak GPU memory via `torch.cuda.max_memory_allocated()`.
4. **Comparison anchors (context only, no claim of parity):** EuroSAT benchmark 98.57% [73] (much heavier training budget than ours); PyTorch tutorial 0.9346 fine-tuning accuracy [72] (protocol sanity reference).
5. **Expected outcomes and success criteria (added 2026-09-18 after supervisor query; estimates are labeled as such — the report will contain only measured values):**
   - **Verified anchor:** the EuroSAT authors report 98.57% overall accuracy [73] with training far heavier than our budget. 10% is the random-guess floor on 10 classes.
   - **Reasoned expectation (NOT a sourced fact):** EuroSAT is widely treated as a near-saturated benchmark for ImageNet-pretrained backbones; our 25-epoch fine-tune of StarNet-S2 is expected to land in the **~95–99% test top-1** band. Classes are expected to be uneven, with confusion concentrated among visually similar land-cover types (e.g., crop/grassland families, River vs Highway).
   - **Early signal:** if the 2-epoch pilot (G3) already shows validation accuracy well above 90%, the band is plausible; if it is far below, investigate pipeline/LR before G4.
   - **Success criteria (in rubric order of importance):** (1) the complete pipeline runs end-to-end on the 8 GiB laptop within schedule; (2) test top-1 is far above 10% and is reported with the full evidence chain (frozen split, metrics.json, curves, confusion matrix); (3) result is interpreted against the 98.57% anchor with an honest compute-budget comparison; (4) Grad-CAM attention is qualitatively sensible for land-cover structure. **Beating 98.57% is NOT the goal** — the rubric grades the AI-assisted workflow, experimental rigor, and reporting, not leaderboard results. A 90–95% outcome with a sound diagnosis (epochs/LR/data) is an acceptable "what you have learnt" result; a silent leaderboard chase is not.

---

## 6. Schedule (conservative; finish target 2026-09-20 evening, deadline 2026-09-21)

| Day | Work | Gate |
|---|---|---|
| 09-18 (today) | Stage 02 design written and submitted | — |
| 09-19 morning | G1: install dependencies; G2: download EuroSAT RGB + checkpoint; license/URL audit; count per-class images; freeze split | G1, G2, G3a |
| 09-19 afternoon | G3: pilot run (2 epochs) — verify pipeline, measure epoch time, VRAM; report findings to supervisor | G3, pause for review |
| 09-19 evening → 09-20 | G4: full 25-epoch run; evaluation; Grad-CAM; results table | G4 |
| 09-20 evening | Results consolidated; HTML visualization (separate approval) or final-report outline (separate approval) | — |
| 09-21 | Buffer only | — |

---

## 7. Approval gates required before any action

| Gate | Action requested | Content |
|---|---|---|
| **G1** | Install Python packages | `timm` (latest stable compatible with `starnet_s2.in1k`; version pinned and recorded at install), `scikit-learn`, `matplotlib`; optional `pytorch-grad-cam` |
| **G2** | Download data + weights | EuroSAT RGB archive (exact URL to be confirmed from the official repository's download page at download time; archive size not yet verified — will be recorded); `starnet_s2.in1k` checkpoint auto-fetched by timm from Hugging Face Hub (size not yet verified — will be recorded) |
| **G3** | Execute pilot | 2-epoch pilot run on the frozen split; report timing/VRAM/convergence findings back before scaling |
| **G4** | Execute full run | 25-epoch training + evaluation + Grad-CAM |

Each gate is requested separately; a "go" on Stage 02 design is **not** a blanket authorization to install, download, or execute.

---

## 8. Risks and mitigations

| Risk | Mitigation |
|---|---|
| VRAM overrun at batch 64 | Halve to 32; StarNet-S2 is the smallest verified candidate (3.7M), so risk is low |
| timm version incompatibility with `starnet_s2.in1k` | Pin and record installed version; the card is author-trained and native to timm, so risk is low; fallback is the official repo's released checkpoints |
| Download failure (mirror/host unavailable) | Official repository lists download sources; record the actual URL used; torchvision's dataset downloader is a fallback |
| Convergence trouble with SGD protocol | Tutorial protocol is a verified working recipe [72]; if pilot diverges, report and propose (with approval) an AdamW variant |
| Timeline slip | Single seed; 25-epoch budget fits the provisional window; full run is ~1 hour-class, so one repeat is affordable if pilot timing confirms |
| Per-class imbalance surprises | Stratified split by construction; per-class counts recorded at download |

---

## 9. Deliverables of the execution stage (post-G4)

| Artifact | Path (planned) |
|---|---|
| Training/eval script | `src/train_starnet_eurosat.py` (single file, commented) |
| Split manifest | `runs/starnet_s2_eurosat/split_indices.json` |
| Checkpoint | `runs/starnet_s2_eurosat/best.pt` |
| Metrics | `runs/starnet_s2_eurosat/metrics.json` (accuracy, macro-F1, per-class F1, per-epoch times, peak VRAM, package versions, seed) |
| Training curve | `runs/starnet_s2_eurosat/curves.png` |
| Confusion matrix | `runs/starnet_s2_eurosat/confusion_matrix.png` |
| Grad-CAM overlays | `runs/starnet_s2_eurosat/gradcam/*.png` |
| Experiment log (markdown, incremental) | `research_records/stage_03_experiment_log.md` |

Criterion 6 (webpage link of source codes): a public repository or page will be proposed **after** results exist, as a separate approval item (GitHub access/tooling currently not confirmed on this machine).

---

## 10. Grading-criteria mapping (approved scope)

| Criterion | Where served |
|---|---|
| 1. How you asked AI to find the algorithm | Bilingual conversation log + Stage 01–01d search protocol/ledger |
| 2. Algorithm description | Section 2 here → final report (star operation equation + diagram; transfer-learning disclosure) |
| 3. How AI implemented the algorithm | Minimal timm-based script (Section 4.1) + implementation prompts logged |
| 4. Experiment settings and results | Sections 3–5; `metrics.json` + curves + confusion matrix |
| 5. What you have learnt | Domain shift (satellite imagery), transfer vs scratch, FLOPs-unit lesson, split-reproducibility practice |
| 6. Webpage link of source codes | Repo publication (separate approval; MIT/Apache-2.0 stack is publishable) |

---

## 11. Open items

1. Exact EuroSAT download URL and archive size — to be recorded at G2.
2. timm version to be installed — to be pinned at G1.
3. Grad-CAM target-layer module path — to be discovered from the model structure at implementation.
4. Exact UMMoodle submission deadline — supervisor to confirm if the 2026-09-21 target is affected.
5. Source-repo visibility (public repo for criterion 6) — decision deferred until after G4.
