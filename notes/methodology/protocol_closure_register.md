# Protocol Closure Register and Decision Reconciliation

**Project:** Evaluating Retrieval Strategies for Evidence-Grounded Question Answering over Solar Photovoltaic Scientific Literature  
**Date:** 2026-10-21  
**Phase:** Protocol Closure and Consolidation (Pre-Manuscript Drafting)  
**Status:** PARTIAL RESEARCHER SIGN-OFF RECORDED — DEC-02 AND HYPOTHESIS FRAMING APPROVED; DEC-05 CANDIDATES APPROVED IN PRINCIPLE — FINAL PROTOCOL CLOSURE AND PILOT REMAIN BLOCKED  

---

## Governing Research Question (Frozen)

> *How do BM25, dense, and hybrid retrieval strategies, compared under identical corpus, question-benchmark, preprocessing, generator, prompt, and evaluation conditions, affect retrieval quality, answer quality, and evidence attribution in question answering over solar-PV scientific literature?*

*(Preserved without alteration. BM25, dense, and hybrid comparison conditions remain strictly identical across all downstream evaluation tracks.)*

---

## 1. Purpose and Scope of Protocol Closure

This document consolidates and reconciles all protocol-design decisions, methodological specifications, and audit findings accumulated across Phases 1 through 8.3 into a unified, definitive registry. Its purpose is to:
1. Provide a single point of reference for all methodological policies.
2. Resolve documentation ambiguities and contradictions across earlier notes, specifically establishing strict publication-year semantics and eliminating any possibility of silent deposit-date leakage.
3. Explicitly delineate policies that are provisionally established, policies requiring empirical pilot observation, and policies that strictly require researcher approval before authorization of real-paper discovery or benchmark construction.

---

## 2. Master Protocol Decision and Reconciliation Register

The table below consolidates all decisions across corpus design, retrieval architecture, benchmark construction, evaluation framework, and quality control.

