# Deep Research Report: StarNet-S2 vs LSNet-T vs LSNet-S — Final Model Selection Evidence for CISC3024 Assignment 1

**Date:** 2026-09-18
**Depth:** standard (1 retrieval subagent Wave 1 + 2 gap-fill subagents Wave 2 + 1 verification subagent Phase 3.1)
**Status:** Research only — this report authorizes no downloads, installations, or training. All decisions remain subject to supervisor approval.
**Companion files:** `DEEP_RESEARCH_MODEL_SELECTION.md` (overall selection history), `research_records/stage_01d_emerging_candidates.md` (Stage 01d verification), `research_records/conversation_log.md` (bilingual log).

---

## TL;DR

Three candidates — StarNet-S2 (CVPR 2024) and the two LSNet variants LSNet-T and LSNet-S (CVPR 2025) — were compared with **no winner presupposed**, across local training mechanics, application-data feasibility, design feasibility, and a draft experiment design. After 31 retrieved sources and a citation-verification pass (8 claims: 7 SUPPORTED, 1 PARTIAL, 0 UNSUPPORTED), the evidence supports:

- **StarNet-S2 — primary recommendation.** Smallest (3.7M params), author-trained Apache-2.0 weights in native timm, single-equation explainability, and no unresolved reproducibility issues. Strongest fit for the assignment's grading criteria on an 8 GiB / 3-day budget.
- **LSNet-S — legitimate alternative** if the supervisor prioritizes CVPR 2025 recency and the best paper accuracy (77.8% top-1, 79.0% distilled). Costs: 16.1M params, exposure to an open reproducibility issue, higher estimated training memory, and a more complex mechanism to explain.
- **LSNet-T — weakest fit for this rubric.** Its unique advantages (lowest FLOPs at 0.3G, card throughput 14,708 img/s) do not translate into an accuracy advantage over StarNet-S2 (74.9% vs 74.8%), while it triples the parameter count, shares every LSNet risk, and shares the recency advantage with LSNet-S anyway.
- **Draft experiment design included** (Section 5): identical-protocol fine-tuning of all three on one small dataset, EuroSAT as the evidence-backed primary dataset (MIT-verified license, published 98.57% benchmark target), with a timm-native training protocol.

The choice between StarNet-S2 and LSNet-S is a genuine trade-off (simplicity/risk vs recency/accuracy) and is submitted for supervisor decision.

---

## 1. Executive Summary

This report closes the model-selection investigation requested by the supervisor. Previous stages (Stage 01, 01b, 01c, 01d) had narrowed eleven candidates down to StarNet-S2 and the LSNet family as the only practically viable options. This stage was explicitly commissioned to be **neutral**: the retrieval agent was instructed not to presuppose a winner, to evaluate local training mechanics, real application-data feasibility, and design feasibility, and to produce a draft experiment design. LSNet-T and LSNet-S were to be assessed **separately**, not as one family.

