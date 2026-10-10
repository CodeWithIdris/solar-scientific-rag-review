# Phase 8.2 — Final Corpus Protocol Consistency and Sign-Off Gate

**Project:** Solar Scientific RAG Literature Review  
**Date:** 2026-10-10  
**Phase:** Phase 8.2 — Protocol Consistency Audit & Formal Sign-Off Gate  
**Status:** PROTOCOL FINALIZATION COMPLETE — REAL-PAPER DISCOVERY & PILOT SEARCHES BLOCKED PENDING RESEARCHER SIGN-OFF  

---

## Governing Research Question (Frozen)

> *How do BM25, dense, and hybrid retrieval strategies, compared under identical corpus, question-benchmark, preprocessing, generator, prompt, and evaluation conditions, affect retrieval quality, answer quality, and evidence attribution in question answering over solar-PV scientific literature?*

---

## 1. Objective and Scope

This document provides the definitive, ambiguity-free methodological specification for the Solar-PV Scientific Literature Corpus Protocol. It resolves all remaining documentation questions regarding:
1. Citation chaining and disjoint authorship definitions for pre-2024 literature.
2. Pilot-search accounting ($N_{\text{slots}}$, $N_{\text{raw}}$, $N_{\text{unique}}$, $N_{\text{duplicate}}$, $N_{\text{eligible}}$) and predefined known-item benchmark papers.
3. Publication date precedence hierarchy and safeguards against deposit date substitution.
4. Strict document-type boundaries for the Primary Index ($I_{\text{primary}}$) versus Sensitivity Index ($I_{\text{all}}$).
5. Comprehensive consistency alignment across protocol documents.
6. A formal, itemized Researcher Sign-Off Matrix.

**Strict Gate Notice:** No real papers have been searched, scraped, or ingested. Software readiness is verified; scientific corpus readiness remains **BLOCKED**.

---

## 2. Technical and Methodological Specifications

### 2.1 Citation Chaining Operationalization (DEC-02)

#### 2.1.1 Disjoint Authorship Definition
To prevent author self-citation clusters from qualifying older papers while avoiding the exclusion of legitimate foundational studies in collaborative subfields, the concept of **disjoint authorship** is formally operationalized as follows:

1. **Lead Leadership Separation (Mandatory):**
   $$\{FirstAuthor(P_1), CorrespAuthor(P_1)\} \cap \{FirstAuthor(P_2), CorrespAuthor(P_2)\} = \emptyset$$
   The primary leadership (first author and corresponding author) of Citing Core Paper 1 ($P_1$) and Citing Core Paper 2 ($P_2$) must be completely disjoint.
2. **Candidate Independence / No Self-Citation (Mandatory):**
   $$\{Authors(Candidate)\} \cap \{FirstAuthor(P_1), CorrespAuthor(P_1), FirstAuthor(P_2), CorrespAuthor(P_2)\} = \emptyset$$
   Neither citing paper may be lead-authored or correspond-authored by any author of the pre-2024 candidate paper.
3. **Middle-Author Overlap Ceiling:**
   In specialized subfields or large international testing consortia (e.g. NREL/Fraunhofer measurement groups), middle co-authors frequently overlap. To balance independence with real-world scientific collaboration:
   - Middle co-authors may overlap only if the overlapping authors constitute $<50\%$ of the author list of both citing papers.
   - If middle-author overlap $\ge 50\%$, the two papers are considered a single collaborative cluster and count as only **1 citing credit**.
4. **Distinction from "Completely Disjoint Author Lists":**
   Requiring 100% disjoint author lists across large author teams (e.g. 15-author consortia with a shared institutional facility director) introduces severe false-negative risks, inappropriately excluding landmark foundational studies (e.g., Green efficiency tables, Jordan degradation rate syntheses). The primary leadership separation plus middle-author ceiling eliminates self-citation bias while preserving legitimate domain consensus.

