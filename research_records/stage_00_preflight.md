# Stage 00 — Research Supervision and Assignment Preflight

Date: 2026-09-18

Status: Requirements checked; supervision guidance saved; initial dialogue archived; local compute verified. No research model has been selected, implemented, or trained. Following this preflight, the supervisor approved deep-research installation; installation and activation are verified in Section 11. Literature screening awaits a clarification of pretrained-weight constraints.

Sections 1–9 preserve the initial preflight snapshot before the subsequent tool-selection answer. Section 11 records the later approval and supersedes earlier pending/not-installed states; Section 10 is the current artifact inventory.

This is an English working-stage report, not the final assessed report. Its companion Word version deliberately does not overwrite or represent compliance with the final report template.

## 1. Purpose and supervision contract

The supervisor commissioned an AI-led search, design, experimentation, and reporting process, with explicit human approval between stages. The assistant is responsible for generating code and reports; the supervisor provides decisions and evaluations. The original request and its full English translation are preserved in `conversation_log.md`.

Approval gates:
1. Approve a model from an evidence-based literature shortlist.
2. Approve the algorithm and experimental plan before implementation.
3. Review feasibility at each experiment scale before expansion.
4. Review backend readiness before adding an HTML visualization interface.
5. Approve the report structure before final report drafting and submission preparation.

Installing or using a proposed additional skill or extension also requires approval. No third-party package, extension, model weight, or dataset was downloaded during this preflight. Installed document libraries, local inspection tools, and a read-only marketplace search were used. No files were published or uploaded to an external document-processing service.

## 2. Authoritative requirements and interpretation

### 2.1 Assignment PDF

Source: `AIassign1.pdf`, page 1; extracted evidence: `AIassign1_extracted.txt`, lines 6–19.

- The course is CISC3024 Pattern Recognition, AI Assignment #1, September 2026.
- Find a recent deep CNN or deep autoencoder algorithm with an application in computer vision and pattern recognition.
- Use an AI tool or agent for all work, explicitly including algorithm searching, programming, and report writing.
- Submit a report detailing the steps online through UMMoodle the following week, followed by a Turnitin similarity check.
- Students are explicitly NOT allowed to write code themselves.

The PDF is one page. Text was extracted successfully using the already-installed `pdftotext` utility. The native PDF rendering tool failed because `pdftoppm` was unavailable; PDF page appearance was not visually inspected.

### 2.2 Six mandatory report components

Source: `Requirement.txt`, lines 1–7.

| Requirement | Evidence to preserve | Proposed final-report destination |
| --- | --- | --- |
| How the student asks AI tools to find the algorithm | Complete prompts, English translations, search queries, screening records, supervisor selection | AI-Assisted Literature Search and Selection |
| Algorithm description | Paper-verified architecture, mathematical formulation, objective, declared adaptations | Algorithm Description |
| How AI implements the algorithm | AI-generated implementation steps, prompts, tests, failures, corrections, supervisor interventions | AI-Assisted Implementation |
| Experiment settings and results | Dataset splits, seeds, configuration, environment, metrics, timing, plots, feasibility reports | Experimental Settings and Results |
| What the student learned | Actual supervisor reflections and observed lessons, not invented personal experiences | Reflection and Lessons Learned |
| A webpage link to source code | A working, accessible source-code webpage with reproducibility instructions | Source Code Availability |

This mapping is a provisional checklist, not the final report outline. Final outline approval remains pending.

### 2.3 Differences, additions, and unresolved interpretation

