# Deep Research: Model Selection for CISC3024 AI Assignment 1

> Generated 2026-09-18 | Depth: standard, with three specialist verification passes | 22 newly retrieved screening records plus one background reference | 16 selected bibliography sources

Status: Stage 1 complete; model approval pending. No candidate has been implemented, downloaded as a checkpoint, trained, or benchmarked locally. This is an English research-stage report, not the final assessed report or its approved outline. Its Word working copy does not replace or modify the supplied final-report template.

## TL;DR

Recommend **StarNet-S2**, from *Rewrite the Stars* (CVPR 2024), as the first model for supervisor approval: its compact CNN architecture has an explainable central mechanism, the 3.7-million-parameter figure is supported, and a timm distribution identifies its weights as author-trained. **MobileNetV4-Conv-Small** is the practical classification alternative; **EfficientAD-S** and **Dinomaly-Small** offer richer anomaly-detection demonstrations but introduce substantially more unresolved data, implementation, or interpretation questions. These are evidence-based research judgments, not measured 8-GiB feasibility or promised marks (Ma et al., 2024; Qin et al., 2024; Batzner et al., 2024; Guo et al., 2025).

## Executive Summary

The supervisor asked the AI researcher to identify a recent deep CNN or deep autoencoder for a real computer-vision/pattern-recognition task and to compare complexity, local resource needs, implementation difficulty, novelty, and assignment coverage. The supervisor subsequently allowed fine-tuning, which makes an openly documented pretrained model preferable to an unsupported promise of reproducing large-scale pretraining. Model selection still requires approval, followed by a separately approved algorithm and experiment plan.

Three retrieval tracks covered classification CNNs, autoencoder-based anomaly detection, and convolutional image restoration. The consolidated ledger contains 23 unique records: 22 retrieved in this run and one explicitly unvisited background locator. Nine papers received closer methods or experimental-section extraction, with uneven table reliability. Three verification passes checked the claims most likely to influence a decision. They confirmed important classification facts, exposed checkpoint-versus-paper differences, and prevented inconsistent restoration tables from becoming numerical ranking evidence.

StarNet-S2 is recommended because the central element-wise-product operation is straightforward to explain, the model is compact, and a documented distribution provides a practical route to author-trained weights. MobileNetV4-Conv-Small is similarly attractive operationally, but the inspected timm checkpoint was trained by Ross Wightman, not established as Google's original weights. EfficientAD offers a meaningful convolutional autoencoder and anomaly maps, but its original student regularization consumes additional pretraining images; a teacher checkpoint alone does not eliminate that dependency. Dinomaly is a genuine transformer-based feature autoencoder and a 2025 publication, but it must not be called a CNN, and its original environment and Small-backbone integration remain unverified.

The conclusion is intentionally conditional. No local training memory, time, downstream accuracy, or repository-level compatibility has been established. The next decision is whether to select StarNet-S2; the next deliverable after that decision is a precise design, not immediate training.

## 1. Status Quo and Assignment Fit [Confidence: Medium]

### 1.1 What the assignment actually requires

The authoritative one-page assignment asks for a recent deep CNN or deep autoencoder with an application in computer vision and pattern recognition. It explicitly permits AI to conduct searching, programming, and report writing, and prohibits the student from writing code personally. Requirement.txt adds six report components: prompting AI to find the algorithm, describing the algorithm, explaining AI implementation, presenting experimental settings/results, reflecting on learning, and providing a source-code webpage. These local requirements are documented in the Stage 00 report and are not inferred from a research paper.

Consequently, a good choice is not simply the network with the highest published accuracy. The assignment also needs an identifiable algorithm, a reproducible implementation process, meaningful comparative experiments, and an honest record of supervisor decisions. A small transfer-learning project can satisfy these aims if the report distinguishes an implemented/adapted experiment from the original paper's training regime. Conversely, a large current model can be a poor choice if most available time is spent on inaccessible weights or incompatible infrastructure.

The request for HTML visualization is an additional supervisor goal, not a stated requirement in the two original task files. It remains desirable after backend acceptance, but should not displace essential experiments and reporting. Similarly, no numerical marking rubric was supplied. This report evaluates coverage and defensibility, not a predicted grade. The final report must use English, APA 7 citations, and the supplied template; this intermediate document is intentionally a working research report.

### 1.2 What fine-tuning permission changes

The supervisor's response, “Fine-tuning is allowed,” removes any requirement to train the selected network entirely from scratch. It does not authorize a particular checkpoint, dataset, dependency installation, or experimental run. It also does not make all pretrained weights interchangeable. An author-trained checkpoint, a library maintainer's independent retraining, and a pretrained foundation backbone are different experimental starting points that must be named accurately.

This distinction is especially important here. The StarNet-S2 timm card describes author-trained ImageNet weights. The inspected MobileNetV4 card describes Ross Wightman's timm training with paper-inspired hyperparameters and library-specific changes. Dinomaly starts from a general-purpose DINOv2 feature encoder and learns a new reconstruction component; it is not simply fine-tuning an already trained industrial defect detector. These are all potentially legitimate research choices, but they support different claims about reproduction and adaptation (timm, n.d.-a, n.d.-c; Guo et al., 2025).

### 1.3 What is known about the local environment

Stage 00 established an RTX 4060 Laptop GPU with approximately 8 GiB memory, approximately 32 GiB system RAM, an i9-13900H, and approximately 59 GiB free workspace storage. Python 3.12.10 and PyTorch 2.7.1+cu128 were already installed, and a trivial CUDA operation succeeded. Stage 1 metadata inspection additionally found torchvision 0.22.1+cu128, but no installed timm, anomalib, Lightning, TensorBoard, or W&B in that interpreter. These are local inspection results, not paper claims.

These observations justify considering compact pretrained networks. They do not prove that a research repository installs cleanly or that a training batch fits. Parameter count excludes important activation and optimizer costs; resolution, frozen versus trained layers, data loading, and laptop power limits also matter. No candidate was instantiated to test these issues because model and design approval have not yet been granted. The later pilot must replace these preliminary judgments with actual measurements.

## 2. Emerging Approaches and Search Coverage [Confidence: Medium]

### 2.1 Breadth without overstating completeness

The search was bounded primarily to 2024–2026 material available by 2026-09-18. Its 22 newly retrieved records include papers, accepted abstracts, and discovery-level leads; they are not 22 complete paper reads. Nineteen retrieved records have a 2024-or-later initial/publication year in the ledger, but that number includes rejected or unresolved items and must not be described as 19 eligible finalists. Two older classification baselines and SPAN's 2023 initial manuscript are separately identifiable. NAFNet is the one unvisited background reference and is excluded from the fresh-screening count.

Nine records received closer methods or experiment-section extraction: MobileNetV4, RepViT, StarNet, RepNeXt, EfficientAD, Dinomaly, SPAN, PLKSR, and ESPAN. “Closer extraction” does not imply that every PDF table was visually inspected. Indeed, restoration-table inconsistencies are an explicit result of the verification process. A complete CSV ledger and three track-specific English records preserve the distinctions rather than converting every search hit into a claimed full review.

The evidence supports several active directions: compact convolutional block design, CNNs borrowing design principles from transformers without becoming transformers, feature-space reconstruction for anomalies, and large-kernel or reparameterized restoration networks. It does not establish an exhaustive state of the art or prove that no stronger September 2026 model exists. Recency is one decision criterion; evidence quality and deliverability determine whether a recent lead belongs in this particular assignment (Ma et al., 2024; Wang et al., 2024; Guo et al., 2025; Lee et al., 2024).

### 2.2 Why the newest year is not automatically the best choice

Several 2025–2026 leads were retained as records but not promoted. Some had only indexed metadata, some had unresolved architecture or checkpoint identity, and others did not match the intended task. For example, the retrieved MobileNetV5-related citation was a vision-language/NPU system, not sufficient evidence for selecting a standalone compact classifier. This is a limitation of that citation, not a claim that no MobileNetV5 exists. The ledger also separates reconstruction-free anomaly detection from a trained autoencoder.