#### 2.1.2 Threshold Preservation
The threshold of **$\ge 2$ independent citing primary research papers** (2024–2026 core) is preserved without modification. Citing mentions in review articles (`document_type="review"`) do **not** count toward this threshold.

#### 2.1.3 Missing Metadata & Audit Trail
- If API citation metadata or author lists are truncated or missing (e.g., "et al."), manual full-text PDF inspection of the citing papers is required and logged.
- If author disambiguation remains unverifiable, the citation cannot count toward the threshold.
- Every pre-2024 paper accepted via this rule must be logged in `citation_chaining_audit.jsonl` with:
  `candidate_doi`, `citing_dois`, `author_overlap_percentage`, `verification_timestamp_utc`, and `auditor_id`.

---

### 2.2 Pilot-Search Accounting and Predefined Known-Item Benchmark (DEC-04 / DEC-05)

#### 2.2.1 Distinct Search Metric Accounting
The pre-ingestion pilot search must strictly distinguish between the following five counts to avoid misleading volume claims:

```
+-----------------------------------------------------------------------------------------+
|                                SEARCH COUNT DEFINITIONS                                 |
+-----------------------------------------------------------------------------------------+
| 1. Raw Retrieval Slots (N_slots):                                                       |
|    Total theoretical query capacity (4 query families x 3 sources x 25 rank positions   |
|    = 300 slots).                                                                        |
|                                                                                         |
| 2. Raw Source Records (N_raw):                                                          |
|    Total bibliographic records returned across API calls (<= N_slots).                  |
|                                                                                         |
| 3. Unique Candidate Papers (N_unique):                                                  |
|    Distinct scholarly works remaining after de-duplication across sources via           |
|    normalized DOI and canonical title/year identities.                                  |
|                                                                                         |
| 4. Duplicate Records (N_duplicate):                                                     |
|    Redundant cross-source or multi-query records: N_duplicate = N_raw - N_unique.       |
|                                                                                         |
| 5. Eligible Papers (N_eligible):                                                        |
|    Unique candidates meeting all screening criteria and having lawful full text.        |
+-----------------------------------------------------------------------------------------+
```

#### 2.2.2 Deterministic Query Execution & Ordering
To guarantee exact reproducibility across runs:
- **OpenAlex API:** Explicit parameter string `sort=publication_date:desc,id:asc`, `per-page=25`, `page=1`, with API endpoint version recorded.
- **Crossref API:** Explicit parameter string `rows=25&offset=0&sort=published&order=desc`, polite header (`mailto`), and timestamp logged.
- **Semantic Scholar API:** Explicit parameter string `limit=25&offset=0&fields=title,authors,year,doi,abstract,venue,isOpenAccess,openAccessPdf`.
- Raw API JSON responses and their SHA-256 hashes must be preserved in `pilot_search_raw/`.

#### 2.2.3 Predefined 10 Known-Item Landmark Papers
The 10 landmark known-item benchmark papers are specified *prior* to pilot search execution to test query sensitivity without post-hoc selection:

| Item ID | Topic Subdomain | Target Work & Landmark Scope | Representative Publication Venue | Publication Window |
|---|---|---|---|---|
| **KI-01** | Perovskite-Silicon Tandem | 2-terminal tandem efficiency limits and operational stability | *Nature Energy* / *Science* | 2024 |
| **KI-02** | TOPCon Silicon Cells | Contact passivation and metallization degradation kinetics | *Solar Energy Materials & Solar Cells* | 2024 |
| **KI-03** | Silicon Heterojunction (HJT) | Damp heat stability and light/elevated temperature degradation | *Progress in Photovoltaics* | 2024 |
| **KI-04** | Bifacial PV Modules | Rear-side irradiance modeling and albedo sensitivity | *IEEE Journal of Photovoltaics* | 2024 |
| **KI-05** | Perovskite Degradation | Accelerated aging protocols (ISOS) and moisture encapsulation | *ACS Energy Letters* | 2024 |
| **KI-06** | Inverter & System Reliability | Power electronic thermal stress and IGBT failure modes | *Solar Energy* | 2024 |
| **KI-07** | PV Output Forecasting | Physical & ML hybrid solar irradiance prediction models | *Applied Energy* | 2024 |
| **KI-08** | Potential-Induced Degradation | PID-polarization and PID-shunting in high-voltage strings | *Progress in Photovoltaics* | 2024 |
| **KI-09** | Organic PV (OPV) | Non-fullerene acceptor degradation and indoor PV performance | *Advanced Energy Materials* | 2024 |
| **KI-10** | Techno-Economic / LCA | Lifetime greenhouse gas footprint and LCOE for utility-scale PV | *Renewable and Sustainable Energy Reviews* | 2024 |

