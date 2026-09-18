# Stage 01 — CNN Image Restoration Retrieval Evidence

Date: 2026-09-18

Status: Historical initial retrieval record; later verification is complete in stage_01_verification.md. The exact SPAN/ESPAN parameter, compute, PSNR and protocol assignments below were NOT reliably corroborated and are withdrawn from decision scoring. The proposed configuration explanation is likewise unverified. Preserve them only as evidence of an extraction error, not as final research facts. No architecture or implementation is approved.

## Coverage

The agent reported eight WebSearch and five WebFetch calls. Two PDF extraction failures led to in-memory recovery attempts using existing tools; ESPAN text was recovered, UCAN recovery was blocked. No files were saved and no model/data/code was executed by the agent. GitHub CLI was unavailable, so repository, checkpoint, license and dependency auditing did not occur.

Seven ledger entries were returned, of which NAFNet is an older background locator not accessed in this run. Therefore this is six newly retrieved paper/search-lead records plus one foundation reference, not seven freshly reviewed papers. Discovery-only entries must not be described as full-paper reads.

## Actual queries reported

1. 2025 2024 efficient image super resolution challenge RHA RHA-Net CNN official code
2. 2024 2025 reparameterization large kernel CNN image restoration deblurring denoising official github
3. 2024 2025 compact efficient super resolution SPAN reparameterization PLKSR paper official
4. PLKSR Partial Large Kernel CNNs Efficient Super Resolution CVPR 2024 github parameters
5. "RHA" "super-resolution" 2024 2025 network
6. 2024 2025 "CNN" "restoration" "large kernel" "deblurring"
7. "SPAN" "PLKSR" pretrained license github 2024 2025
8. "NTIRE 2025" "Efficient Super-Resolution" challenge paper RHA

## Screening ledger

| Paper/model | Publication evidence | Architecture/task | Initial decision |
| --- | --- | --- | --- |
| Swift Parameter-free Attention Network for Efficient Super-Resolution / SPAN | 2023 arXiv, revised 2024; 2024 challenge use corroborated in ESPAN; standalone venue unverified | Convolutional reparameterization and activation-derived attention for SR | Conditional lead; exact paper/challenge variant must be distinguished. |
| Partial Large Kernel CNNs for Efficient Super-Resolution / PLKSR | 2024 arXiv; proceedings venue not independently established | Partial-channel large-kernel CNN for SR | Conditional PLKSR-tiny lead; weights, configuration and licensing require checks. |
| Expanded SPAN for Efficient Super-Resolution / ESPAN | CVPR Workshops 2025, not main-conference CVPR | CNN SR with reparameterization and training-time self-distillation | Recent reserve; complex full training and missing verified artifacts weaken deadline suitability. |
| LIR: Efficient Degradation Removal for Lightweight Image Restoration | 2024 arXiv discovery | Restoration; exact operator classification not audited | Hold; insufficient implementation/weight/hardware evidence. |
| UCAN: Unified Convolutional Attention Network for Expansive Receptive Fields in ... | CVPR 2026 proceedings locator; title truncated in retrieved index | Exact restoration operators unverified | Hold; failed text retrieval, no pure-CNN or compactness claim inferred from title. |
| AKNet: an aligned kernel network for image restoration | Springer article indexed 2026-07-23; journal details not inspected | Kernel-based restoration candidate; architecture unverified | Exclude from immediate shortlist because evidence is discovery-only. |
| Simple Baselines for Image Restoration / NAFNet | ECCV 2022 background, not freshly accessed | CNN encoder-decoder denoising/deblurring | Foundation only; not a newly screened recent finalist. |

The RHA/RHA-Net lead did not yield a verified standalone identity or implementation. This is an unresolved search lead, not proof that no such method exists. RFDN (2020) and RLFN (2022) appear as older foundations discussed in ESPAN, not recent contributions.

## SPAN compact challenge configuration