| Topic | Original source | Supervisor outline | Handling |
| --- | --- | --- | --- |
| Recency | A recent algorithm | Latest networks and novelty comparison | Search current literature through 2026-09-18; do not claim the absolute latest without evidence. Older algorithms may be baselines rather than the selected contribution. |
| Coding authorship | Student must not write code | Supervisor guides the AI researcher | Preserve AI authorship and human supervision evidence; do not ask the supervisor to edit code manually. |
| Deadline | Next week; no exact date or time | Finish before September 21 | Work toward 2026-09-20 evening. Confirm the exact UMMoodle cutoff before submission rather than infer it from the PDF. |
| Submission | UMMoodle and Turnitin | Not explicitly included in the outline | Add submission readiness and honest attribution; no promises about a similarity percentage. |
| Source publication | Source-code webpage required by Requirement.txt | GitHub may be provided if needed | Arrange a repository or other accepted accessible source webpage later. Do not publish without approval. A local folder alone does not satisfy this requirement. |
| HTML interface | Not required in either requirements file | Requested after backend success | Retain as a supervised enhancement, but protect the required experiments, report, and source link if time becomes constrained. |
| Evaluation | No numeric rubric or target accuracy supplied | Compare likelihood of scoring well | Assess documented requirement coverage and evidence quality, not a fabricated mark prediction. |
| APA 7 and template | Word/PDF specified; APA 7 not stated in the two requirement files | APA 7, English report, exact supplied template formatting | Treat these as additional supervisor constraints. |

## 3. Planning presentation and Word template

### 3.1 Planning presentation

All 15 slide XML text streams in `Agent_coding.pptx` were extracted. Text evidence appears in `supporting_documents_extracted.txt`, lines 1–112. Slide images, animations, and speaker notes were not visually audited.

The presentation emphasizes decomposition, task description, preparation, execution, supervision, verification, presentation, evaluation, and iteration. Slides 7–9 emphasize goals, scope, constraints, inputs, outputs, and precise reference-based descriptions. Slide 11 explicitly recommends milestones, a minimum viable product, and AI-generated plans refined by a human.

The LeNet/MNIST example is teaching guidance, not a requirement to choose LeNet. Slide 8 warns that vaguely saying LeNet can produce a different implementation from the historical LeNet-5. The experiment plan should therefore name the exact paper, model variant, input resolution, activations, downsampling, loss, and any departures from the reference.

### 3.2 Template inspection

`Report Template.docx` was inspected as a read-only Office Open XML package. The original file was not modified.

- The cover contains university/faculty/department text, `CISCXXXX YYYY / XXX Report`, name/student-number placeholders, and `18 Sep 2026`.
- The document contains an automatic table-of-contents field using heading levels 1–3, existing heading and table-of-contents styles, author/student-number ASK fields, and one embedded image.
- Page size is 21.59 × 27.94 cm (US Letter), with 2.54 cm top/bottom margins and 3.175 cm left/right margins.
- Normal style explicitly specifies Times New Roman, 12 pt. Heading styles and direct paragraph formatting differ; the eventual final report must reuse the actual template rather than approximate it using a generic APA layout.
- The supervisor must later clarify whether keeping the cover unchanged permits replacing only the existing course/title/name/student-number placeholders. Until then, preserve the cover literally.
- Exact rendered appearance and table-of-contents pagination have not been verified in Word/PDF. Native rendering, field updates, and a visual comparison are required before final delivery.

## 4. Local compute and software feasibility

Read-only environment inspection and a trivial CUDA matrix multiplication were performed. This was an environment smoke test, not implementation or training of the research network.

| Resource | Observed value | Implication |
| --- | --- | --- |
| CPU | Intel Core i9-13900H; 14 cores, 20 logical processors | Suitable for moderate data loading and preprocessing; benchmark actual pipeline throughput. |
| System RAM | 33,968,410,624 bytes, approximately 31.64 GiB | Avoid keeping multiple large image datasets decoded in memory. |
| GPU | NVIDIA GeForce RTX 4060 Laptop GPU | Local GPU experiments are feasible in principle. |
| GPU memory | 8,585,216,000 bytes, approximately 8 GiB total | Prefer compact variants and measure batch-size/activation requirements before expansion. |
| Free GPU memory | 7,405,043,712 bytes during the check | Transient measurement; other applications may change availability. |
| Workspace drive | Approximately 59.01 GiB free on D: | Budget datasets, checkpoints, logs, and environment files; do not download full-scale datasets by default. |
| Python | 3.12.10 | Existing interpreter; isolate any future project dependency changes after approval. |
| PyTorch | 2.7.1+cu128; CUDA build 12.8 | `torch.cuda.is_available()` returned true. |
| CUDA execution | 2×2 matrix multiplication returned `[[2.0, 3.0], [6.0, 11.0]]` | Basic CUDA execution works; no training-time estimate follows from this result. |
| Document tools | pdftotext, PyPDF2, python-docx, python-pptx installed | Initial document work requires no new installation. |
| Missing shell commands | gh, pandoc, soffice not found in PATH | This does not prove that GUI Word or other applications are absent. Defer installation decisions until needed. |

