# Manuscript Status and Drafting Tracker

**Project Title:** Evaluating Retrieval Strategies for Evidence-Grounded Question Answering over Solar Photovoltaic Scientific Literature  
**Active Document:** `manuscript/manuscript_v0_3.md`  
**Version:** v0.3 (Researcher Decisions Recorded; Protocol Closure Still Pending)  
**Date:** 2026-10-21  
**Current Status:** DEC-02 AND HYPOTHESIS FRAMING APPROVED; DEC-05 CANDIDATES APPROVED IN PRINCIPLE; FINAL ELIGIBILITY AUDIT AND REMAINING PROTOCOL SIGN-OFFS PENDING; PILOT BLOCKED STRICTLY BLOCKED  

---

## 1. Frozen Governing Declarations

### Frozen Title
> **Evaluating Retrieval Strategies for Evidence-Grounded Question Answering over Solar Photovoltaic Scientific Literature**

### Frozen Research Question
> **How do BM25, dense, and hybrid retrieval strategies, compared under identical corpus, question-benchmark, preprocessing, generator, prompt, and evaluation conditions, affect retrieval quality, answer quality, and evidence attribution in question answering over solar-PV scientific literature?**

---

## 2. Key Scientific Audit Improvements in Version 0.2

Version 0.2 implements the comprehensive integrity audit across five core dimensions:
1. **Research Gap Narrowing:** All absolute assertions of novelty (e.g., claiming "no prior work exists") were removed. The contribution is strictly bounded as a controlled comparative evaluation within our screened evidence base (Table 1).
2. **Citation Grounding & Discrepancy Transparency:**
   - *Wang et al. (`wang_multi-level_2026`):* Explicitly noted as paywalled/inaccessible after extensive targeted retrieval attempts; abstract-only facts are reported without inferring missing experimental controls.
   - *RILS (`orabi_rag-based_2026`):* Internal corpus-count discrepancies (18,000 docs/28,800 passages in Table 1 vs. 21,000 docs/32,800 passages in §6.2) and bundled system modifications are objectively reported.
   - *OpenScholar (`asai_openscholar_2024`, `asai_synthesizing_2026`):* Count discrepancies between abstract (237M passages, 2,967 questions) and methods (234M passages, 2.2k teaser, 208 long-form expert answers) are explicitly preserved.
   - *Solar Intelligence (`singh_solar_2026`):* Corpus date discrepancies (text 1994–2026 vs. Table 1 1994–2006) are noted.
3. **Hypothesis Audit & Refinement (Task 3):**
   - *H1 (Retrieval Level):* Directional hypothesis retained strictly for evidence Recall@k and MRR.
   - *H2 (Downstream Answer Quality):* Re-framed with an explicit competing rival null hypothesis ($H2_{null}$) acknowledging that an invariant generator and matched context budget may flatten downstream answer accuracy differences.
   - *H3 (Evidence Attribution):* Narrowed H3a strictly to fine-grained numerical queries; framed general attribution (H3b) as an empirical non-directional contrast between keyword specificity and semantic context.
   - *H4 (Corpus Stratification Sensitivity):* Made non-directional and exploratory, testing whether review literature alters relative performance without dogmatically asserting dense superiority.
4. **Premature Certainty Elimination (Task 4):**
   - Explicitly labeled all provisional technical choices (chunk size, dense model candidates, generator LLM candidates, RRF $k=60$, context budgets, benchmark sample size).
   - Clarified that statistical power cannot be assumed or guaranteed prior to corpus freeze and pilot observations; outlined MDES, bootstrap intervals, and sensitivity power curves.
   - Emphasized that full-text extraction CER/WER cutoffs remain **OPEN** pending the 20-paper empirical pilot.
5. **Traceability Matrix Hardening:** Expanded [`manuscript/evidence_and_claim_register.csv`](./evidence_and_claim_register.csv) to 10 columns, documenting specific evidence locations, support levels, discrepancies, and required actions for all 50 claims.

---

## 3. Section-by-Section Readiness Breakdown

