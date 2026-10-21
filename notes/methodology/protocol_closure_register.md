# Protocol Closure Register and Decision Reconciliation

**Project:** Evaluating Retrieval Strategies for Evidence-Grounded Question Answering over Solar Photovoltaic Scientific Literature  
**Date:** 2026-10-21  
**Phase:** Protocol Closure and Consolidation (Pre-Manuscript Drafting)  
**Status:** PROTOCOL CLOSED — POLICY/PROCEDURE SIGN-OFF COMPLETE 2026-10-21; PILOT EXECUTION HOLD ACTIVE  

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
| **DEC-01** | Publication Period | 2024–2026 primary systematic search window. | **Researcher-approved 2026-10-21:** Core search from 2024-01-01 through search execution date; pre-2024 literature only via approved backward citation chaining. | Bounded, reproducible discovery scope. | `phase3_corpus_design_protocol.md` §3; researcher approval 2026-10-21 | **NO — APPROVED** | **NO** | **RESEARCHER-APPROVED — RULE LOCKED** |
| **DEC-02** | Foundational Chaining | Phase 8.2 rule: disjoint first/corresponding authors across citing papers, <50% middle-author overlap. | **Researcher-approved Alternative B (2026-10-21):** Pre-2024 candidate must be cited by ≥2 core (2024–2026) primary papers with distinct first authors. No author of the candidate may appear anywhere in either citing paper's author list. Review citations do not count. Record author overlap and metadata uncertainty; do not claim this proves independent labs or institutions. | Avoids dependence on unstandardized corresponding-author metadata, prevents direct candidate self-citation, and states the inference narrowly. | `phase8_2_signoff_checklist.md` §2.1; `phase8_3_final_methodological_challenge.md` §3.1; researcher decision recorded 2026-10-21 | **NO — APPROVED 2026-10-21** | **NO** | **RESEARCHER-APPROVED — OPERATIONALIZATION LOCKED** |
| **DEC-03** | Date Semantics & Precedence | `publication_year` could conflate formal issue year and online date. | **Researcher-approved 2026-10-21:** Formal VoR issue year governs; if absent, verified online VoR date; acceptance date only when publisher-verified and allowed by the inclusion rule. Repository deposit date never substitutes for publication year. Keep disaggregated date fields and `year_source`. | Prevents repository deposit-date leakage. | `corpus_data_dictionary.md` §3; researcher approval 2026-10-21 | **NO — APPROVED** | **NO** | **RESEARCHER-APPROVED — DATE SEMANTICS LOCKED** |
| **DEC-04** | Discovery Sources & Query Execution | Multi-source discovery and pinned Q1–Q4 query families. | **Researcher-approved 2026-10-21:** Use OpenAlex, Crossref, Semantic Scholar, and lawful OA repositories; log queries/parameters; make no exhaustiveness claim; deterministic client-side ordering is fallback. API pagination and server-side sorting remain pilot-verification items. | Auditable multi-source search without overstating coverage. | `corpus_acquisition_workflow.md`; researcher approval 2026-10-21 | **NO — PROCEDURE APPROVED** | **YES — endpoint behavior pilot-dependent** | **PROCEDURE APPROVED; TECHNICAL VERIFICATION PENDING PILOT** |
| **DEC-05** | Query Registry & Known Items | Four query families (Q1–Q4) and ten known-item papers. | **Researcher-approved and frozen 2026-10-21:** KI-10 replaced by “Organic Solar Modules with Good Stability under Ultraviolet Irradiation” (DOI 10.1002/solr.202400101). Ten metadata-discovery targets are mapped to five declared subdomains with two items each. Known-item sensitivity tests metadata discovery, not total corpus recall. Lawful full-text access is checked separately during corpus screening; inaccessible items are not ingested. | Creates an executable, pre-frozen discovery sanity check and separates metadata discovery from full-text corpus eligibility. | `phase8_2_signoff_checklist.md` §2.2.3; publisher metadata; researcher approval 2026-10-21 | **NO — DECISION RESOLVED** | **YES — only after separate pilot authorization** | **CLOSED — BENCHMARK FROZEN; FULL-TEXT SCREENING SEPARATE** |
| **DEC-06** | Document Stratification | Dual index: primary research and sensitivity corpus including reviews. | **Researcher-approved 2026-10-21:** `I_primary` includes eligible primary journal articles and peer-reviewed conference papers; `I_all` adds eligible reviews/systematic reviews. Retractions and corrections excluded from chunks; evaluation conditions remain matched. | Separates primary evaluation from review sensitivity analysis. | `phase3_corpus_design_protocol.md` §4; `corpus_data_dictionary.md` §2; researcher approval 2026-10-21 | **NO — APPROVED** | **NO** | **RESEARCHER-APPROVED — INDEX RULE LOCKED** |
| **DEC-07** | Text-First Artifact Policy | Text-first extraction of article text, captions, tables, and available math representations. | **Researcher-approved 2026-10-21:** Retain text, captions, structured tables, available LaTeX/MathML; do not index raw image pixels; log extraction failures and OCR provenance. Threshold values remain pilot-dependent under DEC-08. | Preserves evidence-bearing text and exposes extraction limits. | `corpus_data_dictionary.md`; extraction workflow; researcher approval 2026-10-21 | **NO — APPROVED** | **YES — calibration pilot for threshold estimates** | **RESEARCHER-APPROVED — EXTRACTION SCOPE LOCKED** |
| **DEC-08** | Extraction Quality Thresholds | Numerical CER/WER thresholds were intentionally left open. | **Researcher-approved procedure 2026-10-21:** Set numeric extraction-quality thresholds from the stratified 20-paper calibration pilot; report observed distributions, rationale, and exclusions. Values remain pending that pilot. | Avoids arbitrary cutoffs. | `phase8_2_signoff_checklist.md`; extraction workflow; researcher approval 2026-10-21 | **NO — PROCEDURE APPROVED** | **YES — 20-paper calibration pilot** | **PROCEDURE APPROVED; NUMERIC VALUES PILOT-DEPENDENT** |
| **DEC-09** | Reference List Handling | Bibliographies could contaminate lexical retrieval if included in chunks. | **Researcher-approved 2026-10-21:** Parse references to structured metadata only; exclude bibliography text from searchable chunks. | Prevents false lexical matching on reference strings. | `corpus_data_dictionary.md` §4; researcher approval 2026-10-21 | **NO — APPROVED** | **NO** | **RESEARCHER-APPROVED — REFERENCE RULE LOCKED** |
| **DEC-10** | Screening Calibration & Stability | Single reviewer with 10% masked re-screen after 14 days. | **Researcher-approved 2026-10-21:** Retain the single-reviewer workflow; report the delayed masked re-screen as intra-rater temporal consistency only, not inter-rater reliability. | Transparent treatment of reviewer limitations. | `SCREENING_PROTOCOL.md` §3; researcher approval 2026-10-21 | **NO — APPROVED** | **YES — calibration execution** | **RESEARCHER-APPROVED — CALIBRATION POLICY LOCKED** |
| **DEC-11** | Retrieval Architecture | BM25, dense, and hybrid retrieval are the three comparison arms. | **Researcher-approved selection procedure 2026-10-21:** Select dense embedding, chunking, fusion, and index parameters using the pre-specified development procedure before confirmatory evaluation; keep arms matched on corpus, benchmark, generator, prompt, and context budget. Actual values remain open until development. | Avoids confirmatory test-set tuning. | `phase1_experimental_design.md`; `phase2_retrieval_architecture_specification.md`; researcher approval 2026-10-21 | **NO — SELECTION PROCEDURE APPROVED** | **YES — development/smoke validation** | **PROCEDURE APPROVED; PARAMETERS PENDING DEVELOPMENT** |
| **DEC-12** | Generator Configuration | One fixed generator is shared across retrieval arms. | **Researcher-approved selection procedure 2026-10-21:** Choose one accessible generator through the pre-specified feasibility/development procedure; freeze model/version, prompt, decoding parameters, and context budget before confirmatory evaluation. | Isolates retrieval strategy as the primary independent variable. | `phase1_experimental_design.md`; `phase2_retrieval_architecture_specification.md`; researcher approval 2026-10-21 | **NO — SELECTION PROCEDURE APPROVED** | **YES — generator/prompt smoke validation** | **PROCEDURE APPROVED; MODEL PENDING DEVELOPMENT** |
| **DEC-13** | Question Benchmark Size & Stratification | Benchmark size and category proportions were provisional. | **Researcher-approved selection procedure 2026-10-21:** Set final size/mix after corpus freeze using the existing taxonomy, gold-evidence feasibility, and prospective precision/power justification. Do not tune the benchmark to favor a retrieval method. | Grounds benchmark size in corpus and analysis needs. | `phase4_benchmark_protocol.md` §4–§8; `phase5_evaluation_statistical_analysis_plan.md`; researcher approval 2026-10-21 | **NO — SELECTION PROCEDURE APPROVED** | **YES — benchmark validation pilot** | **PROCEDURE APPROVED; FINAL SIZE/MIX PENDING CORPUS** |
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
- **DEC-05 — CLOSED:** The ten known-item metadata targets are frozen in `phase8_2_signoff_checklist.md` §2.2.3, including the approved KI-10 replacement. Five subdomains have two targets each. This freezes the metadata-discovery test; lawful full-text access remains a separate inclusion condition for the experimental corpus. No pilot has been authorized.

