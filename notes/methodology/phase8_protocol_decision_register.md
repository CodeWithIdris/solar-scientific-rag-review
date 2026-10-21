# Phase 8 — Corpus Protocol Decision Register and Methodological Specification

**Project:** Solar Scientific RAG Literature Review  
**Date:** 2026-10-09  
**Phase:** Phase 8 — Corpus Protocol Finalization  
**Status:** PROTOCOL CLOSED 2026-10-21 — PILOT EXECUTION HOLD ACTIVE  

---

## Researcher Decision Log (2026-10-21)

- **DEC-02:** Alternative B approved with the caveat that distinct first authors and no candidate-author overlap do not establish independent research groups.
- **Hypotheses:** v0.2 framing approved: directional H1 for retrieval quality; cautious downstream answer-quality and attribution comparisons; H4 exploratory/non-directional.
- **DEC-05:** Ten proposed known-item candidates approved in principle, subject to final bibliographic and eligibility checks. This does not authorize any search or pilot.

## Governing Research Question (Frozen)

> *How do BM25, dense, and hybrid retrieval strategies, compared under identical corpus, question-benchmark, preprocessing, generator, prompt, and evaluation conditions, affect retrieval quality, answer quality, and evidence attribution in question answering over solar-PV scientific literature?*

---

## 1. Protocol Decision Register Summary

| Decision ID | Area | Decision Topic | Selected Policy | Status | Approval Level Required |
|---|---|---|---|---|---|
| **DEC-01** | Publication Period | Core Search Window | 2024–2026 (inclusive) as primary discovery window. | **RESEARCHER-APPROVED 2026-10-21** | Project Lead / Methodologist |
| **DEC-02** | Publication Period | Pre-2024 Foundational Literature | Algorithmic backward citation chaining (≥2 core primary citing papers with distinct first authors and no candidate-author overlap with either citing paper); explicitly does not prove lab/institution independence. | **RESEARCHER-APPROVED 2026-10-21** | Project Lead / Methodologist |
| **DEC-03** | Publication Period | Publication Date Semantics | Formal peer-reviewed Version of Record (VoR) year governs `publication_year`. Both online and issue dates captured. | **RESEARCHER-APPROVED 2026-10-21** | Technical Lead |
| **DEC-04** | Discovery Sources | Source Mix & Roles | Multi-source strategy: OpenAlex (broad discovery/concepts), Crossref (authoritative DOI/metadata), Semantic Scholar (citations), and lawful OA repositories (full-text). | **PROCEDURE APPROVED 2026-10-21; PILOT VERIFICATION PENDING** | Project Lead |
| **DEC-05** | Discovery Sources | Query Registry Architecture | Four focused query families (Q1–Q4); ten known-item metadata targets frozen 2026-10-21 with two targets in each of five subdomains; KI-10 is the approved organic-solar-module replacement. Full-text access remains a separate corpus-screening check. API endpoint/sorting verification remains pilot-dependent. | **CLOSED 2026-10-21; PILOT HOLD ACTIVE** | Technical Lead |
| **DEC-06** | Document Types | Review Article Policy | Stratified inclusion: Review articles included but explicitly tagged (`document_type="review"`) to allow primary vs. review sensitivity analysis. | **RESEARCHER-APPROVED 2026-10-21** | Methodologist |
| **DEC-07** | Extraction & Media | Tables, Equations & Figures | Text-first representation: Captions and structured tabular text extracted; images/pixels excluded; formulas captured in LaTeX/MathML text when available. | **RESEARCHER-APPROVED 2026-10-21** | Technical Lead |
| **DEC-08** | Extraction Quality | OCR & Quality Thresholds | No arbitrary numeric cutoff before pilot. Numerical thresholds remain OPEN pending a 20-paper extraction pilot. | **PROCEDURE APPROVED 2026-10-21; NUMERIC VALUES PILOT-DEPENDENT** | Calibration Pilot Lead |
| **DEC-09** | Reference Lists | Bibliography Retrieval Policy | References excluded from searchable corpus chunks; parsed to structured metadata only. | **RESEARCHER-APPROVED 2026-10-21** | Methodologist |
| **DEC-10** | Screening & Review | Reviewer Workflow & Calibration | Primary screening with 10% re-screening calibration sample; explicit evidence citations for all exclusions. | **RESEARCHER-APPROVED 2026-10-21** | Methodologist |