Publication chronology can itself be misleading. PLKSR has a 2024 preprint and a verified 2026 IEEE Access record. The latter does not make the original architectural idea newly invented in 2026, and it must not be relabelled ECCV 2024 without evidence. The University of Seoul record corroborates the journal, volume, pages, and DOI, but the extraction did not establish a precise publication day. The decision record therefore preserves both dates and avoids inventing a venue or day (Lee et al., 2024, 2026; University of Seoul, n.d.).

For this deadline, the practical implication is to prefer a recent, well-evidenced architecture over a more recent but weakly documented name. This is not an assertion that 2024 models are universally better. If novelty were the dominant goal and the deadline longer, more investigation of 2025–2026 candidates would be justified. Under the present constraints, unresolved access and reproducibility questions directly consume the time reserved for experiments and reporting.

## 3. Four Candidates for Supervisor Review [Confidence: Medium]

### 3.1 First recommendation: StarNet-S2, CVPR 2024

StarNet's central mechanism is element-wise multiplication of transformed feature branches. The authors analyze this “star operation” as generating rich nonlinear feature interactions within a compact CNN. It is not token-pair dot-product self-attention. The assignment can therefore explain a concrete architectural contribution without having to present the model as a transformer or rely on a vague claim that multiplication itself was newly invented (Ma et al., 2024).

Independent source inspection confirmed the accepted paper's StarNet-S2 row: 3.7 million parameters, 547 million paper-labelled FLOPs, and 74.8% ImageNet-1k top-1. Supplementary material documents 224-pixel training images and 300 epochs. The compute table does not independently specify a profiling resolution, and its label is FLOPs, not MACs. The report should therefore preserve that label and avoid presenting 0.547 GMACs as a verified conversion. The ImageNet result is a paper result, not a target for a different downstream dataset (Ma et al., 2024).

The documented distribution is `timm/starnet_s2.in1k`. Its card identifies the weights as author-trained and reports 3.7 million parameters, 224-by-224 images and a rounded 0.5-GMAC statistic. The inspected manifest lists configuration and both safetensors/PyTorch weight artifacts. Card metadata declares Apache-2.0, but no separate LICENSE file was listed, and the upstream author repository was not audited. These facts support an available distribution route, not a claim that model loading or the full license chain has been tested locally (timm, n.d.-c).

StarNet-S2 is the preferred balance of explanation and execution risk. Its mechanism gives the algorithm-description section a clear focus, and its modest size makes controlled transfer-learning experiments plausible. A later plan could compare a frozen feature extractor with partial or full fine-tuning, provided comparisons are fair and validation-driven. A naive operation-removal experiment on unchanged pretrained weights would not automatically be a valid causal ablation; architectural changes require controlled initialization and training. The exact comparisons belong in the approved design, not in this selection decision.

### 3.2 Practical alternative: MobileNetV4-Conv-Small, ECCV 2024

MobileNetV4's Conv family uses Universal Inverted Bottleneck blocks selected for efficient mobile models. Optional depthwise convolutions around expansion/projection allow related convolutional block configurations. The Hybrid family adds Mobile MQA attention; choosing Conv-Small explicitly avoids confusing the assignment's CNN route with a separate hybrid variant. ECCV's conference listing provides venue evidence separately from the inspected arXiv manuscript (Qin et al., 2024; European Conference on Computer Vision, 2024).

The inspected checkpoint is `timm/mobilenetv4_conv_small.e2400_r224_in1k`. Its card reports 3.8 million parameters, 0.2 GMACs, 224-pixel training and 256-pixel testing. The card does not explicitly connect the compute number to a profiling resolution. It also attributes training to Ross Wightman using timm, including changes beyond the original recipe. The project must call this a timm-trained MobileNetV4 checkpoint rather than Google's original weights or a faithful reproduction of the authors' full training (timm, n.d.-a).

This is a strong low-resource alternative because the architecture and native timm loading route are documented. The same limitations apply: timm is not yet installed, the declared Apache-2.0 metadata is not an upstream license audit, and no actual training run has occurred. Published phone or accelerator inference results do not predict laptop fine-tuning time. Its apparent compute advantage over another card also cannot be interpreted as a proportional speed advantage without aligned measurement protocols.

Compared with StarNet, MobileNetV4 emphasizes a broader efficient architecture family rather than one especially compact explanatory mechanism. That can make the report more technically detailed but slightly harder to keep focused. It is a reasonable selection if the supervisor prefers a widely recognizable mobile-CNN family and accepts the documented maintainer-trained checkpoint provenance. It is not rejected for using library-trained weights; the provenance simply needs explicit approval and disclosure.

### 3.3 Convolutional-autoencoder route: EfficientAD-S, WACV 2024

EfficientAD combines student–teacher discrepancies with a trained convolutional autoencoder that reconstructs teacher feature maps rather than RGB pixels. The paper describes a 64-dimensional bottleneck and complementary local/global anomaly information. This gives the assignment an application-oriented story: learn normal appearance, identify abnormal images, and display localization maps. It is more than scoring fixed pretrained features with a nearest-neighbor rule (Batzner et al., 2024).

The verified training description uses 256-by-256 images and 70,000 iterations. Crucially, the student penalty consumes an image from a pretraining dataset such as ImageNet. A pretrained distilled teacher does not replace these extra regularization images. Removing that term, substituting a small source, shortening the schedule, or reducing the task to a category-specific experiment can be sensible adaptations, but they cannot be concealed under a claim to reproduce the paper-wide results (Batzner et al., 2024).

The complete-system parameter count and compute could not be recovered reliably from Appendix E. Teacher-only statistics would be misleading because the executed system also includes the student and autoencoder. Neither the exact official teacher-checkpoint route nor code/weight licensing was verified by the permitted retrieval route. The second extraction also did not expose an explicit teacher-freezing statement, so that implementation detail must be checked before the design is accepted. Unknown here means unverified, not unavailable.

EfficientAD offers strong report and visualization potential, including an appropriately controlled comparison involving its global autoencoder branch. Nevertheless, the auxiliary-data obligation and incomplete artifact verification make it a less predictable three-day choice than the classification candidates. It is the more natural alternative if the supervisor explicitly prefers a convolutional autoencoder and industrial-defect demonstration. Selection should be conditional on resolving the teacher, auxiliary-data and license gates before training is authorized.

### 3.4 More recent autoencoder route: Dinomaly-Small, CVPR 2025

Dinomaly is a transformer-based deep feature autoencoder, not a CNN. It uses a frozen DINOv2-with-registers encoder, a noisy MLP bottleneck and an eight-layer Transformer decoder trained to reconstruct intermediate features with a cosine-based objective. This supports a genuine deep-autoencoder interpretation: it includes newly trained reconstruction components rather than merely evaluating an untouched feature extractor. The paper's CVPR 2025 listing corroborates publication separately from its manuscript (Guo et al., 2025; Conference on Computer Vision and Pattern Recognition, 2025).

The inspected Table 4 reports the Small variant at 37.4 million parameters and 26.3G MACs, versus 148.0 million and 104.7G for Base. These are reported model-complexity values, not explicitly optimized/trainable parameter counts. The documented preprocessing resizes to 448 and center-crops to 392; the MVTec/VisA experiments use 10,000 iterations. Those settings are not directly comparable to the 224-pixel classification cards, and published inference throughput does not establish training memory (Guo et al., 2025).

The paper reports Python 3.8 and PyTorch 1.12.0. This does not prove incompatibility with the current laptop, but it creates an untested integration question. Official Transformers documentation establishes a PyTorch DINOv2-with-registers backbone route, including a Base example, not a complete Dinomaly detector or a verified drop-in replacement for its original Small feature pipeline. The exact Small artifact, feature-layer integration, dependency pins and code/weight terms remain to be checked (Guo et al., 2025; Hugging Face, n.d.).

