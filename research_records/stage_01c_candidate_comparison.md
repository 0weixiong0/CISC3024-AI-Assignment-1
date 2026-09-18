# Stage 01c — Horizontal Comparison of All Candidates and Track-Level Recommendation

Date: 2026-09-18

Request: Supervisor directive (U005) to investigate the remaining shortlisted candidates (MobileNetV4-Conv-Small, RepViT-M0.9, EfficientAD, Dinomaly, PLKSR), compare them horizontally against StarNet-S2 and ShiftwiseConv, and record all consulted literature with PDF links for later APA 7 citation.

Method: three parallel retrieval subagents under the installed deep-research workflow (adapted as a gap-fill wave of the Stage 01 run; Phase 0 clarifications were already answered earlier in this project). Budget actually used: 18 WebSearch attempts and 15 WebFetch attempts across the three agents, including 3 failed searches and several blocked/404 fetches. RESEARCH ONLY: no datasets, checkpoints, or packages were downloaded; no model code was executed; no repositories were cloned. All numbers below are primary-source values unless explicitly marked UNSUPPORTED.

Evidence policy: values recovered in this wave do not retroactively upgrade Stage 01 verification; they extend it. Any conflict between this file and Stage 01 is flagged rather than silently resolved.

## Track A — Classification: MobileNetV4-Conv-Small and RepViT-M0.9

### New primary-source findings

1. MobileNetV4-Conv-S paper accuracy: the arXiv HTML attributes "MNv4-Conv-S is 73.8% Top-1, 3.8M params, 0.2G MACs" to Table 6 (same table: Conv-M 79.9%, Conv-L 82.9%). CRITICAL PROVENANCE SPLIT: this accuracy corresponds to Google's paper training, while the timm checkpoint (`mobilenetv4_conv_small.e2400_r224_in1k`, 2400 epochs, trained by Ross Wightman) is an independent reproduction; the card does not state the timm weights' achieved top-1. The final report must quote paper accuracy and timm-weights accuracy as separate claims.
2. Venue: ECCV 2024 oral confirmed via the ECVA virtual site (oral 482). The exact ECVA proceedings PDF path was not resolved; cite the virtual page plus arXiv.
3. timm integration confirmed: the card documents `timm.create_model("hf_hub:timm/mobilenetv4_conv_small.e2400_r224_in1k", pretrained=True)`. Card BibTeX first author: Qin, Danfeng (not "Bolya").
4. MobileNetV4 has no official PyTorch release from Google; the working PyTorch implementation/weights page is the timm card and collection.
5. RepViT CVF proceedings entry verified: CVPR 2024, pp. 15909-15920, PDF at openaccess.thecvf.com; author list per CVF: Ao Wang, Hui Chen, Zijia Lin, Jungong Han, Guiguang Ding. Note the timm card's arXiv BibTeX lists Hengjun Pu instead of Jungong Han; the CVF list governs the proceedings citation.
6. RepViT parameter discrepancy characterized: paper Table 1 M0.9 = 5.1M / 0.8 GMACs; timm card = 5.5M / 0.8 GMACs. GMACs match exactly, so only the parameter-counting convention differs (candidates: fused inference graph vs. unfused module incl. head/BN). Root cause: UNSUPPORTED. Report should quote both numbers side-by-side.
7. Explainability cost (from paper descriptions): MobileNetV4-Conv-S requires explaining the UIB micro-block, ExtraDW, and NAS provenance (~2-3 concepts; Mobile MQA applies only to Hybrid variants and can be excluded). RepViT requires mobile block + SE + fusing-and-reparameterizing design + structural re-parameterization (~3-4 concepts). StarNet-S2 baseline: 1 equation.
8. Transfer evidence: RepViT's paper demonstrates downstream fine-tuning on COCO and ADE20k. MobileNetV4 fine-tuning on small custom datasets is demonstrated by third-party tutorials (Roboflow, Tier 2). Published fine-tuning VRAM figures at 224px batch 16-32: UNSUPPORTED for both.