#### 2.2.4 Known-Item Sensitivity Calculation
$$\text{Sensitivity}_{\text{known-item}} = \left( \frac{\text{Count of Predefined Known Items in Candidate Set}}{10} \right) \times 100\%$$
Reported overall and broken down by source (OpenAlex, Crossref, Semantic Scholar). No claims of complete domain coverage may be made.

---

### 2.3 Publication Date Precedence Hierarchy (DEC-03)

#### 2.3.1 Date Category Definitions
1. **Formal Publication Year ($Y_{\text{formal}}$):** The official calendar year assigned to the final journal volume/issue in the publisher's Version of Record (VoR).
2. **Online-First Publication Year ($Y_{\text{online}}$):** The calendar year when the peer-reviewed, copyedited VoR was first posted online with a DOI before volume/issue assignment.
3. **Accepted Manuscript Year ($Y_{\text{accepted}}$):** The date the peer-reviewed manuscript was accepted by the journal before publisher layout/VoR formatting.
4. **Repository Deposit Year ($Y_{\text{deposit}}$):** The date a file was uploaded to an institutional repository, arXiv, or Zenodo.

#### 2.3.2 Strict Rule Against Deposit Date Substitution
> **RULE:** A repository deposit date must **NEVER** be substituted for a publication date.  
> *Rationale:* A paper published in 2018 but deposited into an institutional repository in 2024 remains a 2018 paper. Using deposit dates would introduce severe temporal inflation and contaminate the 2024–2026 core window with historical literature.

#### 2.3.3 Precedence Resolution Hierarchy
1. **Priority 1 ($Y_{\text{formal}}$):** Formal VoR volume/issue year governs `publication_year`.
2. **Priority 2 ($Y_{\text{online}}$):** If volume/issue has not yet been assigned, the online-first VoR year governs.
3. **Priority 3 ($Y_{\text{accepted}}$):** Used only where VoR is absent and a lawful accepted manuscript is the canonical version.
4. **Preprints:** Unreviewed preprints are excluded under Phase 3 Section 4.2; deposit dates do not qualify preprints as published works.
5. **Conflict & Missing Date Handling:** All dates are preserved in metadata (`formal_date`, `online_date`, `deposit_date`). Discrepancies $>1$ year are flagged in `date_exceptions.log`. Missing dates must remain `publication_year = None`; fabricating dates is prohibited.

---

### 2.4 Primary ($I_{\text{primary}}$) and Sensitivity ($I_{\text{all}}$) Corpus Boundaries (DEC-06)

#### 2.4.1 Document Type Allocation
- **Primary Index ($I_{\text{primary}}$):**
  - **Eligible Types:** `journal_article`, `conference_paper` (primary peer-reviewed research papers only).
  - **Ineligible Types:** `review`, `systematic_review`, `report`, `preprint`.
  - **Governing Role:** Evaluates the frozen confirmatory research question (*BM25 vs. Dense vs. Hybrid*).
