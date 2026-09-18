# Stage 01 — Classification CNN Retrieval Evidence

Date: 2026-09-18

Status: Historical initial retrieval record. Later corrections and completed artifact checks are in stage_01_verification.md; the final cross-track recommendation is in DEEP_RESEARCH_MODEL_SELECTION.md. This record preserves what the first retrieval found, including then-unresolved values. Track-specific recommendations below are not the final selection. No model is approved.

## Coverage and limitations

The agent reported eight WebSearch calls and five WebFetch calls. Full-text extraction targeted MobileNetV4, RepViT, StarNet and RepNeXt; another fetch inspected a timm model card. Numerical extraction from some PDF tables was unreliable, so unsupported exact numbers were withheld. GitHub CLI was unavailable; repository links were identified, but no repository code, dependency files, licenses or checkpoint files were read.

Nine distinct paper/search-lead records were returned. MogaNet and EfficientViT were not sufficiently verified to count as screened. The ledger includes two older baseline papers and an out-of-domain audio paper; these must not inflate a claim about recent eligible vision papers.

## Actual queries reported

1. MobileNetV4 ECCV 2024 paper official models parameters MAdds
2. RepViT Revisiting Mobile CNN From ViT Perspective CVPR 2024 Rewrite the Stars StarNet
3. MobileNetV5 2026 paper publication
4. RepNeXt RepCNN efficient CNN 2025 2026 paper
5. "Rewrite the Stars" "MogaNet" CVPR 2024
6. "RepCNN" paper 2025 2026
7. "FasterNet" "ConvNeXt V2" "EfficientViT" CVPR 2023
8. site:openaccess.thecvf.com ("Rewrite the Stars" OR "MogaNet" OR "FasterNet" OR "ConvNeXt V2")

## Screening ledger

| Model/paper | Publication evidence | Architecture and application | Initial decision |
| --- | --- | --- | --- |
| MobileNetV4: Universal Models for the Mobile Ecosystem | ECCV 2024; paper and venue evidence A01–A03 | Convolutional and hybrid families; classification | Retain Conv-Small; choose Conv explicitly, not Hybrid. |
| RepViT: Revisiting Mobile CNN From ViT Perspective | 2023 preprint; CVPR 2024, A04–A05 | CNN classification and dense prediction | Retain M0.9; the model name does not make it transformer-only. |
| Rewrite the Stars / StarNet | CVPR 2024, A06 | Compact CNN classification with element-wise products | Conditional candidate; checkpoint/license/numerical verification incomplete. |
| RepNeXt: A Fast Multi-Scale CNN using Structural Reparameterization | Inspected 2024 arXiv v2, A07 | Multiscale CNN for classification/dense prediction | Reserve; venue beyond preprint and usable artifacts not verified. |
| UniConvNet: Expanding Effective Receptive Field while Maintaining Asymptotically Gaussian Distribution | ICCV 2025 search-level proceedings result, A08 | ConvNet | Defer; compact variant and artifacts unverified. |
| Co-Designing Vision-Language Models for NPU Inference / MobileNetV5 lead | 2025-12-02 arXiv result, A09 | Vision-language/NPU focus; exact backbone eligibility unresolved | Defer pending identity/architecture verification; do not claim MobileNetV5 does not exist. |
| ConvNeXt V2: Co-Designing and Scaling ConvNets With Masked Autoencoders | CVPR 2023, A10 | CNN with masked-autoencoder pretraining | Older baseline only, outside main search window. |
| Run, Don't Walk: Chasing Higher FLOPS for Faster Neural Networks / FasterNet | CVPR 2023, A11 | Efficient CNN | Older baseline only. |
| RepCNN: Micro-sized, Mighty Models for Wakeword Detection | Secondary 2024 bibliographic lead; venue unverified, A12 | Audio/wakeword CNN | Exclude from CV scope; weak evidence used only for exclusion. |

## MobileNetV4-Conv-Small

The strongest evidence for immediate practical consideration is the documented timm model `mobilenetv4_conv_small.e2400_r224_in1k`. Its card reports 3.8 million parameters and 0.2 GMACs, with 224-pixel training and 256-pixel test images. The exact input resolution attached to the rounded compute number was not established by the first retrieval and must not be inferred silently.

The convolutional family uses Universal Inverted Bottleneck building blocks; Mobile MQA belongs to a separate hybrid family. The model card identifies Ross Wightman's timm training as the PyTorch weight provenance. These are not established as Google's original checkpoints. The pretrained-loading interface and card metadata were inspected; checkpoint bytes and implementation code were not.

The card declares Apache-2.0. This is evidence of the card's license declaration, not a completed audit of all upstream code and weight licenses. Native usage documents PyTorch, timm, and Pillow; Transformers is an optional alternate loading route. Minimum version compatibility was not verified. A small model at approximately 224-pixel inputs is plausibly feasible on the available laptop, but no local training time, peak memory, or downstream accuracy has been measured.

## RepViT-M0.9

The paper extraction reports M0.9 at 5.1 million parameters, 0.8 GMACs and 78.7% ImageNet top-1; M1.0 at 6.8 million, 1.1 GMACs and 80.0%. These tuples and their image resolution require independent checking against the original table before becoming conclusion-driving numbers.

RepViT is a CNN using structural reparameterization and design changes inspired by ViTs. The retrieved recipe includes RegNetY-16GF distillation. Paper ImageNet accuracy must not be interpreted as an expected result of brief small-dataset fine-tuning. The author repository is https://github.com/THU-MIG/RepViT, identified through paper links but not read. Exact weights, license text, dependency pins, fused/training block compatibility and state-dictionary portability remain unresolved.