This candidate offers greater publication recency and an interesting reconstruction problem, but less implementation certainty. A single-category, smaller-batch or changed-resolution project could still be useful, while no longer reproducing the headline multi-class setting. The supervisor should accept the transformer-autoencoder interpretation explicitly rather than allowing the report to call the model a CNN. It is a valid higher-uncertainty alternative, not the recommended default under the present deadline.

## 4. Critical Assessment and Decision Matrix [Confidence: Medium]

### 4.1 Five requested dimensions

The following scores are researcher judgments on a 1–5 desirability scale. Higher means simpler architecture, lower expected resource burden, easier implementation, stronger novelty, or stronger coverage of documented report requirements. They are not measured benchmarks or a university marking rubric. The weights were disclosed in the search protocol: complexity 15%, hardware fit 25%, implementation 25%, novelty 20%, and report coverage 15%.

| Candidate | Simplicity | Hardware fit | Implementation | Novelty | Report coverage | Weighted judgment |
| --- | --- | --- | --- | --- | --- | --- |
| StarNet-S2 | 5 | 5 | 4 | 3 | 5 | 4.35 / 5 |
| MobileNetV4-Conv-Small | 4 | 5 | 4 | 3 | 4 | 4.05 / 5 |
| Dinomaly-Small | 3 | 3 | 2 | 4 | 4 | 3.10 / 5 |
| EfficientAD-S | 3 | 3 | 2 | 3 | 5 | 3.05 / 5 |

The 0.05 difference between the anomaly options is not meaningful evidence of superiority; treat them as the same higher-uncertainty tier. Hardware scores describe relative plausibility from architecture and evidence, not a promise to fit 8 GiB. Implementation scores deliberately penalize missing artifact/dependency information. StarNet and MobileNetV4 both still require approved dependencies and a successful pilot, so neither receives the maximum implementation score.

The recommendation remains stable if the five dimensions are weighted equally: StarNet scores 4.4, MobileNetV4 4.0, and both anomaly options 3.2. This simple sensitivity check does not validate the subjective inputs; it shows that the recommendation is not solely an artifact of one weighting choice. The supervisor can reasonably choose an anomaly route if application richness or 2025 recency is more important than setup predictability. That would be a preference decision, not a contradiction of the evidence.

### 4.2 Why RepViT and restoration are reserves

RepViT remains a credible classification reserve, not an unsuitable model. Its paper reports M0.9 at 5.1 million parameters and 0.8 GMACs at 224 pixels. The 78.7% top-1 result is specifically a 300-epoch distilled result; the inspected checkpoint is labelled for 450-epoch training, and its card reports 5.5 million parameters. The discrepancy is unresolved. An unverified explanation involving heads or reparameterization must not be invented to make the numbers agree (Wang et al., 2024; timm, n.d.-b).

The four primary choices intentionally span decision routes rather than being an absolute top-four ranking of every model. Including another classifier would reduce visibility of the supervisor's explicit autoencoder option. If the supervisor chooses the classification route but rejects StarNet and MobileNetV4, RepViT is the next reserve to audit. RepNeXt and newer discovery-level CNNs remain in the ledger but currently have weaker verified deployment evidence.

Restoration networks offer visually compelling demonstrations, but their reported efficiency tables did not survive the same verification standard. The first retrieval assigned precise SPAN/ESPAN sizes, operation counts and scores to particular protocols; reinspection produced missing headings, failed extraction and contradictory dataset attribution. Those precise claims were withdrawn from ranking. This is a failure of the available extraction evidence, not proof that the papers are incorrect. PLKSR's exact tiny-model tuple and checkpoint permissions also remain unverified (Lee et al., 2024; stage_01_verification.md).

### 4.3 Reproduction, adaptation and unfair comparisons

The final project must state its experimental object precisely: paper version, architecture variant, pretrained distributor, checkpoint identifier, input preprocessing, and any modifications. A small target-dataset fine-tune is not original ImageNet pretraining. Training only a reconstruction decoder is not end-to-end fine-tuning of a foundation encoder. A category-scoped anomaly experiment is not a reproduction of a multi-class benchmark average. These distinctions are necessary for the algorithm and implementation sections to remain accurate.

Likewise, MACs and FLOPs should not be silently exchanged, scores from different image resolutions should not be treated as equal-compute results, and RGB/Y-channel restoration metrics should not be mixed. The verified StarNet and timm labels illustrate why retaining source terminology matters even when rounded values look similar. Local peak memory, wall-clock training time and synchronized inference measurements must be collected under one documented implementation rather than estimated from unrelated paper hardware (Ma et al., 2024; timm, n.d.-c; Lee et al., 2024).

## 5. Data, Evaluation and Deadline Implications [Confidence: Medium]

For classification, Oxford Flowers102, Oxford-IIIT Pets and DTD were identified only as possible directions. Their exact download sizes, licenses, current official splits and pretraining overlap were not verified in this stage, so no dataset is selected here. The next design must choose a manageable dataset for an actual application, define training/validation/test roles, and justify the task beyond the convenience of a familiar benchmark. The report must not imply that a dataset proposal is already a downloaded, cleaned or approved dataset.

For anomaly detection, stronger dataset-owner evidence was obtained. MVTec AD describes 15 categories, over 5,000 images and a normal-only training/mixed-test protocol with pixel annotations. Its CC BY-NC-SA 4.0 terms include noncommercial restrictions. Dinomaly supplies exact split counts, but those were not independently recovered from the owner's page in this pass. The AWS VisA registry reports 10,821 total images and CC BY 4.0; that total is not itself a training-set size. Archive byte sizes and extracted footprints remain unverified (MVTec Software, n.d.; Registry of Open Data on AWS, n.d.; Guo et al., 2025).

Any plan must prevent test-driven tuning. Preprocessing and checkpoint selection should be fixed using training/validation data. In anomaly detection, map normalization and an operational threshold must not be estimated from test masks, and a test-set maximum F1 should be identified as an oracle diagnostic rather than a deployable threshold. Image AUROC alone also misses localization behavior; the selected protocol should include suitable pixel-level measures and define any AUPRO integration limit. None of these metrics guarantees robustness outside the benchmark (Batzner et al., 2024; Guo et al., 2025).

Pretraining overlap needs careful language. Related flower or animal categories in ImageNet do not prove duplicate-image leakage, while normal-only target training does not prove that a large pretrained model has never seen an evaluation image. The honest report will describe known provenance, inspect available overlap evidence, and state unresolved limitations. It should neither assert contamination without evidence nor imply a completed contamination audit when none occurred.

The working deadline remains completion by the evening of 2026-09-20, before September 21. The present stage does not justify a fixed training-hour promise. After model approval, design and access checks should precede a short measured pilot; the pilot should establish actual memory, throughput and a maximum training budget before scale-up. If that gate fails, return to the supervisor rather than silently choosing a new model or consuming the reporting buffer. HTML work follows backend acceptance, and final reporting must retain time for template fields, references, the source webpage and submission checks.

## 6. Action Plan and Approval Gate [Confidence: Low for unmeasured feasibility]

The next action requested from the supervisor is model selection. The recommended decision is StarNet-S2 with the inspected author-trained, timm-distributed ImageNet checkpoint as the proposed initialization. Approval would authorize preparing the detailed design; it would not yet authorize installing timm, downloading that checkpoint, acquiring data, or starting training. This interpretation preserves the supervisor's original stage boundaries.

- [ ] Supervisor approves StarNet-S2 or chooses one of the alternatives.
- [ ] Prepare the exact algorithm/data/evaluation design, including dependency and weight-license checks, for separate approval.
- [ ] After design approval, run the smallest implementation and measured feasibility pilot; report findings before expansion.
- [ ] Proceed with approved comparisons and failure analysis, then consider visualization after backend acceptance.
- [ ] Build the final report from preserved evidence, obtain actual supervisor reflections, and verify the source-code webpage before submission.