---

## 2. Detailed Decision Specifications

### DEC-01: Core Publication Period Window (2024–2026)

- **Context:** The literature discovery strategy requires a defined temporal boundary that captures contemporary solar-PV technology.
- **Options Considered:**
  1. *Option A (Strict 2024–2026 only):* Fixed contemporary window. Highly bounded, but risks excluding foundational baseline mechanisms (e.g., standard Shockley-Queisser limits, classic degradation kinetic formulations).
  2. *Option B (Broad retrospective window, e.g., 2010–2026):* Large historical coverage, but explodes discovery volume, mixes obsolete PV technologies, and complicates access rights.
  3. *Option C (2024–2026 discovery core + structured foundational chaining):* Primary systematic search focuses on 2024–2026; earlier seminal papers enter strictly via documented citation chaining.
- **Adopted Policy:** **Option C (Provisional)**. The systematic database queries will cover 2024–2026. The search execution date will serve as the exact upper bound.
- **Bias & Validity Implications:** Prevents chronological drift while ensuring modern technical relevance (perovskite-silicon tandems, advanced bifacial modeling, grid-forming PV inverters).
- **Closure Requirement:** Confirmation of the final search execution date.

---

### DEC-02: Pre-2024 Foundational Studies & Citation Chaining

- **Context:** A mechanism is required to include earlier foundational studies without introducing subjective bias or search-result contamination.
- **Options Considered:**
  1. *Ad-hoc expert nomination:* Subject to severe recall and confirmation bias.
  2. *Citation chaining from candidate benchmark questions:* Highly vulnerable to target leakage / data snooping.
  3. *Pre-declared algorithmic backward citation chaining:* Pre-2024 papers qualify for screening *only* if cited by $\ge 2$ distinct eligible core (2024–2026) papers in their introduction/methodology sections.
- **Adopted Policy:** **Pre-declared algorithmic backward citation chaining (Provisional)**.
  - Every chained pre-2024 candidate must pass the identical inclusion criteria (solar-PV focus, peer-reviewed, full-text availability, English).
  - Every included pre-2024 document is permanently tagged with `foundational_earlier=true` and its citing core record IDs logged.
  - Benchmark questions must never be used to discover, suggest, or justify earlier papers.
- **Bias & Validity Implications:** Eliminates benchmark-to-corpus circularity and cherry-picking.

---

### DEC-03: Publication Date Semantics (Online-First vs. Issue Dates)

- **Context:** Contemporary scientific publishing often features an "online-first" date months or years prior to the official journal volume/issue date.
- **Options Considered:**
  1. *Earliest online preprint/first-look date.*
  2. *Formal peer-reviewed Version of Record (VoR) volume/issue year.*
- **Adopted Policy:** **Formal VoR Publication Year (Provisional)**.
  - The integer `publication_year` field represents the formal peer-reviewed VoR year.
  - When available, both `online_publication_date` (ISO-8601) and `issue_publication_date` are recorded in candidate metadata.
  - If a paper appeared online in late 2023 but assigned to a 2024 journal issue, it is eligible under the 2024–2026 core window.
- **Bias & Validity Implications:** Ensures alignment with official indexing databases (Crossref/OpenAlex) and avoids misclassifying peer-reviewed papers as out-of-period.

---

### DEC-04: Discovery Sources & Multi-Source Synthesis

