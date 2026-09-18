# Stage 01 — Autoencoder and Visual Anomaly Detection Retrieval Evidence

Date: 2026-09-18

Status: Historical initial retrieval record; completed verification is in stage_01_verification.md and the final cross-track recommendation is in DEEP_RESEARCH_MODEL_SELECTION.md. In particular, exact EfficientAD system size/artifacts and an explicit teacher-freezing statement were not independently recovered. This record is not an approved design or measured local experiment.

## Coverage and limitations

Eight WebSearch and five WebFetch calls were reported, with additional read-only in-memory primary-page retrieval after extraction failures. One guessed arXiv address led to an unrelated paper, was discarded, and was corrected; no claim relies on the unrelated result. This was a retrieval mistake, not evidence for a candidate. Future source access should begin from verified search/proceedings URLs.

GitHub CLI was unavailable, and repositories were not inspected through another route. No implementation, installation, file edits, dataset/model downloads or publication occurred. Seven distinct recent papers/search leads were returned; no older foundations were included in this track's count.

## Actual queries reported

1. EfficientAD WACV 2024 RealNet CVPR 2024 Dinomaly CVPR 2025 anomaly detection autoencoder
2. 2025 2026 reconstruction autoencoder industrial anomaly detection CVPR InvAD MambaAD
3. site.openaccess.thecvf.com Dinomaly RealNet anomaly detection
4. 2026 RcAE Recursive Reconstruction 2025 autoencoder anomaly detection RD-EAGLE MambaAD
5. Dinomaly Less Is More 2025 arxiv autoencoder 768 parameters training 10000
6. MVTec AD VisA dataset size license CC BY NC SA 4.0 2.5GB 2026
7. industrial anomaly detection benchmark leakage test threshold AUROC MVTec AD 2026
8. DiAD MambaAD 2024 anomaly detection autoencoder AAAI ECCV

Query 3 is recorded exactly as reported, including its malformed-looking site prefix; do not rewrite the historical search record as if a different query were used.

## Screening ledger

| ID | Paper | Publication evidence | Architecture and initial decision |
| --- | --- | --- | --- |
| B01 | EfficientAD: Accurate Visual Anomaly Detection at Millisecond-Level Latencies | WACV 2024; preprint 2023 | CNN student/teacher plus trained convolutional feature autoencoder; preferred anomaly-track candidate, with auxiliary-data and artifact gates. |
| B02 | RealNet: A Feature Selection Network with Realistic Synthetic Anomaly for Anomaly Detection | CVPR 2024 | Feature reconstruction/selection plus diffusion-generated anomalies; reserve, full reconstruction architecture and generation costs unverified. |
| B03 | Dinomaly: The Less Is More Philosophy in Multi-Class Unsupervised Anomaly Detection | CVPR 2025; preprint started 2024 | Frozen DINOv2 encoder, trained bottleneck and transformer decoder; conditional deep-autoencoder candidate, explicitly not a CNN. |
| B04 | MambaAD: Exploring State Space Models for Multi-class Unsupervised Anomaly Detection | NeurIPS 2024, not ECCV | Pretrained encoder and state-space reconstruction decoder with convolutions; defer for architecture and custom-kernel uncertainty. |
| B05 | Wave-MambaAD: Wavelet-driven State Space Model for Multi-class Unsupervised Anomaly Detection | ICCV 2025 | Wavelet/state-space feature processing; defer, abstract-level architecture and dependency evidence. |
| B06 | RcAE: Recursive Reconstruction Framework for Unsupervised ... | AAAI 2026 publisher result dated March 14; incomplete metadata | Hold; full title, authors, network, artifacts and compute not recovered. |
| B07 | InvAD: Inversion-based Reconstruction-Free Anomaly Detection with Diffusion Models | CVPR 2026 | DDIM inversion and latent-prior deviation, explicitly reconstruction-free; exclude from autoencoder shortlist. |

## EfficientAD-S

The paper describes a small patch-description teacher CNN distilled from ImageNet-pretrained WideResNet-101 features. During anomaly training, the teacher is frozen while the student and convolutional autoencoder are trained. The autoencoder compresses the full image through a 64-dimensional bottleneck and reconstructs teacher features rather than RGB pixels. Its global branch is complementary to local student-teacher discrepancies.

Reported losses combine hard-mined student-teacher squared error using quantile 0.999, an ImageNet-image penalty to discourage generalization outside normal data, autoencoder-to-teacher reconstruction, and a second student output matching the autoencoder. Normalized local and global discrepancy maps are averaged. The resulting method is not simply nearest-neighbor scoring over fixed features. The teacher alone has only four convolutional layers; assignment fit should emphasize the trained deep autoencoder/system rather than invent a new deep classification backbone.