No throughput, accuracy, generalization, or full-scale training feasibility has yet been measured. A model's parameter count alone is insufficient to predict GPU memory consumption or runtime. Input resolution, activation memory, optimizer state, data loading, laptop power limits, and training strategy must be considered.

## 5. Research and extension preparation

### 5.1 Proposed literature-screening scope

This is a proposal, not a completed search or an approved model choice.

- Search mainly 2024–2026 publications available by 2026-09-18, with older work retained for foundations and baselines where justified.
- Aim initially to screen 20–30 relevant papers at title/abstract level, read 6–8 feasible candidates more closely, and present 3–4 finalists. Adapt the counts to actual search quality rather than pad the bibliography.
- Prefer primary papers, official conference/publisher pages, author repositories, and official dataset documentation. Check publication status, code availability, licensing, pretrained weights, and reproducibility.
- Verify that each finalist is genuinely a deep CNN or deep autoencoder suitable for the assignment. Do not reclassify a transformer-only method as a CNN merely to fit the brief.
- Score candidates for architectural complexity, measured/local hardware feasibility, implementation difficulty, novelty, and coverage of documented assessment requirements. Clearly distinguish faithful reproduction, transfer learning, and an adapted smaller-scale experiment.

Before model approval, no dataset download or candidate implementation is authorized by this proposal.

### 5.2 Extension discovery status

Already-visible capabilities include `research`, `grilling`, `tdd`, `diagnosing-bugs`, `code-review`, browser tools, and web search/fetch. The locally configured Chinese communication and engineering workflow skills, plus the extension-discovery skill, were loaded during preflight. No new extension was installed. The `research` skill itself has not yet been activated.

Source status:
- Qoder marketplace: completed a read-only `research` query across skill, MCP, and plugin kinds; no provider failures returned. Six skill entries were returned on the first skill page, including two plausible research/writing matches. This was a first-page discovery, not an exhaustive market review.
- skills.sh: not queried because its prescribed search client would download/execute `npx --yes skills@1.5.22 find -- 'research'`. The supervisor requires approval before such third-party execution. Do not label this source as searched or as having no matches.
- Enterprise skills provider: none identified in the current MCP catalog. QMind is a knowledge-base connector, not an enterprise skill marketplace, and was not treated as one.

| Candidate | Type / source / publisher | Version and state | Assessment |
| --- | --- | --- | --- |
| research | Installed local skill; publisher not supplied in visible catalog | Version unspecified; available, not yet activated | Recommended first choice: already present and described as primary-source research with a Markdown evidence record. No installation needed. |
| deep-research | Skill; Qoder official-market channel; Jose-Luis-Nunez | 1.0.0; not installed; metadata says no configuration required | Relevant source verification and citation workflow, but overlaps with the installed skill. Actual instructions have not been audited. |
| content-research-writer | Skill; Qoder official-market channel; ComposioHQ | 1.0.0; not installed; metadata says no configuration required | Potential later report-writing support; not necessary for initial paper selection. |

Qoder's official-market source identifies the distribution channel, not necessarily first-party authorship. Installation and actual usability remain unverified. After approval, re-query the selected candidate to obtain a current opaque installation reference; do not treat an expired reference or a matching display name as authorization.

Stable discovery identities: `official03866510` for deep-research and `official99793663` for content-research-writer. Other returned entries concerned market analysis, competitive research, Chinese report workflows, drug-development intelligence, or investment research; they were not recommended for this assignment.

## 6. Proposed schedule and stop conditions

