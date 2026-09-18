# Stage 01 — Independent Claim Verification and Corrections

Date: 2026-09-18

Status: All three verification tracks returned; final corrections are recorded below. This file overrides unsupported initial retrieval claims where explicitly stated. SUPPORTED means directly supported by an inspected source, not independently reproduced on the local laptop. UNSUPPORTED can mean insufficient evidence rather than a claim proven false.

## Classification verification

The verifier reported five WebSearch calls, including two failures, and eight WebFetch calls, plus direct read-only in-memory inspection to resolve extraction problems. No GitHub access, file writes, checkpoint/data downloads, installation or model execution occurred.

### MobileNetV4-Conv-Small

SUPPORTED: the timm card lists 3.8M parameters, 0.2 GMACs, 224-by-224 training and 256-by-256 testing. PARTIAL: the card does not explicitly tie its rounded GMAC statistic to a profiling resolution; do not infer it from a training/test size.

SUPPORTED: the weights were trained by Ross Wightman using timm with paper-inspired hyperparameters and timm enhancements. They are not established as original Google-trained weights. Card YAML declares Apache-2.0; the inspected Hugging Face manifest contains configuration and weight artifacts but no separate LICENSE file. A declaration is not a complete upstream license audit.

SUPPORTED: the original paper distinguishes Conv UIB architectures from Hybrid models interleaving Mobile MQA attention. UIB uses optional depthwise convolutions around expansion/projection to cover several convolutional block configurations. Local 8-GiB training feasibility remains an inference, not a source measurement.

Sources: https://huggingface.co/timm/mobilenetv4_conv_small.e2400_r224_in1k ; https://huggingface.co/api/models/timm/mobilenetv4_conv_small.e2400_r224_in1k ; https://arxiv.org/html/2404.10518v1

### RepViT

SUPPORTED: original Table 1 distinguishes Params (M), GMACs, Epochs and Top-1 (%). At 224-by-224 training/testing (Section 4.1), M0.9 has 5.1M parameters and 0.8 GMACs; M1.0 has 6.8M and 1.1 GMACs. The respective 78.7% and 80.0% ImageNet results use 300-epoch RegNetY-16GF teacher-distilled training. The 450-epoch distilled values are 79.1% and 80.3%. Table 2 without distillation reports 77.4% and 78.6% at 300 epochs.

Correction: do not attach the 300-epoch accuracy to a 450-epoch checkpoint as a verified artifact measurement.

SUPPORTED: the timm card `repvit_m0_9.dist_450e_in1k` says the weights were trained by the paper authors and lists 224-by-224 usage, 0.8 GMACs and 5.5M parameters. The paper's 5.1M and card's 5.5M are unresolved different-source values; do not silently choose one or invent a distillation-head explanation. The card declares Apache-2.0, the manifest lists `model.safetensors`, `pytorch_model.bin` and `config.json`, and no separate LICENSE file was found. Documented loading does not prove execution compatibility.

Publication metadata: Ao Wang, Hui Chen, Zijia Lin, Jungong Han, Guiguang Ding; CVPR 2024 camera-ready manuscript. Cite paper authors rather than inconsistent model-card author strings.

Sources: https://arxiv.org/html/2307.09283 ; https://arxiv.org/abs/2307.09283 ; https://huggingface.co/timm/repvit_m0_9.dist_450e_in1k ; https://huggingface.co/api/models/timm/repvit_m0_9.dist_450e_in1k

### StarNet

SUPPORTED: accepted CVPR Table 6, printed page 5700, gives StarNet-S1: 2.9M parameters, 425M paper-labelled FLOPs and 73.5% ImageNet top-1; StarNet-S2: 3.7M parameters, 547M paper-labelled FLOPs and 74.8% top-1. Supplementary Table 12 documents 224-pixel image size and 300 epochs for StarNet training. Table 6 does not separately state the compute-profiling resolution.

Correction: preserve the paper's FLOPs label. Do not rename 547M FLOPs to 0.547 GMACs without an explicit operation-count convention. The timm S2 card separately reports a rounded 0.5 GMAC statistic; this is a different-source measurement convention, not a verified conversion of the paper's value.

SUPPORTED: StarNet uses element-wise multiplication of transformed feature branches rather than token-pair dot-product self-attention. The publication presents a compact CNN with implicit nonlinear feature interactions. Additional training/distillation is discussed as a possible enhancement, not the provenance of the cited basic results.

SUPPORTED: `timm/starnet_s2.in1k` is a documented timm-hosted distribution that identifies the weights as trained by the paper authors. Card metadata lists 3.7M parameters, 0.5 GMACs, 224-by-224 images and Apache-2.0. The manifest lists both safetensors and PyTorch weight artifacts plus config; no separate LICENSE file was found. Hub metadata gives creation date 2025-05-26, before the research cutoff. The distributor is timm, not a verified author-owned Hub account. Loading, upstream license terms and local execution remain untested.