A suitable design document must name the dataset and official split, any internal validation allocation, the exact checkpoint and classifier/reconstruction head, trainable layers, loss, optimizer, regularization, seeds, evaluation metrics, checkpoint-selection rule, and stopping criteria. It must also explain how any comparison isolates the intended factor. These requirements describe the contents of the next deliverable; they are not filled with speculative values here because the model has not been approved.

The design should separately list installations or downloads requiring consent. A working `gh` route would allow direct author-repository/license inspection, while timm would enable the documented classifier route. Neither has been installed in this research stage. If the supervisor does not approve an additional tool, the next stage should identify the specific remaining evidence gap rather than bypass the tool boundary or claim an audit that did not occur.

## 7. Open Questions and Caveats [Confidence: Medium]

The recommended network has not been selected by the supervisor, and its local execution has not been tested. The presence of safetensors/PyTorch files in a distributor manifest is useful provenance evidence, not a guarantee that a particular timm release, classifier modification, or training configuration will load correctly. A card's Apache-2.0 declaration also should not be overstated as a complete audit of upstream code and weights. Those checks remain prerequisites of an implementation plan.

The biggest research limitations are bounded search coverage and uneven retrieval quality. Some recent leads were discovery-only, several full-paper tables were difficult to extract, and GitHub CLI absence prevented direct repository auditing. The report therefore retains unresolved findings rather than making every candidate look equally verified. Restoration methods may become competitive after better artifact/table access; their current lower priority reflects evidence and deadline conditions, not an assertion of lower scientific merit.

This review also did not verify an exact UMMoodle cutoff, a numerical grading rubric, or whether the instructor intends a narrower definition of deep autoencoder than a transformer-based feature reconstructor. The original task supports recent CNN or autoencoder work; the supervisor may still prefer the simplest interpretation. Exact cover-placeholder replacement and public repository visibility remain separate decisions carried forward from Stage 00.

Most importantly, no experimental results exist yet. Published ImageNet accuracy, anomaly AUROC or throughput must never appear in the final report as the assignment's own result. A successful final report will separate literature evidence, AI-generated implementation, observed local results, and the supervisor's actual evaluation. Personal learning reflections must be elicited from the supervisor rather than invented by the assistant.

## Methodology

The installed deep-research workflow was used after the supervisor approved its installation and answered the pretrained-weight clarification. Three retrieval agents worked on distinct tracks, then three specialist verification agents checked architecture, numerical tuples, provenance, dependencies and evaluation conditions. The extra verification split was an adaptation of the standard workflow to keep unrelated evidence checks parallel; it did not create three independent experimental replications.

The agents reported 24 retrieval WebSearch calls and 15 retrieval WebFetch calls, followed by 13 verification search attempts and 20 verification fetch calls. The lead agent performed two additional metadata fetches. Thus the reported tool totals are 37 search attempts and 37 fetch calls, including failures. Some agents also used existing tools for read-only, in-memory source extraction; these totals are not an exhaustive HTTP-request count. No datasets, checkpoints or additional packages were downloaded, and no model code was executed.

The lead merged records into a CSV and validated unique IDs/URLs, track counts, newly retrieved flags and closer-read counts. The counts were 9 classification, 7 anomaly and 7 restoration records, with one restoration background record excluded from the 22 fresh retrievals. Mirrors, conference pages and model cards were treated as provenance sources, not additional independent papers. The selected bibliography contains 16 sources, including documentation and dataset pages; it is not a claim of 16 independent confirming studies.

Confidence labels distinguish primary-source support from practical transferability. Exact architecture or metadata can be well supported by one primary source, while laptop feasibility remains unmeasured. No section is promoted to high confidence merely because several tools repeated the same paper. Failed source access was treated as an evidence limitation. One anomaly search initially used an incorrect arXiv address, discarded the unrelated result and corrected the reference; this mistake is preserved in the track record rather than hidden.

Verification changed the report substantially but did not change its research question. It clarified MobileNetV4's non-Google checkpoint provenance, added RepViT's epoch/distillation and parameter-count qualifications, recovered StarNet's exact paper rows without renaming FLOPs as MACs, and withdrew unreliable restoration tuples. It also corrected PLKSR venue chronology and exposed EfficientAD's auxiliary-image obligation. These corrections explain why the final recommendation differs from simply choosing each retrieval agent's first suggestion.

## Bibliography

Bibliographic entries use author–date conventions suitable for later APA 7 preparation. Proceedings page ranges not independently checked are omitted rather than invented. Living documentation was accessed on September 18, 2026. Paper and distributor sources must remain distinct in the final assessed report.

Batzner, K., Heckler, L., & König, R. (2024). EfficientAD: Accurate visual anomaly detection at millisecond-level latencies. In *Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision*. https://openaccess.thecvf.com/content/WACV2024/papers/Batzner_EfficientAD_Accurate_Visual_Anomaly_Detection_at_Millisecond-Level_Latencies_WACV_2024_paper.pdf

Bayar, E. (n.d.). *QFAE* [Computer software]. GitHub. Retrieved September 18, 2026, from https://github.com/emirhanbayar/QFAE

Conference on Computer Vision and Pattern Recognition. (2025). *Dinomaly: The less is more philosophy in multi-class unsupervised anomaly detection* [Conference listing]. https://cvpr.thecvf.com/virtual/2025/poster/34672

Dalmonte, F., Bayar, E., Akbas, E., & Georgescu, M.-I. (2026). Q-Former autoencoder: A modern framework for medical anomaly detection. In *Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision*. https://openaccess.thecvf.com/content/WACV2026/papers/Dalmonte_Q-Former_Autoencoder_A_Modern_Framework_for_Medical_Anomaly_Detection_WACV_2026_paper.pdf

European Conference on Computer Vision. (2024). *MobileNetV4: Universal models for the mobile ecosystem* [Conference listing]. https://eccv.ecva.net/virtual/2024/oral/482

Guo, J., Lu, S., Zhang, W., Chen, F., Li, H., & Liao, H. (2025). Dinomaly: The less is more philosophy in multi-class unsupervised anomaly detection [Author manuscript, version 5]. *arXiv*. https://arxiv.org/html/2405.14325v5

dslisleedh. (n.d.). *PLKSR: Partial large kernel networks* [Computer software]. GitHub. Retrieved September 18, 2026, from https://github.com/dslisleedh/PLKSR

ETH Zurich Computer Vision Laboratory. (n.d.). *DIV2K dataset*. Retrieved September 18, 2026, from https://data.vision.ee.ethz.ch/cvl/DIV2K/

guojiajeremy. (n.d.). *Dinomaly* [Computer software]. GitHub. Retrieved September 18, 2026, from https://github.com/guojiajeremy/Dinomaly

Hugging Face. (n.d.). *DINOv2 with registers*. Transformers documentation. Retrieved September 18, 2026, from https://huggingface.co/docs/transformers/model_doc/dinov2_with_registers

jameslahm. (n.d.). *lsnet_b* [Model card]. Hugging Face. Retrieved September 18, 2026, from https://huggingface.co/jameslahm/lsnet_b

nelson1425. (n.d.). *EfficientAD* [Computer software]. GitHub. Retrieved September 18, 2026, from https://github.com/nelson1425/EfficientAD

Lee, D., Yun, S., & Ro, Y. (2024). Partial large kernel CNNs for efficient super-resolution [Preprint]. *arXiv*. https://arxiv.org/html/2404.11848v1

Lee, D., Yun, S., & Ro, Y. (2026). Partial large kernel CNNs for efficient super-resolution. *IEEE Access, 14*, 63847–63856. https://doi.org/10.1109/ACCESS.2026.3686799