- **Sensitivity Index ($I_{\text{all}}$):**
  - **Eligible Types:** `journal_article`, `conference_paper`, `review`, `systematic_review`.
  - **Governing Role:** Evaluates the secondary exploratory question: *Does the inclusion of review articles alter the relative performance gap or ranking of the three retrieval strategies?*

#### 2.4.2 Methodological Interpretation of Sensitivity Analysis
Because $|I_{\text{all}}| > |I_{\text{primary}}|$, differences in corpus size and evidence density introduce known statistical effects:
- **BM25 Impact:** Review articles increase document frequencies ($df$) of domain terminology, altering inverse document frequency (IDF) weights, while review passages contain high keyword density that may favor broad lexical matching.
- **Dense Impact:** Review passages produce embedding vectors situated near broad conceptual centroids, altering k-NN cosine rankings.
- **Hybrid (RRF) Impact:** Reciprocal rank fusion reflects whether BM25 and dense agree on review passages versus primary papers.
- **Experimental Invariant:** Benchmark questions, ground-truth claim rubrics, generation prompts, and evaluation metrics must remain **strictly identical** across $I_{\text{primary}}$ and $I_{\text{all}}$ evaluations.

---

### 2.5 Extraction Calibration Protocol (DEC-08)

- **20-PDF Calibration Stratum:**
  - 5 standard 2-column peer-reviewed research papers.
  - 5 heavy mathematical/physics papers (dense LaTeX formulas).
  - 5 data-dense experimental papers with nested tables.
  - 3 conference proceedings papers with graphic figures.
  - 2 legacy/scanned PDFs requiring OCR.
- **Measurement Matrix:** Reading order reflow, table structure accuracy, formula syntax preservation (LaTeX/MathML), figure caption extraction completeness, and Character Error Rate (CER).
- **Threshold Status:** Numerical cutoffs for `successful`, `partial`, and `failed` remain **OPEN** until pilot empirical distributions are recorded.

---

### 2.6 Single-Reviewer Screening Transparency (DEC-10)

