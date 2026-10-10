# Phase 8.1 — Methodological Challenge and Sign-Off Preparation Report

**Project:** Solar Scientific RAG Literature Review  
**Date:** 2026-10-09  
**Phase:** Phase 8.1 — Methodological Challenge & Protocol Audit  
**Status:** PROTOCOL AUDIT COMPLETE — REAL-PAPER DISCOVERY & EXPERIMENTAL EXECUTION BLOCKED  

---

## Governing Research Question (Frozen)

> *How do BM25, dense, and hybrid retrieval strategies, compared under identical corpus, question-benchmark, preprocessing, generator, prompt, and evaluation conditions, affect retrieval quality, answer quality, and evidence attribution in question answering over solar-PV scientific literature?*

---

## 1. Executive Summary & Objective

This document conducts a critical methodological stress-test of the Phase 8 Corpus Acquisition and Curation Protocol. It addresses potential sources of selection bias, ambiguity in citation chaining and review stratification, single-reviewer calibration constraints, publication date precedence, pilot search design, and extraction calibration. 

No real scientific papers have been discovered, scraped, downloaded, or ingested. Software readiness is validated; scientific corpus readiness and confirmatory experiment readiness remain **BLOCKED**.

---

## 2. Critical Methodological Challenges & Operational Specifications

### 2.1 Citation Chaining Operationalization (DEC-02 Challenge)

#### Ambiguity & Risk
The provisional rule in DEC-02 allows pre-2024 foundational studies to enter the candidate pool if cited by $\ge 2$ distinct eligible core (2024–2026) papers. However, without strict operational rules, this mechanism is vulnerable to:
1. *Author self-citation inflation:* A single research group writing two 2024 papers citing their own 2020 paper.
2. *Review citation leakage:* Broad review articles citing hundreds of papers, pulling in non-foundational earlier literature.
3. *Target leakage / circularity:* Using Phase 4 benchmark questions or desired answers to selectively chain earlier papers.

#### Operationalized Rules
1. **Independent Citing Papers Requirement:**
   - The $\ge 2$ citing papers must be distinct, eligible core (2024–2026) records.
   - The citing papers must have **disjoint primary authorship** (different first author and different corresponding author) to prevent self-citation clustering from satisfying the threshold.
2. **Document Type of Citing Papers:**
   - Citing papers must be original primary research articles (`document_type in {"journal_article", "conference_paper"}`).
   - Citations appearing in review articles (`document_type="review"`) do **not** count toward the $\ge 2$ threshold.
3. **Contextual Citation Requirement:**
   - The pre-2024 work must be cited in the introduction, theory, or methodology section as a foundational method, model, or baseline mechanism—not merely in a generic bibliography list.
4. **Retrieval & Audit Trail:**
   - Citation links must be retrieved from structured Crossref/OpenAlex/Semantic Scholar reference graphs and logged in an immutable `citation_chaining_log.jsonl` record:
     ```json
     {
       "candidate_doi": "10.1016/j.solmat.2020.100000",
       "citing_core_records": ["doc-core-001", "doc-core-089"],
       "citing_dois": ["10.1016/j.solmat.2024.112001", "10.1109/JPHOTOV.2024.335002"],
       "disjoint_authorship_verified": true,
       "foundational_earlier_tag": true,
       "auditor": "operator_id",
       "timestamp_utc": "2026-10-09T09:00:00Z"
     }
     ```
5. **Handling Missing Citation Metadata:**
   - If structured citation metadata is unavailable from API sources, manual inspection of the core paper's reference list is required and must be logged. If fewer than 2 independent verified citations exist, the candidate is excluded (`outside_publication_period`).

---

### 2.2 Review-Article Stratification & Retrieval Index Separation (DEC-06 Challenge)

#### Ambiguity & Risk
Review articles present a fundamental challenge to retrieval experiments. Because reviews synthesize dozens of experimental studies into dense summaries, their passages contain high keyword density and broad conceptual coverage. If reviews are indexed in the primary retrieval corpus:
- Lexical (BM25) and dense retrievers may disproportionately retrieve review passages rather than primary experimental evidence.
- Multiple-document question answering benchmarks become confounded because a single review passage can act as an artificial shortcut for questions intended to test cross-paper synthesis.