Li, D., Li, L., Chen, Z., & Li, J. (2025). ShiftwiseConv: Small convolutional kernel with large kernel effect. In *Proceedings of the 2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition*. https://openaccess.thecvf.com/content/CVPR2025/papers/Li_ShiftwiseConv_Small_Convolutional_Kernel_with_Large_Kernel_Effect_CVPR_2025_paper.pdf

Ma, X., Dai, X., Bai, Y., Wang, Y., & Fu, Y. (2024). Rewrite the stars. In *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*. https://openaccess.thecvf.com/content/CVPR2024/papers/Ma_Rewrite_the_Stars_CVPR_2024_paper.pdf

MVTec Software. (n.d.). *MVTec AD: A comprehensive real-world dataset for unsupervised anomaly detection*. Retrieved September 18, 2026, from https://www.mvtec.com/research-teaching/datasets/mvtec-ad

Qin, D., Leichner, C., Delakis, M., Fornoni, M., Luo, S., Yang, F., Wang, W., Banbury, C., Ye, C., Akin, B., Aggarwal, V., Zhu, T., Moro, D., & Howard, A. (2024). MobileNetV4: Universal models for the mobile ecosystem [Preprint, version 1]. *arXiv*. https://arxiv.org/html/2404.10518v1

Roboflow. (2024, July 22). *How to use MobileNetV4 for classification*. https://blog.roboflow.com/how-to-use-mobilenetv4-for-classification/

Sah, S., & Kumar, R. (2026). STResNet & STYOLO: A new family of compact classification and object detection models for MCUs [Preprint]. *arXiv*. https://arxiv.org/abs/2601.05364

THU-MIG. (n.d.-a). *LSNet* [Computer software]. GitHub. Retrieved September 18, 2026, from https://github.com/THU-MIG/lsnet

THU-MIG. (n.d.-b). *RepViT* [Computer software]. GitHub. Retrieved September 18, 2026, from https://github.com/THU-MIG/RepViT

Registry of Open Data on AWS. (n.d.). *Visual Anomaly (VisA)*. Retrieved September 18, 2026, from https://registry.opendata.aws/visa/

timm. (n.d.-a). *mobilenetv4_conv_small.e2400_r224_in1k* [Model card]. Hugging Face. Retrieved September 18, 2026, from https://huggingface.co/timm/mobilenetv4_conv_small.e2400_r224_in1k

timm. (n.d.-b). *repvit_m0_9.dist_450e_in1k* [Model card]. Hugging Face. Retrieved September 18, 2026, from https://huggingface.co/timm/repvit_m0_9.dist_450e_in1k

timm. (n.d.-c). *starnet_s2.in1k* [Model card]. Hugging Face. Retrieved September 18, 2026, from https://huggingface.co/timm/starnet_s2.in1k

University of Seoul. (n.d.). *Partial large kernel CNNs for efficient super-resolution* [Publication record]. Retrieved September 18, 2026, from https://pure.uos.ac.kr/en/publications/partial-large-kernel-cnns-for-efficient-super-resolution/

Wang, A., Chen, H., Lin, Z., Han, J., & Ding, G. (2024a). RepViT: Revisiting mobile CNN from ViT perspective. In *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition* (pp. 15909–15920). https://openaccess.thecvf.com/content/CVPR2024/papers/Wang_RepViT_Revisiting_Mobile_CNN_From_ViT_Perspective_CVPR_2024_paper.pdf

Wang, A., Chen, H., Lin, Z., Han, J., & Ding, G. (2024b). RepViT: Revisiting mobile CNN from ViT perspective [CVPR 2024 camera-ready author manuscript]. *arXiv*. https://arxiv.org/html/2307.09283

Wang, A., Chen, H., Lin, Z., Han, J., & Ding, G. (2025). LSNet: See large, focus small. In *Proceedings of the 2025 IEEE/CVF Conference on Computer Vision and Pattern Recognition* (pp. 9718-9729). https://openaccess.thecvf.com/content/CVPR2025/papers/Wang_LSNet_See_Large_Focus_Small_CVPR_2025_paper.pdf

Zhao, M. (n.d.). *RepNeXt* [Computer software]. GitHub. Retrieved September 18, 2026, from https://github.com/suous/RepNeXt

Zhao, M., Luo, Y., & Ouyang, Y. (2024). RepNeXt: A fast multi-scale CNN using structural reparameterization [Preprint]. *arXiv*. https://arxiv.org/abs/2406.16004

## Source Extracts and Evidence Map

The entries below are paraphrased source findings, not extended quotations. Complete track records preserve actual queries and broader exclusions; the verification register identifies corrections. Tier 1 denotes primary author, publisher, official distributor or dataset-owner provenance, not independent replication or automatic peer review.

### StarNet — primary paper and distributor card

The accepted paper explains element-wise feature multiplication and provides separate variant rows. The S2 parameter count agrees with the inspected timm card, while operation counts use different source labels. The checkpoint card identifies author training and provides documented loading with listed weight artifacts. Evidence depth: selected paper text, table/supplement cross-check and model-card/manifest inspection. Source type: academic paper plus distributor documentation. Tier: 1. Local execution: not performed.

### MobileNetV4 — manuscript, conference listing and distributor card

The manuscript distinguishes Conv UIB configurations from Hybrid Mobile MQA models. The conference listing establishes ECCV 2024 presentation, while the card identifies a timm-trained implementation rather than original Google weights. The card's compute-resolution association remains unspecified. Evidence depth: architecture/manuscript, venue listing, raw card and file manifest. Source type: academic paper, conference metadata and distributor documentation. Tier: 1. Independent training replication: not established.

### RepViT — manuscript and distributor card

The manuscript separates distilled/non-distilled and 300/450-epoch results. The inspected card describes an author-trained 450-epoch checkpoint but gives a different parameter count from the paper. Both counts are preserved with their sources rather than reconciled through speculation. Evidence depth: original HTML table headings/rows and card/manifest. Source type: academic paper and distributor documentation. Tier: 1. Final status: classification reserve with an unresolved artifact-accounting issue.

### EfficientAD — paper and manuscript rendering

The available text supports feature autoencoding, the bottleneck, input size, training iterations and auxiliary-image penalty. Appendix E and exact checkpoint/license details were not recovered reliably. Consequently, the review does not publish a guessed whole-system size or an invented official checkpoint URL. Evidence depth: selected methods, algorithm and evaluation passages with appendix gaps. Source type: proceedings paper/author manuscript. Tier: 1. Adoption gates remain unresolved.

### Dinomaly — manuscript, venue and backbone documentation

The manuscript establishes a frozen feature encoder with a learned bottleneck/decoder and supplies the Small/Base model-complexity rows and preprocessing. The backbone documentation confirms a generic PyTorch-loading route, not the entire original anomaly implementation or a tested Small replacement. Evidence depth: methods/table/appendix passages, conference listing and official library documentation. Source type: academic/official documentation. Tier: 1. Local environment compatibility: unknown.

### PLKSR and restoration evidence limitations

The manuscript and university record establish a 2024 preprint and a later 2026 IEEE Access article. Exact tiny-model complexity and checkpoint permissions remain unverified. Separate SPAN/ESPAN numerical extractions conflicted and were withdrawn. The review deliberately retains the error history while excluding those values from the decision matrix. Evidence depth: selected manuscript text, university metadata and failed/inconsistent table extraction. Source type: academic and institutional records. Tier: 1 provenance with uneven claim support.

### Dataset-owner evidence

The MVTec owner page supports broad size, categories, normal-only training and noncommercial/share-alike licensing. Exact MVTec split arithmetic in this review traces to Dinomaly's description rather than a separately inspected file listing. The VisA registry supplies total counts, resource metadata and a different license. Neither source access involved downloading image archives or checking every sample. Source type: owner/official registry documentation. Tier: 1. Data-integrity, storage and overlap audits: pending.

