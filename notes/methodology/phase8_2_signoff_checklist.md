# Phase 8.2 — Final Corpus Protocol Consistency and Sign-Off Gate

**Project:** Solar Scientific RAG Literature Review  
**Date:** 2026-10-21  
**Phase:** Phase 8.2 — Final Protocol Consistency & Sign-Off Gate  
**Status:** PARTIAL RESEARCHER SIGN-OFF RECORDED — DEC-02/HYPOTHESES APPROVED; DEC-05 CANDIDATES APPROVED IN PRINCIPLE; FINAL ELIGIBILITY AUDIT AND REMAINING SIGN-OFFS PENDING  

---

## Governing Research Question (Frozen)

> *How do BM25, dense, and hybrid retrieval strategies, compared under identical corpus, question-benchmark, preprocessing, generator, prompt, and evaluation conditions, affect retrieval quality, answer quality, and evidence attribution in question answering over solar-PV scientific literature?*

---

## 1. Executive Summary & Purpose

This document provides the definitive, audit-ready methodological specification for the Solar-PV Scientific Literature Corpus Protocol. It resolves all remaining documentation ambiguities, establishes precise mathematical and operational definitions, and compiles the formal Researcher Protocol Sign-Off Matrix.

### Key Protocol Invariants:
1. **Frozen Research Question:** The three-arm comparison (BM25 vs. Dense vs. Hybrid RRF) under shared controls remains strictly preserved.
2. **Strict Operational Boundaries:** No real papers have been searched, scraped, or downloaded. No live API pilots or extraction pilots have been executed.
3. **Sign-Off Authority:** All policies are presented with their current status, rationale, remaining uncertainties, and approval levels. **No decision is marked as approved on the researcher's behalf.**

---

## 2. Detailed Technical & Methodological Specifications

### 2.1 Task 1: Citation Chaining & Pre-2024 Foundational Inclusion (DEC-02)

#### 2.1.1 Precise Definition of Disjoint Authorship
To prevent author self-citation loops from qualifying older papers while avoiding the exclusion of legitimate foundational studies in collaborative subfields, the concept of **disjoint authorship** is defined at two structural tiers:

1. **Lead Leadership Separation (Mandatory Strict Disjointness):**
   $$\{FirstAuthor(P_1), CorrespAuthor(P_1)\} \cap \{FirstAuthor(P_2), CorrespAuthor(P_2)\} = \emptyset$$
   The primary intellectual leadership (first author and corresponding/senior author) of Citing Core Paper 1 ($P_1$) and Citing Core Paper 2 ($P_2$) must be completely disjoint.
2. **Candidate Independence / Anti-Self-Citation (Mandatory):**
   $$\{Authors(Candidate)\} \cap \{FirstAuthor(P_1), CorrespAuthor(P_1), FirstAuthor(P_2), CorrespAuthor(P_2)\} = \emptyset$$
   No author of the pre-2024 candidate paper may serve as first author or corresponding author of either citing core paper.
3. **Middle-Author Overlap Ceiling (Collaborative Balance):**
   In photovoltaic research, large multi-institutional consortia (e.g., NREL, Fraunhofer ISE, AIST) often feature recurring technical contributors across multiple papers.
   - Middle co-authors may overlap between $P_1$ and $P_2$ **only if** the overlapping authors constitute $<50\%$ of the total author list of both $P_1$ and $P_2$.
   - If middle-author overlap $\ge 50\%$, $P_1$ and $P_2$ are classified as a single collaborative research cluster and contribute only **1 citing credit** toward the threshold.
4. **Distinction from "Completely Disjoint Author Lists":**
   Requiring 100% disjoint author lists across all middle co-authors would introduce severe false-negative bias by disqualifying landmark foundational studies (e.g., Green et al. solar efficiency tables, Jordan & Kurtz PV degradation surveys) simply because a shared institutional co-author appears on two recent 2024 papers. The combination of lead-author disjointness and the $<50\%$ middle-author ceiling eliminates self-citation bias while accommodating legitimate multi-institutional scholarship.

#### 2.1.2 Citing Document Type Restrictions (Review Exclusion)
- **Primary Research Only:** Only primary peer-reviewed research papers (`document_type in {"journal_article", "conference_paper"}`) qualify as citing core papers.
- **Review Citations Excluded:** Citations appearing in review articles (`document_type in {"review", "systematic_review"}`) do **not** count toward the $\ge 2$ threshold. Reviews cite hundreds of background papers; allowing review citations to qualify earlier papers would flood the candidate pool with generic historical citations.