The evidence base comprises 31 sources ([41]–[53], [61]–[68], [71]–[80]), including both primary papers (re-verified this run against arXiv full text), official model cards, official repositories and issues, official dataset pages, and the official PyTorch transfer-learning tutorial. A Phase 3.1 verification subagent re-fetched the 8 highest-impact claims; 7 were SUPPORTED verbatim and 1 (the characterization of LSNet issue #15) required a wording correction, which is incorporated below.

Three findings materially shape the final comparison:

1. **The FLOPs picture is different from what the paper numbers alone suggest.** StarNet-S2's paper reports 547M "FLOPs (M)" (Table 6) while its timm card reports 0.5 GMACs — a pairing consistent only if the paper's "FLOPs" label uses the multiply-accumulate (MAC) convention common in the field. LSNet's table column is likewise labelled "FLOPs (G)" with no unit footnote. Under that (inferred, unverified) common convention, **StarNet-S2 (0.5 GMACs) and LSNet-S (0.5G) are the same compute class; LSNet-T (0.3G) is roughly 40% lighter**. The exact unit convention remains UNSUPPORTED and is flagged wherever compute is compared.
2. **The only verified small-dataset option is EuroSAT.** Its official repository states an MIT license, 27,000 labeled images in 10 classes, and — in the authors' first-person sentence — "With the proposed novel dataset, we achieved an overall classification accuracy of 98.57%" (Helber et al., IEEE J-STARS 2019). Download sizes and licenses for CIFAR-10/100, Flowers-102, Oxford-IIIT Pet, Food-101, and STL-10 remain UNSUPPORTED after two retrieval waves and must be recorded empirically at download time.
3. **No published head-to-head or fine-tuned baseline exists for any of the three candidates.** No paper or blog compares StarNet-S2 against LSNet directly, no formal critique of the star operation was found (only derivative adoptions [50][51][52]), and no source provides fine-tuned accuracy for these backbones on any candidate dataset. The draft experiment design therefore generates our own comparison numbers under an identical protocol — which also serves grading criterion 4 (experiment settings and results) directly.

---

## 2. Methodology

- **Pipeline:** deep-research skill, standard depth. Phase 0 clarification had been completed in the prior session; the supervisor explicitly ordered the launch. One retrieval subagent (Wave 1, areas A–E, sources [41]–[53]) and two gap-fill subagents (Wave 2: model-side [61]–[68], data-side [71]–[80]) ran in sequence with merge and triangulation after each wave. One verification subagent (Phase 3.1, ≤10 fetches) re-checked 8 claims.
- **Verification results:** Claims verified SUPPORTED: starnet_s2.in1k card facts (verbatim "Trained on ImageNet-1k by paper authors", apache-2.0, 3.7M, GMACs 0.5, 224×224, Original link); LSNet paper table values (T: 11.4M/0.3G/74.9% → 76.1% distilled; S: 16.1M/0.5G/77.8% → 79.0% distilled; batch 2048, 224×224; column header "FLOPs (G)"); StarNet paper Table 6 ("FLOPs (M)"; S2: 3.7M/547M/74.8%; family context S1 425M/73.5%, S3 757M/77.3%, S4 1075M/78.4%); official StarNet repo ("[CVPR 2024] Rewrite the Stars", sidebar Apache License 2.0, checkpoint section but no training scripts); LSNet_t HF card (License "mit"; verbatim load line `model = timm.create_model("hf_hub:jameslahm/lsnet_t", pretrained=True)`; card also lists variants `t/t_distill/s/s_distill/b/b_distill`); EuroSAT (MIT; 27,000 labeled images; 98.57% quote); PyTorch tutorial (resnet18 IMAGENET1K_V1, Hymenoptera, SGD lr=0.001 momentum=0.9, StepLR(7, 0.1), 25 epochs, batch 4, RandomResizedCrop(224)+RandomHorizontalFlip, val acc 0.9346 finetuning / 0.9477 feature extraction). PARTIAL: LSNet issue #15 — opened 2025-09-24 by user Raven-Z-china ("有人成功复现了吗？我用一张3090跑不出论文的结果"); the single reply (2025-12-10) is from **another user (Daylawrence), not a maintainer**, and offers no fix or hyperparameters; the issue is **still open**. Corrected wording used throughout this report.
- **Known retrieval failures:** the CVF PDF URL for LSNet returned 404 to the fetcher (possibly bot-blocking), so LSNet table values were verified against arXiv:2503.23135 full text instead; the CVF proceedings entry remains the formal citation of record. The `lsnet_s` HF card body was not fetched this run (its existence is verified by the Stage 01d investigation and by the `lsnet_t` card's variant list) — marked as such.
- **Confidence labels** follow the skill's rules (source count × credibility tier). Absence-of-evidence findings are capped at [Low]/[Medium].

---

## 3. Evidence by Key Area

### Area A — Local training mechanics [High]

All three models load through one identical mechanism: `timm.create_model(<name>, pretrained=True)`. StarNet-S2 uses the native card `starnet_s2.in1k`; LSNet-T/S use hub cards `hf_hub:jameslahm/lsnet_t` / `lsnet_s`. This was verified verbatim for both card families this run ([62], [67]). The training vehicle is timm's `train.py`/`validate.py`, which "ship in the github root folder" and "are not currently packaged in the pip release" [41] — so the pilot will need the timm repository (not just the pip package). Native AMP is the default since timm 0.4.3 [41]; an independent research codebase (MadryLab's timm-bench) reuses `train.py` as-is, confirming it is the standard fine-tuning vehicle [45].

Official timm documentation provides **only ImageNet-scale recipes** (150–600 epochs, 2–8 GPUs, cosine + warmup, `--aa rand-m9-mstd0.5`, random erasing) [41] — there is no small-dataset fine-tune recipe in official docs. The strongest community example is timm.fast.ai's, which trains on imagenette2-320 (a 10-class ~10k-image ImageNet subset) with `epochs=200, lr=0.01, opt='sgd'` [64] — a long-schedule from-pretrained example, not a 3-day-budget protocol. Any shorter schedule we adopt is therefore **our own engineering choice, documented as such**, not sourced guidance.

**Per-model mechanics differences are small.** Both families are pure-timm, no custom CUDA, no Python-version conflicts (unlike ShiftwiseConv, rejected in Stage 01b). One asymmetry matters: LSNet's SKA module generates per-sample dynamic kernel weights at runtime, which plausibly increases activation memory during training relative to a static-kernel CNN of equal parameter count. This is a **reasoned engineering estimate, UNSUPPORTED** — no source quantifies training memory for either family. The official StarNet repository offers pretrained checkpoints but no training scripts [61, verified]; neither repo documents small-dataset fine-tuning.

### Area B — Application-data feasibility [High for EuroSAT; Low elsewhere]

Dataset candidates were screened against the assignment's constraints (8 GiB VRAM, 3-day deadline, single-GPU laptop):

- **EuroSAT — the only fully verified option.** MIT license [73], 27,000 labeled Sentinel-2 patches in 10 classes [73], published benchmark "overall classification accuracy of 98.57%" from the dataset paper itself [73][47]. 64×64 patches, typically upscaled to 224 for pretrained backbones. Advantages for grading criterion 4: a published reference number to compare against, a domain shift from ImageNet (satellite imagery) that strengthens the "what you have learnt" section, and small size for fast epochs. Download size in MB not quoted anywhere retrieved — record empirically.
- **CIFAR-10 / CIFAR-100** [74]: canonical, universal, tiny; license terms and exact sizes UNSUPPORTED this run (the canonical Toronto page was confirmed live but its text was not captured). 32×32 → 224 upscaling is a 7× resize, the most aggressive of the candidates. CIFAR-10-style training is demonstrably fast on a single GPU — "94% on CIFAR-10 in 3.29 Seconds on a Single GPU" — though that is a from-scratch ResNet9 at 96px, not fine-tuning, so it bounds only the lower limit of difficulty [46].
- **Oxford 102 Flowers** [75][80]: fine-grained, small (~8k images commonly stated, UNSUPPORTED), a classic transfer-learning benchmark with a good report narrative; the customary research-use license statement was not captured — UNSUPPORTED.
- **Deprioritized:** Oxford-IIIT Pet (viable but least distinctive), Food-101 (~5 GB commonly stated, UNSUPPORTED — heavy for 3 days), STL-10 (semi-supervised design mismatch), Caltech-101 (licensing/retrieval friction, UNSUPPORTED), Imagenette (ImageNet subset — weak "new domain" story).

The torchvision datasets documentation lists **no download sizes and no license statements** [71] — a negative result that closes the "cite torchvision for sizes" route. Sizes and licenses (except EuroSAT MIT) must be recorded empirically at download time. Fine-tuned accuracy references for CIFAR-100, Flowers-102, and Pet with these backbones were **not found** in two retrieval waves — searches surfaced only leaderboard pages and project repos whose snippets did not expose exact figures [76][77][78][79]. No accuracy expectation for any dataset other than EuroSAT's 98.57% can therefore be stated.

### Area C — Design feasibility (implementation, licensing, explainability) [High]

- **Implementation risk: effectively zero-difference.** Both families load with one timm line and run through `train.py`/`validate.py` [41][62][67]. No custom compilation, no Python pinning, no framework lock-in (unlike PLKSR/BasicSR or ShiftwiseConv/shiftadd, rejected earlier).
- **License position: verified permissive for both.** StarNet: repo sidebar Apache License 2.0 (verified this run) and timm card apache-2.0 [61][62]. LSNet: HF card License "mit" for lsnet_t (verified this run) [67]; MIT per Stage 01d for the family. Either choice is publishable in a student repo (grading criterion 6) subject to dataset licensing.
- **Explainability — the largest qualitative differentiator.** StarNet's mechanism is one equation, y = f(x) ⊙ g(x), plus a two-branch diagram; the paper's Table 6 family (S1 425M → S4 1075M FLOPs) also gives a clean scaling story. LSNet requires explaining two cooperating components (LKP large-kernel perception + SKA small-kernel aggregation with runtime weight generation), plus the distillation variants — a multi-concept explanation. For grading criterion 2 (algorithm description) this favors StarNet-S2 on effort and error surface.
- **Interpretability tooling.** pytorch-grad-cam supports models via explicit target-layer specification (e.g., ViT `model.blocks[-1].norm1`); the README does not literally mention timm, so the correct report wording is "target layers are set by module path," supported by the maintainer-assisted discussion #380 concerning the timm model `volo_d2_224` [65][66]. This applies equally to both families.
- **Weight provenance parity.** Both models ship author-trained checkpoints: StarNet-S2's card states "Trained on ImageNet-1k by paper authors" [62]; the LSNet cards are published by jameslahm (the first author's handle) [67]. Neither family depends on third-party reproductions (unlike MobileNetV4-Conv-S, Stage 01c).