## StarNet and RepNeXt

StarNet's paper describes element-wise multiplication as a way to create richer nonlinear interactions in a compact CNN; this is not self-attention. StarNet-S1 or S2 could be interesting exact variants, but initial table extraction was not reliable enough to publish a parameter/compute tuple. The paper-linked https://github.com/ma-xu/Rewrite-the-Stars repository was not read. Weight, license and dependency status remain unknown.

RepNeXt's inspected preprint describes a multiscale reparameterized CNN evaluated on ImageNet, COCO and ADE20K. It reports RepNeXt-M1 with 4.8 million parameters, but the complete compute/resolution tuple was not established. The paper-linked https://github.com/suous/RepNeXt repository was not read, and a peer-reviewed venue was not established by this retrieval.

## Candidate datasets and critical limitations

Oxford Flowers102, Oxford-IIIT Pets and DTD were suggested as possible small classification datasets. They were not researched within this agent's budget: exact sizes, official splits, licensing, provenance and potential pretrained-data overlap remain unverified. These suggestions are not an experimental plan.

The main hazards are confusing timm-trained versus original author checkpoints, claiming paper-scale reproduction after transfer learning, tuning on test data, ignoring duplicate images or pretrained overlap, using incompatible reparameterized blocks/checkpoint heads, comparing MACs with FLOPs, and extrapolating phone inference latency to laptop training time. Parameter count does not include all activation/gradient/optimizer memory. Python 3.12 compatibility also remains untested for older research repositories.

Track-specific initial recommendation: MobileNetV4-Conv-Small first, RepViT-M0.9 as an alternative, StarNet as a conditional novelty-oriented option. This is a requirement-coverage judgment, not a score guarantee or a measured feasibility result.

## Sources

All sources accessed 2026-09-18. Tier 1 denotes primary source status, not automatically peer review. Same-author papers and code are not independent replication.

- A01. Qin, D., et al. (2024). MobileNetV4: Universal models for the mobile ecosystem. arXiv v1, 2024-04-16. https://arxiv.org/html/2404.10518v1 — Tier 1; full-paper extraction.
- A02. ECCV. (2024). MobileNetV4 venue listing. https://eccv.ecva.net/virtual/2024/oral/482 — Tier 1; search-level venue evidence.
- A03. Wightman, R., / timm. (n.d.). mobilenetv4_conv_small.e2400_r224_in1k model card. https://huggingface.co/timm/mobilenetv4_conv_small.e2400_r224_in1k — Tier 1; card and examples inspected, implementation not read.
- A04. Wang, A., et al. (2023/2024). RepViT: Revisiting mobile CNN from ViT perspective. Retrieved arXiv version dated 2024-03-14. https://arxiv.org/html/2307.09283 — Tier 1; full-paper extraction.
- A05. CVPR. (2024). RepViT venue listing. https://cvpr.thecvf.com/virtual/2024/poster/29201 — Tier 1; search-level venue evidence.
- A06. Ma, X., Dai, X., Bai, Y., Wang, Y., & Fu, Y. (2024). Rewrite the stars. CVPR. https://openaccess.thecvf.com/content/CVPR2024/papers/Ma_Rewrite_the_Stars_CVPR_2024_paper.pdf — Tier 1; full-paper extraction, numerical tables not yet trusted.
- A07. Zhao, Luo, & Ouyang. (2024). RepNeXt. arXiv v2, 2024-07-20. https://arxiv.org/html/2406.16004v2 — Tier 1; preprint/full-paper extraction; author initials not yet verified.
- A08. Wang et al. (2025). UniConvNet: Expanding effective receptive field while maintaining asymptotically Gaussian distribution. ICCV. https://openaccess.thecvf.com/content/ICCV2025/papers/Wang_UniConvNet_Expanding_Effective_Receptive_Field_while_Maintaining_Asymptotically_Gaussian_Distribution_ICCV_2025_paper.pdf — Tier 1; search-level proceedings discovery.
- A09. Authors not extracted. (2025). Co-designing vision-language models for NPU inference. 2025-12-02 preprint. https://arxiv.org/abs/2512.02924 — Tier 1; search-level abstract discovery.
- A10. Woo, S., et al. (2023). ConvNeXt V2: Co-designing and scaling ConvNets with masked autoencoders. CVPR. https://openaccess.thecvf.com/content/CVPR2023/html/Woo_ConvNeXt_V2_Co-Designing_and_Scaling_ConvNets_With_Masked_Autoencoders_CVPR_2023_paper.html — Tier 1; search-level older baseline.
- A11. Chen, J., et al. (2023). Run, don't walk: Chasing higher FLOPS for faster neural networks. CVPR. https://openaccess.thecvf.com/content/CVPR2023/html/Chen_Run_Dont_Walk_Chasing_Higher_FLOPS_for_Faster_Neural_Networks_CVPR_2023_paper.html — Tier 1; search-level older baseline.
- A12. Authors not fully verified. (2024 lead). RepCNN: Micro-sized, mighty models for wakeword detection. https://www.researchgate.net/publication/383654040_RepCNN_Micro-sized_Mighty_Models_for_Wakeword_Detection — Tier 3; secondary discovery used only for scope exclusion.

Bibliographic entries are working source records, not the final APA 7 reference list. Missing author details must be resolved before final report submission.