| Decision ID | Focus Area | Current Operative Policy | Recommended Resolution | Methodological Rationale | Supporting Project Document(s) | Researcher Approval Required? | Pilot Required? | Current Status |
|---|---|---|---|---|---|---|---|---|
| **DEC-01** | Publication Period | 2024–2026 primary systematic search window. | Core systematic discovery bounded to 2024-01-01 through search execution date. Pre-2024 literature entered strictly via backward citation chaining. | Captures modern solar-PV research (TOPCon, HJT, perovskite-silicon tandems, advanced degradation modeling) while maintaining a tractable, auditable discovery scope. | `phase3_corpus_design_protocol.md` §3; `phase8_protocol_decision_register.md` §2.1; `phase8_3_final_methodological_challenge.md` §4 | **YES** | **NO** | **PROVISIONAL — PENDING RESEARCHER SIGN-OFF** |
| **DEC-02** | Foundational Chaining | Phase 8.2 rule: disjoint first/corresponding authors across citing papers, <50% middle-author overlap. | **Researcher-approved Alternative B (2026-10-21):** Pre-2024 candidate must be cited by ≥2 core (2024–2026) primary papers with distinct first authors. No author of the candidate may appear anywhere in either citing paper's author list. Review citations do not count. Record author overlap and metadata uncertainty; do not claim this proves independent labs or institutions. | Avoids dependence on unstandardized corresponding-author metadata, prevents direct candidate self-citation, and states the inference narrowly. | `phase8_2_signoff_checklist.md` §2.1; `phase8_3_final_methodological_challenge.md` §3.1; researcher decision recorded 2026-10-21 | **NO — APPROVED 2026-10-21** | **NO** | **RESEARCHER-APPROVED — OPERATIONALIZATION LOCKED** |
| **DEC-03** | Date Semantics & Precedence | `publication_year` as single integer; potential ambiguity between online and volume date. | **Strict Date Precedence:** Formal VoR Issue Year $\succ$ Online VoR Date $\succ$ Accepted Manuscript Date (if verified). **Negative Rule:** Institutional/repository deposit dates (arXiv/Zenodo) must **NEVER** substitute for publication year. Disaggregated schema fields in data dictionary. | Prevents silent deposit-date leakage where an older preprint deposited in 2024 is incorrectly classified as contemporary core literature. | `corpus_data_dictionary.md` §3; `phase8_2_signoff_checklist.md` §2.3; `phase8_3_final_methodological_challenge.md` §3.2 | **YES** | **NO** | **PROVISIONAL — PENDING RESEARCHER SIGN-OFF** |
| **DEC-04** | Discovery Sources | Multi-source strategy: OpenAlex, Crossref, Semantic Scholar, OA repositories. | Retain 4-source mix. Pinned query strings; no claims of exhaustive or complete coverage. Pinned server-side sorting syntax treated as provisional pending live API verification; client-side sorting fallback. | Multi-source reduces single-index indexing bias. Acknowledging API limits prevents unsupported coverage claims. Client-side fallback ensures deterministic rank ordering. | `corpus_acquisition_workflow.md` §3; `phase8_protocol_decision_register.md` §2.4; `phase8_3_final_methodological_challenge.md` §3.4 | **YES** | **YES** (Live API endpoint check) | **PROVISIONAL — PENDING PILOT VERIFICATION** |
| **DEC-05** | Query Registry & Known Items | Four query families (Q1–Q4) and 10 known-item papers; candidate list was previously uninstantiated. | Researcher approved the ten proposed candidates in principle on 2026-10-21, subject to final bibliographic and eligibility checks. Candidate titles, DOIs, years, first-author metadata, publisher source links, and access caveats are recorded in `phase8_2_signoff_checklist.md` §2.2.3. Replace and re-present any candidate that fails verification; do not silently substitute. Known-item sensitivity is a metadata-discovery sanity check, not corpus recall. | Makes the test executable while preserving a pre-search freeze and separating metadata discovery from lawful full-text eligibility. | `phase8_2_signoff_checklist.md` §2.2.3; `phase8_3_final_methodological_challenge.md` §3.3; researcher decision recorded 2026-10-21 | **PARTIAL — candidate set approved in principle; replacements require review** | **YES** (300-slot pilot, only after protocol closure) | **APPROVED IN PRINCIPLE — FINAL ELIGIBILITY AUDIT OPEN** |
| **DEC-06** | Document Stratification | Dual index proposed: $I_{\text{primary}}$ and $I_{\text{all}}$. Document types in dictionary lacked explicit mapping. | Primary Index ($I_{\text{primary}}$): `journal_article`, `conference_paper` only. Sensitivity Index ($I_{\text{all}}$): adds `review`, `systematic_review`. Retractions, corrections, reports excluded from retrieval chunks. Shared benchmark, prompts, generator, and metrics across both indexes. | Excludes review-article synthetic shortcuts from primary causal evaluation. Enables secondary sensitivity analysis to evaluate whether reviews introduce semantic aggregation artifacts. | `phase3_corpus_design_protocol.md` §4; `corpus_data_dictionary.md` §2; `phase8_3_final_methodological_challenge.md` §3.5 | **YES** | **NO** | **PROVISIONAL — PENDING RESEARCHER SIGN-OFF** |
| **DEC-07** | Artifact Extraction Policy | Text-first preservation (captions, tables, formulas). Image pixels excluded. | Extract text, figure captions, structured Markdown tables, and LaTeX/MathML formula representations where present in text streams. Exclude raw image pixels / raster graphics. PyMuPDF adapter interface specified. | Maintains strict text-retrieval comparison without confounding text models with vision-language multimodal architectures. Captures essential scientific tabular and mathematical data. | `phase2_retrieval_architecture_specification.md` §3; `phase8_protocol_decision_register.md` §2.7; `src/solar_rag/extractors.py` | **YES** | **YES** (20-paper extraction pilot) | **PROVISIONAL — PENDING EXTRACTION PILOT** |
| **DEC-08** | Full-Text Extraction Thresholds | OPEN pending observation. | No fabricated numerical CER/WER cutoffs. Quantitative acceptance thresholds remain **OPEN** until empirical distribution of errors is observed across a stratified 20-paper sample (5 2-col, 5 math, 5 tables, 3 conf, 2 OCR). | Arbitrary error thresholds (e.g. 1% CER) risk mass rejection of legitimate mathematical papers. Cutoffs must be empirically grounded in observed PDF extractor distributions. | `corpus_quality_control.md` §2.4; `phase8_protocol_decision_register.md` §2.8; `phase8_3_final_methodological_challenge.md` §3.6 | **YES** | **YES** (20-paper extraction pilot) | **OPEN — PENDING PILOT OBSERVATIONS** |
| **DEC-09** | Reference List Handling | Excluded from searchable chunks; metadata only. | Reference lists and bibliographies parsed into structured metadata, strictly excluded from chunking and retrieval text. | Including reference strings causes false-positive lexical BM25 retrieval based on cited paper titles rather than substantive evidence content. | `corpus_data_dictionary.md` §4; `phase8_protocol_decision_register.md` §2.9; `phase8_3_final_methodological_challenge.md` §4 | **YES** | **NO** | **PROVISIONAL — PENDING RESEARCHER SIGN-OFF** |
| **DEC-10** | Screening Calibration & Stability | Single reviewer + 10% re-screening after 14 days. | Retain single reviewer with 10% 14-day masked re-screen. **Strict Metric Demarcation:** Measures **intra-rater temporal consistency only**. Declared honestly in manuscript limitations as single-reviewer screening (no false claims of dual independent screening). | Prevents misleading reviewers regarding inter-rater reliability while establishing reproducible intra-rater stability. | `SCREENING_PROTOCOL.md` §3; `phase8_protocol_decision_register.md` §2.10; `phase8_3_final_methodological_challenge.md` §3.6 | **YES** | **YES** (10% calibration sample) | **PROVISIONAL — PENDING RESEARCHER SIGN-OFF** |
| **DEC-11** | Production Retrieval Configuration | Scaffold uses placeholder/injected dense interface and RRF fusion ($k=60$). Chunk size, overlap, top-k candidate depth OPEN. | Candidate settings (chunk size $\in \{256, 512\}$, overlap $\in \{10\%, 20\%\}$, embedding model, top-k candidate pool $k \in \{5, 10, 20\}$, RRF parameter $k_{rrf}=60$) must be formally evaluated on development benchmark split and locked before test execution. | Prevents data peeking and post-hoc hyperparameter tuning on the final test benchmark. | `phase1_experimental_design.md` §3; `phase2_retrieval_architecture_specification.md` §4–§7 | **YES** | **YES** (Development split evaluation) | **OPEN — PENDING PRODUCTION SELECTION** |
| **DEC-12** | Controlled Generation Pipeline | Shared abstract interface, example configuration template. Production model and prompt unselected. | Shared frozen generator model, fixed prompt template with strict citation schema, temperature = 0.0, identical token context budget across BM25, dense, and hybrid arms. | Guarantees that retrieval strategy is the sole independent variable. Eliminates generator capability and prompt engineering confounds. | `phase1_experimental_design.md` §3; `phase2_retrieval_architecture_specification.md` §10; `phase5_evaluation_statistical_analysis_plan.md` §2 | **YES** | **YES** (Prompt & generator smoke validation) | **OPEN — PENDING MODEL SELECTION** |
| **DEC-13** | Question Benchmark Size & Stratification | Phase 4 defines taxonomy, difficulty, answerability, and gold evidence requirements; target size (100–200 questions) provisional. | Benchmark size and category proportions (factual extraction, multi-hop synthesis, comparative analysis, unanswerable cases) remain provisional pending corpus construction and formal statistical power analysis. | Benchmark design must reflect actual corpus composition and satisfy statistical power requirements ($1-\beta \ge 0.80$ at $\alpha = 0.05$) without arbitrary question fabrication. | `phase4_benchmark_protocol.md` §4–§8; `phase5_evaluation_statistical_analysis_plan.md` §4 & §11 | **YES** | **YES** (Benchmark validation pilot) | **OPEN — PENDING CORPUS FREEZE & JUSTIFICATION** |
| **DEC-14** | Hypothesis Formulations | v0.2 hypotheses previously marked for researcher review. | Researcher approved v0.2 hypothesis framing on 2026-10-21: H1 directional for retrieval quality; downstream answer-quality and general evidence-attribution comparisons remain cautious; H4 is exploratory and non-directional. No outcome is assumed in advance. | Preserves the approved distinction between retrieval gains and downstream outcomes and avoids asserting an untested review-corpus mechanism. | `manuscript/manuscript_v0_2.md` §4; researcher decision recorded 2026-10-21 | **NO — APPROVED 2026-10-21** | **NO** | **RESEARCHER-APPROVED — HYPOTHESIS FRAMING LOCKED** |