## 8. Supplementary Investigation: ShiftwiseConv (CVPR 2025) [Confidence: Medium]

The supervisor requested further investigation of 2025-2026 candidates. Four parallel subagents investigated ShiftwiseConv, the strongest 2025 candidate found in the initial retrieval. This investigation uncovered a **critical parameter-count discrepancy** that materially changes the comparison.

### 8.1 Initial retrieval claim vs. verified paper data

The initial retrieval subagent reported ShiftwiseConv SW-Tiny at approximately 5.8 million parameters with 83.39% ImageNet top-1 accuracy. The deep investigation subagent, which fetched the arXiv HTML and CVF open-access paper, found the published SW-Tiny actually has **31 million parameters** and 5.0G FLOPs. No variant with approximately 5.8M parameters exists in the published paper or official repository. The initial 5.8M figure was a retrieval error (Li et al., 2025).

### 8.2 Corrected comparison

| Dimension | StarNet-S2 (CVPR 2024) | ShiftwiseConv SW-Tiny (CVPR 2025) |
|-----------|------------------------|----------------------------------|
| Parameters | 3.7M | **31M** (corrected) |
| Compute | 547M FLOPs | 5.0G FLOPs |
| ImageNet top-1 | 74.8% | 83.4% |
| timm integration | Yes | No |
| Custom CUDA module | No | Yes (shiftadd/ must compile) |
| Python version | Standard | 3.8 required (local: 3.12.10) |
| Setup risk | Low | High |
| Explainability | High (single equation) | Moderate (multi-layer shifts) |

ShiftwiseConv is approximately 8.4x larger than StarNet-S2 in parameter count, not 1.6x as initially believed.

### 8.3 GitHub verification findings