- **Context:** No single bibliographic database provides complete, unbiased coverage of solar-PV literature.
- **Source Roles & Constraints:**
  - **OpenAlex:** Primary source for broad entity discovery, concept filtering (`Concepts: Photovoltaics, Solar Energy`), and open-access URL discovery. *Limitation:* Machine-assigned concept tags contain false positives; requires secondary screening.
  - **Crossref:** Authoritative source for DOI resolution, official publication dates, publisher metadata, and funder/license statements. *Limitation:* Abstract text is missing for approximately 25% of records; no full-text indexing.
  - **Semantic Scholar:** Supplementary source for citation graph traversal, influential citations, and reference link parsing. *Limitation:* API rate limits apply; subject classification is broader.
  - **Lawful Full-Text Repositories (Publisher OA, arXiv, Institutional Repositories):** Source for downloadable full text under verified open-access licenses (CC-BY, CC-BY-SA, Open Access VoR). *Limitation:* Paywalled subscriber-only content without lawful open copies will be assigned `full_text_inaccessible` and excluded from retrieval indexing.
- **Deduplication Across Sources:** Normalized DOI is the primary cross-source link (`status: duplicate`).
- **Adopted Policy:** **Multi-Source Hybrid Discovery (Provisional)**.

---

### DEC-05: Versioned Query Registry Architecture

- **Context:** Search queries must be exact, version-controlled, reproducible, and tracked in an auditable registry.
- **Query Families:**
  - **Family Q1 (Broad PV Identity):**
    ```text
    ("photovoltaic" OR "photovoltaics" OR "solar PV" OR "solar photovoltaic" OR "PV module" OR "PV cell" OR "solar cell")
    ```
  - **Family Q2 (PV Systems, Performance & Reliability):**
    ```text
    ("photovoltaic" OR "solar PV" OR "solar photovoltaic") AND ("PV system" OR "module performance" OR "PV performance" OR "efficiency" OR "degradation" OR "reliability" OR "monitoring")
    ```
  - **Family Q3 (PV Materials & Device Physics):**
    ```text
    ("photovoltaic" OR "solar cell" OR "PV cell") AND ("silicon" OR "perovskite" OR "tandem" OR "bifacial" OR "thin film" OR "heterojunction")
    ```
  - **Family Q4 (Forecasting, Resources & Diagnostics):**
    ```text
    ("photovoltaic" OR "solar PV" OR "PV system") AND ("forecasting" OR "irradiance prediction" OR "fault detection" OR "diagnostics" OR "thermal behavior" OR "techno-economic")
    ```
- **Mandatory Query Registry Fields:**
  `search_run_id`, `query_id`, `query_version`, `source_name`, `exact_query_string`, `field_restrictions`, `date_filters`, `document_type_filters`, `language_filters`, `execution_timestamp_utc`, `result_count`, `records_exported`, `export_file_hash`, `searcher_id`.

---

### DEC-06: Review Article Stratification Policy

- **Context:** Review articles synthesize literature across dozens of primary works. Mixing reviews into a primary evidence corpus can distort lexical and dense retrieval comparisons by providing synthetic summaries of multiple experiments.
- **Options Considered:**
  1. *Include reviews without distinction:* Causes severe passage-level evidence redundancy.
  2. *Exclude reviews entirely:* Omits high-level conceptual syntheses and consensus statements.
  3. *Stratified inclusion with explicit tagging:* Reviews are ingested and indexed, but permanently tagged as `document_type="review"`. The primary evaluation is conducted on original research papers (`document_type in {"journal_article", "conference_paper"}`), with a secondary sensitivity analysis evaluating the impact of review inclusion.
- **Adopted Policy:** **Stratified Tagged Inclusion (Provisional)**.
  - Phase 4 benchmark question construction must record whether expected gold evidence resides in primary experimental papers or review synthesis.

---

### DEC-07: Tables, Equations, Figures, and OCR Policy

- **Context:** Scientific information in solar-PV research is heavily concentrated in figures, tables, and mathematical formulations.
- **Evidence-Preservation Rules:**
  - **Main Body Prose:** Extracted with section headings, paragraph boundaries, and source offset locators.
  - **Tables:** Extracted as structured text (markdown or pipe-delimited text) along with table captions. If table formatting cannot be faithfully parsed, the caption is retained with `extraction_note="Table formatting omitted"`.
  - **Figure Captions:** Fully extracted and indexed. Figure pixel data/images are excluded (the study is strictly text-first).
  - **Equations:** Inline and display mathematical expressions are preserved in LaTeX or MathML string format where supported by extraction tools. If an equation is rendered as an unextractable embedded image, nearby explanatory text is retained and an extraction flag logged.
  - **Supplementary Material:** Excluded from the primary text chunk index to maintain consistent document boundaries, but archived in metadata when available.
  - **References:** Extracted to structured bibliographic metadata only; excluded from searchable chunk stores to prevent artificial lexical matching against cited titles.