- **Honest Limitation:** Inter-rater reliability (dual-reviewer Cohen's kappa) cannot be claimed without independent raters.
- **Intra-Rater Calibration Protocol:** A 10% stratified random sample is re-screened under masked conditions after a **14-day temporal washout period**.
- **Metrics:** Intra-rater percentage agreement and intra-rater Cohen's kappa ($\kappa_{\text{intra}}$) are recorded in study reporting.

---

## 3. Comprehensive Protocol Consistency Audit

| Protocol Document | Cross-Checked Area | Finding & Reconciliation | Status |
|---|---|---|---|
| [`notes/methodology/phase8_protocol_decision_register.md`](./phase8_protocol_decision_register.md) | DEC-01 through DEC-10 | Fully aligned with Phase 8.1 and 8.2 specifications. | **CONSISTENT** |
| [`notes/methodology/corpus_acquisition_workflow.md`](./corpus_acquisition_workflow.md) | Query Families & Date Rules | Section 20 links directly to decision register; date precedence aligned. | **CONSISTENT** |
| [`notes/methodology/corpus_data_dictionary.md`](./corpus_data_dictionary.md) | `document_type` controlled enums | Updated line 20 to snake_case controlled vocabulary (`journal_article`, `conference_paper`, `review`, `systematic_review`). | **CONSISTENT** |
| [`notes/methodology/corpus_quality_control.md`](./corpus_quality_control.md) | Retraction triggers & QC sampling | Review triggers strictly include `corrected` and `review_required`. | **CONSISTENT** |
| [`notes/research-gaps/phase3_corpus_design_protocol.md`](../research-gaps/phase3_corpus_design_protocol.md) | Document type & preprint exclusions | Primary corpus excludes preprints without VoR; matches Phase 8.2 boundaries. | **CONSISTENT** |
| [`SCREENING_PROTOCOL.md`](../../SCREENING_PROTOCOL.md) | RAG Literature Review vs Corpus Screening | Clarified: `SCREENING_PROTOCOL.md` governs methodological literature review (Phases 1–2); corpus workflow governs solar-PV literature (Phase 3 & 7/8). | **CONSISTENT** |
| [`src/solar_rag/corpus_workflow.py`](../../src/solar_rag/corpus_workflow.py) | Python validation engine | Enforces all controlled enums; 69 tests pass cleanly. | **CONSISTENT** |

---

## 4. Researcher Protocol Sign-Off Matrix

```
==========================================================================================================================================
RESEARCHER PROTOCOL SIGN-OFF MATRIX
==========================================================================================================================================
ID     Topic                     Current Policy                                    Remaining Uncertainty              Ready for Sign-Off?
------------------------------------------------------------------------------------------------------------------------------------------
DEC-01 Core Publication Window   2024–2026 (inclusive) based on VoR year.          Exact upper-bound date at search.  READY FOR SIGN-OFF
DEC-02 Pre-2024 Chaining         >=2 independent core citing papers; disjoint      Exact yield of chained candidates  READY FOR SIGN-OFF
                                 lead authors; <50% middle author overlap.         prior to pilot run.
DEC-03 Date Precedence           Formal VoR > Online-First > Accepted Manuscript.  None (precedence deterministic).   READY FOR SIGN-OFF
                                 Deposit date substitution strictly prohibited.
DEC-04 Discovery Source Mix      Multi-source (OpenAlex, Crossref, S2, OA).        Source overlap ratio (tested in    READY FOR SIGN-OFF
                                 No single source claimed complete.                300-slot pilot).
DEC-05 Query Registry            4 Query Families (Q1–Q4) with exact parameter     None (syntax templates locked).    READY FOR SIGN-OFF
                                 logging and deterministic ordering.
DEC-06 Review Stratification     I_primary: primary research articles only.        None (index boundary locked).      READY FOR SIGN-OFF
                                 I_all: primary research + review articles.
DEC-07 Artifact Preservation     Text-first: captions & structured tables;         None (scope locked to text-first). READY FOR SIGN-OFF
                                 LaTeX/MathML formulas; image pixels excluded.
DEC-08 Extraction Thresholds     Open threshold protocol; numerical cutoffs        Awaiting 20-PDF extraction pilot   OPEN (Awaiting
                                 established from 20-paper empirical pilot.        measurements.                      Pilot Run)
DEC-09 Reference List Handling   Bibliographies parsed to metadata only;           None (chunk exclusion locked).     READY FOR SIGN-OFF
                                 excluded from searchable retrieval chunks.
DEC-10 Screening & Calibration   Single reviewer + 10% stratified calibration      Awaiting primary screening run.    READY FOR SIGN-OFF
                                 sample re-screened after 14-day washout.
==========================================================================================================================================
```

---

## 5. Explicit Prohibitions & Current Gate Status

### 5.1 Strict Operational Prohibitions
To preserve scientific integrity and prevent experimental confounding, the following actions remain **STRICTLY PROHIBITED**:
- **DO NOT** execute web scraping or download real scientific papers.
- **DO NOT** execute the 300-slot pilot search or query live APIs until sign-off is given.
- **DO NOT** execute the 20-paper PDF extraction pilot until sign-off is given.
- **DO NOT** construct or populate the Phase 4 question benchmark.
- **DO NOT** select production embedding models, dense vector indexes, or generator LLMs.
- **DO NOT** run retrieval or generation experiments.
- **DO NOT** alter the frozen research question.

### 5.2 Current Gate Verdict
- **Protocol Consistency & Sign-Off Preparation:** **COMPLETE**
- **Researcher Explicit Sign-Off:** **PENDING RESEARCHER ACTION**
- **Real-Paper Discovery Authorization:** **BLOCKED**
- **Scientific Corpus Readiness:** **BLOCKED**
- **Confirmatory Experiment Readiness:** **BLOCKED**