### 4.2 Remaining decisions and pilot-dependent items
- **Protocol closure audit: PASS.** DEC-01 through DEC-14 policies/procedures have researcher sign-off; the known-item benchmark is frozen and balanced at two items per each of five subdomains. Pilot-dependent values remain deliberately unresolved under their approved decision procedures.
- **Corpus-screening condition:** For every discovered paper, verify publication type, topic, eligibility, and lawful full-text access before ingestion. A known-item can be counted for metadata discovery without being eligible for corpus ingestion.
- **Execution hold:** The researcher explicitly instructed on 2026-10-21 not to run any pilot yet. Both the 300-slot discovery pilot and 20-paper extraction calibration pilot remain blocked pending separate authorization.
- **DEC-08 pilot-dependent:** Extraction quality thresholds remain open until the approved 20-paper calibration pilot is performed and documented.
- **DEC-04/DEC-05 pilot-dependent:** API endpoint behavior and deterministic sorting remain unverified until an authorized pilot.
- **DEC-11/DEC-12/DEC-13:** Production models, parameters, and benchmark size remain unresolved; freeze these before confirmatory test evaluation, using development data and prospective precision/power assessment as specified in the analysis plan.

---

## 5. Execution Gate Notice

```
=============================================================================================
EXECUTION GATE: PROTOCOL CLOSED — NO PILOT AUTHORIZED YET; EXECUTION HOLD ACTIVE
=============================================================================================
[X] PROTOCOL FORMALLY CLOSED: 2026-10-21
[X] DEC-01–DEC-14 POLICY/PROCEDURE SIGN-OFF RECORDED
[X] DEC-05 KNOWN-ITEM METADATA BENCHMARK FROZEN: 10 ITEMS / 5 SUBDOMAINS / 2 ITEMS PER SUBDOMAIN
[X] KI-10 REPLACEMENT APPROVED AND RECORDED: DOI 10.1002/solr.202400101
[!] USER EXECUTION HOLD: DO NOT RUN ANY PILOT UNTIL SEPARATE AUTHORIZATION
[ ] 300-SLOT DISCOVERY PILOT: NOT RUN; BLOCKED BY USER HOLD
[ ] 20-PAPER EXTRACTION CALIBRATION PILOT: NOT RUN; BLOCKED BY USER HOLD
[ ] REAL FULL-TEXT DOWNLOADING: NOT AUTHORIZED
[ ] QUESTION BENCHMARK CONSTRUCTION: NOT AUTHORIZED
[ ] CONFIRMATORY EXPERIMENT EXECUTION: BLOCKED
=============================================================================================
```

