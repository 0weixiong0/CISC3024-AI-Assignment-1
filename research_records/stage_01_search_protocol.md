# Stage 01 — Literature Search Protocol and Decision Rules

Date: 2026-09-18

Status: Protocol established before retrieval results. This is not a completed literature review or an approved implementation plan.

## Supervisor decision

U003: "Fine-tuning is allowed." Official pretrained weights may therefore be considered in candidate selection. This permission does not select a model, approve a dataset, authorize a download, or waive later design and scale-up reviews. The original Chinese response and its translation are in the dialogue archive.

## Research question

Which recent deep CNN or deep autoencoder offers the strongest defensible combination of practical computer-vision/pattern-recognition relevance, local feasibility, implementation clarity, novelty, and assignment-requirement coverage when official pretrained fine-tuning is allowed and the work must finish before 2026-09-21?

## Known constraints

- Authoritative task: a recent deep CNN or deep autoencoder, AI-led searching/programming/reporting, detailed process evidence, six required report components, and a source-code webpage link.
- Local resources previously verified: RTX 4060 Laptop GPU with approximately 8 GiB VRAM; approximately 32 GiB RAM; i9-13900H; approximately 59 GiB free workspace storage; Python 3.12.10 and PyTorch 2.7.1+cu128. CUDA smoke testing succeeded, but no candidate has been benchmarked locally.
- The local GitHub CLI was not found in PATH. GitHub inspection must use the required GitHub tool route; if unavailable, use paper/official non-GitHub evidence and explicitly leave repository internals unverified rather than claim a code audit.
- Research communication is Chinese; research artifacts and code are English. The dialogue archive retains original Chinese as evidence alongside full translations.
- No dataset, model weight, additional dependency, cloud job, or remote publication during literature screening. Web research reads public evidence only.

## Depth and coverage

Standard research depth, using three independent retrieval agents and a later citation-verification agent. Target approximately 20–30 distinct papers at initial screening, 6–8 closer inspections when available, and 3–4 final candidates. These are targets, not counts already achieved. A paper and its author repository are not two independent studies; mirrors are deduplicated.

The main search window is 2024–2026 through 2026-09-18. Older foundational methods may appear as baselines or rejection examples, but must not inflate the count of recent eligible candidates. A claimed 2026 publication is not automatically usable: its release date, paper availability, code/weights, and reproducibility must be checked. No exhaustive or PRISMA-compliant systematic-review claim will be made.

## Key areas and subquestions

### 1. Compact CNNs for classification and transfer learning

What constitutes the new convolutional contribution? Which exact small variant is documented? Are usable official weights available? Can a manageable dataset support meaningful transfer experiments without compromising novelty?

### 2. Autoencoder-based anomaly detection

Is the proposed method genuinely a deep autoencoder or CNN rather than a feature-memory pipeline alone? What is pretrained versus learned on the target dataset? Are local/global anomaly maps interpretable? What data splits and metrics avoid leakage?

### 3. Compact CNN image restoration

Is the core computation convolutional rather than transformer/Mamba-only? Is the pretrained task aligned with an affordable experiment? Are degradation, image scale, crop, channel, and metric protocols clear? Does training require custom operators or full-resolution resources beyond the local budget?

### 4. Hardware and dependency feasibility

What do reported parameters and MACs mean at the stated resolution? Which operations, libraries, or checkpoint sources are required? Which costs are author measurements versus local estimates? What must be measured in an approved pilot before making a feasibility claim?

### 5. Evidence quality and reproducibility

Is the source a proceedings paper, preprint, official documentation, or derivative summary? Were full sections inspected or only an abstract/snippet? Is publication status corroborated? Are code, weights, dataset licensing, and actual training instructions confirmed or merely claimed?

### 6. Assignment fit and decision value

Can the algorithm be explained precisely, with defensible adaptation boundaries? Can AI implementation and correction steps be documented? Will experiments support comparative evidence rather than a visual demo alone? Is the novelty worth the uncertainty under the deadline?

