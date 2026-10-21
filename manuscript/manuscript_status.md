# Manuscript Status and Drafting Tracker

**Project Title:** Evaluating Retrieval Strategies for Evidence-Grounded Question Answering over Solar Photovoltaic Scientific Literature  
**Document:** `manuscript/manuscript_v0_1.md`  
**Version:** v0.1 (Pre-Experimental Protocol & Conceptual Draft)  
**Date:** 2026-10-21  
**Current Status:** DRAFTING COMPLETE FOR PROTOCOL & FOUNDATIONAL SECTIONS; RESULTS & DISCUSSION SECTIONS PROVISIONALLY OUTLINED; EXPERIMENTAL EXECUTION STRICTLY BLOCKED  

---

## 1. Frozen Governing Declarations

### Frozen Title
> **Evaluating Retrieval Strategies for Evidence-Grounded Question Answering over Solar Photovoltaic Scientific Literature**

### Frozen Research Question
> **How do BM25, dense, and hybrid retrieval strategies, compared under identical corpus, question-benchmark, preprocessing, generator, prompt, and evaluation conditions, affect retrieval quality, answer quality, and evidence attribution in question answering over solar-PV scientific literature?**

---

## 2. Section-by-Section Drafting Status

| Section Number | Section Title | Current Status | Word Count (approx) | Content Summary & Scientific Grounding | Blocking Dependencies / Open Decisions |
|---|---|---|---|---|---|
| **Front Matter** | Title, Abstract, Keywords | **DRAFTED (Placeholder Abstract)** | ~250 | Title and keywords frozen. Abstract explicitly structured with background, objective, planned methods, and explicit placeholders for pending results and conclusions. | Confirmatory experiment execution required for final abstract results. |
| **Section 1** | Introduction | **DRAFTED** | ~850 | Technical motivation in solar-PV engineering; hallucination risks in technical QA; emergence of RAG; core problem of unexamined retrieval strategies; four major confounding issues in prior work; frozen research question; narrow contribution statement. | None. Fully grounded in project notes and literature review. |
| **Section 2** | Background and Related Work | **DRAFTED** | ~1,600 | Four subsections: 2.1 Retrieval Paradigms (BM25, dense, RRF); 2.2 Scientific RAG (OpenScholar, Lit3R, SQuAI, HySemRAG, LitLLM, Han et al., Wang et al., PeerQA, IRPAPERS, SciRerankBench, DeepEra, etc.); 2.3 Solar-PV AI/IR (RILS, Solar Intelligence, Solar GenAI, AskOEDI, etc.); 2.4 Tripartite Outcome Distinction (retrieval vs. answer vs. attribution). | `wang_multi-level_2026` noted as abstract-only / pending full-text verification if accessible. |
| **Section 3** | Research Gap and Contributions | **DRAFTED** | ~750 | Includes Table 1 comparative matrix detailing 7 closest comparators; specifies the exact unresolved empirical question; articulates narrowly scoped, defensible contributions without claiming unprecedented novelty. | None. Traceable to `research_gap_matrix.md` and `final_pre_freeze_assessment.md`. |
| **Section 4** | Research Questions and Hypotheses | **DRAFTED** | ~550 | Formalizes frozen primary RQ and four sub-questions (RQ1 retrieval, RQ2 answer quality, RQ3 attribution, RQ4 corpus stratification) with explicit, testable hypotheses (H1, H2, H3a–c, H4). | Hypotheses to be tested during experimental execution. |
| **Section 5** | Methodology | **DRAFTED** | ~2,100 | Eight subsections: 5.1 Study Design (within-question matched factorial design); 5.2 Corpus Construction (2024–2026 core window, strict VoR date precedence, deposit date prohibition, Alternative B anti-self-citation chaining, dual index $I_{\text{primary}}$/$I_{\text{all}}$, text-first extraction); 5.3 Question Benchmark (taxonomy, gold passages, atomic claims, tolerances, unanswerable controls); 5.4 Retrieval Architecture (BM25, dense bi-encoder, RRF hybrid); 5.5 Generation Controls (frozen LLM, prompt $\mathcal{P}$, temp=0.0, identical context budget $\mathcal{B}$); 5.6 Metrics; 5.7 Statistical Analysis (Friedman, Wilcoxon, Holm-Bonferroni, $d_z$); 5.8 Data Governance. | Production model selections and numerical extraction cutoffs marked provisional / pending pilot observation. |
| **Section 6** | Results | **EMPTY PLANNED STRUCTURE** | ~100 | Contains section outline (6.1–6.5) only. Explicitly states that no empirical data or fabricated results are reported. | **BLOCKED** pending protocol sign-off and confirmatory experiment execution. |
| **Section 7** | Discussion | **SUBSECTION OUTLINE ONLY** | ~120 | Contains outline of planned discussion subsections (7.1–7.4). No claims of demonstrated findings. | **BLOCKED** pending experimental results. |
| **Section 8** | Limitations | **DRAFTED** | ~400 | Candidly articulates six methodological limitations: single-reviewer screening intra-rater calibration, English-language publication bias, text-first exclusion of image pixels, 2024–2026 temporal scope, generator model specificity, and empirical extraction thresholds. | None. Reflects strict methodological honesty. |
| **Section 9** | Conclusion | **PROVISIONAL OUTLINE** | ~100 | Brief provisional summary of study design and intended contributions without asserting unproven results. | Final conclusions pending study outcomes. |
| **Back Matter** | Data & Code Availability, References | **DRAFTED** | ~650 | Open code repository, Zenodo archive plan, lawful access guidelines. References section contains 32 verified citations strictly matching `Solar Scientific RAG.bib`. | None. All citation keys verified. |