---

## 3. Reconciliation of Prior Documentation Contradictions

### 3.1 Publication-Year Semantics and Deposit-Date Substitution
- **Contradiction Identified:** Earlier notes (`phase3_corpus_design_protocol.md` vs. `corpus_acquisition_workflow.md`) used the term "publication date" without distinguishing between online preprint posting, formal online VoR release, print issue publication, and repository deposit. This created the risk that an older manuscript deposited to arXiv or an institutional repository in 2024 would be silently included in the 2024–2026 core window.
- **Definitive Reconciliation:**
  1. `formal_publication_year` (calendar year assigned to the formal journal volume/issue) governs canonical `publication_year`.
  2. If a formal issue year is not yet assigned, a verified `online_publication_date` for the peer-reviewed Version of Record governs.
  3. An accepted manuscript qualifies **only** if it possesses a documented, publisher-verified `acceptance_date` within 2024–2026.
  4. `repository_deposit_date` (e.g., arXiv submission date, Zenodo upload date) is recorded for provenance but is **strictly prohibited from substituting for publication year**.
  5. The record schema in `corpus_data_dictionary.md` has been disaggregated to store all four date components and an explicit `year_source` field.

### 3.2 Citation Chaining and Author Independence
- **Contradiction Identified:** Phase 8.2 introduced a rule requiring disjoint "corresponding authors" between citing papers $P_1$ and $P_2$. However, neither Crossref nor Semantic Scholar APIs expose standardized corresponding-author flags. Furthermore, disjoint first and corresponding authors does not establish genuine research-group or institutional independence.
- **Definitive Reconciliation:**
  1. Replaced the unexecutable corresponding-author rule with **Alternative B**: distinct first authors ($First(P_1) \neq First(P_2)$) combined with **100% strict candidate anti-self-citation** (no candidate author may appear anywhere on the author list of either citing paper).
  2. The methodological claim is transparently scoped: it guarantees distinct lead authorship and completely eliminates self-citation, without making unverifiable claims of total institutional or laboratory independence.
  3. Review articles citing the candidate do not count toward the $\ge 2$ core citation threshold.