The official repository (https://github.com/lidc54/shift-wiseConv) has an MIT License held by Meta Platforms, Inc., indicating derivative code. Only one pretrained weight is available (SW-Tiny), hosted on Google Drive. The code requires compiling a custom CUDA module (`shiftadd/`), specifies Python 3.8 and torchvision 0.11.0, and has no timm integration. These create untested compatibility questions with the local environment (Python 3.12.10, torchvision 0.22.1, CUDA 12.8).

### 8.4 Report explainability assessment

StarNet-S2's mechanism (y = f(x) ⊙ g(x)) is explainable in a single equation with a simple two-branch diagram. ShiftwiseConv requires explaining how shifted 3x3 convolutions accumulate across layers to create a large effective receptive field, which needs multi-panel diagrams and more background. For a three-day deadline, StarNet-S2 is easier to write about and diagram.

### 8.5 GPU feasibility (corrected)

Even at 31M parameters, batch 16-32 at 224x224 should fit in 8 GiB with mixed precision. However, the shift operations may require additional memory for shifted feature map copies, which is untested. StarNet-S2 at 3.7M parameters has significantly more headroom.

### 8.6 Recommendation after investigation

**StarNet-S2 remains the recommended choice.** ShiftwiseConv's advantages (CVPR 2025 recency, 83.4% ImageNet) are outweighed by its 31M parameter count (8.4x larger than StarNet-S2), custom CUDA compilation requirement, Python version mismatch, lack of timm integration, and lower explainability. The full investigation is documented in the Stage 01b supplementary file.

### 8.7 Other 2025-2026 candidates found

LSNet (CVPR 2025) uses LS convolution combining large-receptive-field and small-kernel focus paths. Exact parameters and accuracy were not extracted. RepNeXt (arXiv 2024, no confirmed venue) has 13.3M params and 82.3% ImageNet. STResNet (arXiv 2026-01) has 0.95M-3.99M params but only 58.8%-71.6% ImageNet. Q-Former Autoencoder (WACV 2026) targets medical imaging with no MVTec results. None of these have sufficient verified detail to displace StarNet-S2 under the current deadline. (All four candidates were subsequently verified in the Stage 01d investigation; see Section 10.)

## 9. Horizontal Comparison of All Candidates and Final Selection [Confidence: Medium]

The supervisor then requested the same comparison-focused investigation for every remaining shortlisted candidate, with all consulted literature recorded for APA 7 citation. Three parallel gap-fill subagents covered the classification pair (MobileNetV4-Conv-Small, RepViT-M0.9), the anomaly pair (EfficientAD, Dinomaly), and the restoration track (PLKSR, plus SPAN/ESPAN context). They reported 18 search attempts and 15 fetch attempts, including three failed searches and several blocked fetches. No downloads, installations, or executions occurred. Full per-track findings, verbatim table rows, and a 26-entry source list are preserved in the Stage 01c comparison file.

### 9.1 New evidence that changes the picture

1. **MobileNetV4-Conv-S paper accuracy recovered**: 73.8% top-1 at 3.8M/0.2G (paper Table 6). Critically, this number corresponds to Google's training, while the timm checkpoint is an independent 2400-epoch reproduction by Ross Wightman whose achieved top-1 the card does not state; the report must keep these two claims separate. ECCV 2024 oral status confirmed; no official PyTorch release exists outside timm.
2. **RepViT proceedings citation verified**: CVPR 2024, pp. 15909-15920, with the CVF author list (including Jungong Han; the timm card's arXiv BibTeX lists a different fourth author, so CVF governs). The 5.1M (paper) vs 5.5M (card) parameter difference is characterized but its root cause remains UNSUPPORTED; GMACs match at 0.8.
3. **EfficientAD-S parameter count recovered**: the paper states 1.6M (-S) and 2.7M (-M) parameters, with 98.8%/99.1% MVTec image AUROC and roughly twenty minutes of per-category training on an RTX A6000. Whether the parameter figure covers the whole pipeline is UNSUPPORTED. The only code is an unofficial community repository (nelson1425, Apache-2.0) with teacher checkpoints included; the ImageNet auxiliary-image subset size remains the route's main unverified dependency.
4. **Dinomaly gap confirmed**: the Apache-2.0 repository provides only ViT-Base (Dinomaly-B) checkpoints, pins a Python 3.8.12-era environment against an RTX 3090 24 GB reference, and its README uses 20k iterations where the paper says 10k. ViT-Small checkpoint existence, backbone weight size, and ViT-S AUROC remain UNSUPPORTED.
5. **PLKSR comparison data is intentionally non-standard**: the paper refuses to report parameters/FLOPs for its own variants, using latency and maximum GPU memory on HD input at RTX 4090 FP16 instead; its training protocol is 450k iterations on DIV2K at batch 64 of 96x96 patches, which cannot be reproduced from scratch within the deadline. The repository is MIT but BasicSR-based with Google Drive-hosted checkpoints. All reported PSNR/SSIM values are Y-channel with scale-equal border crops. SPAN/ESPAN headline numbers remain unverified and withdrawn.

### 9.2 Seven-candidate comparison

| Candidate | Track | Params | Reported accuracy | Weights / license | 8 GiB + deadline fit | Implementation | Explainability |
|---|---|---|---|---|---|---|---|
| StarNet-S2 (CVPR 2024) | Classification | 3.7M | 74.8% top-1 | Author-trained; timm; Apache-2.0 | Highest headroom | timm-native | 1 equation |
| MobileNetV4-Conv-S (ECCV 2024) | Classification | 3.8M | 73.8% top-1 (paper training; timm weights are a reproduction) | timm-trained; Apache-2.0 | High headroom | timm-native | ~2-3 concepts (UIB, ExtraDW, NAS) |
| RepViT-M0.9 (CVPR 2024) | Classification | 5.1M/5.5M | 78.7%/79.1% | Author-trained, distilled; timm; Apache-2.0 | High headroom | timm-native | ~3-4 concepts (block, SE, re-parameterization) |
| ShiftwiseConv SW-Tiny (CVPR 2025) | Classification | 31M | 83.4% top-1 | MIT (Meta); one Drive weight | Untested shift-op memory | Custom CUDA; Python 3.8 | Multi-layer shift accumulation |
| EfficientAD-S (WACV 2024) | Anomaly | 1.6M (scope ambiguous) | 98.8% image AUROC | Unofficial repo; Apache-2.0 | Fast training; ImageNet auxiliary images unverified | Standalone repo; no timm | ~4 concepts (teacher-student, AE, penalty) |
| Dinomaly ViT-S (CVPR 2025) | Anomaly | 37.4M | ViT-S AUROC unrecovered | Apache-2.0; only ViT-B checkpoints | 24 GB reference setup; dependency risk | DINOv2 + custom decoder | ~4-5 concepts |
| PLKSR-tiny (2024/2026) | Restoration | Not reported | 38.11 dB Set5 x2 (Y-channel) | MIT; Drive; BasicSR-based | 450k-iteration protocol infeasible | BasicSR framework | Moderate; non-standard metrics |

### 9.3 Final selection recommendation

**Primary recommendation — StarNet-S2, classification track.** After investigating every alternative, StarNet-S2 is the only candidate combining verified author-trained timm weights, timm-native loading, the lowest explainability cost for the graded algorithm-description requirement, and no external dependency beyond a still-undecided small classification dataset. No new finding this wave weakened that position; two findings (MobileNetV4's reproduction-weight provenance split, EfficientAD's unofficial implementation and auxiliary-image gap) weakened the nearest competitors.

**Conditional runner-up — EfficientAD-S, anomaly track.** If the supervisor prefers an anomaly-detection application story on MVTec AD, EfficientAD-S is the strongest alternative: 1.6M parameters, 98.8% image AUROC, and workstation-grade training speed. Two gates must clear before Stage 02 design: (a) the auxiliary pretraining-image subset must be verified laptop-sized; (b) the supervisor must accept an unofficial community implementation as the codebase.

**Fallback — MobileNetV4-Conv-Small.** Feasibility nearly identical to StarNet-S2; retained as the pilot-failure fallback with the paper-vs-timm accuracy split documented in any report that uses it.

**Not recommended under the deadline:** RepViT (explainability cost plus unresolved parameter accounting), ShiftwiseConv (31M, custom CUDA, Python 3.8), Dinomaly ViT-S (incomplete evidence, heavy setup), PLKSR (non-standard metrics, unreproducible training protocol, framework dependency).

This recommendation is submitted for supervisor decision; it does not authorize installation, downloads, or training.

## 10. Emerging-Candidates Verification: LSNet, RepNeXt, STResNet, Q-Former Autoencoder [Confidence: Medium]

The supervisor then requested verification of the four Stage 01b candidates whose data had been unverified (Section 8.7), asking whether any beats StarNet-S2 and for a complete horizontal comparison across all investigated models. Four parallel deep-research subagents (one per candidate) ran under the primary-sources-only policy; no downloads, installations, or executions occurred. Full per-candidate findings, verbatim table rows, a twelve-item UNSUPPORTED register, and a 24-entry numbered source list are preserved in the Stage 01d file.

### 10.1 Verification outcomes

1. **LSNet (CVPR 2025) — real, and a genuine challenger.** Variants verified from the paper table (Wang, Chen, Lin, Han & Ding, 2025): LSNet-T 11.4M/0.3G/74.9% top-1 (76.1% distilled), LSNet-S 16.1M/0.5G/77.8% (79.0%), LSNet-B 23.2M/1.3G/80.3% (81.6%). Official repo THU-MIG/lsnet, MIT license per the official HuggingFace card, all ImageNet-1k checkpoints on `jameslahm/lsnet` with a documented one-line load: `timm.create_model('hf_hub:jameslahm/lsnet_t', pretrained=True)`. No custom CUDA kernels; 8 GiB fine-tuning is comfortable. Mechanism: large-kernel perception (depthwise K=7) plus small dynamic-kernel aggregation whose mixing weights the perception branch generates — one figure and about two equations to explain, versus StarNet's single `y = f(x) ⊙ g(x)`. **LSNet is the only candidate across Stages 01a-01d that matches StarNet-S2 on practicality while adding 2025 recency and equal-or-better accuracy-per-compute; it is now the formally verified alternative.**
2. **RepNeXt (arXiv 2406.16004) — real; the supervisor's "RepNeXt-M4" is confirmed real** (M4 = 13.3M params, 82.3% top-1, 1.48 ms). Variant family M0-M5 verified. However, it is an unrefereed tech report (arXiv comments field: "Tech report"), the Alibaba affiliation is UNSUPPORTED, there is no timm or HuggingFace card (weights are fused GitHub-release assets requiring repo code to load), and the reported checkpoints were distilled 300 epochs from a RegNetY-16GF teacher. Paper metrics dominate StarNet-S2, but rubric fit (criterion 1 credibility, criterion 3 convenience, criterion 2 explanation length) is worse. Not recommended.
3. **STResNet (arXiv 2601.05364) — real, with corrections.** "STResNet & STYOLO" (Sah & Kumar, 2026-01) is a compact MCU-oriented family made by Tucker-decomposing ResNet-18 with an ILP rank search; the Stage 01b note's "0.95M-3.99M / 58.8%-71.6%" covers only Nano-Tiny — the full family spans Pico-Tiny at 0.60M-3.99M / 48.8%-71.6% — and the paper reports **no FLOPs anywhere**. No code repository, no license, no classification checkpoints, no timm card; preprint only. Not viable: fine-tuning is impossible without weights, and grading criterion 6 (code webpage) cannot be satisfied.
4. **Q-Former Autoencoder (WACV 2026) — real, confirmed as poster #732.** Medical-only anomaly detection (BraTS2021, RESC, RSNA, LiverCT) with a frozen DINOv2 ViT-L/14 backbone and 784 learnable queries; official MIT repo and HuggingFace checkpoints exist, but **no MVTec/VisA/BTAD results**, so there is no head-to-head metric against EfficientAD-S, and the compute (frozen ViT-L/14, 300 epochs, batch 64) far exceeds the 8 GiB / 3-day window. Not viable; citable only as evidence of search breadth under criterion 1.

### 10.2 Complete eleven-candidate comparison

The full comparison table now covers StarNet-S2, MobileNetV4-Conv-S, RepViT-M0.9, ShiftwiseConv SW-Tiny, LSNet-T, LSNet-S, RepNeXt-M1, STResNet-Tiny, EfficientAD-S, Dinomaly ViT-S, and PLKSR-tiny (Q-Former Autoencoder excluded as it has no comparable metric on any track). The table is maintained in the Stage 01d file, Section 6; the headline additions over Section 9.2 are rows 5-8 (LSNet-T/S, RepNeXt-M1, STResNet-Tiny).

### 10.3 Recommendation after Stage 01d

**Primary recommendation unchanged: StarNet-S2.** Three of the four emerging candidates failed practicality outright. The one genuine discovery is LSNet: **StarNet-S2 stays the primary recommendation where the shortest possible algorithm explanation is valued; LSNet-T (or LSNet-S) is the verified alternative where CVPR 2025 recency and the "see large, focus small" narrative are valued.** Both are Stage-02-ready and the final call rests with the supervisor. EfficientAD-S remains the conditional anomaly-track runner-up under its two gates; MobileNetV4-Conv-Small remains the fallback.

This recommendation is submitted for supervisor decision; it does not authorize installation, downloads, or training.



## 11. Final Head-to-Head: StarNet-S2 vs LSNet-T vs LSNet-S [Confidence: High for verified facts; Low for unmeasured feasibility]

On the supervisor's instruction ("no presupposed winner"), a final deep-research pass compared StarNet-S2 with the two LSNet variants assessed **separately**, across local training mechanics, application-data feasibility, design feasibility, and a draft experiment design. 31 sources were retrieved ([41]–[53], [61]–[68], [71]–[80]) and 8 highest-impact claims were re-verified by an independent citation-checking subagent: 7 SUPPORTED verbatim, 1 PARTIAL (LSNet issue #15's sole reply is from a non-maintainer user, not a maintainer; the issue remains open as of 2025-12-10), 0 UNSUPPORTED.

### 11.1 Findings that change the picture

1. **Compute framing corrected.** StarNet-S2's paper Table 6 says "FLOPs (M)" (547M) while its timm card says GMACs 0.5 — consistent only under the multiply-accumulate convention; LSNet's table column is likewise labelled "FLOPs (G)" with no unit footnote (values measured at batch 2048, 224×224). Under that inferred-but-unverified shared convention, StarNet-S2 (0.5 GMACs) and LSNet-S (0.5G) are the same compute class and LSNet-T (0.3G) is ~40% lighter. Reports must not claim StarNet-S2 uses fewer FLOPs than LSNet-T.
2. **Weight provenance is now fully verified for both families.** starnet_s2.in1k card verbatim: "Trained on ImageNet-1k by paper authors", apache-2.0, 3.7M, GMACs 0.5, 224×224; official repo ma-xu/Rewrite-the-Stars ("[CVPR 2024] Rewrite the Stars", Apache-2.0 sidebar, checkpoints but no training scripts). lsnet_t card verbatim: License "mit", load line `timm.create_model("hf_hub:jameslahm/lsnet_t", pretrained=True)`, 11.4M / Top-1 74.9/76.1* / 0.3G / throughput 14708; card enumerates variants t/t_distill/s/s_distill/b/b_distill.
3. **EuroSAT is the only fully verified dataset option** (MIT license; 27,000 labeled images / 10 classes; authors' own quote "overall classification accuracy of 98.57%", Helber et al., IEEE J-STARS 2019). Sizes/licenses for CIFAR-10/100, Flowers-102, Pet, Food-101, STL-10 remain UNSUPPORTED; torchvision docs list no sizes or licenses (negative result). No fine-tuned accuracy numbers for any of the three models on any candidate dataset exist in retrieved literature.
4. **Training protocol anchors verified.** timm `train.py`/`validate.py` ship in the repo root, not the pip package; native AMP default ≥0.4.3; official docs contain only ImageNet-scale recipes; the official PyTorch transfer-learning tutorial protocol (resnet18, SGD lr=0.001 momentum=0.9, StepLR(7, 0.1), 25 epochs, batch 4, RandomResizedCrop(224)+RandomHorizontalFlip, val acc 0.9346 finetuning / 0.9477 feature-extraction) was verified verbatim and adopted as the citable protocol skeleton.

### 11.2 Separate verdicts

- **StarNet-S2** — 3.7M params, 0.5 GMACs / 547M paper FLOPs, 74.8% top-1. Strongest on: footprint, provenance, one-equation explainability for grading criterion 2, no community red flags, lowest estimated memory risk. Weakness: 2024 recency; FLOPs-branding caveat must be worded carefully.
- **LSNet-S** — 16.1M params, 0.5G, 77.8% (79.0% distilled). Legitimate alternative: best paper accuracy at equal compute class, identical timm path, CVPR 2025 recency. Costs: 4.3× the parameters of StarNet-S2, open issue #15 exposure, dynamic-kernel training-memory estimate (UNSUPPORTED), multi-concept explanation, non-replicable distillation edge.
- **LSNet-T** — 11.4M params, 0.3G, 74.9% (76.1% distilled). Weakest fit for this rubric: its unique advantages (lowest FLOPs, throughput 14708 img/s on the card) yield only +0.1 top-1 over StarNet-S2 while tripling parameters and sharing every LSNet-family risk. Dominated by StarNet-S2 (simpler, equal accuracy) and LSNet-S (more accurate, same code effort); choose only if the lowest-FLOPs 2025 model is explicitly desired.

### 11.3 Recommendation after the final head-to-head

**Primary — StarNet-S2; alternative — LSNet-S (gates: open issue #15 exposure and 8-GiB memory risk accepted); not recommended for this rubric — LSNet-T.** The draft experiment design (identical-protocol three-way fine-tuning, EuroSAT primary, timm `train.py` with the tutorial-verified SGD/momentum/StepLR/25-epoch protocol, Grad-CAM via target-layer paths) is contained in the final report's Section 5 and awaits Stage 02 approval. Full report: `DEEP_RESEARCH_STARNET_VS_LSNET_FINAL.md` (TL;DR, evidence by area with confidence labels, separate T/S verdicts, red-team assessment, draft design, APA 7 bibliography with verified PDF links, tier-tagged source extracts).

This recommendation is submitted for supervisor decision; it does not authorize installation, downloads, or training.



## Artifact Locations and Approval State

All Stage 1 files and updated persistent records are listed with full paths. The first eight rows are new Stage 1 deliverables; the dialogue and memory rows point to existing records updated during this stage.

| Artifact | Full absolute path |
| --- | --- |
| English research report | `D:\claude\workspace\CISC3024 AI Assignment 1\DEEP_RESEARCH_MODEL_SELECTION.md` |
| Word working report | `D:\claude\workspace\CISC3024 AI Assignment 1\research_records\stage_01_model_selection.docx` |
| Search protocol and exact retrieval briefs | `D:\claude\workspace\CISC3024 AI Assignment 1\research_records\stage_01_search_protocol.md` |
| Classification retrieval evidence | `D:\claude\workspace\CISC3024 AI Assignment 1\research_records\stage_01_retrieval_classification.md` |
| Autoencoder/anomaly retrieval evidence | `D:\claude\workspace\CISC3024 AI Assignment 1\research_records\stage_01_retrieval_anomaly.md` |
| Restoration retrieval and withdrawn-claim history | `D:\claude\workspace\CISC3024 AI Assignment 1\research_records\stage_01_retrieval_restoration.md` |
| Machine-readable screening ledger | `D:\claude\workspace\CISC3024 AI Assignment 1\research_records\stage_01_screening_ledger.csv` |
| Independent claim-verification register | `D:\claude\workspace\CISC3024 AI Assignment 1\research_records\stage_01_verification.md` |
| ShiftwiseConv supplementary investigation | `D:\claude\workspace\CISC3024 AI Assignment 1\research_records\stage_01b_shiftwiseconv_investigation.md` |
| Horizontal comparison and 26-source list (Stage 01c) | `D:\claude\workspace\CISC3024 AI Assignment 1\research_records\stage_01c_candidate_comparison.md` |
| Emerging-candidates verification and 11-candidate comparison (Stage 01d) | `D:\claude\workspace\CISC3024 AI Assignment 1\research_records\stage_01d_emerging_candidates.md` |
| Final head-to-head report: StarNet-S2 vs LSNet-T vs LSNet-S with draft experiment design | `D:\claude\workspace\CISC3024 AI Assignment 1\DEEP_RESEARCH_STARNET_VS_LSNET_FINAL.md` |
| Finalized Stage 02 experiment design (StarNet-S2 on EuroSAT) | `D:\claude\workspace\CISC3024 AI Assignment 1\research_records\stage_02_experiment_design.md` |
| Durable supervision guidance | `C:\Users\weixiong\.qoder\projects\D--claude-workspace-CISC3024-AI-Assignment-1\memory\research-supervision.md` |

Supervisor approvals received: the research workflow, installation/use of deep-research, permission to consider fine-tuning, and — on 2026-09-18 — model selection (**StarNet-S2**), dataset selection (**EuroSAT**), and entering Stage 02 (algorithm/experiment design). The Stage 02 design is complete at `research_records\stage_02_experiment_design.md`; it narrows the draft three-way comparison to the approved single-model scope and defines gated execution requests G1 (install dependencies) / G2 (download EuroSAT + checkpoint) / G3 (pilot run) / G4 (full run), all **pending**. Also pending/unapproved: each of G1–G4 individually, scale-up reviews, HTML visualization, final-report outline, and source publication.