---

## 3. Evidence and Claim Traceability

All 50 substantive claims, methodological statements, and literature comparisons made in `manuscript_v0_1.md` are indexed in [`manuscript/evidence_and_claim_register.csv`](./evidence_and_claim_register.csv) with unique identifiers (`CLM-001` through `CLM-050`):
- **32 Claims** classified as `SUPPORTED_BY_PROJECT_SOURCE` (grounded in existing bibliography and audited notes).
- **1 Claim** classified as `NEEDS_VERIFICATION` (`CLM-017`: Wang et al., ScienceDirect full text remains unavailable; abstract snippets used).
- **15 Methodological Statements** classified as `METHOD_DECISION_PENDING` (pre-registered hypotheses, architecture settings, benchmark design, and pilot protocols).
- **2 Sections** classified as `RESULTS_PENDING` (`CLM-048`, `CLM-049`: Results and Discussion sections).

---

## 4. Methodological Decisions Requiring Researcher Approval

Before real-paper discovery, pilot execution, or experiment execution can be authorized, the researcher must formally resolve the following items in [`notes/methodology/protocol_closure_register.md`](../notes/methodology/protocol_closure_register.md):

1. **DEC-05 (Nomination of 10 Known-Item Benchmark Papers):**
   - Provide verified Titles and DOIs for 10 landmark 2024 peer-reviewed solar-PV papers across the 5 declared subdomains.
2. **DEC-02 (Citation Chaining Rule Approval):**
   - Formally approve Alternative B (Distinct First Authors + 100% Candidate Anti-Self-Citation) to replace the unexecutable "corresponding author" API assumption.
3. **DEC-08 (Extraction Quality Threshold Policy):**
   - Confirm that numerical CER/WER thresholds will be established empirically from the 20-paper calibration pilot rather than pre-declared arbitrarily.
4. **DEC-11 & DEC-12 (Production Retrieval & Generation Architecture):**
   - Approve final selections for chunk size/overlap, dense embedding model, and generator LLM.
5. **DEC-13 (Benchmark Size and Stratification):**
   - Approve the final benchmark question count and difficulty distribution.

---

## 5. Execution State and Next Steps

```
=============================================================================================
MANUSCRIPT & EXPERIMENTAL READINESS STATUS
=============================================================================================
[X] PROTOCOL CLOSURE REGISTER: notes/methodology/protocol_closure_register.md
[X] MANUSCRIPT DRAFT v0.1: manuscript/manuscript_v0_1.md (Sections 1–5, 8, Back Matter)
[X] EVIDENCE & CLAIM REGISTER: manuscript/evidence_and_claim_register.csv (50 claims)
[X] MANUSCRIPT TRACKER: manuscript/manuscript_status.md
[X] SOFTWARE UNIT TESTS: 69 / 69 passing (0 failures, 0 errors)
[X] SYNTHETIC SMOKE TEST: Passed (2 docs, 2 questions, 6 condition runs)
---------------------------------------------------------------------------------------------
[ ] RESEARCHER APPROVAL: PENDING (DEC-01 to DEC-13)
[ ] 10 KNOWN-ITEM DOIS: PENDING RESEARCHER NOMINATION
[ ] 300-SLOT DISCOVERY PILOT: BLOCKED
[ ] 20-PAPER EXTRACTION CALIBRATION PILOT: BLOCKED
[ ] REAL FULL-TEXT DOWNLOADING: BLOCKED
[ ] QUESTION BENCHMARK CONSTRUCTION: BLOCKED
[ ] CONFIRMATORY EXPERIMENT: BLOCKED
=============================================================================================
```

**Shortest Defensible Next Step:**  
Await researcher review and formal sign-off on [`protocol_closure_register.md`](../notes/methodology/protocol_closure_register.md) and receipt of the 10 known-item benchmark DOIs (DEC-05). Upon authorization, proceed to Phase 9: executing the 300-slot metadata discovery pilot and the 20-paper extraction calibration pilot.