Paper authors: Xu Ma, Xiyang Dai, Yue Bai, Yizhou Wang, Yun Fu.

Sources: https://openaccess.thecvf.com/content/CVPR2024/papers/Ma_Rewrite_the_Stars_CVPR_2024_paper.pdf ; https://arxiv.org/html/2403.19967v1 ; https://huggingface.co/timm/starnet_s2.in1k ; https://huggingface.co/api/models/timm/starnet_s2.in1k

### MobileNetV5 / AutoNeural lead

The verifier reported that arXiv 2512.02924 resolves to AutoNeural: Co-Designing Vision-Language Models for NPU Inference, Wei Chen et al., initially 2025-12-02 and revised 2026-07-20. It describes an NPU-oriented vision-language system with a MobileNetV5-style vision backbone and a hybrid language component.

Conclusion limited to this evidence: the retrieved paper is not a standalone compact CNN classifier selection. It does not establish that no MobileNetV5 exists elsewhere. Do not make a global nonexistence claim from a failed or mismatched search lead.

Source: https://arxiv.org/abs/2512.02924

## Restoration verification

The verifier reported four WebSearch attempts, one failed, and six WebFetch calls. PDF extraction remained insufficient for several exact claims. The purpose of recording these failures is to prevent plausible but unverified numbers from entering the final ranking.

### PLKSR

PARTIAL: the retrieved paper presents PLKSR as a partial large-kernel CNN. A complete operator-level purity audit was not independently achieved. The paper's BasicSR, PyTorch 2.1.0 and CUDA 12.1 values are reported experimental-environment details, not established minimum requirements or exclusive supported versions.

UNSUPPORTED: PLKSR-tiny's exact parameter/MAC/FLOP values with scale and profiling resolution were not recovered. This does not mean the paper omits them. No guessed tuple will be used in the shortlist.

Venue correction: ECCV 2024 publication was not verified. An official University of Seoul record instead identifies an IEEE Access 2026 article, volume 14, pages 63847–63856, DOI 10.1109/ACCESS.2026.3686799. The 2024 manuscript and 2026 journal record must be distinguished, and the exact publication date remains to be checked against the record.

PARTIAL: the paper links the author repository, but no official checkpoint or code/weight license was verified. The paper's CC BY license cannot be extended to software or checkpoints. The paper reports Y-channel PSNR/SSIM with a border crop equal to the SR scale.

Sources: https://arxiv.org/html/2404.11848v1 ; https://arxiv.org/abs/2404.11848 ; https://pure.uos.ac.kr/en/publications/partial-large-kernel-cnns-for-efficient-super-resolution/ ; https://ieeexplore.ieee.org/iel8/6287639/6514899/11493906.pdf ; https://github.com/dslisleedh/PLKSR (linked only, contents not inspected).

### SPAN and ESPAN: withdrawn precision

SUPPORTED: SPAN's arXiv chronology begins in 2023 and includes a 2024 revision. A standalone peer-reviewed venue was not verified. Challenge participation is not sufficient proof of such a venue.

UNSUPPORTED BY REINSPECTION: the initially retrieved SPAN 151K/9.83G and ESPAN 192K/12.56G tuples, their 256-LR/1024-HR compute interpretation, the 28.87/28.89 PSNR values and their RGB/DIV2K assignment. The verification extraction omitted headings, later failed, and an extraction assigned those scores to Set5 instead. Neither the Set5 nor DIV2K assignment is adopted from those inconsistent outputs.

UNSUPPORTED BY REINSPECTION: the precise mapping of the proposed 481K paper configuration versus 151K challenge configuration. Do not treat them as interchangeable, but also do not assert that the reason for their difference has been independently established.

Action: preserve the initial retrieval as a historical record, but withdraw these exact values from decision scoring and do not claim an independently checked 0.02 dB improvement or 28% compute increase. Source appearance of compactness does not establish local activation memory or runtime.

The ESPAN official locator places the publication in CVPR 2025 Workshops, NTIRE, not main-conference CVPR. Full author/page metadata and exact performance tables remain inadequately verified by the second inspection. This weaker numerical/artifact evidence is a reason not to prioritize the restoration route under the immediate deadline, not proof that the methods themselves perform poorly.

Sources: https://arxiv.org/abs/2311.12770 ; https://openaccess.thecvf.com/content/CVPR2025W/NTIRE/papers/Wang_Expanded_SPAN_for_Efficient_Super-Resolution_CVPRW_2025_paper.pdf

## Anomaly verification

The verifier reported four WebSearch attempts, including one failure, and six WebFetch calls. No file writes, installation, model execution, dataset/checkpoint downloads or GitHub access occurred.

### EfficientAD

PARTIAL: paper text supports the 64-dimensional autoencoder bottleneck, teacher-feature rather than RGB reconstruction, 256-by-256 input and 70,000 iterations. The student regularization penalty consumes images from a pretraining dataset such as ImageNet. A teacher checkpoint does not replace those extra images. Substituting another image source or removing the penalty changes the published recipe and must be labelled an adaptation. The verification extraction did not expose an explicit teacher-freezing statement; that detail remains supported only by the initial retrieval account and must be checked before design.