### 3.3 Scope Demarcation: Screening Protocol vs. Corpus Acquisition Workflow
- **Contradiction Identified:** Overlap between `SCREENING_PROTOCOL.md` (originally created for auditing the literature review on RAG systems) and `notes/methodology/corpus_acquisition_workflow.md` (governing the acquisition of solar-PV scientific papers for the experimental corpus).
- **Definitive Reconciliation:**
  1. `SCREENING_PROTOCOL.md` governs the methodological screening of literature-review papers (the background literature studying RAG, QA, and retrieval).
  2. `corpus_acquisition_workflow.md` and `phase3_corpus_design_protocol.md` govern the acquisition, screening, and ingestion of solar-PV scientific domain papers that comprise the experimental retrieval corpus.
  3. The two workflows maintain separate data directories: `screening/` for literature-review auditing, and `corpus/` (once authorized) for experimental solar-PV papers.

---

## 4. Approval Log and Remaining Decisions

### 4.1 Researcher decisions recorded on 2026-10-21
- **DEC-02 — APPROVED:** Alternative B: at least two qualifying core primary citing papers with distinct first authors and no author overlap between the earlier candidate and either citing paper. This does not establish research-group or institutional independence.
- **Hypothesis formulations — APPROVED:** Directional H1 for retrieval-level Recall@k/MRR; cautious downstream answer-quality and general attribution comparisons; H4 exploratory and non-directional.
- **DEC-05 — APPROVED IN PRINCIPLE:** The ten candidate known-item papers may be included after bibliographic and eligibility checks. Failed candidates must be flagged and replacements presented for review. No pilot has been authorized.

### 4.2 Remaining decisions and pilot-dependent items
- **Researcher sign-off still required:** DEC-01 publication window; DEC-03 publication-year precedence; DEC-04 discovery-source/query implementation; DEC-06 primary/sensitivity corpus stratification; DEC-07 text-first artifact policy; DEC-09 bibliography handling; DEC-10 single-reviewer calibration policy; DEC-11 retrieval architecture; DEC-12 generator configuration; DEC-13 benchmark size/composition. Do not infer approval from approval of DEC-02, DEC-05, or the hypotheses.
- **DEC-05 final eligibility audit:** Confirm title, DOI, year, publication type, topic, and lawful full-text availability. Metadata known-item sensitivity and full-text corpus eligibility are distinct. If a candidate fails the declared rules, pause and present a replacement for researcher review.
- **DEC-08 pilot-dependent:** Extraction quality thresholds remain open until the approved 20-paper calibration pilot is performed and documented.
- **DEC-04/DEC-05 pilot-dependent:** API endpoint behavior and deterministic sorting remain unverified until an authorized pilot.
- **DEC-11/DEC-12/DEC-13:** Production models, parameters, and benchmark size remain unresolved; freeze these before confirmatory test evaluation, using development data and prospective precision/power assessment as specified in the analysis plan.

---

## 5. Execution Gate Notice

```
=============================================================================================
EXECUTION GATE: PARTIAL SIGN-OFF RECORDED — PROTOCOL NOT YET CLOSED; DISCOVERY AND EXPERIMENT REMAIN BLOCKED
=============================================================================================
[X] PROTOCOL DESIGN CONSOLIDATED: notes/methodology/protocol_closure_register.md
[ ] REMAINING RESEARCHER SIGN-OFF: PENDING (DEC-01, DEC-03, DEC-04, DEC-06, DEC-07, DEC-09, DEC-10, DEC-11, DEC-12, DEC-13)
[X] DEC-02 CITATION CHAINING RULE APPROVED: 2026-10-21
[X] DEC-05 KNOWN-ITEM CANDIDATES APPROVED IN PRINCIPLE: FINAL ELIGIBILITY AUDIT PENDING
[X] HYPOTHESIS FORMULATIONS APPROVED: 2026-10-21
[ ] 300-SLOT DISCOVERY PILOT: BLOCKED
[ ] 20-PAPER EXTRACTION CALIBRATION PILOT: BLOCKED
[ ] REAL FULL-TEXT DOWNLOADING: BLOCKED
[ ] QUESTION BENCHMARK CONSTRUCTION: BLOCKED
[ ] CONFIRMATORY EXPERIMENT EXECUTION: BLOCKED
=============================================================================================
```