The retrieved operating point is 256-by-256 inputs and 70,000 anomaly-training iterations. The paper reports EfficientAD-S at 2.2 ms and 614 images/s and M at 4.5 ms and 269 images/s on an RTX A6000. These are author inference measurements, not laptop training predictions. The reported S-model MVTec AD image AUROC is 98.8% in the paper's multi-run evaluation. Exact complete-system parameter/compute counts in Appendix E were not recovered; teacher-only counts must not be substituted.

A distilled teacher checkpoint can avoid teacher pretraining but does not automatically remove the separate ImageNet-image regularization requirement. A small auxiliary dataset, omission of the penalty or shorter training would be an adaptation and must be disclosed. The author checkpoint route and code/weight terms were not verified in this retrieval. Described standard convolutions/interpolation suggest fewer platform hazards than custom state-space kernels, but local compatibility remains untested.

## Dinomaly-Small

Dinomaly is a feature-reconstruction autoencoder with a frozen DINOv2 encoder, noisy MLP bottleneck, and an eight-layer transformer decoder. The default encoder is DINOv2-with-registers ViT-Base/14. Training uses bottleneck dropout (default 0.2), linear attention, grouped reconstruction constraints and a global-cosine reconstruction objective with hard-mining/gradient suppression.

This is not a CNN, and DINOv2 initialization is foundation-model pretraining rather than a downloaded fully trained industrial anomaly detector. The encoder remains frozen while reconstruction modules learn normal target data. Whether this is the preferred interpretation of the assignment's deep-autoencoder option should be explained to the supervisor, not silently collapsed into a CNN claim.

| Variant | Reported parameters | MACs | Author RTX 3090 throughput, batch 16 |
| --- | --- | --- | --- |
| ViT-Small | 37.4M | 26.3G | 153.6 images/s |
| ViT-Base | 148.0M | 104.7G | 58.1 images/s |
| ViT-Large | 275.3M | 413.5G | 24.2 images/s |

Table 4 values are publication measurements and require verification of resolution and parameter accounting. They are MACs, not interchangeable GFLOPs. Default preprocessing resizes to 448 squared and center-crops to 392 squared; MVTec AD and VisA training uses 10,000 steps. The paper's Base model reports 99.60% image AUROC, 98.35% pixel AUROC and 69.29% pixel AP on MVTec AD, illustrating why high pixel AUROC alone is not sufficient.

Small is the plausible local candidate, not an assurance that the published batch-16 operating point fits training in 8 GiB. Reduced batch/resolution or single-category training must be reported as departures from a headline multi-class experiment when applicable. The author repository https://github.com/guojiajeremy/Dinomaly was identified, but contents, model artifacts, dependency versions and code/weight terms remain uninspected. A paper webpage's CC BY 4.0 license is not a code or checkpoint license.

## RealNet and other reserves

The accepted RealNet abstract supports SDAS diffusion-based realistic anomaly synthesis, AFS pretrained-feature selection and RRS reconstruction-residual selection. It states that code/data/models are available through https://github.com/cnulab/RealNet. This establishes a substantive trained reconstruction direction, not a tested 8-GiB recipe. Diffusion generation costs, generated-data storage, exact reconstruction layers, losses, parameter counts and licenses remain unresolved. Pre-generated data could help only if access and permitted use are verified.

MambaAD is NeurIPS 2024, correcting an uncertain ECCV lead. Hybrid state-space methods and their selective-scan implementations carry extra compatibility questions. Wave-MambaAD and RcAE are interesting recent leads but lack enough implementation evidence to outrank mature alternatives under the deadline. InvAD's explicitly reconstruction-free mechanism is not evidence for a deep autoencoder selection.

## Dataset evidence

| Dataset | Inspected facts | License and caveat |
| --- | --- | --- |
| MVTec AD | Official page describes over 5,000 images, 15 object/texture categories, normal-only training and mixed normal/anomalous testing with pixel masks. Dinomaly lists 3,629 training-normal images. | CC BY-NC-SA 4.0; noncommercial restriction and share-alike conditions. Official evaluation scripts are offered. |
| VisA | AWS registry reports 10,821 images: 9,621 normal and 1,200 anomalous, 12 classes, image/pixel annotations and public S3 resources. Dinomaly uses 8,659 training-normal images. | CC BY 4.0. Total normal-image count is not the count in a particular training split. |

Archive byte sizes and extracted footprints were not verified. Do not promise that all datasets, ImageNet auxiliary images, synthetic anomalies and caches fit available disk. Dataset downloads remain unapproved.

## Evaluation safeguards

No test-based checkpoint selection is allowed in the proposed assignment. EfficientAD's paper reports a concern about a SimpleNet implementation selecting on repeated test evaluation and describes disabling that behavior; this is an author critique, not an independently performed audit.