#### 2.1.3 Assessment of the Two-Independent-Citing-Paper Threshold
- **Threshold Analysis:**
  - *Threshold = 1:* High risk of idiosyncratic bias or single-lab niche references entering the corpus.
  - *Threshold $\ge 3$:* High risk of historical amnesia; foundational concepts established decades ago are often treated as common knowledge or cited sparingly in recent experimental papers.
  - *Threshold = 2 (Selected Standard):* Strikes the optimal balance between peer-validated relevance in current (2024–2026) literature and protection against single-group gaming.
- **Threshold Preservation:** The threshold of **$\ge 2$ independent citing primary research papers** is preserved without modification. Any proposed change must be separately documented and submitted for formal approval.

#### 2.1.4 Handling Missing Author or Citation Metadata
- If API metadata (OpenAlex, Crossref, Semantic Scholar) is incomplete, truncated, or reports "et al.", automated citation credit is withheld.
- Mandatory manual inspection of the citing paper's full-text PDF is required to verify the complete author list and confirm that the citation appears contextually in the Introduction, Theory, or Methods section.
- If author disambiguation remains unverifiable after manual audit, the citation cannot count toward the threshold.

#### 2.1.5 Audit Trail and Recording
Every chained pre-2024 candidate accepted into the screening queue is logged in an immutable `citation_chaining_audit.jsonl` record with:
```json
{
  "candidate_doi": "10.1016/j.solmat.2020.100000",
  "candidate_title": "Foundational Degradation Modeling in Silicon Modules",
  "citing_core_records": ["doc-core-014", "doc-core-092"],
  "citing_dois": ["10.1016/j.solmat.2024.112001", "10.1109/JPHOTOV.2024.335002"],
  "citing_document_types": ["journal_article", "journal_article"],
  "lead_author_disjoint": true,
  "middle_author_overlap_ratio": 0.12,
  "candidate_author_in_citing_leads": false,
  "contextual_section_verified": "Introduction / Methodology",
  "foundational_earlier_tag": true,
  "auditor_id": "operator_id",
  "timestamp_utc": "2026-10-21T17:00:00Z"
}
```

---

### 2.2 Task 2: Pilot-Search Accounting & Predefined Known-Item Benchmark (DEC-04 / DEC-05)

#### 2.2.1 Distinct Search Metric Accounting
To prevent conflation between search capacity, gross downloads, and actual unique scientific literature, the pilot search enforces five strictly separated metrics:

```
+---------------------------------------------------------------------------------------------------+
|                                     SEARCH METRIC ACCOUNTING                                      |
+---------------------------------------------------------------------------------------------------+
| 1. Raw Retrieval Slots (N_slots):                                                                 |
|    Total theoretical capacity planned: 4 query families x 3 sources x 25 rank positions = 300.   |
|                                                                                                   |
| 2. Raw Source Records (N_raw):                                                                    |
|    Total gross bibliographic entries returned by APIs across all queries (<= N_slots).            |
|                                                                                                   |
| 3. Unique Candidate Papers (N_unique):                                                            |
|    Distinct scholarly works remaining after cross-source de-duplication by normalized DOI and     |
|    canonical title/year hash.                                                                     |
|                                                                                                   |
| 4. Duplicate Records (N_duplicate_records):                                                       |
|    Redundant bibliographic instances across sources: N_duplicate_records = N_raw - N_unique.      |
|                                                                                                   |
| 5. Duplicate Candidate Groups (N_duplicate_candidates):                                           |
|    Clusters of candidate records flagged for manual review due to title or DOI collision.         |
|                                                                                                   |
| 6. Eligible Papers (N_eligible):                                                                  |
|    Unique candidates meeting all inclusion criteria and verified lawful full-text access.         |
+---------------------------------------------------------------------------------------------------+
```

#### 2.2.2 Reproducible Query Execution & Deterministic Ordering
API queries must use deterministic parameters and log raw responses:
- **OpenAlex API:** Pinned parameters `sort=publication_date:desc,id:asc`, `per-page=25`, `page=1`. API endpoint version logged.
- **Crossref API:** Pinned parameters `rows=25&offset=0&sort=published&order=desc`, polite header (`mailto`), and timestamp logged.
- **Semantic Scholar API:** Pinned parameters `limit=25&offset=0&fields=title,authors,year,doi,abstract,venue,isOpenAccess,openAccessPdf`.
- Raw API JSON responses and their SHA-256 hashes must be preserved in `pilot_search_raw/`. No claims of complete database coverage are permitted.