## Planned query vocabulary

These are planned starting terms, not a record of queries actually executed. Actual queries returned by the agents will be retained in the stage report/source ledger.

1. efficient convolutional neural network classification 2026 pretrained
2. MobileNetV4 convolutional 2024 official small parameters
3. RepViT StarNet 2024 convolutional ImageNet pretrained
4. lightweight CNN 2025 2026 reproduction limitations
5. autoencoder visual anomaly detection 2026 official implementation
6. EfficientAD 2024 autoencoder training memory
7. RealNet 2024 anomaly feature reconstruction pretrained
8. reconstruction anomaly detection 2025 2026 leakage evaluation
9. efficient CNN image restoration 2026 pretrained
10. convolutional image super resolution 2024 2025 lightweight
11. CNN restoration 2025 2026 custom CUDA reproduction
12. super resolution PSNR SSIM benchmark protocol limitations

## Agent allocation and retrieval records

Agent A covers compact classification CNNs; source identifiers begin A01. Agent B covers anomaly-detection/autoencoder methods; identifiers begin B01. Agent C covers compact restoration CNNs; identifiers begin C01. Each agent receives the same hardware, deadline, fine-tuning permission, approval boundaries, and source-verification requirements.

Each agent is asked to return actual search queries, a paper screening ledger, evidence for top candidates, critical limitations, and source metadata. Per-agent budget: at most eight web searches and five page fetches, with limited approved-route GitHub inspection if available. Initial abstracts and closer section reads must be distinguished. Agents must not edit project files; the lead agent retains responsibility for the merged report and decisions.

## Evidence coding and verification

- Tier 1: primary papers or official technical documentation. Label preprints as preprints, not as peer reviewed.
- Tier 2: reputable engineering analyses or independent implementations with identifiable provenance.
- Tier 3: derivative, marketing, anonymous, or discussion sources; use only for discovery/context.
- Evidence depth: snippet, abstract, selected full-paper sections, full paper, or code inspected. Never label abstract-only screening as a full-paper review.
- Confidence: distinguish factual support from practical transferability. Exact model statistics may be supported by one authoritative paper, while local runtime remains unmeasured.
- Record source URLs as returned by tools; never invent bibliographic details or fabricate access to a repository.
- Verify 5–10 conclusion-driving claims through a separate agent. Correct or remove unsupported numbers and state remaining gaps.

An author's paper and code can jointly establish provenance but do not establish independent replication. Confidence labels will not be upgraded by counting copies of the same underlying claim. Existence of pretrained weights does not establish compatibility with the intended environment or a permitted license.

## Candidate evaluation

The five supervisor-requested dimensions will be scored on a 1–5 desirability scale: lower architectural complexity, lower hardware burden, easier implementation, stronger novelty, and stronger coverage of documented assignment requirements. Suggested weights are 15%, 25%, 25%, 20%, and 15%, respectively, reflecting the short deadline. These are explicit researcher judgments, not a course marking rubric, benchmark, or promised grade. Show component scores so the supervisor can disagree with the weighting.

Use an eligibility screen before scoring: credible recent source, clear deep-CNN/deep-autoencoder fit, genuine CV/PR application, a plausible local experiment, and no unresolved requirement that makes the model impractical within the remaining window. A higher novelty score must not conceal inaccessible weights, custom compilation, or ambiguous architecture fit.

Model size and author-reported inference speed must not be presented as training VRAM or local runtime measurements. Any hours suggested for a later experiment remain provisional until a pilot measures throughput, peak allocation, and validation behavior.

## Expected deliverables and stopping point

The final stage package will contain an English citation-backed comparison report, a machine-readable screened-paper ledger if sufficient structured evidence is returned, a Word working copy, and the updated bilingual dialogue archive. The supervisor receives a concise Chinese candidate table and recommendation.