The retrieved SPAN paper describes convolutional reparameterization and attention obtained from activations rather than transformer token attention. The author-linked repository is https://github.com/hongyuanyu/SPAN; its contents, official checkpoints and code/weight licenses were not inspected.

ESPAN Table 3 reports a SPAN challenge comparator with 151K parameters and 9.83G MACs for 256-by-256 low-resolution input and 1024-by-1024 output at 4x SR. The SPAN arXiv extraction, however, reports a 481K-parameter model. These configurations are not interchangeable. A compact challenge row must not be relabeled as the full paper model.

The original training involves large datasets and long schedules, not a demonstrated laptop-scale reproduction. A verified pretrained checkpoint followed by bounded patch-based fine-tuning is the feasible direction to investigate. Actual batch size, input patch size, memory and elapsed time require an approved pilot. Proposed 48–64-pixel LR patches and batch 1–4 are researcher suggestions, not measurements or an approved experiment plan.

Training-branch versus fused/deployment checkpoint compatibility is an important access gate. A deployment model can require a different loading or fine-tuning path from the original multi-branch training network.

## PLKSR-tiny

PLKSR combines partial-channel large kernels, channel mixing and element-wise attention. The paper source supports a CNN interpretation. Its author-linked repository is https://github.com/dslisleedh/PLKSR, but code, weights and both license scopes remain unverified.

The retrieved paper identifies BasicSR, PyTorch 2.1.0 and CUDA 12.1. Compatibility with the local Python 3.12 / PyTorch 2.7.1 / CUDA 12.8 build was not tested. No mandatory custom CUDA operator was established from the paper, but this is not evidence that the repository has no such requirement.

A reliable parameter/MAC tuple with unambiguous input resolution was not recovered. Publication latency/memory numbers were also withheld because input-versus-output resolution was unclear. These gaps should be resolved before quantitative ranking. The paper describes DIV2K/DF2K synthetic SR and Y-channel PSNR/SSIM evaluation with scale-dependent border removal.

The tiny variant is plausibly useful for small-patch fine-tuning, but large-kernel workspace and execution time may differ materially from another model with a similar parameter count. This has not been measured locally.

## ESPAN

The CVPR Workshops 2025 paper describes a SPAN-derived network with 32-channel configurations, a 9-by-9 input convolution, general reparameterization, self-distillation and progressive removal of extra layers. Table 3 reports 192K parameters and 12.56G MACs for 256-by-256 LR to 1024-by-1024 HR at 4x.

The full training recipe uses 85,791 images from DIV2K plus LSDIR, repeated 500K-iteration stages, 2x-to-4x transfer, teacher/student learning and progressive pruning, with HR crops increasing from 256 to 512. Recreating this process is outside the available assignment budget. No author implementation or released checkpoint was established in the inspected material. A compact deployed model does not make its training method an inexpensive reproduction.

## Comparable publication measurements recovered

All following values come from ESPAN Table 3, under that paper's 4x, 256-by-256 LR compute setting and RGB DIV2K validation evaluation. They are publication results, not local experiments.

| Configuration | Parameters | MACs | PSNR | SSIM |
| --- | --- | --- | --- | --- |
| SPAN challenge comparator | 151K | 9.83G | 28.87 | 0.8143 |
| ESPAN | 192K | 12.56G | 28.89 | 0.8159 |

The reported 0.02 dB improvement is small relative to access and implementation uncertainties. The MAC count rises by approximately 28%. This comparison is not an independent replication of either model. ESPAN Table 5 uses a FLOPs label where Table 3 uses MACs; preserve each table's terminology rather than silently treating both quantities as identical. The memory column also warns against assuming that small parameter counts guarantee low activation/workspace costs.

Do not compare RGB measurements directly with PLKSR's Y-channel results, and do not treat A100, V100 or RTX 4090 timings as RTX 4060 Laptop measurements.

## Evaluation hazards and approval-gated possibilities