UNSUPPORTED / NOT RECOVERED: exact whole-system EfficientAD-S parameters and compute. Appendix E was truncated and PDF retrieval did not yield usable text. Do not substitute a teacher-only or PDN-only size. This does not mean the information is absent from the paper.

UNSUPPORTED / UNKNOWN: exact author-repository/checkpoint URL and code/weight permissions were not recovered by this verification. No guessed official artifact URL should be reported. This is an adoption gate, not a claim that official artifacts do not exist.

Verified bibliographic names: Kilian Batzner, Lars Heckler, Rebecca König. WACV 2024 venue is supported by the official proceedings locator; the methods evidence came from the author manuscript rendering.

Sources: https://ar5iv.labs.arxiv.org/html/2303.14535 ; https://openaccess.thecvf.com/content/WACV2024/papers/Batzner_EfficientAD_Accurate_Visual_Anomaly_Detection_at_Millisecond-Level_Latencies_WACV_2024_paper.pdf

### Dinomaly

SUPPORTED: Table 4 reports ViT-Small at 37.4M parameters/26.3G MACs and ViT-Base at 148.0M/104.7G. These are reported model-complexity values, not explicitly identified trainable-parameter counts. Preprocessing resizes to 448 and center-crops to 392. Training is 10,000 iterations for the MVTec/VisA experiments and 50,000 for Real-IAD.

SUPPORTED: a frozen DINOv2-with-registers encoder feeds a noisy MLP bottleneck and a trained eight-layer Transformer decoder under feature/cosine reconstruction. Transformer-based deep feature autoencoder is a defensible architectural description; CNN is not. Whether a course expects a narrower autoencoder definition should be addressed with the supervisor, rather than mislabelling the network.

PARTIAL: the paper reports Python 3.8 and PyTorch 1.12.0. These are historical experimental-environment facts, not a demonstrated incompatibility with the local versions. The paper-linked https://github.com/guojiajeremy/Dinomaly was not inspected. Official Transformers docs describe a DINOv2-with-registers PyTorch model and `facebook/dinov2-with-registers-base`, establishing an available backbone-loading route rather than a full Dinomaly implementation. The Small checkpoint identifier and original feature-layer integration were not verified. Do not replace the original implementation silently or mistake a documented classification head for the anomaly decoder.

Verified author names: Jia Guo, Shuai Lu, Weihang Zhang, Fang Chen, Huiqi Li, Hongen Liao. CVPR 2025 venue evidence comes from the first retrieval's official conference/proceedings pages; the verifier independently checked manuscript details rather than repeating the venue query.

Sources: https://arxiv.org/html/2405.14325v5 ; https://huggingface.co/docs/transformers/model_doc/dinov2_with_registers ; https://cvpr.thecvf.com/virtual/2025/poster/34672

### MVTec AD and overlap claims

SUPPORTED: the owner describes 15 categories, over 5,000 images and CC BY-NC-SA 4.0 with noncommercial restrictions. Dinomaly's text reports 3,629 normal training, 467 normal test and 1,258 anomalous test images. Their arithmetic gives 1,725 test and 5,354 total images; exact split counts were not independently recovered from the owner's page during this verification.

Normal-only target training is not proof of absent backbone/test overlap. Related object categories in pretraining are not proof of image duplication either. No image-level contamination audit was completed. No threshold, score or local runtime guarantee follows from the dataset metadata.

Source: https://www.mvtec.com/research-teaching/datasets/mvtec-ad

## Lead-agent metadata checks and final disposition

Two additional WebFetch metadata checks were performed after the verification agents returned. MobileNetV4 v1 lists fourteen authors: Danfeng Qin, Chas Leichner, Manolis Delakis, Marco Fornoni, Shixin Luo, Fan Yang, Weijun Wang, Colby Banbury, Chengxi Ye, Berkin Akin, Vaibhav Aggarwal, Tenghui Zhu, Daniele Moro, Andrew Howard. Its inspected manuscript date is 2024-04-16; later ECCV venue evidence is separate.

The University of Seoul record confirms the Lee/Yun/Ro IEEE Access 2026 citation, volume 14, pages 63847–63856, DOI 10.1109/ACCESS.2026.3686799. It did not provide a precise publication day in the extracted result. The final review therefore records a 2024 PLKSR preprint and a 2026 journal record without inventing an ECCV publication or an exact day.

Final evidence policy: StarNet/MobileNetV4 architecture and available distributor metadata support a conditional model-selection recommendation; they do not constitute a local execution check. RepViT's paper/card discrepancy remains explicit. EfficientAD's auxiliary-data and artifact gaps, and Dinomaly's dependency/backbone integration gaps, remain approval-stage considerations. Unreliably extracted restoration tuples are excluded from scoring. No unresolved detail is silently converted into a verified fact.
