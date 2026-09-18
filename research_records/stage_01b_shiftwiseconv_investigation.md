# Stage 01b — ShiftwiseConv (CVPR 2025) Supplementary Investigation

> Generated 2026-09-18 | Four parallel investigation subagents | Triggered by supervisor request to explore 2025-2026 candidates

Status: Investigation complete. **Critical parameter-count discrepancy discovered.** ShiftwiseConv SW-Tiny is reported at 31M parameters in the published paper, not the 5.8M initially reported by retrieval subagents. This materially changes the GPU feasibility assessment. No model has been downloaded, installed, or trained.

## 1. Paper Details and APA 7 Citation

### Full APA 7 Reference

Li, D., Li, L., Chen, Z., & Li, J. (2025). ShiftwiseConv: Small convolutional kernel with large kernel effect. In *Proceedings of the 2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)* (pp. TBD). June 11--15, 2025, Nashville, TN, USA. IEEE.

**Author affiliation:** All four authors are affiliated with Shenzhen University, College of Computer Science and Software Engineering. Lead author Dachong Li (GitHub: lidc54).

**Paper history:** Originally posted on arXiv as v1 (2024-01-23) under the title "Shift-ConvNets: Small Convolutional Kernel with Large Kernel Effects." Renamed and revised as v2 (2025-03-13) to "ShiftwiseConv: Small Convolutional Kernel with Large Kernel Effect" for CVPR 2025.

**DOI:** Not found in any accessible source. IEEE Xplore DOI may not yet be assigned.

### PDF and Source Links

| Resource | URL |
|----------|-----|
| CVF open access (HTML) | https://openaccess.thecvf.com/content/CVPR2025/html/Li_ShiftwiseConv_Small_Convolutional_Kernel_with_Large_Kernel_Effect_CVPR_2025_paper.html |
| CVF open access (PDF) | https://openaccess.thecvf.com/content/CVPR2025/papers/Li_ShiftwiseConv_Small_Convolutional_Kernel_with_Large_Kernel_Effect_CVPR_2025_paper.pdf |
| CVF supplementary | https://openaccess.thecvf.com/content/CVPR2025/supplemental/Li_ShiftwiseConv_Small_Convolutional_CVPR_2025_supplemental.pdf |
| arXiv abstract | https://arxiv.org/abs/2401.12736 |
| arXiv HTML (v2) | https://arxiv.org/html/2401.12736v2 |
| arXiv PDF | https://arxiv.org/pdf/2401.12736 |
| CVPR virtual poster | https://cvpr.thecvf.com/virtual/2025/poster/34598 |
| GitHub (official) | https://github.com/lidc54/shift-wiseConv |

## 2. Architectural Mechanism

### Core Idea: Shift-Wise Sparse Dependency

The paper identifies two factors behind large-kernel effectiveness:
1. Extracting features at a certain granularity (determined by kernel size)
2. Fusing features by multiple pathways (diverse spatial connections)

ShiftwiseConv achieves both using only 3x3 convolutions through the SW (Shift-Wise) operator:

- **Coarse-grained pruning:** A conceptual large kernel is decomposed, then most positions are pruned, leaving only sparse positions occupied by 3x3 convs.
- **Spatial shift offsets:** The remaining sparse 3x3 convs are placed at shifted spatial positions across the feature map. Each path processes a shifted subset of spatial features.
- **Multi-path long-distance sparse dependency:** Multiple shifted paths carry features from distant spatial locations. When fused (via addition or concatenation), the network captures long-range dependencies equivalent to a large dense kernel, but with far fewer parameters.
- **Group convolutions:** Used within SW blocks to further reduce cost while maintaining independent feature paths.
- **Re-parameterization:** Multi-branch structure collapses to a single equivalent convolution at inference time.

### Effective Receptive Field

By stacking shifted sparse 3x3 convolutions across layers, the effective receptive field grows to match that of a large dense kernel (e.g., equivalent to 31x31 or larger), while actual parameter count stays comparable to dense 3x3 convolutions.

