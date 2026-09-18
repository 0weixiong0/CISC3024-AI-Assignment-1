# Stage 05 — Final Report Outline (for supervisor review)

Course: CISC3024 Pattern Recognition — AI Assignment #1
Template: faculty Word template (University of Macau cover page, Table of Contents, three heading levels "First/Second/Third layout title", Table/Figure caption styles)
Language: English; citations APA 7; all content drawn from approved stage records (stage_00–stage_04 logs) — no new claims, no fabricated results.
Estimated length: 12–15 pages, 5 figures, 4 tables.

## Grading-criteria mapping

| # | Criterion (Requirement.txt) | Covered by |
|---|---|---|
| 1 | How you ask AI tools to find the algorithm | §1, §2 |
| 2 | Algorithm description | §3 |
| 3 | How AI implements it | §4 |
| 4 | Experiment settings and results | §5 |
| 5 | What you have learnt | §7 |
| 6 | Webpage link of source codes | §6 |

## Cover page (template verbatim, placeholders to fill)

University of Macau / Faculty of Information Science and Computing / Department of Computer Science — "CISC3024 AI Assignment 1 Report" — by *Your Name*, Student No: *UD……* — date.

## Section-by-section outline

### 1. Task Description and Agent Workflow  *(what it does: frames the assignment and shows how work was delegated to the AI agent; mirrors the course's agent-coding workflow — Description → Plan → Execution → Supervision → Verification → Presentation)*
- 1.1 Goal, scope, constraints: find a recent Deep CNN or Deep Autoencoder with a computer-vision application; the AI tool/agent does everything; no self-written code allowed; deadline.
- 1.2 Delegation protocol used with the agent: stage-by-stage approval gates, verbatim prompt records, bilingual conversation log, no-fabrication policy; one example prompt shown verbatim. *(Source: stage_00 preflight, conversation_log U001–U027)*

### 2. Algorithm Searching and Selection  *(what it does: answers criterion 1 — the actual prompts and the funnel from many candidates to one)*
- 2.1 Search strategy and prompts: retrieval rounds for classification and restoration, screening ledger, 11+ candidate algorithms. *(Source: stage_01 retrieval/screening records)*
- 2.2 Screening criteria and comparison table: parameter count, ImageNet top-1, recency (2024–2025 venues), CPU/browser deployability. *(Source: stage_01c/01d comparison)*
- 2.3 Final choice — StarNet-S2 — and justification with verified citations. *(Source: stage_01 final comparison, U016)*

### 3. Algorithm Description: StarNet-S2  *(what it does: answers criterion 2 — the algorithm itself, in our own words with a cited architecture figure)*
- 3.1 The star operation (element-wise multiplication of two linear branches) and the star-block topology; why it is cheap. *(Cited: Ma et al., 2024, CVPR)*
- 3.2 The 10-class variant used here: four stages 32×56×56 → 64×28×28 → 128×14×14 → 256×7×7, global-average-pool head, 3.7M parameters. *(Source: checkpoint introspection, stage_04 addendum)*

### 4. AI Implementation  *(what it does: answers criterion 3 — how the agent turned the plan into code, and the engineering decisions it made)*
- 4.1 From design doc to training script: the prompts and iterations. *(Source: stage_02 experiment design, stage_03 log)*
- 4.2 Key decisions: timm `starnet_s2.in1k`, frozen split seed 42, AdamW + cosine schedule, AMP training, checkpointing; no manual code edits.

### 5. Experiment Settings and Results  *(what it does: answers criterion 4 — dataset, setup, numbers, evidence)*
- 5.1 Dataset: EuroSAT, 27,000 RGB 64×64 images, 10 classes; frozen split 18,900 / 4,050 / 4,050. *(Source: stage_03 G2 record)*
- 5.2 Training configuration: 25 epochs, AdamW, cosine schedule, mixed precision, hardware actually used.
- 5.3 Results: best val accuracy 0.9738 (epoch 23); test top-1 0.9765; macro-F1 0.9758; training/validation curves figure; confusion matrix figure. *(Source: stage_03 metrics.json, G4 report)*
- 5.4 Interpretability: Grad-CAM on the final-norm features (analytic form; correlation 1.0 vs pytorch_grad_cam) and per-stage feature maps. *(Source: stage_04 addendum)*

### 6. Interactive Visualization Webpage  *(what it does: answers criterion 6 — the deliverable webpage and its source)*
- 6.1 Two versions: local Python-server version; pure-frontend version (13.7 MB ONNX, onnxruntime-web, runs entirely in the browser, GitHub Pages ready).
- 6.2 Features and verification: dataset browser, live prediction, Grad-CAM, multi-layer feature maps; browser-vs-server agreement numbers. *(Source: stage_04 log and addendum)*
- 6.3 Webpage link: placeholder — to be filled with the GitHub Pages URL once publication is approved by the supervisor.

### 7. What I Have Learnt  *(what it does: answers criterion 5 — reflection, in first person)*
- Structured prompting and approval gates; verification-first (numerical parity checks before trusting outputs); the Grad-CAM stride bug as a case study of "a test can pass and the page still be wrong"; deployability trade-offs (server vs in-browser).

### 8. References (APA 7)
- StarNet paper, EuroSAT paper, timm, onnxruntime-web, pytorch-grad-cam — only entries already verified in stage records.

## Production method (decision needed only if you prefer otherwise)

Recommended: write the report directly as .docx with python-docx 1.2.0 (already used for the stage 00/01 deliverables) — no new tools needed. Alternative: author in LaTeX and convert to Word — requires installing Pandoc, which is not currently on this machine; only worth it if you want LaTeX for the final document.
