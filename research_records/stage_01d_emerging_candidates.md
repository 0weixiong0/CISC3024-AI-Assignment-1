# Stage 01d: Emerging Candidates Investigation — LSNet, RepNeXt, STResNet, Q-Former Autoencoder

Date: 2026-09-18. Status: research-only (no downloads, installations, cloning, or executions). Triggered by supervisor request U006: verify the four candidates flagged with unverified data in Stage 01b (Section 8.7 / DEEP_RESEARCH_MODEL_SELECTION.md), determine whether any beats StarNet-S2, and extend the horizontal comparison to a complete set. Method: four parallel deep-research subagents (one per candidate), primary-sources-only policy, credibility tiers, UNSUPPORTED flagging. All findings below carry source numbers unique to this file.

---

## 1. LSNet (CVPR 2025) — verified, strong challenger

**Identity and disambiguation.** "LSNet: See Large, Focus Small", Ao Wang, Hui Chen, Zijia Lin, Jungong Han, Guiguang Ding (Tsinghua / Liverpool), CVPR 2025 proceedings pp. 9718-9729. Unrelated to the homonymous 2020 large-kernel detection LSNet and the 3D point-cloud LSNet. arXiv:2503.23135 (v1, 2025-03-29). [1][2][6]

**Verified variant metrics (paper Table 1, ImageNet-1k, 224x224)** [2][3][4]:

| Model | Params (M) | FLOPs (G) | Throughput (img/s, RTX 3090) | Top-1 (%) | Top-1 distilled* |
|---|---|---|---|---|---|
| LSNet-T | 11.4 | 0.3 | 14,708 | 74.9 | 76.1 |
| LSNet-S | 16.1 | 0.5 | 9,023 | 77.8 | 79.0 |
| LSNet-B | 23.2 | 1.3 | 3,996 | 80.3 | 81.6 |

(*distilled variants; reproducing them is out of assignment scope.)