---

### DEC-08: Extraction Quality & OCR Pilot Protocol (Open Threshold)

- **Context:** Arbitrary numeric thresholds for character error rates (CER) or word error rates (WER) should not be fabricated without empirical grounding.
- **Adopted Policy:** **Open Threshold with Defined Extraction Pilot Protocol (Open)**.
  - **Pilot Design:** Before large-scale text extraction, an extraction calibration sample of 20 structurally diverse solar-PV PDFs (including multi-column layouts, complex tables, mathematical proofs, and legacy scans) will be processed using the target extraction pipeline.
  - **Metrics Measured:**
    1. Reading order fidelity across multi-column text.
    2. Character Error Rate (CER) on mathematical symbols, subscripts, and units.
    3. Structural preservation of table rows/columns.
  - **Resolution Trigger:** Quantitative thresholds for `partial` vs. `failed` extraction status will be established from the pilot distribution and frozen before production extraction begins.

---

### DEC-09: Reference-List Exclusion from Retrieval Chunks

- **Context:** Scientific reference lists contain titles and authors of related work. If indexed as retrieval chunks, BM25 and dense retrievers may match queries against cited titles rather than evidence-bearing passages.
- **Adopted Policy:** **Bibliographies Excluded from Searchable Chunks (Provisional)**.
  - Reference lists are parsed during extraction and stored in structured metadata for citation chaining.
  - Chunks generated from reference sections are excluded from the retrieval corpus.

---

### DEC-10: Screening Adjudication & Calibration Protocol

- **Context:** Dual independent screening is the ideal standard, but staffing constraints must be documented honestly rather than inventing a fictional second reviewer.
- **Adopted Policy:** **Transparent Single Reviewer with 10% Calibration Re-screening (Provisional)**.
  - **Primary Screening:** All discovered candidates screened by the primary operator using the 14-code exclusion taxonomy.
  - **Calibration Audit Sample:** A randomly selected 10% sample of all screening decisions (stratified across included, excluded, and duplicate candidates) undergoes formal re-screening with explicit evidence locators documented.
  - **Uncertain Eligibility:** Any candidate where relevance, peer-review status, or access rights cannot be conclusively verified is marked `screening_status="potentially_relevant"` and queued for manual full-text audit.

---

## 3. Protocol Inconsistencies Resolved

1. **Date Boundary Alignment:** Reconciled discrepancies between screening protocol drafts and corpus workflow code; formal VoR publication year is established as the canonical `publication_year`.
2. **Review Article Handling:** Resolved ambiguity regarding whether reviews should be excluded or mixed; established the stratified tagging rule (`document_type="review"`).
3. **OCR Threshold Fabrication:** Eliminated arbitrary numeric OCR confidence requirements, replacing them with a structured 20-paper empirical pilot protocol.
4. **DOI Normalization Rules:** Formally locked the requirement that DOI normalization must strip query parameters, fragments, and resolver URLs while verifying standard `10.` prefixes.

---

## 4. Current Readiness Verdict

| Gate | Status | Evaluation |
|---|---|---|
| **Protocol Specification** | **CLOSED** | Researcher policy/selection procedures are approved; pilot-dependent numeric thresholds and model/benchmark choices remain assigned to their approved later stages. |
| **Known-Item Metadata Benchmark** | **FROZEN** | Ten items, five declared subdomains, two items per subdomain; KI-10 replacement recorded. |
| **Pilot Execution** | **ON HOLD — NOT AUTHORIZED YET** | User explicitly instructed not to run any pilot. |
| **Scientific Corpus Readiness** | **NOT ESTABLISHED** | No real corpus has been acquired, screened, or ingested. |
| **Confirmatory Experiment Readiness** | **BLOCKED** | Corpus, benchmark, and development-stage model/parameter choices remain unbuilt/unvalidated. |