#### Operationalized Policy & Index Separation
```
+-------------------------------------------------------------------------------+
|                             CANONICAL CORPUS REPO                             |
|  (All eligible, screened, quality-controlled, licensed solar-PV literature)    |
+---------------------------------------+---------------------------------------+
                                        |
                   +--------------------+--------------------+
                   |                                         |
                   v                                         v
+-------------------------------------+   +-------------------------------------+
|      PRIMARY RETRIEVAL INDEX        |   |    SENSITIVITY / SECONDARY INDEX    |
|            (I_primary)              |   |               (I_all)               |
|                                     |   |                                     |
|  Eligible Primary Research Only:    |   |  All Eligible Literature:           |
|  - journal_article                  |   |  - journal_article                  |
|  - conference_paper                 |   |  - conference_paper                 |
|                                     |   |  - review (tagged)                  |
|  *USED FOR FROZEN CONFIRMATORY RQ*  |   |  *USED FOR SECONDARY SENSITIVITY*   |
+-------------------------------------+   +-------------------------------------+
```

1. **Primary Experimental Index ($I_{\text{primary}}$):**
   - Contains **only** primary research documents (`document_type in {"journal_article", "conference_paper"}`).
   - Review articles are **excluded** from $I_{\text{primary}}$.
   - All primary confirmatory evaluations for the frozen research question (BM25 vs. Dense vs. Hybrid) execute against $I_{\text{primary}}$.
2. **Secondary / Sensitivity Index ($I_{\text{all}}$):**
   - Contains both primary research and review articles (`document_type="review"`).
   - Used exclusively for secondary sensitivity analysis to answer: *Does the inclusion of review articles alter the relative ranking or performance gap between BM25, dense, and hybrid retrieval?*
3. **Data Dictionary Alignment:**
   - `document_type` strictly takes controlled values: `journal_article`, `conference_paper`, `review`, `methodological_article`.

---

### 2.3 Single-Reviewer Screening, Intra-Rater Calibration & Limitations (DEC-10 Challenge)