Stop at model approval. No algorithm implementation, dataset acquisition, checkpoint download, final experiment split, or training is authorized by completion of this literature stage.

## Incremental issues and decisions

- Confirmed: official pretrained fine-tuning is permitted.
- Open: exact selected model and variant; all model/design approvals remain pending.
- Known limitation: GitHub CLI availability may restrict direct code/license verification.
- Reporting guardrail: this stage is a bounded, traceable screening exercise, not an exhaustive survey of every publication available through the date cutoff.

## Local dependency inventory

Read-only installed-package metadata was queried during retrieval. This did not import or instantiate candidate models and is not a dependency compatibility test.

| Package | Installed version |
| --- | --- |
| torch | 2.7.1+cu128 |
| torchvision | 0.22.1+cu128 |
| numpy | 2.4.6 |
| Pillow | 12.2.0 |
| scipy | 1.17.1 |
| scikit-learn | 1.9.0 |
| matplotlib | 3.11.0 |
| pandas | 3.0.3 |
| PyYAML | 6.0.3 |
| python-docx | 1.2.0 |
| timm, tensorboard, wandb, lightning, anomalib | Not installed in the inspected interpreter |

A model reported as available in timm or anomalib will therefore still require an approved dependency decision or an explicitly scoped independent implementation. No package was installed or upgraded during this check.

## Appendix: delegated retrieval prompts

These are assistant-authored research delegation prompts, not statements made by the supervisor. They are retained to document how AI organized the search. Their candidate names are search leads, not verified findings.

### Agent A — Exact prompt

Research only; do not implement, install, download model weights/datasets, publish, or edit project files. We are preparing a supervised CISC3024 Pattern Recognition AI assignment. Need a recent deep CNN or deep autoencoder with actual CV/PR application. Today 2026-09-18; exclude future material. Supervisor permits pretrained fine-tuning but must approve model before design/implementation. Hardware RTX4060 Laptop ~8GiB VRAM, i9-13900H,32GiB RAM,~59GiB free disk, PyTorch2.7.1cu128/Python3.12.10; deadline before Sep21. Your assigned area is compact CNNs for classification/transfer learning, MAINLY 2024-2026. Other agents cover anomaly autoencoders and image restoration so do not duplicate those. Search 8-12 distinct relevant papers; authoritatively inspect top 3-4. Potential starting leads, not facts: MobileNetV4, MobileNetV5 if actually published by cutoff, RepViT, StarNet/Rewrite the Stars, MogaNet, newer RepNeXt/RepCNN. Include rejection of transformer-only/hardware-inappropriate cases, and older baselines identified as such. Use primary venue proceedings, papers, author repos and official timm model docs. Budget max8 WebSearch+5 WebFetch, plus limited Bash gh for GitHub (must use gh; if unavailable use other primary sources and record inability). Never fabricate sources or metrics, distinguish arxiv preprint from peer review, no copied-paper quotes over25 words/source. Return <=2400 English words: (1) exact queries and retrieval coverage; (2) 8-12 row screening ledger with title/year/venue/type/URL/retain-or-exclude reason; (3) top candidate evidence with parameter/MAC/image-size values (variant exact), official weight/code/license verification state, required dependencies, possible small dataset (~Oxford Flowers102/Oxford Pets alternatives) and honest inference on feasibility not measured runtime; (4) critical failure/leakage/reproduction pitfalls; (5) sources author/title/date URL with Tier1/2/3 and access2026-09-18; assign source IDs A01... Clearly tag abstracts vs full-paper sections vs code actually read. Paper and same authors' repo are NOT independent confirmation. Scope conservative score as requirement coverage not predicted grade. Report precise known vs unknown.

### Agent B — Exact prompt