## 3. CRITICAL CORRECTION: Parameter Count Discrepancy

### What the retrieval subagents initially reported

The first-wave retrieval subagent reported SW-Tiny at ~5.8M parameters with 83.39% ImageNet top-1.

### What the published paper actually reports

The deep investigation subagent, which fetched the arXiv HTML and CVF paper, found:

| Variant | Params (M) | FLOPs (G) | Top-1 Acc (%) | Stages | Channels |
|---------|-----------|-----------|---------------|--------|----------|
| SW-Tiny | **31** | 5.0 | 83.4 | [3,3,18,3] | [80,160,320,640] |
| SW-Small | **56** | 9.4 | 83.9 | -- | -- |

**The published SW-Tiny has 31M parameters, not 5.8M.** No variant with ~5.8M parameters exists in the published paper or official repository. The initial retrieval subagent's 5.8M figure was an error.

### Impact on decision

This discrepancy materially changes the comparison:
- StarNet-S2: 3.7M params, 74.8% ImageNet
- ShiftwiseConv SW-Tiny: **31M params**, 83.4% ImageNet

ShiftwiseConv is approximately 8.4x larger than StarNet-S2 in parameter count, not 1.6x as initially believed.

## 4. GitHub Repository Verification

### Repository Overview

| Property | Value |
|----------|-------|
| URL | https://github.com/lidc54/shift-wiseConv |
| Stars | 62 |
| Forks | 11 |
| Open issues | 4 |
| LICENSE file | Yes -- MIT License |
| LICENSE holder | **Meta Platforms, Inc.** and affiliates |
| requirements.txt | No (dependencies inline in README) |
| MODEL_ZOO.md | No |

### Pretrained Weights

| Property | Value |
|----------|-------|
| Available variants | **Only SW-Tiny** (SW_v2_unirep_tiny) |
| Hosting | Google Drive |
| Download link | https://drive.google.com/file/d/1U4DOZv5V9_7wJdqdicjp0tCmNIdRNJOc/view |
| Source | Author-trained (implied) |
| Performance | 83.39% top-1 at 224x224, 300 epochs |
| File format/size | Not stated in README |

### License Details

- **Code license:** MIT License
- **Copyright holder:** Meta Platforms, Inc. -- indicates code is derived from or based on Meta/Facebook research code (likely RepLKNet or related large-kernel CNN project)
- **Weight license:** Not explicitly stated separately from code

### Dependencies and Compatibility Concerns

| Dependency | Required | Local version | Compatible? |
|------------|----------|---------------|-------------|
| Python | 3.8 | 3.12.10 | **Untested** |
| PyTorch | >= 1.10.0 | 2.7.1+cu128 | Likely yes |
| CUDA | 11.7 (tested) | 12.8 | **Untested** |
| torchvision | 0.11.0 | 0.22.1+cu128 | **Version mismatch** |
| timm | required | not installed | Needs install |
| Custom CUDA module | `shiftadd/` must be compiled | -- | **Requires compilation** |

**Critical compatibility concerns:**
1. Python 3.8 required vs. local 3.12.10 -- untested
2. Custom CUDA kernel in `shiftadd/` must be compiled via `python setup.py install`
3. torchvision 0.11.0 specified vs. local 0.22.1 -- significant version gap
4. No timm integration -- manual model setup required

## 5. GPU Feasibility Assessment (Corrected)

### If 5.8M params (initially believed, now known incorrect)

Total VRAM at batch 32, 224x224, float32: estimated ~1.5-2 GB out of 8 GB. Comfortable.

### If 31M params (published SW-Tiny, corrected)

| Component | Size |
|-----------|------|
| Model parameters (FP32) | ~124 MB |
| Gradients | ~124 MB |
| Optimizer state (Adam) | ~248 MB |
| PyTorch/CUDA overhead | ~800-1500 MB |
| **Static subtotal** | **~1.3-1.7 GB** |