The supervisor's deadline is treated conservatively as completion by the evening of 2026-09-20. These are planning allocations, not measured runtimes or a guarantee. Approval delays reduce the available work window.

| Date / stage | Planning allocation | Deliverable and gate |
| --- | --- | --- |
| September 18: paper screening and model choice | 2–4 hours | Search ledger, exclusion reasons, 3–4 candidates, recommendation; await model approval. |
| September 18: algorithm and experiment plan | 1–2 hours | Exact model variant, dataset/splits, baseline, metrics, expected outcomes, runtime budget and risks; await plan approval. |
| September 18: approved minimal pilot | 1–3 hours after approval | Data/label checks, forward/backward execution, tiny-subset fitting check, peak memory and timing; report feasibility before expansion. |
| September 19: experiments | Reserve 6–12 GPU-hours, conditional on pilot results | Controlled main/baseline runs, validation-led tuning, error analysis, a justified ablation if time permits; review each increase in scale. |
| September 20: completion | 2–3 hours for an approved UI; 4–6 hours for report and checks | Backend acceptance first, then visualization if feasible; final English report, APA 7 audit, source link, template/TOC check, submission buffer. |

Provisional stop conditions to define precisely in the approved plan:
- Stop expansion if memory use, observed training time, or data problems exceed the agreed budget.
- Do not use test-set results for tuning. Establish train/validation/test separation and duplicate/leakage checks before comparative experiments.
- Stop and diagnose non-finite losses, failed tiny-subset fitting, or incorrect labels/tensor shapes before expensive training.
- Preserve minimal required experiments and report evidence ahead of optional extra datasets or elaborate visualization. Any scope change requires supervisor agreement.
- Do not promise target accuracy before candidate, dataset, baseline, and pilot evidence are known.

## 7. Evidence and recordkeeping plan

The following are planned records for subsequent stages, not claims of experiments already performed:

- Literature ledger: query, search date, source, paper metadata, publication status, inclusion/exclusion reason, architecture fit, official code, license, dataset and hardware notes.
- Experiment ledger: run identifier, exact configuration, code version/hash, seed, dataset version and splits, environment, elapsed time, peak GPU memory, validation metrics, checkpoint selection, and test evaluation policy.
- Feasibility reports: what ran, observed measurements, deviations from the paper, failures/lessons, recommendation, and the supervisor's actual approval or rejection.
- Dialogue archive: original prompts/responses and full English translations; decisions remain pending until actually received. Record tool-provided selection questions and their actual answers as dialogue when they occur.
- Source-code publication review: do not expose credentials, personal identifiers, private conversation records, or restricted datasets by automatically uploading the whole workspace. Publish only approved source and necessary reproducibility materials.

The current workspace is not a Git repository. Local version tracking can be proposed during implementation planning; no remote repository was created and no code was published.

## 8. Errors, lessons, and limitations

1. Native PDF reading failed because the renderer expected `pdftoppm`. Resolution: use the installed `pdftotext`; do not install Poppler without approval. Text content was checked, not visual layout.
2. The initial PowerShell disk-query filter lost its quotes in shell parsing and produced an invalid-query error. Disk space was subsequently obtained using Python's `shutil.disk_usage`; CPU and RAM results were unaffected.
3. Windows video-controller AdapterRAM reported a misleading value for the discrete GPU. Use PyTorch CUDA device properties for actual GPU-memory capacity rather than that WMI field.
4. Inspection confirmed available hardware but did not benchmark model training. Do not confuse environment readiness with algorithm feasibility.
5. The report template contains live Word fields and inherited/direct formatting. A plain-text extraction or python-docx open/save check cannot prove visual equivalence or updated page numbers.
6. No paper has yet been screened, no experimental result exists, and no supervisor approval beyond the initial preflight/recordkeeping instructions has been received.
7. The first Word-export validation incorrectly expected nine tables; the source contains eight. The validation was corrected to derive the expected table count from the Markdown source and check source content, rather than rely on a manually guessed count.

## 9. Approval register