Fit normalization and operational thresholds using held-out normal training data, not test masks. EfficientAD's quantile map normalization is not a universal fixed classification threshold. Evaluate both image and pixel behavior: image AUROC, pixel AUROC, pixel AP and, where appropriate, AUPRO with its false-positive-rate integration range stated. EfficientAD uses AUPRO up to FPR 0.30. A test-set best F1 value is an oracle diagnostic rather than a deployable threshold chosen without labels.

Cropping needs explicit treatment: EfficientAD criticizes benchmark-specific center cropping, whereas Dinomaly uses it in the reported preprocessing. Faithful benchmark reproduction and full-image defect coverage are different questions. Related objects in pretraining do not themselves prove duplicate-image leakage; provenance and overlap must be assessed carefully.

## Possible supervised scope

The agent's preferred anomaly-track direction is EfficientAD-S on one MVTec category, perhaps followed by one texture category if approved. Train the student/autoencoder rather than merely run a downloaded category-trained detector. A with/without global-autoencoder ablation is a meaningful option only if split, training budget and evaluation protocol are matched.

Preserve architecture and original settings for a category-scoped reproduction; label changed losses, auxiliary data, steps or architecture as adaptation. Neither justifies claiming reproduction of the paper-wide average. Record real GPU memory, training time and synchronized inference latency after implementation approval. No numeric local runtime promise is supported yet.

## Sources

All accessed 2026-09-18. Tier 1 denotes authoritative publisher/author/dataset evidence, not independent replication. Working author abbreviations require completion for a final APA 7 bibliography.

- B01. Batzner, K., Heckler, L., & Konig, R. (2024). EfficientAD: Accurate visual anomaly detection at millisecond-level latencies. WACV. https://openaccess.thecvf.com/content/WACV2024/papers/Batzner_EfficientAD_Accurate_Visual_Anomaly_Detection_at_Millisecond-Level_Latencies_WACV_2024_paper.pdf ; alternate full-text rendering https://ar5iv.labs.arxiv.org/html/2303.14535 — Tier 1; methods/evaluation sections and tables, incomplete appendix extraction. Author diacritic to verify.
- B02. Zhang, Xu, & Zhou. (2024). RealNet: A feature selection network with realistic synthetic anomaly for anomaly detection. CVPR. https://openaccess.thecvf.com/content/CVPR2024/html/Zhang_RealNet_A_Feature_Selection_Network_with_Realistic_Synthetic_Anomaly_for_CVPR_2024_paper.html — Tier 1; accepted abstract/metadata, not full methods.
- B03. Guo, Lu, Zhang, Chen, Li, & Liao. (2025). Dinomaly: The less is more philosophy in multi-class unsupervised anomaly detection. CVPR. https://arxiv.org/html/2405.14325v5 ; venue https://cvpr.thecvf.com/virtual/2025/poster/34672 — Tier 1; methods, Tables 4–5 and Appendix B inspected.
- B04. He et al. (2024). MambaAD: Exploring state space models for multi-class unsupervised anomaly detection. NeurIPS. https://arxiv.org/html/2404.06564v1 ; proceedings https://proceedings.neurips.cc/paper_files/paper/2024/file/833b21da1956c6b92f6df253bf655cf5-Paper-Conference.pdf — Tier 1; abstract/introduction inspected, publisher search for venue.
- B05. Zhang, Shao, Chen, Lv, & Xu. (2025). Wave-MambaAD: Wavelet-driven state space model for multi-class unsupervised anomaly detection. ICCV. https://openaccess.thecvf.com/content/ICCV2025/html/Zhang_Wave-MambaAD_Wavelet-driven_State_Space_Model_for_Multi-class_Unsupervised_Anomaly_Detection_ICCV_2025_paper.html — Tier 1; accepted abstract/metadata.
- B06. RcAE authors not recovered. (2026). Recursive reconstruction framework for unsupervised ... [Incomplete title]. https://ojs.aaai.org/index.php/AAAI/article/view/38048 — Tier 1 publisher; metadata only, retrieval failed.
- B07. Sakai, He, Gu, Sigal, & Hasegawa. (2026). InvAD: Inversion-based reconstruction-free anomaly detection with diffusion models. CVPR. https://openaccess.thecvf.com/content/CVPR2026/html/Sakai_InvAD_Inversion-based_Reconstruction-Free_Anomaly_Detection_with_Diffusion_Models_CVPR_2026_paper.html — Tier 1; accepted abstract/metadata.
- B08. MVTec Software. (n.d.). MVTec AD dataset. https://www.mvtec.com/research-teaching/datasets/mvtec-ad — Tier 1; dataset, license and evaluation sections.
- B09. AWS / VisA dataset authors. (n.d.). Visual Anomaly dataset. https://registry.opendata.aws/visa/ — Tier 1; description, license and resource metadata.
