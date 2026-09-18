# Stage 03 Experiment Log — StarNet-S2 on EuroSAT

Incremental log of executed actions and measured results. Design reference: `research_records/stage_02_experiment_design.md`.

---

## 2026-09-18 — G1: dependencies installed and recorded

| Package | Version | Note |
|---|---|---|
| timm | 1.0.29 | PyPI install |
| matplotlib | 3.11.0 | PyPI install |
| scikit-learn | 1.9.0 | already present |
| grad-cam | (import `pytorch_grad_cam`) | PyPI package name is `grad-cam`, not `pytorch-grad-cam` |
| torch | 2.7.1+cu128 | pre-existing; CUDA available |
| torchvision | 0.22.1+cu128 | pre-existing |
| Python | 3.12.10 | — |

Hardware confirmed: NVIDIA GeForce RTX 4060 Laptop GPU, CUDA available.

Note: timm 1.0.29 no longer auto-resolves `timm/starnet_s2.in1k` (repo-id-looking name) — the native registry name `starnet_s2.in1k` is the correct `create_model` argument. Deviation from design doc 5.3's literal string, same model, same weights.

---

## 2026-09-18 — G2: dataset and weights acquired, split frozen

- **Download source (actual):** `https://madm.dfki.de/files/sentinel/EuroSAT.zip` (official README link) **timed out** from this network (WinError 10060). Succeeded via the EuroSAT authors' official Zenodo deposit: `https://zenodo.org/records/7711810/files/EuroSAT_RGB.zip?download=1` — **94.7 MB** (matches the record's listed size; record title "EuroSAT: A Novel Dataset and Deep Learning Benchmark for Land Use and Land Cover Classification"). TorchGeo HF mirror (`torchgeo/eurosat` EuroSAT.zip, 94.3 MB) verified as second fallback but not needed.
- **Per-class counts (empirically counted after extraction — closes the Stage-02 TODO):** AnnualCrop 3000, Forest 3000, HerbaceousVegetation 3000, Residential 3000, SeaLake 3000, Highway 2500, Industrial 2500, PermanentCrop 2500, River 2500, Pasture 2000 — **total 27,000**, matching the published description.
- **Frozen split** (seed 42, stratified 70/15/15, two sklearn `train_test_split` calls): **train 18,900 / val 4,050 / test 4,050** → `runs/starnet_s2_eurosat/split_indices.json` (contains per-class counts, actual archive URL/size, classes list, relative file paths per subset). The split is frozen and will not be regenerated.
- **Checkpoint:** `starnet_s2.in1k` fetched by timm from the Hugging Face Hub on first `create_model(pretrained=True)`; runtime normalization confirmed as ImageNet defaults (0.485, 0.456, 0.406) / (0.229, 0.224, 0.225) from `resolve_model_data_config` — as designed, not hardcoded.

---

## 2026-09-18 — G3: 2-epoch pilot (completed)

Command: `python src/train_starnet_eurosat.py --epochs 2 --out runs/starnet_s2_eurosat_pilot`

| Epoch | train_loss | train_acc | val_acc | epoch_sec | peak VRAM (GiB) |
|---|---|---|---|---|---|
| 1 | 1.0165 | 0.6719 | 0.8170 | 94.6 (warmup) | 1.25 |
| 2 | 0.3514 | 0.8887 | 0.9069 | 27.8 | 1.25 |

Test evaluation with the 2-epoch best checkpoint: **top-1 0.9175, macro-F1 0.9144**.

Findings:
1. **VRAM:** 1.25 GiB peak at batch 64 with AMP — far under the 8 GiB budget; batch 64 confirmed, no OOM risk.
2. **Epoch time:** 27.8 s steady-state (epoch 1 includes warmup) ⇒ **25 epochs ≈ 12 minutes** — well under the provisional 25–75 min estimate; the full-run schedule is comfortable.
3. **Convergence:** val 0.9069 after 2 epochs — above the design's "clearly above 90%" early-signal threshold; the ~95–99% expectation band for the full run is plausible. LR remains at 1e-3 until epoch 8 (StepLR).
4. Pilot artifacts: `runs/starnet_s2_eurosat_pilot/` (history.json, best.pt, metrics.json, curves.png, confusion_matrix.png).