## Track B — Anomaly detection: EfficientAD and Dinomaly

### New primary-source findings

1. EfficientAD parameter count recovered: paper states EfficientAD-S and -M use "1.6 and 2.7 million" parameters (contrasted against GCAD's 31 million). SCOPE AMBIGUITY: the fetched passage does not state whether this covers the full pipeline (teacher + student + autoencoder) or teacher-student only. Either way it is below StarNet-S2's 3.7M.
2. MVTec AD image-level AUROC: EfficientAD-S 98.8%, EfficientAD-M 99.1% (paper). Inference latency 2.2 ms (-S) / 4.5 ms (-M) on RTX A6000.
3. Training wall-clock: paper reports approximately "twenty minutes" per MVTec category on an RTX A6000. No consumer-GPU (RTX 4060) figure exists; a 3-4x slowdown extrapolation keeps per-category training under ~2 hours.
4. Auxiliary-image obligation stands: the student regularization penalty consumes images from a pretraining dataset such as ImageNet; the community repo confirms ImageNet. Exact subset, image count, and download size: UNSUPPORTED. This is the single largest feasibility unknown for the anomaly route.
5. Repository: github.com/nelson1425/EfficientAD is an UNOFFICIAL community implementation (the paper's authors do not host code), Apache-2.0, with pretrained teacher checkpoints provided in its /models directory. There is no author-owned code release.
6. Dinomaly repository: github.com/guojiajeremy/Dinomaly is live, Apache-2.0. README offers pretrained checkpoints for Dinomaly-B (Base) on MVTec/VisA/Real-IAD via Google Drive; ViT-Small checkpoints NOT confirmed. Reference setup: Python 3.8.12 and an RTX 3090 (24 GB). README training command uses 20k iterations for MVTec (the paper said 10,000) — a paper/README discrepancy to flag if this route is chosen.
7. DINOv2-with-registers backbone weight file size and ViT-Small training footprint at 392px: UNSUPPORTED. ViT-Small MVTec AUROC: UNSUPPORTED this wave (Stage 01 values for ViT-S/Base complexity remain: 37.4M/26.3G and 148.0M/104.7G).
8. Dataset: MVTec AD owner page confirms 15 categories, 5,000+ images, CC BY-NC-SA 4.0 with explicit noncommercial wording. Archive byte size: UNSUPPORTED (commonly cited ~5 GB; verify on the download page before committing disk space).

## Track C — Restoration: PLKSR (SPAN/ESPAN supplementary)

### New primary-source findings

1. CRITICAL: the PLKSR paper does NOT report parameters/MACs/FLOPs for its own variants. It deliberately reports Latency (ms) and MGO (max GPU memory occupancy, MB) on HD (1280x720) input at RTX 4090 FP16, framed as a critique of FLOPs-based comparison. Verbatim Table 1 rows: EDSR-baseline 316G/1370K/9.9ms/320.2MB; RCAN 3530G/15444K/101.8ms/401.2MB; SwinIR-light 243.7G/910K/124.9ms/1764.3MB; SRFormer-light 229.4G/853K/152.7ms/1744.4MB. Per-scale PLKSR-tiny (Table 4, same protocol): x2 16.6ms/228.5MB; x3 5.9ms/103.2MB; x4 3.6ms/65.3MB. Any third-party "PLKSR-tiny = 137K params" style tuples are non-primary.
2. PSNR/SSIM recovered verbatim (Table 4, Y-channel, scale-equal border crop; DIV2K-trained tiny): x2 Set5 38.11/0.9608, Set14 33.73/0.9193, BSD100 32.25/0.9008, Urban100 32.43/0.9314, Manga109 38.84/0.9775; x4 Set5 32.18/0.8956, Set14 28.67/0.7838, BSD100 27.61/0.7380, Urban100 26.12/0.7888, Manga109 30.52/0.9087; x3 DIV2K: Set5 34.50/0.9279, Set14 30.45/0.8447, BSD100 29.15/0.8070, Urban100 28.35/0.8571, Manga109 33.71/0.9460.
3. Training protocol (verbatim basis): DIV2K (and a DF2K variant), L1 loss, 64 patches of 96x96, Adam, 450k iterations. DIV2K official page: 800 train / 100 val / 100 test images, "academic research purpose only"; exact zip sizes not shown (UNSUPPORTED). From-scratch training on the paper protocol is infeasible within the deadline on an RTX 4060; the realistic path would be fine-tuning/evaluating released checkpoints.
4. Repository: github.com/dslisleedh/PLKSR is MIT-licensed, built on the BasicSR framework, with pretrained models in a single Google Drive folder whose variant/scale contents were not itemized (UNSUPPORTED).
5. Evaluation convention: all benchmark numbers are Y-channel PSNR/SSIM, not RGB — any cross-track comparison table must state the convention.
6. ESPAN: CVF CVPR 2025 Workshops (NTIRE) page verified to exist; headline numbers NOT extracted (UNSUPPORTED). SPAN's own tables: still UNSUPPORTED; the previously withdrawn tuples remain withdrawn. Context: the NTIRE 2025 ESR challenge report (arXiv 2504.10686) and PLKSR-Rep (CVPRW 2026) confirm the design lineage is current, but neither was audited in depth.

## Horizontal Comparison Table (all seven candidates)

| Candidate | Track | Params (primary source) | Reported accuracy | Weight provenance / license | 8 GiB + deadline feasibility | Implementation complexity | Report explainability | Evidence quality |
|---|---|---|---|---|---|---|---|---|
| StarNet-S2 (CVPR 2024) | Classification | 3.7M | 74.8% ImageNet top-1 | Author-trained; timm; Apache-2.0 | Highest headroom; simplest pipeline | timm-native, no custom ops | 1 equation (y = f(x) ⊙ g(x)) | Verified (paper + card) |
| MobileNetV4-Conv-S (ECCV 2024) | Classification | 3.8M | 73.8% top-1 (Google training; timm weights are a reproduction) | timm-trained (Wightman); Apache-2.0 | High headroom | timm-native | UIB + ExtraDW + NAS (~2-3 concepts) | Verified; paper-vs-weights accuracy split |
| RepViT-M0.9 (CVPR 2024) | Classification | 5.1M (paper) / 5.5M (card) | 78.7% (300e) / 79.1% (450e) | Author-trained, distilled; timm; Apache-2.0 | High headroom | timm-native | Mobile block + SE + re-parameterization (~3-4 concepts) | Verified; unresolved param-count discrepancy |
| ShiftwiseConv SW-Tiny (CVPR 2025) | Classification | 31M (corrected) | 83.4% top-1 | MIT (Meta); single Drive-hosted weight | Untested shift-op memory behavior | Custom CUDA compile; Python 3.8 pin | Multi-layer shift accumulation | Verified after correction |
| EfficientAD-S (WACV 2024) | Anomaly | 1.6M (pipeline scope ambiguous) | 98.8% MVTec image AUROC | Unofficial repo (nelson1425); Apache-2.0; teacher ckpts included | ~20 min/category on A6000; ImageNet auxiliary images UNSUPPORTED = main blocker | Standalone repo; no timm | Teacher-student + AE + penalty (~4 concepts) | Partial (param scope + aux subset unverified) |
| Dinomaly ViT-S (CVPR 2025) | Anomaly | 37.4M | ViT-S MVTec AUROC not recovered | Apache-2.0 repo; only ViT-B checkpoints confirmed | Reference GPU is 24 GB; batch cuts + dependency risk (Python 3.8-era pins) | DINOv2 backbone + custom decoder | Frozen DINOv2 + noisy MLP + 8-layer decoder (~4-5 concepts) | Partial |
| PLKSR-tiny (2024 preprint / 2026 IEEE Access) | Restoration | Not reported by paper (latency/MGO convention) | x2 Set5 38.11 dB (Y-channel) | MIT repo; Drive checkpoints; BasicSR-based | 450k-iteration protocol infeasible from scratch; fine-tune-only path | BasicSR framework + Drive downloads | Partial large-kernel conv (moderate) | Partial (params absent from paper) |

## Track-Level Assessment Against the Graded Report Requirements

Requirement.txt grades: (1) how AI tools were asked to find the algorithm, (2) algorithm description, (3) how AI implements the algorithm, (4) experiment settings and results, (5) lessons learnt, (6) source-code webpage link.

- Requirement 2 (algorithm description) favors StarNet-S2 (1 equation) over MobileNetV4 (UIB/NAS), RepViT (re-parameterization), EfficientAD (three cooperating subnetworks), Dinomaly (frozen ViT + decoder), and ShiftwiseConv (shift accumulation).
- Requirement 3 (AI implementation) favors timm-native classification models: a documented `create_model(..., pretrained=True)` route exists for StarNet-S2, MobileNetV4-Conv-S, and RepViT. The anomaly and restoration routes require third-party repositories (EfficientAD unofficial, Dinomaly, PLKSR on BasicSR) with untested local compatibility.
- Requirement 4 (experiment settings and results) is most tractable for StarNet-S2 and MobileNetV4-Conv-S; EfficientAD-S is attractive (fast per-category training, strong AUROC) but carries the unverified auxiliary-image dependency and the informal implementation provenance; PLKSR's paper protocol cannot be reproduced; Dinomaly's ViT-S evidence is incomplete.
- Requirement 6 (source-code link) is cleanest for the classification route with a small, self-contained training script plus a public repository.

## Final Selection Recommendation (for supervisor approval)

1. **Primary recommendation — unchanged: StarNet-S2 (classification track).** It now wins on even wider margins after this wave: it is the only candidate combining verified author-trained timm weights, timm-native loading, the lowest explainability cost, and no dataset-side dependencies beyond a still-undecided small classification dataset.
2. **Conditional runner-up: EfficientAD-S (anomaly track).** If the supervisor prefers an anomaly-detection application story (MVTec AD industrial inspection), EfficientAD-S is the strongest alternative: 1.6M params, ~98.8% image AUROC, ~20-minute per-category training on a workstation GPU. Two gates must clear first: (a) verify the auxiliary pretraining-image subset is laptop-sized; (b) accept an unofficial (community, Apache-2.0) implementation. Both gates are verifiable before Stage 02 design.
3. **Fallback within classification: MobileNetV4-Conv-Small.** Nearly identical feasibility to StarNet-S2; kept as the pilot-failure fallback, with the paper-vs-timm-weights accuracy split to be stated in the report.
4. **Not recommended under the deadline:** RepViT (fine but higher explainability cost and a param discrepancy to document), ShiftwiseConv (custom CUDA + Python 3.8 + 31M), Dinomaly ViT-S (incomplete ViT-S evidence, 24 GB reference setup), PLKSR (no params reported, 450k-iteration protocol, Y-channel convention, BasicSR dependency).

## UNSUPPORTED Register (this wave)

- MobileNetV4: exact ECVA proceedings PDF path; fine-tuning VRAM at 224px batch 16-32; timm-weights top-1.
- RepViT: root cause of the 5.1M vs 5.5M discrepancy.
- EfficientAD: whether 1.6M/2.7M covers the full pipeline; auxiliary-image subset/count/download size; teacher checkpoint file sizes; MVTec archive byte size.
- Dinomaly: DINOv2-with-registers weight size; ViT-Small checkpoint existence; ViT-S MVTec AUROC; requirements.txt contents; resolution of the paper-10k vs README-20k iteration discrepancy.
- PLKSR: DIV2K zip sizes; Drive-folder variant/scale inventory; IEEE Access 2026 publication month; SPAN/ESPAN headline numbers (remain withdrawn).

## Merged Source List (for APA 7 preparation)

Tier 1 = peer-reviewed/official/primary; Tier 2 = credible organizational or author-code sources; Tier 3 = supplementary.

1. Qin, D., Leichner, C., Delakis, M., Fornoni, M., Luo, S., Yang, F., Wang, W., Banbury, C., Ye, C., Akin, B., Aggarwal, V., Zhu, T., Moro, D., & Howard, A. — MobileNetV4: Universal Models for the Mobile Ecosystem (arXiv HTML) — https://arxiv.org/html/2404.10518 (PDF: https://arxiv.org/pdf/2404.10518) — accessed 2026-09-18 — Tier 1 — DOI: 10.48550/arXiv.2404.10518
2. Wightman, R. — timm model card mobilenetv4_conv_small.e2400_r224_in1k — https://huggingface.co/timm/mobilenetv4_conv_small.e2400_r224_in1k — accessed 2026-09-18 — Tier 1
3. timm — MobileNetV4 pretrained-weights collection — https://huggingface.co/collections/timm/mobilenetv4-pretrained-weights — accessed 2026-09-18 — Tier 1
4. ECVA — ECCV 2024 Virtual, Oral 482: MobileNetV4 — https://eccv.ecva.net/virtual/2024/oral/482 — accessed 2026-09-18 — Tier 1
5. Wang, A., Chen, H., Lin, Z., Han, J., & Ding, G. — RepViT: Revisiting Mobile CNN From ViT Perspective, CVPR 2024, pp. 15909-15920 — https://openaccess.thecvf.com/content/CVPR2024/html/Wang_RepViT_Revisiting_Mobile_CNN_From_ViT_Perspective_CVPR_2024_paper.html (PDF: https://openaccess.thecvf.com/content/CVPR2024/papers/Wang_RepViT_Revisiting_Mobile_CNN_From_ViT_Perspective_CVPR_2024_paper.pdf) — accessed 2026-09-18 — Tier 1
6. Wang, A., Chen, H., Lin, Z., Han, J., & Ding, G. — RepViT (arXiv HTML v8, Table 1) — https://arxiv.org/html/2307.09283v8 (PDF: https://arxiv.org/pdf/2307.09283) — accessed 2026-09-18 — Tier 1 — DOI: 10.48550/arXiv.2307.09283
7. THU-MIG — RepViT official code repository — https://github.com/THU-MIG/RepViT — accessed 2026-09-18 — Tier 1
8. timm — model card repvit_m0_9.dist_450e_in1k — https://huggingface.co/timm/repvit_m0_9.dist_450e_in1k — accessed 2026-09-18 — Tier 1
9. Roboflow — How to use MobileNetV4 for Classification (2024-07-22) — https://blog.roboflow.com/how-to-use-mobilenetv4-for-classification/ — accessed 2026-09-18 — Tier 2
10. Batzner, K., Heckler, L., & König, R. — EfficientAD (arXiv HTML v3) — https://arxiv.org/html/2303.14535v3 (PDF: https://arxiv.org/pdf/2303.14535) — accessed 2026-09-18 — Tier 1 — DOI: 10.48550/arXiv.2303.14535
11. Batzner, K., Heckler, L., & König, R. — EfficientAD, WACV 2024 proceedings PDF — https://openaccess.thecvf.com/content/WACV2024/papers/Batzner_EfficientAD_Accurate_Visual_Anomaly_Detection_at_Millisecond-Level_Latencies_WACV_2024_paper.pdf — accessed 2026-09-18 — Tier 1
12. nelson1425 — EfficientAD community implementation (Apache-2.0) — https://github.com/nelson1425/EfficientAD — accessed 2026-09-18 — Tier 2
13. Guo, J., Lu, S., Zhang, W., Chen, F., Li, H., & Liao, H. — Dinomaly (arXiv HTML v4) — https://arxiv.org/html/2405.14325v4 (PDF: https://arxiv.org/pdf/2405.14325) — accessed 2026-09-18 — Tier 1 — DOI: 10.48550/arXiv.2405.14325
14. Guo, J., et al. — Dinomaly OpenReview PDF — https://openreview.net/pdf/d89580d0c0039d5f24293f1f29958787d37c112b.pdf — accessed 2026-09-18 — Tier 1
15. guojiajeremy — Dinomaly repository (Apache-2.0) — https://github.com/guojiajeremy/Dinomaly — accessed 2026-09-18 — Tier 2
16. MVTec Software — MVTec AD dataset page (size, license) — https://www.mvtec.com/research-teaching/datasets/mvtec-ad — accessed 2026-09-18 — Tier 1
17. MVTec-hosted EfficientAD PDF mirror — https://www.mvtec.com/fileadmin/Redaktion/mvtec.com/05_research_teaching/Batzner_EfficientAD_Accurate_Visual_Anomaly_Detection_at_Millisecond-Level_Latencies_WACV_2024_paper.pdf — accessed 2026-09-18 — Tier 2
18. Anomalib — EfficientAD reference documentation — https://anomalib.readthedocs.io/en/v1.2.0/markdown/guides/reference/models/image/efficient_ad.html — accessed 2026-09-18 — Tier 2
19. facebookresearch — DINOv2 repository (upstream weights) — https://github.com/facebookresearch/dinov2 — accessed 2026-09-18 — Tier 2
20. Lee, J., Yun, T.-M., & Ro, Y. M. — Partial Large Kernel CNNs for Efficient Super-Resolution (arXiv HTML v1) — https://arxiv.org/html/2404.11848v1 (PDF: https://arxiv.org/pdf/2404.11848v1) — accessed 2026-09-18 — Tier 1 — DOI: 10.48550/arXiv.2404.11848
21. dslisleedh — PLKSR repository (MIT, BasicSR-based) — https://github.com/dslisleedh/PLKSR — accessed 2026-09-18 — Tier 2
22. ETH Zurich Computer Vision Laboratory — DIV2K dataset official page — https://data.vision.ee.ethz.ch/cvl/DIV2K/ — accessed 2026-09-18 — Tier 1
23. University of Seoul — Partial Large Kernel CNNs... (journal record, DOI 10.1109/ACCESS.2026.3686799) — https://pure.uos.ac.kr/en/publications/partial-large-kernel-cnns-for-efficient-super-resolution/ — accessed 2026-09-18 — Tier 2
24. Wang et al. — Expanded SPAN for Efficient Super-Resolution, CVPR 2025 Workshops (NTIRE) — https://openaccess.thecvf.com/content/CVPR2025W/NTIRE/html/Wang_Expanded_SPAN_for_Efficient_Super-Resolution_CVPRW_2025_paper.html (PDF: https://openaccess.thecvf.com/content/CVPR2025W/NTIRE/papers/Wang_Expanded_SPAN_for_Efficient_Super-Resolution_CVPRW_2025_paper.pdf) — accessed 2026-09-18 — Tier 1
25. Ren et al. — The Tenth NTIRE 2025 Efficient Super-Resolution Challenge Report — https://arxiv.org/html/2504.10686v1 — accessed 2026-09-18 — Tier 1
26. Deng et al. — PLKSR-Rep, CVPR 2026 Workshops (NTIRE) — https://openaccess.thecvf.com/content/CVPR2026W/NTIRE/html/Deng_PLKSR-Rep_A_Compact_Large-Kernel_CNN_for_Mobile_Real-World_Image_Super-Resolution_CVPRW_2026_paper.html — accessed 2026-09-18 — Tier 1

Citation-integrity notes: source 5 governs the RepViT proceedings citation (CVF author list, pp. 15909-15920); source 6 remains the manuscript citation. Source 13/14 are the same paper in different renderings; keep one bibliography entry with the preferred rendering. Source 12 is an unofficial implementation and must never be cited as the authors' code. Source 24 author metadata remains inadequately verified; cite the CVF listing as-is until authors are confirmed. ESPAN/NTIRE/PLKSR-Rep entries (24-26) are context sources, not scored candidates.