### Area D — Counter-evidence and red team [Medium overall; individual findings labeled]

1. **LSNet issue #15 (still open, [Medium]).** A user reported on 2025-09-24 failing to reproduce LSNet's paper results on an RTX 3090; the only reply (2025-12-10, from a non-maintainer user) offers no fix or hyperparameters [43, verified]. This is *not* proof of a defect — it may be user error — but it is the only concrete negative data point in either community and it sits exactly in our hardware class (consumer GPU).
2. **StarNet's efficiency branding vs its FLOPs (needs careful wording, [Low]).** StarNet-S2's 547M "FLOPs" exceeds LSNet-T's 0.3G under both papers' (likely shared, unverified) MACs-as-FLOPs convention. The paper's claim is about the *quality* of compute spent (the star operation's representational efficiency per FLOP), not minimal FLOPs. A report comparing the models must present both papers' numbers with their stated units and the timm GMACs cross-check, and must not claim StarNet is "fewer FLOPs" than LSNet-T.
3. **Distillation cannot be replicated ([High] as a fact of the checkpoints).** LSNet's headline +1.2/+1.2 point edges (76.1%/79.0%) come from distillation variants. We will fine-tune from the standard (non-distill) checkpoints, so 74.9%/77.8% are the honest reference numbers. (The `*_distill` checkpoints do exist on HF and could serve as an optional appendix arm if the supervisor wants them [67].)
4. **No critique / no head-to-head exists ([Low] — absence finding).** Indexed literature retrieved this run contains only derivative StarNet adoptions (YOLOv8-StarNet [50], YOLO-Starfish [51], StarNet-RiceSeg [52]) and no formal critique of the star operation; no direct StarNet-vs-LSNet comparison exists anywhere retrieved. Both models therefore stand on their own papers' evidence plus our own pilot.
5. **Small-dataset transfer behavior is unknown for both ([Low] — the core residual uncertainty).** Neither paper fine-tunes on small datasets; no retrieved source does. The pilot experiment (Section 5) is the only way to close this gap — which is also precisely what grading criterion 4 rewards.