**G4 (full 25-epoch run):** the required pre-training notification was issued 2026-09-18 in the same turn (task, hyperparameters, projected ~12 min, output directory). The launch was then blocked by the session's auto-mode classifier, which reads "在正式训练前需要通知我一声" as requiring explicit supervisor acknowledgment; G4 therefore awaited a one-click confirmation via AskUserQuestion before launching; the supervisor selected "确认启动 (Recommended)" and the run was launched (U013-confirmation/A025).

---

## 2026-09-18 — G4: full 25-epoch run (completed, exit 0)

Command: `python src/train_starnet_eurosat.py --epochs 25 --out runs/starnet_s2_eurosat`

| Metric | Value |
|---|---|
| Total wall time | ≈ 12.9 min (98.7 s warmup + 24 × ~28.3 s, incl. final test eval) |
| Peak VRAM | 1.25 GiB every epoch (batch 64, AMP) |
| Best val_acc | 0.9738 (epoch 23; epoch 24 equal) |
| Final-epoch val_acc | 0.9711 (epoch 25) |
| **Test top-1 accuracy** | **0.9765** |
| **Test macro-F1** | **0.9758** |
| Best checkpoint | epoch 23 (selected automatically by val_acc) |

Per-class test accuracy (weakest → strongest): PermanentCrop 0.9493, AnnualCrop 0.9511, Pasture 0.9633, HerbaceousVegetation 0.9733, Highway 0.9760, River 0.9760, Industrial 0.9840, SeaLake 0.9933, Forest 0.9956, Residential 0.9956.

Main confusions (true → predicted): PermanentCrop → HerbaceousVegetation 12; AnnualCrop → PermanentCrop 12; AnnualCrop → Pasture 5 — all agricultural/vegetation look-alikes; water and built-up classes are near-perfect.

Findings:
1. Result is inside the pre-registered ~95–99% expectation band (design doc §5).
2. vs the published anchor 98.57% (Helber et al., IEEE J-STARS 2019): 0.92 points below, under a deliberately lightweight protocol (3.7M-param / 0.5-GMACs model, official PyTorch transfer-learning recipe, 25 epochs, no heavy augmentation). Beating that anchor was explicitly NOT the goal (design doc §5).
3. LR schedule visible in the curve: val_acc jumps at epoch 8 when lr drops 1e-3 → 1e-4, then plateaus at 0.971–0.974; the epoch-4 dip (0.8881) recovered without intervention.
4. Best-checkpoint selection by val_acc worked as designed (epoch 23, not the final epoch).
5. Artifacts: `runs/starnet_s2_eurosat/` — best.pt, history.json, metrics.json, curves.png, confusion_matrix.png, split_indices.json.

**Stage 03 backend complete (G1–G4). Next steps each require separate supervisor approval: Grad-CAM visualizations, HTML visualization interface (Stage 04), final-report outline (Stage 05), source-code publication (grading criterion 6).**

---

## 2026-09-18 — Transfer-learning ablation: "before training" baseline (completed)

Supervisor approved a read-only baseline evaluation (U017 + AskUserQuestion "批准补测"). Command: `python src/eval_baseline.py` (new script `src/eval_baseline.py`, reuses `SplitDataset`/`build_model`/`evaluate`/`make_transform` from the training script; no training, no downloads).

| Model | Test top-1 | Test macro-F1 |
|---|---|---|
| Before fine-tuning (ImageNet-1k backbone + randomly initialized 10-class head, seed 42) | 0.1281 | 0.0882 |
| Reference: majority-class predictor (largest test class 450/4050) | 0.1111 | — |
| After fine-tuning (G4 best checkpoint, epoch 23) | **0.9765** | **0.9758** |

Findings:
1. The un-fine-tuned model scores 12.81% — at the level of the majority-class baseline (11.11%) and 10-class chance (10%), as expected: the ImageNet 1000-class head was replaced by a randomly initialized head, so the pretrained features alone carry no 10-class EuroSAT decision.
2. Fine-tuning contributes the entire improvement: **+84.84 points** (12.81% → 97.65%).
3. Reproducibility note: the baseline uses the same seed 42 and head initialization as the formal run, so it is exactly the G4 model at epoch 0.
4. Artifact: `runs/starnet_s2_eurosat/baseline_untrained_head.json`; script: `src/eval_baseline.py`.

---