| Decision | State |
| --- | --- |
| Read source documents and preserve instructions/dialogue | Authorized by U001; completed in this preflight |
| New software or extension download/installation | Not authorized; none performed |
| Optional research-skill strategy | Awaiting supervisor choice |
| Selected research network | Not proposed or approved yet |
| Algorithm/experiment plan and datasets | Not approved |
| Scale-up, frontend, final report outline | Not approved |
| Cover placeholder replacement and source-code publication | Deferred for explicit confirmation |

## 10. Artifact locations

Every artifact created during this preflight is listed below using its full absolute path. The Word working report is generated from this Markdown report; its formatting is intentionally not the final assessment template.

| Artifact | Full absolute path |
| --- | --- |
| Project memory index | `C:\Users\weixiong\.qoder\projects\D--claude-workspace-CISC3024-AI-Assignment-1\memory\MEMORY.md` |
| Durable supervision guidance | `C:\Users\weixiong\.qoder\projects\D--claude-workspace-CISC3024-AI-Assignment-1\memory\research-supervision.md` |
| Original/English dialogue archive | `D:\claude\workspace\CISC3024 AI Assignment 1\research_records\conversation_log.md` |
| Assignment PDF text evidence | `D:\claude\workspace\CISC3024 AI Assignment 1\research_records\AIassign1_extracted.txt` |
| Presentation/template text evidence | `D:\claude\workspace\CISC3024 AI Assignment 1\research_records\supporting_documents_extracted.txt` |
| English preflight report, editable source | `D:\claude\workspace\CISC3024 AI Assignment 1\research_records\stage_00_preflight.md` |
| English preflight report, Word working copy | `D:\claude\workspace\CISC3024 AI Assignment 1\research_records\stage_00_preflight.docx` |
| Approved installed research skill | `C:\Users\weixiong\.qoder\skills\deep-research\SKILL.md` |

### Original input fingerprints (SHA-256)

| Input | SHA-256 |
| --- | --- |
| AIassign1.pdf | `61a41a9434a323e26261f8fa0c72b25af094cd68b61b7ca5339bfb609bc1d7ec` |
| Requirement.txt | `ecbfc2888f6c8bc2274ec395ca9eda1ff06bd8fd7d3274326e7ec8c06fabd024` |
| Agent_coding.pptx | `a2e847a5b228bad9fe57690ea5626e89d3495d8afd8b10f149f47ddd91b90783` |
| Report Template.docx | `8225fa1c1862a60776c431510c549e758f247b18e2965b6360db6202a63b0fb1` |

## 11. Post-preflight approval and research readiness

After receiving the preflight findings, the supervisor selected "Install deep-research" in question Q001 (recorded as U002 in the bilingual dialogue archive). This specifically authorized downloading, installing, and using the Jose-Luis-Nunez skill listed in Qoder's official marketplace; it did not authorize other installations or select a neural network.

The assistant re-queried the exact candidate, installed it using the marketplace's opaque reference, and verified the resulting state with another marketplace query. Verification reported `installed=true`, `installedVersion=1.0.0`, `enabledForAgent=true`, and `configurationRequired=false`. The installer reported `runtimeReady=true`; the live skill catalog subsequently exposed `deep-research`, and invoking it succeeded. No restart or additional authentication was requested. The installed file is listed in Section 10.

The skill's workflow was loaded, but paper retrieval has not begun. No RESEARCH_CONTEXT.md or existing DEEP_RESEARCH report was found in the workspace. The pending scope question is whether candidate experiments may use official pretrained weights and fine-tuning, or whether the selected network must be trained from scratch. Fine-tuning is recommended as an allowed option given the deadline, not as a promise that every pretrained model will fit the local GPU.

When applying the skill, the assignment and supervisor constraints take precedence: research artifacts remain English, the final report uses APA 7, model and implementation approval gates remain intact, and arXiv availability must not be mislabeled as peer review. Any skill-default numeric source IDs are evidence identifiers, not substitutes for required final APA 7 citations.

Current approval state: the selected skill is installed and usable; all model/design/scale-up/publication approvals remain pending. The community search client was not executed. No dataset, pretrained weight, or additional Python dependency was downloaded.