#### Methodological Reality
When staffing permits only a single primary screener, claiming independent double-screening or inter-rater reliability (e.g. Cohen's kappa across dual raters) is scientifically false. The protocol must transparently state this constraint and implement rigorous intra-rater calibration.

#### Operationalized Calibration Protocol
1. **Primary Screening Stage:**
   - All candidate records from discovery queries are screened by the primary operator using the 14-code exclusion taxonomy.
2. **10% Stratified Calibration Sample:**
   - Upon completion of primary screening, a pseudo-random sample of exactly 10% of all screened records is drawn (using a seeded, deterministic PRNG).
   - Stratification ensures proportional representation across:
     - `include_core`
     - `include_context`
     - `potentially_relevant`
     - `exclude` (across top exclusion reasons)
3. **Temporal Washout Interval:**
   - Re-screening occurs after a minimum **14-day washout period** following primary screening to minimize recall bias.
4. **Masked Re-Screening:**
   - The operator re-screens the 10% calibration sample with initial decisions, notes, and exclusion codes fully masked.
5. **Comparison & Discrepancy Metric:**
   - Re-screened records are compared across: `screening_status`, `relevance_decision`, `overlap_level`, and `exclusion_reason`.
   - The protocol measures **Intra-Rater Percentage Agreement** and **Intra-Rater Cohen's Kappa ($\kappa_{\text{intra}}$)**.
   - If agreement is $<95\%$ or $\kappa_{\text{intra}} < 0.85$, all borderline decisions (`potentially_relevant`) must undergo mandatory full-text review.
6. **Mandatory Reporting Statement in Study Artifacts:**
   > *"Screening was conducted by a single investigator. To ensure procedural fidelity and quantify temporal screening stability, a 10% stratified random sample was re-screened under masked conditions after a 14-day washout period. Intra-rater agreement was [X]%, with Cohen's kappa = [Y]. Single-reviewer screening is recognized as a study limitation."*

---

### 2.4 Publication Date Deterministic Precedence (DEC-03 Challenge)

#### Conflict Resolution Hierarchy
When conflicting dates appear across discovery engines (e.g. Crossref shows 2024, publisher landing page shows online-first November 2023, OpenAlex shows 2023):

```
+-----------------------------------------------------------------------------+
|                      DATE RESOLUTION PRECEDENCE ORDER                       |
+-----------------------------------------------------------------------------+
| Priority 1: Formal Version of Record (VoR) Journal Volume/Issue Year        |
|             (Authoritative metadata from Crossref / official publisher)      |
|                                                                             |
| Priority 2: Online-First VoR Publication Year                               |
|             (Used only if no journal volume/issue has been assigned yet)    |
|                                                                             |
| Priority 3: Accepted Manuscript Repository Year                             |
|             (Used only for lawful repository copies where VoR is absent)    |
|                                                                             |
| Priority 4: Excluded / Anomaly Logged                                       |
|             (Preprints without peer review are excluded under Section 4.2)  |
+-----------------------------------------------------------------------------+
```

1. **Deterministic Rule:**
   - If an article has a formal 2024 journal issue assignment, `publication_year = 2024` regardless of 2023 online-first availability.
   - `online_publication_date` and `issue_publication_date` are recorded as distinct ISO-8601 strings in candidate metadata.
2. **Ambiguity Handling:**
   - If publication year cannot be determined from authoritative metadata or publisher landing pages, the record is flagged with `publication_year = None` and logged in `date_anomalies.csv`. Fabricating dates is strictly prohibited.

---

### 2.5 Pre-Ingestion Pilot-Search Design (DEC-04 / DEC-05 Challenge)

To evaluate search source coverage, query sensitivity, and metadata completeness without collecting the actual corpus, the following pilot search protocol is specified:

#### Pilot Search Execution Specifications
- **Target Execution Scope:** Execute the 4 query families (Q1–Q4) against OpenAlex API, Crossref API, and Semantic Scholar API, capturing exactly **top 25 metadata records** per query per source ($4 \times 3 \times 25 = 300$ candidate metadata records).
- **Evaluation Metrics (To be calculated without text scraping):**
  1. *Source-Specific Retrieval Counts:* Gross hits returned per source.
  2. *Cross-Source Overlap Rate:* Jaccard similarity of normalized DOIs across OpenAlex, Crossref, and Semantic Scholar.
  3. *Metadata Completeness:* Percentage of records containing valid title, authors, DOI, publication year, abstract, and open-access license URL.
  4. *Known-Item Sensitivity:* Verification that 10 pre-identified landmark 2024–2025 solar-PV benchmark papers appear in the top-25 result sets.
  5. *Open-Access Full-Text Eligibility:* Percentage of candidate records with verified direct open-access PDF links vs. subscription paywalls.

---

### 2.6 20-Paper Text Extraction Calibration Pilot (DEC-08 Challenge)

#### Selection Stratum for 20 Representative PDFs
The 20-paper calibration sample must deliberately stress the extraction pipeline across structural and layout edge cases:

| Stratum ID | Document Layout & Content Characteristics | Target Count | Rationale |
|---|---|---|---|
| **STRAT-A** | Standard 2-column peer-reviewed research papers (Elsevier, IEEE, Wiley) | 5 | Baseline reading order, multi-column paragraph reflow |
| **STRAT-B** | Heavy mathematical & device physics papers (perovskite drift-diffusion, quantum efficiency) | 5 | LaTeX/MathML inline & display equation fidelity |
| **STRAT-C** | Data-dense experimental papers with complex nested tables & supplementary callouts | 5 | Row/column integrity, markdown table conversion |
| **STRAT-D** | Conference proceedings with dense graphics and complex figure caption layouts (EU PVSEC, IEEE PVSC) | 3 | Figure caption separation, non-prose suppression |
| **STRAT-E** | Legacy or scanned PDF requiring OCR processing | 2 | Character error rate (CER), font ligature recovery |

#### Measured Pilot Metrics & Threshold Resolution
- **Prose Reading Order:** Percentage of paragraphs with intact reading order.
- **Table Structural Accuracy:** Percentage of tables converted to readable structured text vs. fallback to caption-only.
- **Equation Syntax Preservation:** Percentage of mathematical formulas converted to valid LaTeX/MathML vs. image placeholders.
- **Figure Caption Completeness:** Percentage of figure captions extracted.
- **OCR Character Error Rate (CER):** Measured against manually verified ground truth for 10 sample pages.
- **Outcome:** Empirical distributions from this 20-paper pilot will be used to freeze the numerical thresholds for `extraction_status` (`successful`, `partial`, `failed`).

---

## 3. Comprehensive Consistency Audit Across Protocol Documents

| Protocol Document | Cross-Checked Element | Consistency Finding | Action Taken / Status |
|---|---|---|---|
| [`notes/methodology/corpus_acquisition_workflow.md`](./corpus_acquisition_workflow.md) | Query Families & Date Policies | Consistent with DEC-01, DEC-05 | Updated with Section 20 references. |
| [`notes/methodology/corpus_data_dictionary.md`](./corpus_data_dictionary.md) | Controlled Enums (`screening_status`, `document_type`, etc.) | Fully aligned with `src/solar_rag/corpus_workflow.py` validation constants. | **VERIFIED**. |
| [`notes/methodology/corpus_quality_control.md`](./corpus_quality_control.md) | QC sampling & Retraction Triggers | Review triggers include `corrected` and `review_required`. | **VERIFIED**. |
| [`SCREENING_PROTOCOL.md`](../../SCREENING_PROTOCOL.md) | Controlled screening decisions | `relevance_decision`, `overlap_level`, `confidence` fully match data dictionary. | **VERIFIED**. |
| [`src/solar_rag/corpus_workflow.py`](../../src/solar_rag/corpus_workflow.py) | Python validation implementation | 69 unit tests passing cleanly; enum checks strictly enforced. | **VERIFIED**. |

---

## 4. Methodological Decision Status Register (Post-Challenge)

```
========================================================================================================
POST-CHALLENGE PROTOCOL STATUS REGISTER
========================================================================================================
ID     Decision Topic                     Status       Permitting Closure Condition
--------------------------------------------------------------------------------------------------------
DEC-01 Core Publication Window (24–26)    PROVISIONAL  Final search execution date recorded
DEC-02 Pre-2024 Algorithmic Chaining      PROVISIONAL  Disjoint authorship verification rule signed off
DEC-03 VoR Date Precedence                PROVISIONAL  Deterministic precedence rule adopted
DEC-04 Multi-Source Discovery Mix         PROVISIONAL  Pre-ingestion pilot search evaluated
DEC-05 Versioned Query Registry (Q1–Q4)   PROVISIONAL  API query strings frozen
DEC-06 Review Article Index Stratification PROVISIONAL Primary (I_primary) vs Sensitivity (I_all) locked
DEC-07 Text-First Artifact Preservation    PROVISIONAL  LaTeX/MathML caption-first policy locked
DEC-08 OCR Numerical Quality Thresholds   OPEN         20-paper extraction calibration pilot executed
DEC-09 Reference List Chunk Exclusion      PROVISIONAL  Metadata-only reference parsing locked
DEC-10 Single-Reviewer 10% Calibration    PROVISIONAL  Intra-rater 14-day protocol locked
========================================================================================================
```

---

## 5. Researcher Sign-Off Checklist

Before real-paper discovery may be authorized, the lead researcher must review and sign off on the following 8 items:

- [ ] **1. Research Question Freeze Confirmation:** Confirm that the three-arm comparison (BM25, Dense, Hybrid) remains the sole manipulated variable under shared controls.
- [ ] **2. Core Window Approval:** Confirm the 2024–2026 core discovery window and the formal Version of Record year precedence rule.
- [ ] **3. Citation Chaining Safeguards:** Approve the rule requiring $\ge 2$ independent citing primary research papers with disjoint authorship for any pre-2024 study.
- [ ] **4. Primary Index Review Exclusion:** Approve the separation of the Primary Retrieval Index ($I_{\text{primary}}$: primary papers only) from the Secondary Sensitivity Index ($I_{\text{all}}$: including reviews).
- [ ] **5. Single-Reviewer Limitation Acceptance:** Acknowledge single-reviewer screening as a stated limitation and approve the 10% masked re-screening protocol with a 14-day washout.
- [ ] **6. Query Registry Families:** Approve the 4 search query families (Q1: Broad Identity, Q2: Systems/Degradation, Q3: Materials/Devices, Q4: Forecasting/Diagnostics).
- [ ] **7. Text-First Representation Policy:** Approve the exclusion of raw image pixels and the preservation of table/figure captions and LaTeX/MathML mathematical notation.
- [ ] **8. Extraction Pilot Execution Authorization:** Authorize the execution of the 20-paper PDF extraction pilot to establish empirical numerical thresholds for DEC-08.

---

## 6. Readiness and Authorization Verdict

- **Phase 8.1 Methodological Challenge:** **COMPLETE**
- **Real-Paper Discovery Authorization:** **NOT AUTHORIZED / BLOCKED** (Awaiting researcher sign-off checklist and pilot executions).
- **Scientific Corpus Readiness:** **BLOCKED**
- **Confirmatory Experiment Readiness:** **BLOCKED**