A possible later project would focus on one synthetic 4x bicubic SR task and compare bicubic interpolation, untouched pretrained inference and modest fine-tuning. This is a direction for supervisor consideration, not an approved design.

Verify the exact author configuration, checkpoint provenance/size, code and weight terms, and training-versus-deploy representation first. Inspect the smallest necessary framework path before approving dependency installation. A CUDA-enabled PyTorch wheel does not itself establish an available native extension build toolchain.

Separate internal validation from fitting using the training images; do not use benchmark test images to tune or choose checkpoints. The official LR release or exactly matched degradation matters because generic PIL/OpenCV bicubic need not reproduce a paper's preprocessing. State scale, mod-crop, border shave, Y/RGB conversion, clipping/rounding, SSIM implementation and per-image aggregation. If tiled inference is needed, validate overlap/border behavior against untiled output on small inputs.

Visualizations can use matched LR/bicubic/model/ground-truth crops and shared-scale absolute-error maps, including failures on edges, text and repeated textures. PSNR/SSIM are fidelity metrics, not guarantees of perceptual realism. An LPIPS evaluator would introduce separately approved model weights.

Archive sizes were not verified. The agent suggested an 8–12 GiB total planning allowance and a capped 4–12-hour fine-tuning budget, but these are unverified estimates and must not be treated as observed resource requirements. Full LSDIR/DF2K downloads are not authorized.

## Sources

All access dates: 2026-09-18. Tier 1 denotes primary-source provenance, not automatic peer review. F = extracted paper text; S = search/index only; B = background locator not accessed.

- C01. SPAN authors (metadata not fully extracted). (2023/2024). Swift parameter-free attention network for efficient super-resolution. https://arxiv.org/abs/2311.12770 — Tier 1; F with extraction limitations.
- C02. SPAN author repository. (n.d.). https://github.com/hongyuanyu/SPAN — Tier 1; S, contents not audited.
- C03. Lee, D., Yun, S., & Ro, Y. (2024, April 18). Partial large kernel CNNs for efficient super-resolution. https://arxiv.org/html/2404.11848v1 — Tier 1; F.
- C04. PLKSR author repository. (n.d.). https://github.com/dslisleedh/PLKSR — Tier 1; S, contents not audited.
- C05. Wang, Q., Wang, Y., An, H., Liu, Y., Zhang, L., & Zhao, S. (2025). Expanded SPAN for efficient super-resolution. CVPR Workshops. https://openaccess.thecvf.com/content/CVPR2025W/NTIRE/html/Wang_Expanded_SPAN_for_Efficient_Super-Resolution_CVPRW_2025_paper.html — Tier 1; F, technical text and Tables 1–8. PDF: https://openaccess.thecvf.com/content/CVPR2025W/NTIRE/papers/Wang_Expanded_SPAN_for_Efficient_Super-Resolution_CVPRW_2025_paper.pdf
- C06. Authors not extracted. (2024). LIR: Efficient degradation removal for lightweight image restoration. https://arxiv.org/html/2402.01368v1 — Tier 1; S.
- C07. Tan et al. (2026). UCAN: Unified convolutional attention network for expansive receptive fields in ... [Title incomplete in retrieved index]. https://openaccess.thecvf.com/content/CVPR2026/papers/Tan_UCAN_Unified_Convolutional_Attention_Network_for_Expansive_Receptive_Fields_in_CVPR_2026_paper.pdf — Tier 1; S, full text unavailable.
- C08. Authors not extracted. (2026). AKNet: an aligned kernel network for image restoration. https://link.springer.com/article/10.1007/s00371-026-04662-0 — Tier 1; S.
- C09. Chen, L., et al. (2022). Simple baselines for image restoration. ECCV background locator. https://arxiv.org/abs/2204.04676 — Tier 1; B, not accessed in this retrieval.

These are working source records, not a final APA 7 bibliography. Incomplete author/title/venue metadata must be resolved for references actually used in the final assessed report.