---

## 4. Per-Candidate Verdicts (LSNet-T and LSNet-S assessed separately)

### 4.1 StarNet-S2 (CVPR 2024)

**Evidence for:**
1. Smallest of the three: 3.7M params; 0.5 GMACs (timm card) / 547M FLOPs (paper, Table 6), 74.8% top-1 — all verified verbatim this run [3-verify][62].
2. Cleanest weight provenance and loading: author-trained native timm card, Apache-2.0 on both repo (sidebar) and card [61][62]; one-line load.
3. Lowest explanation cost for criterion 2: one equation (y = f(x) ⊙ g(x)), one diagram, one scaling table.
4. No unresolved reproducibility issues found in its community (issue search surfaced only a pretrained-checkpoint availability question, #8 [68]); the only concrete negative in the LSNet community (issue #15, open since 2025-09-24) has no StarNet counterpart.
5. Lowest estimated training-memory risk on 8 GiB: fewest params, static kernels (memory reasoning UNSUPPORTED, flagged as estimate).
6. Community adoption exists and is growing [50][51][52] — neutral-to-positive transfer evidence.
7. End-to-end verified evidence trail this run: paper table, official repo, official card, all cross-checked.

**Evidence against / risks:** 2024 recency (weaker "find a recent algorithm" narrative than CVPR 2025); the FLOPs-branding caveat above must be worded carefully; no fine-tuning-specific community evidence at all (neutral); 547M FLOPs is higher than LSNet-T's 0.3G under the (likely shared) convention.

### 4.2 LSNet-S (CVPR 2025)

**Evidence for:**
1. Best paper accuracy of the three: 77.8% top-1 (79.0% with distillation), 16.1M params, 0.5G FLOPs, batch 2048 @ 224×224 — verified against arXiv full text this run [2-verify].
2. Same one-line timm loading path and MIT-licensed checkpoints [67]; `lsnet_s` card existence verified in Stage 01d and listed in the `lsnet_t` card's variant enumeration.
3. CVPR 2025 recency directly strengthens the "how you asked AI to find a recent algorithm" narrative (criterion 1) and the report's novelty framing.
4. Equal-compute-class to StarNet-S2 under the inferred convention (0.5G vs 0.5 GMACs) while scoring +3.0 points on paper top-1 — the strongest accuracy-per-compute position of the three.

**Evidence against / risks:** 16.1M params = 4.3× StarNet-S2, the most VRAM- and time-demanding under an 8 GiB / 3-day budget (estimate UNSUPPORTED); shares the open issue #15 exposure [43]; dynamic-kernel weight generation plausibly inflates training memory (estimate UNSUPPORTED); multi-concept explainability (LKP + SKA + distillation) raises the criterion-2 effort and error surface; its distilled edge cannot be replicated by us.

### 4.3 LSNet-T (CVPR 2025)

**Evidence for:**
1. Lowest compute of the three: 0.3G FLOPs (~40% below StarNet-S2/LSNet-S under the inferred convention) and card-reported throughput 14,708 img/s (hardware unspecified) [67][2-verify].
2. Accuracy 74.9% (76.1% distilled) — essentially equal to StarNet-S2's 74.8% on paper numbers [2-verify].
3. Same MIT/timm path, same CVPR 2025 recency as LSNet-S.

**Evidence against / risks (why it fits this rubric worst):**
1. Its accuracy advantage over StarNet-S2 is +0.1 points — the compute saving does not translate into a headroom argument for better fine-tuned results.
2. 11.4M params = 3.1× StarNet-S2 for equal paper accuracy; the extra parameters consume 8-GiB headroom (estimate UNSUPPORTED) without a returned benefit in this rubric.
3. Shares every LSNet-family risk (issue #15, dynamic-kernel memory, multi-concept explanation) while forfeiting LSNet-S's accuracy advantage.
4. Under this assignment's criteria it is **dominated on both ends**: StarNet-S2 is simpler at equal accuracy; LSNet-S is more accurate at equal code effort. It should be chosen only if the supervisor explicitly wants the lowest-FLOPs 2025 model, or as a fallback if the LSNet-S pilot exceeds VRAM.

---

## 5. Draft Experiment Design (Stage 02 proposal — requires supervisor approval)

**Supervisor decision (2026-09-18):** StarNet-S2 and EuroSAT were selected; entering Stage 02 was approved. The finalized single-model design is `research_records/stage_02_experiment_design.md` (LSNet arms here are NOT in approved scope; deviation 4.1 there changes the training vehicle to a minimal self-written script). The text below is preserved as the original three-way draft.

This draft uses only protocol elements that are citably sourced; every unsourced engineering choice is explicitly marked.

### 5.1 Objective

Fine-tune StarNet-S2, LSNet-T, and LSNet-S under an **identical protocol** on one small dataset, producing our own accuracy/compute comparison for grading criterion 4, with Grad-CAM visualizations for the report.

### 5.2 Dataset (decision required from supervisor)

- **Primary: EuroSAT** [73][47]. Rationale: only option with verified license (MIT), verified size description (27,000 images / 10 classes), and a published benchmark target (98.57%) to compare against; domain shift (satellite) enriches criterion 5 ("what you have learnt").

  **Dataset profile (official repository, re-verified 2026-09-18):**
  - Sentinel-2 satellite remote-sensing image classification; **27,000 labeled patches, 10 land-use/land-cover classes** (AnnualCrop, Forest, HerbaceousVegetation, Highway, Industrial, Pasture, PermanentCrop, Residential, River, SeaLake).
  - Native patch resolution 64×64 pixels; upscaled to 224×224 for fine-tuning the 224-pretrained backbones (Section 5.4).
  - Two distributions exist: **RGB (3-band JPG — the one this design uses)** and multi-spectral (13-band TIFF, not needed).
  - Per-class counts range roughly 2,000–3,000 with a roughly balanced distribution *(exact per-class numbers not verbatim-verified — count the class folders empirically at download time and record in the assignment log)*.
  - License: MIT (verified). Benchmark anchor: the authors' own sentence, "With the proposed novel dataset, we achieved an overall classification accuracy of 98.57%" (Helber et al., IEEE J-STARS 2019) [73][47].
- **Backup: CIFAR-100** [74] (universality) or **Flowers-102** [75][80] (fine-grained narrative). License/size UNSUPPORTED — if chosen, record actual download size and license text empirically before training.
- **Split — EuroSAT ships with NO official train/val/test split** (official repository distributes per-class folders only; re-verified 2026-09-18). This differs from CIFAR-10/100, which ships a fixed 50k-train/10k-test split. The EuroSAT benchmark paper and subsequent literature each use their own random splits, so no canonical split exists; the split we make must be documented and fixed. Our design: **stratified 70/15/15 with a fixed random seed**, shared by all three models for a fair comparison *(engineering choice — no sourced recommendation found)*:

  | Subset | Share | Approx. count (of 27,000) |
  |---|---|---|
  | Train | 70% | ≈ 18,900 |
  | Validation | 15% | ≈ 4,050 |
  | Test | 15% | ≈ 4,050 |

  The exact split indices (seed included) will be recorded in the experiment log so the split is reproducible.

### 5.3 Models

- `timm.create_model('timm/starnet_s2.in1k', pretrained=True, num_classes=10)` [62]
- `timm.create_model('hf_hub:jameslahm/lsnet_t', pretrained=True, num_classes=10)` [67]
- `timm.create_model('hf_hub:jameslahm/lsnet_s', pretrained=True, num_classes=10)` [67, card existence per Stage 01d]
- Optional appendix arm: `*_distill` LSNet checkpoints [67].

### 5.4 Training protocol

- **Vehicle:** timm repository `train.py` (repo root, not pip package [41]); `validate.py` for evaluation.
- **Input:** resize to 224×224 for cross-model comparability with reported figures.
- **Augmentation (baseline):** RandomResizedCrop(224) + RandomHorizontalFlip, per the official PyTorch transfer-learning tutorial [72].
- **Optimizer:** SGD, lr=0.001, **momentum=0.9**, StepLR(step_size=7, gamma=0.1), 25 epochs — the tutorial's exact protocol [72, verified], chosen for citability and 3-day feasibility. *(Alternative: timm-default AdamW + cosine; not selected because official timm docs give only ImageNet-scale schedules [41].)*
- **Batch size 64 with native AMP** *(8 GiB feasibility estimate UNSUPPORTED — confirm in pilot; tutorial uses 4, which is unnecessarily slow for this scale [72]; timm's guidance only says to scale batch and LR proportionally [41])*. If OOM: halve batch, keep protocol otherwise identical.
- **Fixed seed** for the split and training *(engineering choice)*.
- **Not adopted:** 200-epoch timm.fast.ai schedule [64] (infeasible in 3 days); mixup/RandAugment/random-erasing (documented timm options [41]) deferred to a bonus arm if time permits.

### 5.5 Evaluation and reporting

- **Metrics:** top-1/top-5 via `validate.py` [41]; confusion matrix and per-class F1 *(engineering choice; sklearn)*.
- **Compute accounting:** params (card values), FLOPs with both papers' stated units and the GMACs cross-check (Section 3, Area D-2), measured wall-clock per epoch and peak GPU memory via `torch.cuda.max_memory_allocated` *(engineering choice)*.
- **Grad-CAM:** pytorch-grad-cam with target layers specified by module path, per the README's target-layer guidance and discussion #380 precedent for timm models [65][66].
- **Comparison anchors:** EuroSAT 98.57% published benchmark [73]; PyTorch tutorial 0.9346 finetuning accuracy as a protocol sanity reference [72].
- **Log empirically:** actual dataset download size, license text, package versions, seed, hardware.

### 5.6 Risks and mitigations

| Risk | Mitigation |
|---|---|
| LSNet fails to converge / reproduce (cf. open issue #15 [43]) | Pilot first with LSNet-T (cheapest); if unresolved after 1 day, fall back to StarNet-S2 as primary model |
| VRAM overrun on LSNet-S (16.1M + dynamic kernels) | Halve batch; gradient accumulation not needed at this scale; last resort: drop LSNet-S arm |
| 3-day timeline | Single seed first; extra seeds only if pilot timing allows |
| Dataset license friction (non-EuroSAT) | EuroSAT primary precisely because its MIT is verified [73] |

### 5.7 Grading-criteria mapping

| Criterion | Where this design serves it |
|---|---|
| 1. How you asked AI to find the algorithm | Conversation log + search protocol (Stage 01–01d) |
| 2. Algorithm description | StarNet: one equation/diagram; LSNet: LKP+SKA narrative (Section 4) |
| 3. How AI implemented the algorithm | timm-native one-line loading; `train.py` protocol [41][62][67] |
| 4. Experiment settings and results | Section 5.4–5.5; identical-protocol three-way comparison |
| 5. What you have learnt | Domain-shift dataset choice; distillation caveat; FLOPs-unit lesson |
| 6. Webpage link of source codes | MIT/Apache-2.0 models + permissive dataset → publishable repo |

---

## 6. Final Recommendation

**Primary — StarNet-S2.** It holds the strongest verified evidence on every axis this rubric grades: smallest footprint, cleanest provenance (author-trained, Apache-2.0, both repo and card), the lowest explanation cost, and no community red flags, at accuracy statistically indistinguishable from LSNet-T and within 3 points of LSNet-S on paper numbers.

**Alternative — LSNet-S**, if the supervisor weights CVPR 2025 recency and paper accuracy higher than simplicity and risk. It is the strongest accuracy-per-compute option and shares StarNet-S2's zero-friction code path. Gates: accept the open issue #15 exposure and the 16.1M-param memory risk on 8 GiB.

**Not recommended for this rubric — LSNet-T**, unless the lowest-FLOPs CVPR 2025 model is explicitly desired; it trades 3.1× the parameters of StarNet-S2 for +0.1 paper accuracy and shares all family risks.

This recommendation is submitted for supervisor decision. It does not authorize installation, downloads, or training.

**Supervisor decision (2026-09-18):** StarNet-S2 (primary) and EuroSAT (primary dataset) were selected; Stage 02 approved. Finalized design: `research_records/stage_02_experiment_design.md`.

---

## 7. Action Plan (all items pending supervisor approval)

1. Supervisor decides: StarNet-S2 (primary) or LSNet-S (alternative); dataset: EuroSAT (primary) / CIFAR-100 / Flowers-102 (backup).
2. Stage 02: finalize experiment design from Section 5; obtain approval.
3. Stage 03a: install timm (and clone pytorch-image-models for `train.py`/`validate.py`); record versions.
4. Stage 03b: download dataset + model weights; empirically record download size and license text; verify EuroSAT split.
5. Stage 04: pilot run (LSNet-T first, 2–3 epochs) to validate VRAM/epoch-time; then full 25-epoch runs for all three arms.
6. Stage 05: evaluation (validate.py, confusion matrix, per-class F1, Grad-CAM), compute accounting.
7. Stage 06: visualization and HTML report; Stage 07: final report + source-code repo publication.

## 8. Open Questions

1. FLOPs unit convention: are both papers' "FLOPs" columns MACs? The timm GMACs cross-check suggests yes for StarNet; LSNet's is unverified. Only material if the report quotes efficiency numbers — wording in Section 3/D-2 is safe either way.
2. Will the supervisor permit the optional `*_distill` LSNet appendix arm?
3. Exact UMMoodle submission deadline still unconfirmed (target: complete before 2026-09-21).
4. Should the repo be public or private-until-submission (grading criterion 6)?

---

## 9. Bibliography (APA 7 — with verified full-text links)

Primary papers:

- Ma, X., Dai, X., Bai, Y., Wang, Y., & Fu, Y. (2024). Rewrite the stars. In *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition* (pp. 17711–17720). CVF Open Access. https://openaccess.thecvf.com/content/CVPR2024/papers/Ma_Rewrite_the_Stars_CVPR_2024_paper.pdf (full text verified this run via https://arxiv.org/abs/2403.19967)
- Wang, A., Chen, H., Lin, Z., Han, J., & Ding, G. (2025). LSNet: See large, focus small for efficient visual representation learning. In *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition* (pp. 9718–9729). CVF Open Access. https://openaccess.thecvf.com/content/CVPR2025/html/Wang_LSNet_See_Large_Focus_Small_for_Efficient_Visual_Representation_Learning_CVPR_2025_paper.html (table values verified this run via arXiv full text: https://arxiv.org/abs/2503.23135 — the CVF PDF returned 404 to the automated fetcher)

Software, model cards, repositories, and issues:

- Helber, P. (n.d.). *EuroSAT* [Computer software]. GitHub. https://github.com/phelber/EuroSAT (License: MIT; benchmark quote verified)
- Hugging Face. (n.d.). *starnet_s2.in1k* [Model card]. https://huggingface.co/timm/starnet_s2.in1k (all quoted facts verified)
- jameslahm. (2025). *lsnet_t* [Model card]. Hugging Face. https://huggingface.co/jameslahm/lsnet_t (License "mit" and load line verified)
- Ma, X. (n.d.). *ma-xu/Rewrite-the-Stars* [Computer software]. GitHub. https://github.com/ma-xu/Rewrite-the-Stars (title and Apache-2.0 sidebar verified)
- MadryLab. (n.d.). *timm-bench* [Computer software]. GitHub. https://github.com/MadryLab/timm-bench
- PyTorch. (n.d.). *Transfer learning for computer vision tutorial*. https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial.html (protocol verified, incl. momentum=0.9)
- THU-MIG. (n.d.). *lsnet* [Computer software]. GitHub. https://github.com/THU-MIG/lsnet
- THU-MIG. (2025, September 24). *有人成功复现了吗？我用一张3090跑不出论文的结果* [Issue #15]. GitHub. https://github.com/THU-MIG/lsnet/issues/15 (still open; last comment 2025-12-10)
- Wightman, R. (n.d.). *timm: Training script* [Documentation]. Hugging Face. https://huggingface.co/docs/timm/training_script
- jacobgil. (n.d.). *pytorch-grad-cam* [Computer software]. GitHub. https://github.com/jacobgil/pytorch-grad-cam ; Discussion #380: https://github.com/jacobgil/pytorch-grad-cam/discussions/380
- timm.fast.ai. (n.d.). *Training*. https://timm.fast.ai/training

Datasets:

- Krizhevsky, A. (n.d.). *CIFAR-10 and CIFAR-100 datasets*. University of Toronto. https://cave.cs.toronto.edu/kriz/cifar.html (page live; size/license text not captured)
- PyTorch. (n.d.). *torchvision.datasets* [API documentation]. https://docs.pytorch.org/vision/stable/datasets.html
- VGG, University of Oxford. (n.d.). *102 category flower dataset*. https://www.robots.ox.ac.uk/~vgg/data/flowers/102/
- TensorFlow Datasets. (n.d.). *oxford_flowers102* [Catalog]. https://www.tensorflow.org/datasets/catalog/oxford_flowers102

Fine-tuning literature and derivative evidence:

- Barak, O., et al. (2024). *94% on CIFAR-10 in 3.29 seconds on a single GPU*. arXiv. https://arxiv.org/html/2404.00498v2
- Tian, J., et al. (2021). *Improved regularization and robustness for fine-tuning in visual recognition*. arXiv. https://arxiv.org/abs/2111.04578
- (2024). *Unveiling the secret recipe: A guide for supervised fine-tuning*. arXiv. https://arxiv.org/html/2412.13337
- *Barefoot footprint detection algorithm based on YOLOv8-StarNet* (2025). PMC. https://pmc.ncbi.nlm.nih.gov/articles/PMC12349430/
- *YOLO-Starfish: Fish object detection* (2026). *Scientific Reports*. https://www.nature.com/articles/s41598-026-44187-z
- *StarNet-RiceSeg: An efficient high-dimensional feature mapping* (2026). *Agriculture (MDPI)*. https://www.mdpi.com/2077-0472/16/7/775
- Helber, P., Bischke, B., Dengel, A., & Borth, D. (2019). EuroSAT: A novel dataset and deep learning benchmark for land use and land cover classification. *IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing, 12*, 2217–2226. (via https://github.com/phelber/EuroSAT)

## 10. Source Extracts (tier-tagged, numbered as cited)

| # | Source | Tier | Key verified content |
|---|---|---|---|
| [41] | timm Training script docs — https://huggingface.co/docs/timm/training_script | 1 | Scripts in repo root, not pip; native AMP default ≥0.4.3; `--aa rand-m9-mstd0.5`; ImageNet-scale recipes only |
| [42] | THU-MIG/lsnet repo — https://github.com/THU-MIG/lsnet | 1 | Official LSNet repo, live |
| [43] | THU-MIG/lsnet Issue #15 — https://github.com/THU-MIG/lsnet/issues/15 | 1 | Opened 2025-09-24 (RTX 3090 reproduction failure); single non-maintainer reply 2025-12-10, no fix; still open |
| [44]/[67] | jameslahm/lsnet_t card — https://huggingface.co/jameslahm/lsnet_t | 1 | License "mit"; `timm.create_model("hf_hub:jameslahm/lsnet_t", pretrained=True)`; 11.4M, Top-1 74.9/76.1*, 0.3G, throughput 14708; variants t/t_distill/s/s_distill/b/b_distill |
| [45] | MadryLab/timm-bench train.py | 2 | Independent reuse of timm train.py |
| [46] | arXiv 2404.00498 | 2 | "94% on CIFAR-10 in 3.29 Seconds on a Single GPU" (from-scratch ResNet9 context) |
| [47]/[73] | Helber et al. EuroSAT + official repo | 1 | MIT; 27,000 labeled images, 10 classes; "overall classification accuracy of 98.57%" |
| [48] | arXiv 2111.04578 | 2 | Fine-tuning regularization guide |
| [49] | arXiv 2412.13337 | 2 | Supervised fine-tuning guide |
| [50]–[52] | YOLOv8-StarNet (PMC); YOLO-Starfish (Sci Rep); StarNet-RiceSeg (MDPI) | 3 | Derivative StarNet adoptions; no critique found |
| [53]/[64] | timm.fast.ai/training | 2 | imagenette2-320 example: epochs=200, lr=0.01, opt='sgd' |
| [61] | ma-xu/Rewrite-the-Stars | 1 | "[CVPR 2024] Rewrite the Stars"; Apache-2.0 sidebar; checkpoints, no training scripts |
| [62] | timm/starnet_s2.in1k card | 1 | "Trained on ImageNet-1k by paper authors"; apache-2.0; 3.7M; GMACs 0.5; 224×224; Original link |
| [63] | CVF open-access page (StarNet) | 1 | Author list of record (Ma, Dai, Bai, Wang, Fu) |
| [65]/[66] | pytorch-grad-cam README + Discussion #380 | 1 | Target-layer-by-path guidance; timm model `volo_d2_224` precedent |
| [68] | ma-xu/Rewrite-the-Stars Issue #8 | 1 | Pretrained-checkpoint availability question (no fine-tuning issues verified) |
| [71] | torchvision datasets docs | 1 | Negative result: no sizes/licenses listed |
| [72] | PyTorch transfer-learning tutorial | 1 | resnet18 IMAGENET1K_V1; Hymenoptera; SGD lr=0.001 momentum=0.9; StepLR(7, 0.1); 25 epochs; batch 4; RandomResizedCrop(224)+RandomHorizontalFlip; val acc 0.9346 / 0.9477 |
| [74]/[75]/[80] | CIFAR page; Flowers-102 page; TFDS catalog | 1/1/2 | Provenance confirmed live; sizes/licenses not captured |
| [76]–[79] | SOTA/leaderboard & project pages | 3 | Fine-tuned accuracy figures not extractable (UNSUPPORTED) |

**Verification addendum (Phase 3.1):** [62], [67], arXiv 2403.19967 Table 6, arXiv 2503.23135 tables, [61], [73], [72], [43] were re-fetched this run; 7/8 claims SUPPORTED verbatim, 1 PARTIAL (issue #15 characterization corrected above). The `lsnet_s` card body remains unfetched this run (verified in Stage 01d; listed in the `lsnet_t` card variant enumeration). Supplementary fetch (2026-09-18, Section 5.2): the EuroSAT official repository was re-fetched and confirms 27,000 labeled images / 10 classes, RGB and 13-band MS distributions, MIT license, and **no official train/val/test split** (per-class folders only); per-class counts were not exposed by that page and are to be counted empirically at download time.