#### 2.2.3 Predefined 10 Known-Item Landmark Benchmark Papers

> **DEC-05 STATUS (FROZEN 2026-10-21):** The researcher approved the KI-10 replacement. The ten known-item records are mapped to five declared subdomains, with two papers per subdomain. This list is frozen for metadata-discovery sensitivity, not total corpus recall. Full-text access is assessed separately during corpus screening: a paper without confirmed lawful full text may count for metadata-discovery sensitivity but must not be ingested into the experimental corpus unless eligibility and lawful access are confirmed.

| Item ID | Topic Subdomain | Candidate paper title | First author / year | DOI | Bibliographic source and current eligibility note |
|---|---|---|---|---|---|
| **KI-01** | Perovskite/tandem | Perovskite/silicon tandem solar cells with bilayer interface passivation | Liu et al. (2024) | [10.1038/s41586-024-07997-7](https://doi.org/10.1038/s41586-024-07997-7) | [Nature publisher record](https://www.nature.com/articles/s41586-024-07997-7); title, DOI and 2024 publication verified. Full-text corpus eligibility to be checked separately. |
| **KI-02** | Perovskite/tandem | Strained heterojunction enables high-performance, fully textured perovskite/silicon tandem solar cells | Liu et al. (2024) | [10.1016/j.joule.2024.06.015](https://doi.org/10.1016/j.joule.2024.06.015) | [Joule publisher record](https://www.sciencedirect.com/science/article/pii/S2542435124002915); title, DOI and 2024 publication verified; publisher page indicates an open archive. Verify lawful full-text route during corpus screening. |
| **KI-03** | Silicon cell technology | UV-Induced Degradation of Industrial PERC, TOPCon, and HJT Solar Cells: The Next Big Reliability Challenge? | Thome et al. (2024) | [10.1002/solr.202400628](https://doi.org/10.1002/solr.202400628) | [Wiley publisher record](https://onlinelibrary.wiley.com/doi/full/10.1002/solr.202400628); research article, open access; title, DOI and year verified. |
| **KI-04** | Silicon cell technology | Enhancing the reliability of TOPCon technology by laser-enhanced contact firing | Wu et al. (2024) | [10.1016/j.solmat.2024.112846](https://doi.org/10.1016/j.solmat.2024.112846) | [Elsevier publisher record](https://www.sciencedirect.com/science/article/pii/S0927024824001582); research article, open access; title, DOI and year verified. |
| **KI-05** | Module reliability | Electrical Performance and Degradation Analysis of Field-Aged PV Modules in Tropical Climates: A Comparative Experimental Study | Islam et al. (2024) | [10.1016/j.ecmx.2024.100719](https://doi.org/10.1016/j.ecmx.2024.100719) | [Elsevier publisher record](https://www.sciencedirect.com/science/article/pii/S2590174524001971); research article, open access; title, DOI and year verified. |
| **KI-06** | Module reliability | Buyer aware: Three new failure modes in TOPCon modules absent from PERC technology | Sen et al. (2024) | [10.1016/j.solmat.2024.112877](https://doi.org/10.1016/j.solmat.2024.112877) | [Elsevier publisher record](https://www.sciencedirect.com/science/article/pii/S0927024824001892); journal article, open access; title, DOI and year verified. |
| **KI-07** | PV forecasting | Photovoltaic power forecasting: A Transformer based framework | Piantadosi et al. (2024) | [10.1016/j.egyai.2024.100444](https://doi.org/10.1016/j.egyai.2024.100444) | [Energy and AI publisher record](https://www.sciencedirect.com/science/article/pii/S2666546824001101); research article, open access; title, DOI and year verified. |
| **KI-08** | PV forecasting | Probabilistic day-ahead prediction of PV generation. A comparative analysis of forecasting methodologies and of the factors influencing accuracy | Massidda et al. (2024) | [10.1016/j.solener.2024.112422](https://doi.org/10.1016/j.solener.2024.112422) | [Solar Energy publisher record](https://www.sciencedirect.com/science/article/pii/S0038092X24001166); title, DOI and 2024 publication verified. Full-text lawful-access eligibility remains to be checked; metadata discovery can be assessed separately. |
| **KI-09** | Emerging PV | Long-term outdoor study of an organic photovoltaic module for building integration | Luo et al. (2024) | [10.1002/pip.3791](https://doi.org/10.1002/pip.3791) | [Wiley publisher record](https://onlinelibrary.wiley.com/doi/10.1002/pip.3791); research article, open access; title, DOI and year verified. |
| **KI-10** | Emerging PV | Organic Solar Modules with Good Stability under Ultraviolet Irradiation | Tran Ho et al. (2024) | [10.1002/solr.202400101](https://doi.org/10.1002/solr.202400101) | [Wiley publisher record](https://onlinelibrary.wiley.com/doi/10.1002/solr.202400101); *Solar RRL* 8(11), article 2400101; open-access peer-reviewed research article; first published 2024-04-06. Publisher and institutional repository records support title, DOI, year, OA, and article type. |

#### 2.2.4 Known-Item Retrieval Sensitivity Calculation
$$\text{Sensitivity}_{\text{known-item}} = \left( \frac{\text{Count of Predefined Known Items in } N_{\text{unique}}}{10} \right) \times 100\%$$
Sensitivity is reported overall and per source (OpenAlex, Crossref, Semantic Scholar).  
*Methodological Notice:* This metric evaluates whether the discovery queries successfully locate known landmark literature (a query sensitivity sanity check); it does not constitute a statistical estimate of total domain recall because the true unretrieved relevant literature population is unknown.

---

### 2.3 Task 3: Publication Date Precedence & Conflict Handling (DEC-03)

#### 2.3.1 Date Category Definitions
1. **Formal Publication Year ($Y_{\text{formal}}$):** The official calendar year assigned to the journal volume/issue in the publisher's Version of Record (VoR).
2. **Online-First Publication Year ($Y_{\text{online}}$):** The calendar year when the copyedited, DOI-bearing VoR was posted online prior to issue assignment.
3. **Accepted Manuscript Year ($Y_{\text{accepted}}$):** The date the peer-reviewed manuscript was formally accepted by the editorial board.
4. **Preprint Year ($Y_{\text{preprint}}$):** The date an unreviewed manuscript was posted to arXiv, SSRN, or ResearchSquare.
5. **Repository Deposit Year ($Y_{\text{deposit}}$):** The date an electronic file was uploaded to an institutional repository or open archive.

#### 2.3.2 Strict Rule Against Deposit Date Substitution
> **MANDATORY PROTOCOL RULE:** A repository deposit date must **NEVER** be substituted for a publication date.  
> *Methodological Rationale:* A landmark paper published in 2015 that is uploaded to an institutional repository in 2024 remains a 2015 paper. Allowing deposit dates to override publication dates would artificially contaminate the 2024–2026 contemporary window with historical literature.

#### 2.3.3 Deterministic Date Precedence Hierarchy
When dates conflict across discovery sources:
1. **Priority 1 ($Y_{\text{formal}}$):** Formal VoR volume/issue year strictly governs `publication_year`.
2. **Priority 2 ($Y_{\text{online}}$):** If volume/issue has not yet been assigned by the publisher, the online-first VoR year governs.
3. **Priority 3 ($Y_{\text{accepted}}$):** Used only where VoR is paywalled/absent and an authorized accepted manuscript serves as canonical text.
4. **Preprints:** Excluded from the primary corpus under Phase 3 Section 4.2.
5. **Conflict & Missing Date Handling:** All dates are preserved in metadata (`formal_date`, `online_date`, `deposit_date`). Discrepancies $>1$ year are flagged in `date_exceptions.log`. If a publication date cannot be verified from publisher VoR, `publication_year = None`, queued for manual audit, and never fabricated.

---

### 2.4 Task 4: Primary ($I_{\text{primary}}$) and Sensitivity ($I_{\text{all}}$) Corpora (DEC-06)

#### 2.4.1 Document Type Allocation
```
+---------------------------------------------------------------------------------------------------+
|                                CORPUS DOCUMENT TYPE ALLOCATION                                    |
+---------------------------------------------------------------------------------------------------+
| Primary Retrieval Index (I_primary):                                                              |
|   - Eligible: journal_article, conference_paper (primary peer-reviewed research papers only)       |
|   - Ineligible: review, systematic_review, report, preprint, book_chapter, thesis                  |
|   - Governing Role: Evaluates frozen confirmatory RQ (BM25 vs. Dense vs. Hybrid).                 |
|                                                                                                   |
| Secondary / Sensitivity Index (I_all):                                                            |
|   - Eligible: journal_article, conference_paper, review, systematic_review                         |
|   - Ineligible: report, preprint, book_chapter, thesis                                             |
|   - Governing Role: Evaluates sensitivity of retrieval strategy rankings to review literature.    |
+---------------------------------------------------------------------------------------------------+
```

#### 2.4.2 Invariant Shared Experimental Controls
To prevent confounding retrieval strategy with experimental artifacts:
- The question benchmark (Phase 4), ground-truth claim rubrics, generation prompts, generator model, and evaluation metrics remain **strictly identical** across $I_{\text{primary}}$ and $I_{\text{all}}$ evaluations.

#### 2.4.3 Methodological Interpretation of Corpus Differences
Because $|I_{\text{all}}| > |I_{\text{primary}}|$, differences in corpus size and evidence density introduce known statistical effects that must be explicitly analyzed:
- **BM25 Impact:** Review articles inflate document frequencies ($df$) across broad domain terms, compressing inverse document frequency (IDF) weights. Furthermore, review passages contain dense keyword summaries that may artificially elevate BM25 lexical matching over primary empirical passages.
- **Dense Retriever Impact:** Review passages synthesize multiple subtopics, generating embedding vectors located near broad conceptual centroids. This increases semantic collision risks and may crowd out fine-grained empirical passages.
- **Hybrid (RRF) Impact:** Reciprocal rank fusion reflects whether BM25 and dense agree on review passages versus primary papers.
- **Interpretation Rule:** If hybrid retrieval outperforms dense on $I_{\text{primary}}$ but dense outperforms hybrid on $I_{\text{all}}$, this indicates that review-article presence confounds evidence localization. The primary conclusion regarding the frozen research question must rest on $I_{\text{primary}}$.

---

### 2.5 Task 5: Comprehensive Cross-Document Consistency Audit

A systematic comparison across all project governance documents was conducted:

| Governance Document | Cross-Checked Element | Consistency Finding | Resolution / Current Status |
|---|---|---|---|
| [`notes/methodology/phase8_protocol_decision_register.md`](./phase8_protocol_decision_register.md) | DEC-01 through DEC-10 | Fully aligned with Phase 8.1 and 8.2 operational definitions. | **CONSISTENT** |
| [`notes/methodology/corpus_acquisition_workflow.md`](./corpus_acquisition_workflow.md) | Query Families & Date Rules | Section 20 links directly to decision register; date precedence aligned. | **CONSISTENT** |
| [`notes/methodology/corpus_data_dictionary.md`](./corpus_data_dictionary.md) | Controlled enums for `document_type` | Updated to snake_case enums (`journal_article`, `conference_paper`, `review`, `systematic_review`). | **CONSISTENT** |
| [`notes/methodology/corpus_quality_control.md`](./corpus_quality_control.md) | Retraction triggers & QC sampling | Review triggers include `corrected` and `review_required`. | **CONSISTENT** |
| [`notes/research-gaps/phase3_corpus_design_protocol.md`](../research-gaps/phase3_corpus_design_protocol.md) | Document types & preprint policy | Primary corpus excludes preprints without VoR; matches Phase 8.2 boundaries. | **CONSISTENT** |
| [`SCREENING_PROTOCOL.md`](../../SCREENING_PROTOCOL.md) | Scope & Controlled Decisions | Clarified distinction: `SCREENING_PROTOCOL.md` governs methodological literature screening (Phases 1–2); corpus workflow governs solar-PV literature (Phase 3 & 7/8). | **CONSISTENT** |
| [`src/solar_rag/corpus_workflow.py`](../../src/solar_rag/corpus_workflow.py) | Python validation engine | Enforces controlled vocabularies; all 69 unit tests pass cleanly. | **CONSISTENT** |

---

## 3. Researcher Protocol Sign-Off Matrix

The following matrix documents each protocol decision, rationale, remaining uncertainties, and sign-off status. On 2026-10-21, the researcher approved the remaining policy and selection procedures as a bundle. Numeric extraction thresholds, actual model/parameter values, and benchmark size remain pilot/development-dependent; DEC-05 stratification and full-text eligibility remain open.

```
==================================================================================================================================================
## 3. Researcher Protocol Sign-Off Matrix

Researcher decisions recorded on 2026-10-21. Policy/selection procedures are approved as noted; values intentionally assigned to later pilot/development stages remain open. DEC-05 is not fully closed.

| Decision | Approved policy/procedure | What remains open | Status |
|---|---|---|---|
| DEC-01 | Core search window is 2024-01-01 through search execution date; earlier works only via approved citation chaining. | Search execution date is recorded when the authorized search runs. | Approved 2026-10-21 |
| DEC-02 | At least two core primary citing papers with distinct first authors; no candidate-author overlap with either citing paper; review citations excluded. | Candidate yield is unknown until search. This does not prove independent research groups. | Approved 2026-10-21 |
| DEC-03 | Formal VoR issue year takes precedence; otherwise verified online VoR date; repository deposit date never substitutes for publication year. | Record discrepancies and year_source in metadata. | Approved 2026-10-21 |
| DEC-04 | Use OpenAlex, Crossref, Semantic Scholar and lawful OA repositories; log queries/parameters; make no exhaustiveness claim; deterministic client-side sort is fallback. | API pagination, overlap and server-side sorting require pilot verification. | Procedure approved 2026-10-21; pilot verification pending |
| DEC-05 | Four query families and ten known-item candidates approved in principle. Known-item sensitivity is a metadata-discovery sanity check, not total corpus recall. | Current list has six topical labels versus five declared subdomains. KI-01 and KI-08 full texts are not confirmed as lawful OA corpus inputs. Resolve mapping and separate metadata discovery from full-text eligibility. | Partially approved; open blocker |
| DEC-06 | I_primary contains eligible primary journal articles and peer-reviewed conference papers; I_all adds eligible reviews/systematic reviews; retractions/corrections excluded from chunks. | Index construction follows corpus freeze. | Approved 2026-10-21 |
| DEC-07 | Text-first extraction retains text, captions, structured tables and available LaTeX/MathML; no raw image pixels in searchable chunks; log OCR/extraction provenance. | Quality thresholds are handled under DEC-08. | Approved 2026-10-21 |
| DEC-08 | Set CER/WER thresholds from the stratified 20-paper calibration pilot; report observed distributions and decision rationale. | Numeric thresholds remain pilot-dependent. | Procedure approved 2026-10-21; values pending pilot |
| DEC-09 | Parse bibliographies to structured metadata only; exclude reference-list text from searchable chunks. | No policy item open. | Approved 2026-10-21 |
| DEC-10 | Single reviewer; 10% masked re-screen after 14 days reported as intra-rater temporal consistency only. | Calibration results pending execution. | Approved 2026-10-21 |
| DEC-11 | Choose dense model, chunking and fusion through the predefined development procedure; freeze before confirmatory evaluation; keep arms matched. | Actual model and parameter values remain pending development. | Selection procedure approved 2026-10-21 |
| DEC-12 | Choose one accessible generator through the predefined feasibility/development procedure; freeze version, prompt, decoding and context budget before confirmatory evaluation. | Actual model/configuration remains pending development. | Selection procedure approved 2026-10-21 |
| DEC-13 | Set benchmark size and category mix after corpus freeze using taxonomy, gold-evidence feasibility and prospective precision/power justification. | Final question count and category mix remain pending corpus freeze. | Selection procedure approved 2026-10-21 |

**Hypothesis framing:** H1 remains directional at retrieval level; downstream answer-quality and general evidence-attribution comparisons remain cautious; H4 is exploratory and non-directional. Approved 2026-10-21.

---

## 4. Strict Boundaries & Current Gate Status

### 4.1 Strict Operational Prohibitions
To ensure compliance with scientific integrity protocols, the following actions remain **STRICTLY PROHIBITED**:
- **DO NOT** execute web scraping or download real scientific papers.
- **DO NOT** execute the 300-slot pilot search or query live APIs until separate execution authorization is provided.
- **DO NOT** execute the 20-paper PDF extraction pilot until separate execution authorization is provided.
- **DO NOT** construct or populate the Phase 4 question benchmark.
- **DO NOT** select production embedding models, dense vector indexes, or generator LLMs.
- **DO NOT** run retrieval or generation experiments.
- **DO NOT** alter the frozen research question.

### 4.2 Current Gate Verdict
- **Protocol Consistency & Sign-Off Checklist:** **COMPLETE — PROTOCOL CLOSED 2026-10-21**
- **Researcher Policy/Procedure Sign-Off:** **COMPLETE** — DEC-01 through DEC-14 resolved or explicitly assigned to pilot/development stages.
- **Known-item benchmark:** **FROZEN** — ten metadata-discovery targets mapped to five subdomains, two per subdomain. Full-text eligibility is a separate corpus-screening decision.
- **Pilot execution:** **ON HOLD — NOT AUTHORIZED YET BY USER REQUEST**; both pilots remain unrun.
- **Scientific Corpus Readiness:** **NOT ESTABLISHED** — no corpus has been acquired or screened.
- **Confirmatory Experiment Readiness:** **BLOCKED** — benchmark, corpus, and development-stage values remain unbuilt/unvalidated.