| Batch Size | Activations (est.) | **Estimated Total** | Headroom in 8 GB |
|------------|-------------------|-------------------|-----------------|
| 8 | ~150 MB | ~1.7-2.0 GB | ~6.0 GB free |
| 16 | ~300 MB | ~1.9-2.2 GB | ~5.8 GB free |
| 32 | ~600 MB | ~2.2-2.8 GB | ~5.2 GB free |
| 64 | ~1.2 GB | ~2.8-4.0 GB | ~4.0 GB free |

**Conclusion:** Even at 31M params, batch 16-32 at 224x224 should fit in 8 GiB with margin. Mixed precision (AMP) would further reduce activation memory by 30-40%. However, the shift operations may require additional memory for shifted feature map copies, which is untested.

### Recommended Safe Settings

- Resolution: 224x224
- Batch size: 16 (with gradient accumulation of 2 for effective batch 32)
- Mixed precision (AMP): enabled
- Optimizer: AdamW with weight decay
- Run a VRAM probe first: single forward+backward pass with `torch.cuda.max_memory_allocated()`

## 6. Report Explainability Comparison: ShiftwiseConv vs. StarNet-S2

### Explainability

| Criterion | StarNet-S2 | ShiftwiseConv |
|-----------|-----------|---------------|
| Explain in 1 paragraph | Easy: y = f(x) ⊙ g(x) | Harder: requires explaining shift accumulation across layers |
| Visual diagram | One block, one symbol (⊙) | Multi-panel, layer-by-layer accumulation |
| Background needed | Basic convolutions, element-wise ops | Receptive fields, shift operations, large-kernel comparison |
| "Aha moment" | "Multiplication instead of addition!" | "Shifts stack up to cover a big area!" -- takes longer |

**Winner: StarNet-S2** -- significantly easier to explain and visualize.

### Report Writing

| Criterion | StarNet-S2 | ShiftwiseConv |
|-----------|-----------|---------------|
| Citations available | Strong: CVPR 2024, timm card, existing research | Moderate: CVPR 2025, less third-party analysis |
| Clear ablation references | Yes: star op vs. add/cat/attention | Likely yes, but unverified |
| Novelty narrative | Sharp: "multiplicative feature interaction" | Sharper recency, but broader narrative |
| Baseline contrast | Crisp: addition vs. multiplication | Valid but requires more explanation |

**Winner: StarNet-S2** -- more verified citation material already gathered, clearer narrative.

### Experiment Design

| Criterion | StarNet-S2 | ShiftwiseConv |
|-----------|-----------|---------------|
| Fine-tuning setup | Easy: timm one-liner | Harder: manual setup from GitHub |
| Hyperparameter guidance | Known (224px, 300 epochs) | Paper-dependent, less accessible |
| 8 GiB GPU fit | Comfortable (3.7M params) | Plausible but less headroom (31M params) |
| Preprocessing | Standard ImageNet pipeline | Paper-specific, may need manual setup |
| Fallback options | Excellent (timm ecosystem) | Poor (standalone setup) |

**Winner: StarNet-S2** -- significantly easier to set up and run.

### Risk Assessment

| Criterion | StarNet-S2 | ShiftwiseConv |
|-----------|-----------|---------------|
| Unknowns | Few, mostly standard steps | Many: custom CUDA module, Python version, dependency versions |
| First-try success | High probability | Moderate-to-low |
| Fallback options | Excellent (timm ecosystem) | Poor (standalone setup) |
| Time risk | Low: setup < 1 hour | High: setup could take hours or fail |

**Winner: StarNet-S2** -- far fewer risks.

## 7. Updated Candidate Comparison