Research only; no implementation, file edits, installation, or model/dataset downloads. We need recent deep CNN or deep autoencoder candidates for CV/Pattern Recognition assignment, primarily2024-2026 through2026-09-18. Human permits official pretrained-weight fine-tuning, must approve model/design separately. Hardware RTX4060Laptop~8GiB,32GiBRAM,59GiB free disk, PyTorch2.7.1cu128/Python3.12; finish before2026-09-21. Your area: reconstruction/autoencoder-based industrial or visual anomaly detection and practical deep autoencoder methods. Other agents cover classification CNNs and restoration CNNs; keep focus here. Identify7-10 distinct screened papers and inspect top2-3 with primary evidence. Leads only, verify: EfficientAD(WACV2024?), RealNet(CVPR2024?), Dinomaly(CVPR2025?), newer 2025/2026 reconstruction approaches. Older DRAEM/DSR/reverse distillation allowed only clearly-labelled foundations, not inflate recency. Is the architecture truly a deep CNN/autoencoder or does it just use pretrained features without a qualifying new network? Explicitly evaluate algorithm-fit ambiguity, pretrained ImageNet feature teacher versus fully trained anomaly model, single-category or reduced training adaptation vs claimed faithful reproduction. Obtain exact variant parameters/compute if published, teacher/student/autoencoder objectives, official code/weights/license state and accessible dataset size and licenses (MVTecAD vs VisA; do not download), hardware obstacles e.g customCUDA/largeViT. Important critical sources: benchmark leakage, official test thresholds, AUROC/pixel metrics, split constraints. Budget max8WebSearch+5WebFetch; use gh Bash for GitHub and record if gh unavailable. Do not bypass GitHub tool rule via WebFetch. Return <=2400 English words: queries; 7-10-row screened-paper ledger title/year/venue/type/sourceURL/scope decision; 2-3 best candidates evidence; possible experiment scope and risks without inventing measured runtime; source IDs B01... with title/authors/date/access2026-09-18/Tier1/2/3 and snippets-vs-abstract-vs-full-sections distinction. Preserve publication status correctly: arxiv not inherently peer reviewed; official author claims not independent replication. No direct quotes >25words/source.

### Agent C — Exact prompt

Research only, do not write/edit files, install, train, download datasets/weights, or publish. We need recent2024-2026 deepCNN/deepautoencoder for practical CV/Pattern Recognition course assignment as of2026-09-18; allowed official pretrained-weight fine-tuning; model selection & implementation plan require human approval. RTX4060Laptop8GiB,32GiBRAM,59GiBdisk,Python3.12,PyTorch2.7.1cu128; deadline beforeSep21. Assigned area: compact CNN image denoising/deblurring/super-resolution or genuinely CNN encoder-decoder restoration with clear evaluation and visualization. Other agents cover classification CNN and industrial anomaly AE so avoid overlap. Screen7-10 distinct papers primarily2024-26; identify top2-3 feasible recent methods, plus foundational NAFNet/ECCV2022 only as older baseline if relevant. Seek true efficient CNN alternatives, not transformer/Mamba-only just labeled AE without evidence. Consider image superresolution compact 2024/2025 challenge networks (RFDN2020 foundation, RLFN2022 foundation, newer RHA/RHA-Net? verify rather than assume) and Rep/LargeKernel CNN restoration; include negative findings if limited quality. Need official paper/venue/author implementation, pretrained checkpoint availability/license state, actual params/MACs at specified resolution, dependencies/customops, dataset download size and degradation pipeline, benchmark split compatibility, perceptual/PSNR/SSIM evaluation. Risk: training on benchmark test, performance not comparable across scales/crops/colorchannels, tiling artifacts, native CUDA build problem. Budget max8WebSearch+5WebFetch; gh for GitHub (may unavailable) no WebFetch GitHub. Return <=2400 English words: exactqueries;7-10 row ledger with title/year/venue/type/URL/include-exclude reason; top2-3 candidate evidence and estimated feasibility explicitly not measured; critical comparisons; source IDs C01... metadata/Tier/access2026-09-18 and evidence depth labels. Primary sources highest priority. Do not invent metric or publication status; arxiv≠peerreview. Direct quotes<=25words/source.