**Code and weights.** Official repo THU-MIG/lsnet (the abstract itself links github.com/jameslahm/lsnet — same project; jameslahm is first author Ao Wang's handle) [3][5]. License MIT per the official HuggingFace model card (GitHub LICENSE file content not directly fetched — see UNSUPPORTED register). All ImageNet-1k checkpoints (plus distilled variants and training logs) downloadable from HuggingFace `jameslahm/lsnet` (lsnet_t.pth / lsnet_s.pth / lsnet_b.pth), and the card documents a one-line timm load: `timm.create_model('hf_hub:jameslahm/lsnet_b', pretrained=True)`; sibling ids `hf_hub:jameslahm/lsnet_t`, `hf_hub:jameslahm/lsnet_s` [3][4].

**Mechanism.** LS (Large-Small) convolution = large-kernel perception (LKP, depthwise K=7) that "sees large", followed by small-kernel aggregation (SKA, dynamic K=3 conv over channel groups, mixing weights generated from the LKP output) that "focuses small" [5][2]. Report cost: one figure + ~2 equations — more than StarNet's single `y = f(x) ⊙ g(x)`, but the paper's own perception/aggregation vocabulary writes half the section for you.

**Feasibility (8 GiB RTX 4060 Laptop, Python 3.12.10, torch 2.7.1+cu128).** No red flags: plain PyTorch, no custom CUDA kernels, no flash-attention dependency [3]. LSNet-T fine-tuning at 224x224 batch 16-32 fits comfortably. The repo's conda recipe pins Python 3.8 for its ImageNet training scripts — irrelevant when loading via timm. Note: only 3x StarNet-S2's parameter count with comparable top-1 (T) or clearly better top-1 (S).

**Assessment vs StarNet-S2.** Beats it on recency (CVPR 2025 vs 2024), compute efficiency (0.3G vs 547M FLOPs at equal top-1 for T), and headline potential (S: 77.8%). Practicality is equal or better (official HF checkpoints, timm one-liner, MIT). The only dimension where StarNet-S2 still wins is explainability cost (one equation vs two coupled components). **Verdict: the only candidate across Stages 01a-01d that rivals StarNet-S2 on rubric fit; a genuine alternative, final call rests with the supervisor.**

## 2. RepNeXt (arXiv 2406.16004) — real; "M4" confirmed; not recommended

**Identity.** "RepNeXt: A Fast Multi-Scale CNN using Structural Reparameterization", Mingshu Zhao, Yi Luo, Yong Ouyang, arXiv:2406.16004 (v1 2024-06-23, v2 2024-07-20) [11]. The arXiv comments field reads verbatim "Tech report; added general view of the operations and convnext ablation experiments"; no venue acceptance found (targeted search + Semantic Scholar, as of 2026-09-18) [11][14][15]. The prior "Alibaba/Damo" affiliation is UNSUPPORTED (no affiliation listed on arXiv; first author's GitHub is `suous`) [11][12].

**Supervisor's "RepNeXt-M4" is REAL.** Variant naming is M0-M5; the prior claim "13.3M params, 82.3% top-1" belongs to M4 — CONFIRMED (paper Table 2 also gives 1.48 ms latency) [11][12].

**Verified variant metrics** [11][12]:

| Variant | Params | FLOPs | Top-1 |
|---|---|---|---|
| RepNeXt-M0* | 2.3M | 0.4G | 74.2% |
| RepNeXt-M1 | 4.8M | 0.8G | 78.8% |
| RepNeXt-M2 | 6.5M | 1.1G | 80.1% |
| RepNeXt-M3 | 7.8M | 1.3G | 80.7% |
| RepNeXt-M4 | 13.3M | 2.3G | 82.3% |
| RepNeXt-M5 | 21.7M | 4.5G | 83.3% |

(*M0 row sourced from the official README; whether M0 appears in the paper's own table is a minor uncertainty.)

**Code and weights.** github.com/suous/RepNeXt, MIT; models integrate with timm by importing the repo's own model files (`timm.models.create_model('repnext_m1')`) — no upstream timm model card, no HuggingFace/ModelScope card found [12]. Checkpoints are GitHub release v1.0 assets, fused (deploy-form) and distilled 300 epochs with a RegNetY-16GF teacher (verbatim-verified asset: `.../releases/download/v1.0/repnext_m0_distill_300e_fused.pt`; full asset list not fetched) [12][13].

**Mechanism.** Structural re-parameterization: multi-branch train-time convolutions merged into single large-kernel convolutions at inference; reported checkpoints additionally use knowledge distillation. No custom CUDA kernels found [11][12]. Because shipped checkpoints are fused, fine-tuning happens in deploy form — the reparameterization story becomes a reportable explanation rather than part of the actual training loop.

**Assessment vs StarNet-S2.** Paper metrics dominate (M0: same accuracy class at half the size; M1: +4.0 top-1 at 4.8M/0.8G), but three rubric mismatches: (1) unrefereed tech report vs CVPR paper; (2) no timm/HF card — weights must be pulled from a GitHub release and loaded through repo code; (3) reparameterization + SE + distillation is a longer explanation than the star operation. README env recipe says Python 3.8 (soft risk on Python 3.12). **Verdict: does not beat StarNet-S2 for this assignment; if ever used, M1 is the sensible variant.**

## 3. STResNet (arXiv 2601.05364) — real, corrected; not viable

**Existence confirmed; earlier note was accurate, not a hallucination.** "STResNet & STYOLO: A New Family of Compact Classification and Object Detection Models for MCUs", Sudhakar Sah, Ravish Kumar, arXiv 2026-01-08 [21][22]. Entirely distinct from the crowd-flow STResNet (Zhang, Zheng & Qi, AAAI 2017 — the earlier disambiguation note said IJCAI; AAAI is correct [26]). Affiliation not stated verbatim, but STM32N6 benchmarking and the official `STMicroelectronics` HuggingFace org make STMicroelectronics near-certain [22][24]. It is Tucker-decomposition-based compression of ResNet-18 — NOT shift-based (that earlier hypothesis was wrong).

**Corrections to the Stage 01b note.** The quoted "0.95M-3.99M params, 58.8%-71.6%" matches Nano-Tiny exactly, but the family actually spans Pico-Tiny: **0.60M-3.99M params, 48.8%-71.6% top-1**. **The paper reports no FLOPs anywhere** (tables give params, top-1, RAM, STM32N6 latency), so no FLOPs comparison with StarNet's 547M is possible.

**Verbatim Table 6 rows (ImageNet-1k, FP32)** [22]:

| Model | Params (M) | Top-1 (%) | RAM (MB) | STM32N6 latency (ms) |
|---|---|---|---|---|
| STResNetTiny | 3.99 | 71.6 | 1.39 | 21.29 |
| STResNetMilli | 3.00 | 70.0 | 1.39 | 18.29 |
| STResNetMicro | 1.50 | 66.7 | 0.882 | 14.36 |
| STResNetNano | 0.95 | 58.8 | 0.833 | 10.91 |
| STResNetPico | 0.60 | 48.8 | 0.833 | 8.24 |
| MobileNetV2-1.00 (baseline) | 3.50 | 71.8 | 2.01 | 22.44 |

Training: "All the models are trained on ImageNet dataset using default timm training pipeline for 300 epochs" [22].

**Code and weights: none for classification.** No own GitHub repo cited, no license stated, no code-availability claim; HuggingFace hosts only STYOLO detection checkpoints [24]; no timm card exists (timm is only their training pipeline) [22][25].

**Assessment vs StarNet-S2.** Not viable: no pretrained weights (fine-tuning impossible — from-scratch on a modest dataset after hand-rebuilding the architecture), no code page (fails grading criterion 6), no FLOPs for the results table, preprint only. Mention-worthy only as a "candidates considered" citation. **Verdict: reject.**

## 4. Q-Former Autoencoder (WACV 2026) — real, confirmed; not viable

**Identity.** "Q-Former Autoencoder: A Modern Framework for Medical Anomaly Detection", Francesco Dalmonte, Emirhan Bayar, Emre Akbas, Mariana-Iuliana Georgescu. WACV 2026 confirmed as poster #732 (virtual site), with official CVF Open Access PDF, IEEE Xplore record (doc 11492624), arXiv:2507.18481, DOI 10.48550/arXiv.2507.18481 [31][32][33][37].

**Code and weights.** Official repo `emirhanbayar/QFAE`, MIT, `environment.yml`-based; official HuggingFace checkpoints `ebayar/QFAE-checkpoints` (brain/liver/chest/resc `last_ckpt.pth`) [34][36].

**Architecture and results.** Frozen DINOv2 ViT-L/14 backbone (~300M params frozen), Q-Former bottleneck with 784 learnable queries, 6-layer Transformer decoder; reconstruction-based scoring; batch 64, 300 epochs [35]. Benchmarks are exclusively medical: BraTS2021 ~94.1-94.3, RESC ~91.8-91.9, RSNA ~83.8-84.2, LiverCT 65.5 AUROC (README vs paper HTML digits differ by 0.1-0.4 — a direct PDF read would be needed before quoting). **No MVTec AD, VisA, or BTAD results anywhere** [34][35].

**Assessment vs baselines.** Not viable on four grounds: (1) wrong track — no MVTec numbers means no head-to-head against EfficientAD-S's 98.8% image AUROC, and reproducing it on MVTec means building a new protocol; (2) compute — frozen ViT-L/14 with 784-token inputs plus 300-epoch training far exceeds 8 GiB / 3 days; medical datasets themselves are multi-GB; (3) explainability — a learned-query information bottleneck over a foundation model is much harder to explain than the star operation; (4) no ImageNet classification at all, so no comparison to StarNet-S2. One defensible use: cite it as evidence the AI-driven search surfaced a brand-new WACV 2026 paper that was then filtered out on feasibility (supports grading criterion 1). **Verdict: reject.**

## 5. UNSUPPORTED register (Stage 01d additions)

| # | Claim | Status | Notes |
|---|---|---|---|
| U1 | LSNet GitHub LICENSE file content | Unverified | MIT asserted via official HF card [4] only |
| U2 | LSNet FLOPs unit (GMACs vs GFLOPs) | Unverified | Affects exact comparison with StarNet's 547M FLOPs |
| U3 | LSNet main-result training schedule (epochs) | Unverified | One appendix quote says "100 epochs" for analyses |
| U4 | LSNet timm stock-registry name (non-hf_hub) | Unverified | Moot: hf_hub loading needs only a recent timm |
| U5 | RepNeXt Alibaba/Damo affiliation | Unsupported | No affiliation on arXiv; repo owner `suous` [11][12] |
| U6 | RepNeXt M1-M5 release asset URLs | Unverified | Fetch blocked; existence strongly implied by README |
| U7 | RepNeXt venue acceptance | None found | Tech report per arXiv comments [11] |
| U8 | RepNeXt M0 presence in paper table | Unverified | M0 row from README [12] |
| U9 | STResNet author affiliation (STMicroelectronics) | Inferred, not verbatim | From STM32N6 benchmarking + ST HF org [22][24] |
| U10 | QFAE total trainable parameter count | Unverified | Only frozen-backbone scale (~300M ViT-L/14) known |
| U11 | QFAE exact AUROC digits | Conflicting 0.1-0.4 | README [34] vs paper HTML [35]; needs PDF read before quoting |
| U12 | QFAE training GPU / wall-clock, dependency pins | Unverified | Only "CUDA" found; environment.yml pins not extracted |

## 6. Eleven-candidate horizontal comparison (complete set)

Rows 1-7 carry over Stage 01c findings; rows 8-11 are this stage's verified results. "Accuracy" is each paper's own headline metric — cross-track numbers are NOT comparable (ImageNet top-1 vs MVTec AUROC vs super-resolution PSNR).

| # | Candidate | Track | Params | Accuracy (paper) | Weights / license | Rubric fit notes |
|---|---|---|---|---|---|---|
| 1 | StarNet-S2 (CVPR 2024) | Classification | 3.7M | 74.8% top-1 | Author-trained; timm; Apache-2.0 | 1-equation explainability; timm-native |
| 2 | MobileNetV4-Conv-S (ECCV 2024) | Classification | 3.8M | 73.8% top-1 (paper training; timm weights are a 2400-epoch reproduction) | timm; Apache-2.0 | 2-3 concepts (UIB, ExtraDW, NAS) |
| 3 | RepViT-M0.9 (CVPR 2024) | Classification | 5.1M/5.5M | 78.7%/79.1% top-1 | Author-trained, distilled; timm; Apache-2.0 | 3-4 concepts; param accounting unresolved |
| 4 | ShiftwiseConv SW-Tiny (CVPR 2025) | Classification | 31M | 83.4% top-1 | MIT (Meta); one Drive weight | Custom CUDA; Python 3.8; multi-layer shift story |
| 5 | LSNet-T (CVPR 2025) | Classification | 11.4M | 74.9% top-1 (76.1% distilled) | Official HF; MIT; timm hf_hub one-liner | LKP+SKA; ~1 figure + 2 equations; no CUDA |
| 6 | LSNet-S (CVPR 2025) | Classification | 16.1M | 77.8% top-1 (79.0% distilled) | Official HF; MIT; timm hf_hub one-liner | Stronger headline; same story cost |
| 7 | RepNeXt-M1 (arXiv 2024 tech report) | Classification | 4.8M | 78.8% top-1 | GitHub release (fused, distilled); MIT; no timm card | Unrefereed; reparam+SE+distillation story |
| 8 | STResNet-Tiny (arXiv 2026-01 preprint) | Classification | 3.99M | 71.6% top-1 | **None** (no code, no weights, no license) | MCU-focused; no FLOPs reported |
| 9 | EfficientAD-S (WACV 2024) | Anomaly | 1.6M (scope ambiguous) | 98.8% MVTec image AUROC | Unofficial repo; Apache-2.0 | Auxiliary-image subset unverified |
| 10 | Dinomaly ViT-S (CVPR 2025) | Anomaly | 37.4M (B) | ViT-S AUROC unrecovered | Apache-2.0; only ViT-B checkpoints | 24 GB reference setup |
| 11 | PLKSR-tiny (2024/2026) | Restoration | Not reported | 38.11 dB Set5 x2 (Y-channel) | MIT; Drive; BasicSR-based | 450k-iteration protocol infeasible |

(Q-Former Autoencoder is excluded from the table body as it has no classification result and no MVTec result — no comparable metric exists; see Section 4.)

## 7. Updated recommendation

**Primary — StarNet-S2, classification track (unchanged).** After verifying all four emerging candidates, StarNet-S2 remains the safest rubric-optimal choice: lowest explainability cost for grading criterion 2, author-trained native-timm weights, cleanest implementation path within the 3-day window. None of the four new investigations weakened this position; three of the four candidates (RepNeXt, STResNet, QFAE) failed practicality outright.

**Newly verified strong alternative — LSNet-T (or LSNet-S), classification track.** LSNet is the only candidate in the entire Stage 01a-01d search that matches or beats StarNet-S2 on practicality (official MIT checkpoints, timm one-liner, no CUDA, 8 GiB comfortable) while adding CVPR 2025 recency and equal-or-better accuracy-per-compute (T: 74.9% at 0.3G; S: 77.8% at 0.5G). Its single cost is explainability (two coupled components vs one equation). **If the supervisor values 2025 recency and the "see large, focus small" narrative, LSNet-T/S is the pick; if the supervisor values the shortest possible algorithm explanation, StarNet-S2 stays.** Both are Stage-02-ready; the decision is the supervisor's alone.

**Everything else:** rejected with documented reasons (Sections 2-4 above; Stage 01b/01c files for ShiftwiseConv, Dinomaly, PLKSR, RepViT; EfficientAD-S remains conditional runner-up in the anomaly track under its two gates).

This recommendation is submitted for supervisor decision; it does not authorize installation, downloads, or training.

## 8. APA7-ready source additions (Stage 01d)

All papers below have direct PDF links for later citation; software entries follow the report's paper-vs-distributor separation rule.

- Dalmonte, F., Bayar, E., Akbas, E., & Georgescu, M.-I. (2026). Q-Former autoencoder: A modern framework for medical anomaly detection. In *Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision*. https://openaccess.thecvf.com/content/WACV2026/papers/Dalmonte_Q-Former_Autoencoder_A_Modern_Framework_for_Medical_Anomaly_Detection_WACV_2026_paper.pdf — Tier 1 [33]
- Sah, S., & Kumar, R. (2026). STResNet & STYOLO: A new family of compact classification and object detection models for MCUs [Preprint]. *arXiv*. https://arxiv.org/abs/2601.05364 (PDF: https://arxiv.org/pdf/2601.05364) — Tier 1 [21]
- Wang, A., Chen, H., Lin, Z., Han, J., & Ding, G. (2025). LSNet: See large, focus small. In *Proceedings of the 2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition* (pp. 9718-9729). https://openaccess.thecvf.com/content/CVPR2025/papers/Wang_LSNet_See_Large_Focus_Small_CVPR_2025_paper.pdf — Tier 1 [1]
- Zhao, M., Luo, Y., & Ouyang, Y. (2024). RepNeXt: A fast multi-scale CNN using structural reparameterization [Preprint]. *arXiv*. https://arxiv.org/abs/2406.16004 (PDF: https://arxiv.org/pdf/2406.16004) — Tier 1 [11]
- Bayar, E. (n.d.). *QFAE* [Computer software]. GitHub. Retrieved September 18, 2026, from https://github.com/emirhanbayar/QFAE — Tier 1 [34]
- jameslahm. (n.d.). *lsnet_b* [Model card]. Hugging Face. Retrieved September 18, 2026, from https://huggingface.co/jameslahm/lsnet_b — Tier 1 [4]
- THU-MIG. (n.d.). *LSNet* [Computer software]. GitHub. Retrieved September 18, 2026, from https://github.com/THU-MIG/lsnet — Tier 1 [3]
- Zhao, M. (n.d.). *RepNeXt* [Computer software]. GitHub. Retrieved September 18, 2026, from https://github.com/suous/RepNeXt — Tier 1 [12]

### Numbered source list (this file)

- [1] CVF Open Access, CVPR 2025, LSNet paper page + PDF (Tier 1) — https://openaccess.thecvf.com/content/CVPR2025/html/Wang_LSNet_See_Large_Focus_Small_CVPR_2025_paper.html
- [2] arXiv:2503.23135 abs/HTML (Tier 1) — https://arxiv.org/abs/2503.23135
- [3] THU-MIG/lsnet official repo (Tier 1) — https://github.com/THU-MIG/lsnet
- [4] jameslahm/lsnet_b HuggingFace model card (Tier 1) — https://huggingface.co/jameslahm/lsnet_b
- [5] HuggingFace Papers mirror of arXiv:2503.23135 (Tier 2) — https://huggingface.co/papers/2503.23135
- [6] CVPR 2025 Virtual poster #34284 (Tier 1) — https://cvpr.thecvf.com/virtual/2025/poster/34284
- [11] arXiv:2406.16004 abs/HTML (Tier 1) — https://arxiv.org/abs/2406.16004
- [12] suous/RepNeXt official repo README (Tier 1) — https://github.com/suous/RepNeXt
- [13] RepNeXt release v1.0 asset URL (Tier 1, verbatim URL; list not fetched) — https://github.com/suous/RepNeXt/releases/download/v1.0/repnext_m0_distill_300e_fused.pt
- [14] Semantic Scholar record (Tier 2) — https://www.semanticscholar.org/paper/bc1df10bdf209d34b01747daae4d6284be714495
- [15] CVPR 2025 program pages (Tier 2, negative evidence) — https://cvpr.thecvf.com/Conferences/2025
- [21] arXiv:2601.05364 abs (Tier 1) — https://arxiv.org/abs/2601.05364
- [22] arXiv:2601.05364 HTML v1 full text (Tier 1) — https://arxiv.org/html/2601.05364v1
- [23] HuggingFace Papers mirror (Tier 1) — https://huggingface.co/papers/2601.05364
- [24] STMicroelectronics/STYOLOTiny HF card (Tier 1, negative evidence for classification weights) — https://huggingface.co/STMicroelectronics/STYOLOTiny
- [25] timm repository (Tier 1, negative evidence: no STResNet entry) — https://github.com/rwightman/pytorch-image-models
- [26] Zhang, J., Zheng, Y., & Qi, D. (2017). Deep spatio-temporal residual networks. AAAI 2017 (Tier 1, disambiguation only) — https://arxiv.org/abs/1610.06856
- [31] arXiv:2507.18481 abs (Tier 1) — https://arxiv.org/abs/2507.18481
- [32] WACV 2026 virtual poster #732 (Tier 1) — https://wacv.thecvf.com/virtual/2026/poster/732
- [33] CVF Open Access WACV 2026 PDF (Tier 1) — https://openaccess.thecvf.com/content/WACV2026/papers/Dalmonte_Q-Former_Autoencoder_A_Modern_Framework_for_Medical_Anomaly_Detection_WACV_2026_paper.pdf
- [34] emirhanbayar/QFAE official repo (Tier 1) — https://github.com/emirhanbayar/QFAE
- [35] arXiv:2507.18481 HTML full text (Tier 1) — https://arxiv.org/html/2507.18481
- [36] ebayar/QFAE-checkpoints HF card (Tier 1) — https://huggingface.co/ebayar/QFAE-checkpoints
- [37] IEEE Xplore doc 11492624 (Tier 1) — https://ieeexplore.ieee.org/abstract/document/11492624/