| Section Number | Section Title | Current Status | Word Count (approx) | Content Summary & Scientific Grounding | Blocking Dependencies / Open Decisions |
|---|---|---|---|---|---|
| **Front Matter** | Title, Abstract, Keywords | **DRAFTED (Placeholder Abstract)** | ~250 | Title and keywords frozen. Abstract explicitly structured with background, objective, planned methods, and explicit placeholders for pending results and conclusions. | Confirmatory experiment execution required for final abstract results. |
| **Section 1** | Introduction | **DRAFTED (Hardened)** | ~850 | Technical motivation in solar-PV engineering; hallucination risks; emergence of RAG; unexamined retrieval strategies; four major confounding issues in prior work; frozen RQ; narrow contribution statement. | None. Fully grounded in project notes and literature review. |
| **Section 2** | Background and Related Work | **DRAFTED (Hardened)** | ~1,650 | Four subsections: 2.1 Retrieval Paradigms (BM25, dense, RRF); 2.2 Scientific RAG (OpenScholar, Lit3R, SQuAI, HySemRAG, LitLLM, Han et al., Wang et al., PeerQA, IRPAPERS, etc.); 2.3 Solar-PV AI/IR (RILS, Solar Intelligence, Solar GenAI, AskOEDI, etc.); 2.4 Tripartite Outcome Distinction (retrieval vs. answer vs. attribution). | `wang_multi-level_2026` noted as abstract-only / pending full-text verification. |
| **Section 3** | Research Gap and Contributions | **DRAFTED (Hardened)** | ~750 | Includes Table 1 comparative matrix detailing 7 closest comparators; specifies the exact unresolved empirical question; articulates narrowly scoped, defensible contributions without claiming unprecedented novelty. | None. Traceable to `research_gap_matrix.md` and `final_pre_freeze_assessment.md`. |
| **Section 4** | Research Questions and Hypotheses | **DRAFTED (Hardened)** | ~600 | Formalizes frozen primary RQ and four sub-questions (RQ1 retrieval, RQ2 answer quality, RQ3 attribution, RQ4 corpus stratification) with balanced directional/rival/exploratory hypotheses. | Hypotheses awaiting formal researcher sign-off. |
| **Section 5** | Methodology | **DRAFTED (Hardened)** | ~2,150 | Eight subsections: 5.1 Design, 5.2 Corpus, 5.3 Benchmark, 5.4 Retrieval, 5.5 Generation, 5.6 Metrics, 5.7 Statistics, 5.8 Governance. Distinguishes frozen design from provisional choices and open pilot items. | Production model selections and numerical extraction cutoffs marked provisional / pending pilot observation. |
| **Section 6** | Results | **EMPTY PLANNED STRUCTURE** | ~100 | Contains section outline (6.1–6.5) only. Explicitly states that no empirical data or fabricated results are reported. | **BLOCKED** pending protocol sign-off and confirmatory experiment execution. |
| **Section 7** | Discussion | **SUBSECTION OUTLINE ONLY** | ~120 | Contains outline of planned discussion subsections (7.1–7.4). No claims of demonstrated findings. | **BLOCKED** pending experimental results. |
| **Section 8** | Limitations | **DRAFTED** | ~400 | Candidly articulates six methodological limitations: single-reviewer screening intra-rater calibration, English-language publication bias, text-first exclusion of image pixels, 2024–2026 temporal scope, generator model specificity, and empirical extraction thresholds. | None. Reflects strict methodological honesty. |
| **Section 9** | Conclusion | **PROVISIONAL OUTLINE** | ~100 | Brief provisional summary of study design and intended contributions without asserting unproven results. | Final conclusions pending study outcomes. |
| **Back Matter** | Data & Code Availability, References | **DRAFTED** | ~650 | Open code repository, Zenodo archive plan, lawful access guidelines. References section contains 32 verified citations strictly matching `Solar Scientific RAG.bib`. | None. All citation keys verified. |

---

## 4. Methodological Decisions Requiring Researcher Approval

Researcher decisions recorded on 2026-10-21:
- **DEC-02:** Alternative B approved, with the caveat that distinct first authors and candidate-author non-overlap do not prove independent research groups.
- **Hypotheses:** v0.2 framing approved: directional H1 for retrieval quality; cautious downstream answer-quality and attribution comparisons; exploratory/non-directional H4.
- **DEC-05:** Ten known-item candidates approved in principle subject to final bibliographic and eligibility checks.

Remaining decisions and gates:
1. DEC-01, DEC-03, DEC-04, DEC-06, DEC-07, DEC-09, DEC-10, DEC-11, DEC-12, and DEC-13 remain open in the master protocol closure register.
2. DEC-05 candidate eligibility must be finalized; full-text lawful access is separate from metadata discoverability. Failed candidates must be flagged for replacement review.
3. DEC-08 extraction thresholds remain open until the 20-paper calibration pilot is authorized and completed.
4. Production embedding model, chunking parameters, context budget, and generator model remain unresolved.
5. Benchmark size and composition require corpus-informed justification and prospective precision/power assessment.

## 5. Execution State and Next Steps

```
=============================================================================================
MANUSCRIPT & EXPERIMENTAL READINESS STATUS (VERSION 0.3)
=============================================================================================
[X] PROTOCOL CLOSURE REGISTER: notes/methodology/protocol_closure_register.md
[X] MANUSCRIPT DRAFT v0.3: manuscript/manuscript_v0_3.md (Researcher Decisions Recorded; Protocol Closure Pending)
[X] EVIDENCE & CLAIM REGISTER: manuscript/evidence_and_claim_register.csv (50 claims, 10 columns)
[X] MANUSCRIPT TRACKER: manuscript/manuscript_status.md
[X] SOFTWARE UNIT TESTS: 69 / 69 passing (0 failures, 0 errors)
[X] SYNTHETIC SMOKE TEST: Passed (2 docs, 2 questions, 6 condition runs)
---------------------------------------------------------------------------------------------
[X] DEC-02 CITATION CHAINING APPROVED: 2026-10-21
[X] HYPOTHESIS FRAMING APPROVED: 2026-10-21
[X] DEC-05 KNOWN-ITEM CANDIDATES APPROVED IN PRINCIPLE; FINAL ELIGIBILITY AUDIT OPEN
[ ] REMAINING PROTOCOL SIGN-OFFS: DEC-01, DEC-03, DEC-04, DEC-06, DEC-07, DEC-09, DEC-10, DEC-11, DEC-12, DEC-13
[ ] 300-SLOT DISCOVERY PILOT: BLOCKED
[ ] 20-PAPER EXTRACTION CALIBRATION PILOT: BLOCKED
[ ] REAL FULL-TEXT DOWNLOADING: BLOCKED
[ ] QUESTION BENCHMARK CONSTRUCTION: BLOCKED
[ ] CONFIRMATORY EXPERIMENT: BLOCKED
=============================================================================================
```