| Dimension | StarNet-S2 (CVPR 2024) | ShiftwiseConv SW-Tiny (CVPR 2025) |
|-----------|------------------------|----------------------------------|
| **Params** | 3.7M | **31M** (corrected from 5.8M) |
| **Compute** | 547M FLOPs | 5.0G FLOPs |
| **ImageNet top-1** | 74.8% | 83.4% |
| **Year** | 2024 | 2025 (newer) |
| **Weight source** | timm, author-trained | Google Drive, author-trained (implied) |
| **License** | Apache-2.0 (card declaration) | MIT (Meta-held) |
| **timm integration** | Yes | No |
| **Custom CUDA** | No | Yes (shiftadd/ must compile) |
| **Python compatibility** | Standard | 3.8 required, local is 3.12 |
| **Explainability** | High (single equation) | Moderate (multi-layer shifts) |
| **Setup risk** | Low | High |
| **Fallback options** | Excellent (timm) | Poor |

## 8. Recommendation After Investigation

**StarNet-S2 remains the recommended choice.**

ShiftwiseConv's advantages -- CVPR 2025 recency and 83.4% ImageNet accuracy -- are outweighed by:

1. **Parameter count is 31M, not 5.8M** -- 8.4x larger than StarNet-S2
2. **Custom CUDA module** must be compiled; compatibility with local CUDA 12.8 is untested
3. **Python 3.8 required** vs. local 3.12.10; untested compatibility
4. **torchvision version mismatch** (0.11.0 vs. 0.22.1)
5. **No timm integration** -- manual setup increases time risk
6. **Only one weight variant** available (SW-Tiny)
7. **MIT license held by Meta** -- derivative code provenance adds uncertainty
8. **Explainability is lower** -- harder to diagram and explain in a short report

The initial 5.8M parameter figure was a retrieval error. The corrected 31M figure places ShiftwiseConv in a different size class entirely, making it less suitable for a 3-day deadline with an 8 GiB GPU.

## 9. Other 2025-2026 Candidates Found

### LSNet (CVPR 2025)
- "See Large, Focus Small" -- LS convolution combining large-receptive-field + small-kernel focus paths
- Code: https://github.com/THU-MIG/lsnet
- Exact params/accuracy not extracted; lightweight variant confirmed
- Tier 1 (CVPR 2025, Tsinghua)
- Status: Insufficient detail for comparison

### RepNeXt-M4 (arXiv 2024, no confirmed venue)
- Multi-scale reparameterization (1x1, 3x3, 5x5, 7x7 branches)
- 13.3M params, 82.3% ImageNet
- Tier 2-3 (arXiv preprint, no peer-reviewed venue confirmed)

### STResNet (arXiv 2026-01)
- CompressNAS decomposition, 0.95M-3.99M params
- 58.8%-71.6% ImageNet (below StarNet-S2)
- Tier 3 (no venue)

### Q-Former Autoencoder (WACV 2026)
- Medical imaging domain, Q-Former bottleneck on frozen foundation features
- No MVTec results; code "will be released upon acceptance"
- Tier 1 (WACV 2026) but domain mismatch

## 10. Bibliography (APA 7)

Li, D., Li, L., Chen, Z., & Li, J. (2025). ShiftwiseConv: Small convolutional kernel with large kernel effect. In *Proceedings of the 2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*. IEEE. https://arxiv.org/abs/2401.12736

Ma, X., Dai, X., Bai, Y., Wang, Y., & Fu, Y. (2024). Rewrite the stars. In *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*. https://arxiv.org/abs/2403.19967

## 11. Files

| File | Path |
|------|------|
| This investigation | `D:\claude\workspace\CISC3024 AI Assignment 1\research_records\stage_01b_shiftwiseconv_investigation.md` |
| Main selection report | `D:\claude\workspace\CISC3024 AI Assignment 1\DEEP_RESEARCH_MODEL_SELECTION.md` |
| Verification record | `D:\claude\workspace\CISC3024 AI Assignment 1\research_records\stage_01_verification.md` |
| Screening ledger | `D:\claude\workspace\CISC3024 AI Assignment 1\research_records\stage_01_screening_ledger.csv` |
| Conversation log | `D:\claude\workspace\CISC3024 AI Assignment 1\research_records\conversation_log.md` |
