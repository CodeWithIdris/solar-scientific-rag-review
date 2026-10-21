# Phase 8.3 — Final Methodological Challenge and Sign-Off Audit Report

**Project:** Solar Scientific RAG Literature Review  
**Date:** 2026-10-21  
**Phase:** Phase 8.3 — Independent Methodological Challenge & Protocol Audit  
**Status:** AUDIT COMPLETE — PASS WITH OPEN ITEMS (RESEARCHER SIGN-OFF BLOCKED PENDING RESOLUTION OF TWO CRITICAL BLOCKERS)  

---

## Governing Research Question (Frozen)

> *How do BM25, dense, and hybrid retrieval strategies, compared under identical corpus, question-benchmark, preprocessing, generator, prompt, and evaluation conditions, affect retrieval quality, answer quality, and evidence attribution in question answering over solar-PV scientific literature?*

---

## 1. Executive Summary & Verdict

### Executive Verdict: PASS WITH OPEN ITEMS
The protocol architecture, software validation engine (69 unit tests passing), and methodological foundations are sound and consistent across documentation. However, an independent audit of the Phase 8.2 sign-off checklist and underlying protocol artifacts reveals **two critical blockers** and **three major methodological ambiguities** that must be resolved before researcher sign-off can be granted and before real-paper discovery may begin:

1. **CRITICAL BLOCKER 1 (Uninstantiated Known-Item Benchmark):** Table 2.2.3 in [`notes/methodology/phase8_2_signoff_checklist.md`](./phase8_2_signoff_checklist.md) provides only generic topic descriptors and sample journal venues (e.g., "*Nature Energy* / *Science*"), but lacks specific paper titles, DOIs, and author lists. It is an unexecutable benchmark template, not an executable known-item test set.
2. **CRITICAL BLOCKER 2 (Flawed Independence Rule & Missing Corresponding-Author Metadata):** The proposed citation-chaining rule relies on disjoint "corresponding authors." Neither Crossref nor Semantic Scholar APIs reliably supply corresponding-author metadata. Furthermore, disjoint first/corresponding authors does **not** establish genuine research-group or institutional independence (e.g., co-workers in the same lab under the same PI). A simpler, transparent, reproducible alternative must be selected by the researcher.
3. **MAJOR FINDING 1 (Date Metadata Conflation):** The data dictionary lacks disaggregated metadata fields for formal VoR year, online-first date, acceptance date, and deposit date, creating operational risk of silent deposit date substitution.
4. **MAJOR FINDING 2 (Unverified Server-Side API Sorting):** Compound sorting rules across OpenAlex, Crossref, and Semantic Scholar were asserted as fact without acknowledging that API server-side sorting syntax requires verification during the pilot.
5. **MAJOR FINDING 3 (Document Type Eligibility Mapping):** Non-primary document types (`correction`, `retraction_notice`, `report`) in the data dictionary require explicit index-eligibility mapping ($I_{\text{primary}}$ vs. $I_{\text{all}}$ vs. metadata-only).

**Real-paper discovery remains strictly BLOCKED.**

---

## 2. Itemized Findings by Severity

```
========================================================================================================================================
METHODOLOGICAL AUDIT FINDINGS MATRIX
========================================================================================================================================
ID    Severity  Protocol Area                     Summary of Finding
----------------------------------------------------------------------------------------------------------------------------------------
F-01  CRITICAL  Known-Item Benchmark (DEC-05)     Table 2.2.3 lacks specific titles, DOIs, and authors; benchmark is unexecutable.
F-02  CRITICAL  Citation Chaining (DEC-02)        Corresponding-author rule is unexecutable via APIs and falsely equates author
                                                  disjointness with institutional/research-group independence.
F-03  MAJOR     Publication Dates (DEC-03)        Data dictionary lacks disaggregated date fields; risk of deposit date leakage.
F-04  MAJOR     Pilot API Execution (DEC-04)      Compound sorting parameters asserted as verified without live endpoint check.
F-05  MAJOR     Index Eligibility (DEC-06)        Data dictionary enums lack explicit mapping to I_primary, I_all, and metadata-only.
F-06  MINOR     Screening Calibration (DEC-10)    10% re-screen must be strictly labeled intra-rater consistency, not inter-rater.
F-07  MINOR     Screening Scope Demarcation       Clarify boundaries between SCREENING_PROTOCOL.md and Corpus Acquisition Workflow.
========================================================================================================================================
```

---

## 3. Evidence, Critique, and Recommended Resolutions

### 3.1 Task 1: Citation Chaining & Author Independence (Finding F-02)

#### 3.1.1 The Underlying Flaw in the Proposed Rule
The rule formulated in Phase 8.2 requires:
1. $\ge 2$ independent primary research papers (2024–2026) citing the pre-2024 candidate.
2. $\{FirstAuthor(P_1), CorrespAuthor(P_1)\} \cap \{FirstAuthor(P_2), CorrespAuthor(P_2)\} = \emptyset$.
3. Candidate authors $\cap \{First/Corresp(P_1), First/Corresp(P_2)\} = \emptyset$.
4. Middle-author overlap $<50\%$.

#### 3.1.2 Methodological Critique
- **False Claim of Research-Group Independence:** Two citing papers authored by two different postdocs in the exact same laboratory, directed by the same Principal Investigator, share institutional resources, grant funding, and scientific perspective. They satisfy the "disjoint first and corresponding author" rule if one postdoc corresponds for $P_1$ and another corresponds for $P_2$, but they do **not** represent independent research groups. Claiming that author-level disjointness establishes "independent research groups" is methodologically false.
- **API Metadata Missingness:** The Crossref REST API JSON schema provides an `author` array with `given`, `family`, `sequence`, and `affiliation`, but has **no standard corresponding author flag**. Semantic Scholar API similarly omits corresponding author designations. OpenAlex only provides partial, heuristic corresponding-author flags. An automated pipeline relying on programmatic "corresponding author" verification will fail or require manual PDF parsing of every citing paper.
- **Risk of Arbitrary Exclusion:** In specialized subfields (e.g., potential-induced degradation testing protocols), only a few specialized laboratories publish experimental validations. Requiring complex author disjointness risks rejecting seminal papers that established the underlying physics simply because the citing contemporary papers share a consortium co-investigator.

#### 3.1.3 Comparison of Defensible Alternatives

| Dimension | Alternative A: Status Quo Refined (Lead Disjointness + Manual PDF Audit) | Alternative B: Transparent Distinct First Authors + 100% Anti-Self-Citation (RECOMMENDED) | Alternative C: Institutional Affiliation Disjointness (ROR-Based) |
|---|---|---|---|
| **First Author Rule** | Disjoint across $P_1$ and $P_2$ | Distinct first authors: $First(P_1) \neq First(P_2)$ | Distinct first authors |
| **Corresponding Author** | Disjoint across $P_1$ and $P_2$ (requires manual PDF check) | Omitted from automated filter (avoids missing API metadata failure) | Omitted |
| **Anti-Self-Citation** | Candidate authors $\cap$ Lead citing authors $= \emptyset$ | **Strict 100% exclusion:** $\{Authors(Candidate)\} \cap \{Authors(P_1) \cup Authors(P_2)\} = \emptyset$ | Candidate authors $\cap$ Lead citing authors $= \emptyset$ |
| **Middle-Author Overlap** | Overlap ceiling $<50\%$ | Permitted for non-lead authors, with explicit overlap ratio logged | Excluded if primary institutions match |
| **Independence Claim** | Claims "independent research groups" (methodologically invalid) | **Transparently claims "distinct primary-authored citing works without candidate self-citation"** | Claims institutional independence |
| **API Executability** | Low (blocked by missing API metadata) | **High (100% executable from standard Crossref/OpenAlex/S2 fields)** | Low (affiliations often missing/unstructured in Crossref) |

#### 3.1.4 Recommendation
Adopt **Alternative B (Transparent Distinct First Authors with Strict 100% Anti-Self-Citation)**:
- Preserves the threshold of $\ge 2$ citing primary research papers published in 2024–2026.
- Requires distinct first authors: $FirstAuthor(P_1) \neq FirstAuthor(P_2)$.
- Requires that **no author of the candidate paper appears anywhere on the author list of either citing paper**. This completely eliminates self-citation.
- Does not make false claims of "institutional research group independence." Transparently reports that middle-author overlap or institutional co-location may exist.
- Review citations explicitly do **not** count toward the $\ge 2$ threshold.
- If citation metadata is truncated or missing, manual inspection of the citing paper's PDF is mandatory and logged in `citation_chaining_audit.jsonl`.

---

### 3.2 Task 2: Publication Year Semantics & Date Disaggregation (Finding F-03)

#### 3.2.1 Audit of Existing Artifacts
In `notes/methodology/phase8_2_signoff_checklist.md`, Section 2.3 defines date categories, but `corpus_data_dictionary.md` and `src/solar_rag/corpus.py` retain only a single integer field: `publication_year`. This creates an operational gap where an automated harvester or operator could inadvertently map an institutional repository deposit date into `publication_year`.

#### 3.2.2 Required Schema Disaggregation
The record schema must explicitly disaggregate date fields:
1. `formal_publication_year`: `int | None` — Calendar year assigned to the formal journal volume/issue (Version of Record).
2. `online_publication_date`: `str | None` — ISO-8601 date (`YYYY-MM-DD`) when the VoR was posted online.
3. `acceptance_date`: `str | None` — ISO-8601 date (`YYYY-MM-DD`) when the peer-reviewed manuscript was accepted.
4. `repository_deposit_date`: `str | None` — ISO-8601 date (`YYYY-MM-DD`) when the manuscript was uploaded to arXiv, Zenodo, or an institutional repository.
5. `year_source`: `str` — Evidence source (`"crossref_vor_issue"`, `"publisher_vor_online"`, `"accepted_manuscript_header"`, `"manual_audit"`).
6. `publication_year`: `int | None` — The canonical integer year derived strictly via deterministic precedence.

#### 3.2.3 Qualifying Accepted Manuscripts Without Deposit Date Substitution
- **Strict Rule:** `repository_deposit_date` can **NEVER** substitute for `publication_year`.
- **Accepted Manuscript Protocol:** An accepted manuscript qualifies under the 2024–2026 core window **only if** the manuscript contains a verifiable, publisher-documented acceptance date (`acceptance_date`) between 2024-01-01 and the search execution date. A 2021 manuscript deposited into an institutional repository in 2024 has `formal_publication_year = 2021` and `repository_deposit_date = 2024-03-01`; it is strictly excluded from the core window.
- **Unresolvable Dates:** If an item lacks a verifiable VoR issue date, online VoR date, or acceptance date, `publication_year` is set to `None`, flagged `review_required`, and excluded from canonical corpus release until audited.

---

### 3.3 Task 3: Known-Item Pilot Benchmark Validity (Finding F-01)

#### 3.3.1 Critical Finding: Uninstantiated Benchmark Table
Table 2.2.3 in `notes/methodology/phase8_2_signoff_checklist.md` does **not** contain an executable benchmark list. It lists broad topics and generic venue names (e.g., "*Nature Energy* / *Science*"), but omits:
- Specific Paper Titles
- Specific Digital Object Identifiers (DOIs)
- Specific Author Lists
- Verified Publication Dates

An automated script or auditor cannot evaluate whether an API query retrieved "KI-01" because "KI-01" has no canonical identifier. **This is an unresolved blocker.**

#### 3.3.2 Protocol for Freezing the Known-Item Benchmark
To eliminate bias and prevent cherry-picking:
1. **Researcher Nomination Requirement:** Before the 300-slot metadata pilot is executed, the researcher must supply 10 specific peer-reviewed 2024 solar-PV papers with verified Titles and DOIs.
2. **Coverage Guardrails:** The 10 papers must span the declared domain:
   - 2 Perovskite / Tandem physics papers
   - 2 Silicon cell technologies (TOPCon, HJT)
   - 2 Module degradation / reliability papers (PID, damp heat, albedo)
   - 2 System operation / power electronics / forecasting papers
   - 2 Emerging PV / techno-economic / lifecycle papers
3. **Selection Bias & Sensitivity vs. Recall:**
   - Selecting high-impact papers with title keywords matching discovery queries will artificially inflate sensitivity.
   - The pilot report must explicitly state:
     $$\text{Sensitivity}_{\text{known-item}} = \left( \frac{\text{Predefined Known Items Retrieved in } N_{\text{unique}}}{10} \right) \times 100\%$$
   - **Crucial Methodological Caveat:** This metric is a **limited query sensitivity sanity check**, not an empirical estimate of total literature recall, because the true size and composition of the relevant literature universe is unobserved.
4. **Reconciliation & Match Criteria:**
   - A known item is counted as retrieved if its normalized DOI appears in $N_{\text{unique}}$.
   - If a known item is incorrectly specified (e.g., invalid DOI or published in 2023), it must be corrected and the benchmark re-frozen before search execution.

---

### 3.4 Task 4: Pilot Accounting & API Execution Mechanics (Finding F-04)

#### 3.4.1 Strict Accounting Definitions
To prevent inflation of search volume metrics:
- **$N_{\text{slots}}$ (Attempted Retrieval Slots):** Exactly 300 theoretical ranked positions (4 query families $\times$ 3 APIs $\times$ 25 rank positions).
- **$N_{\text{raw}}$ (Raw Records Returned):** Total gross bibliographic records returned across API calls ($N_{\text{raw}} \le N_{\text{slots}}$). Unfilled positions due to short result sets, HTTP 429 rate limits, timeouts, or API errors contribute 0 to $N_{\text{raw}}$ and are recorded in an error ledger.
- **$N_{\text{unique}}$ (Unique Candidate Papers):** Distinct scholarly works after resolving cross-source and cross-query duplicates via normalized DOI and canonical `title|year` hash.
- **$N_{\text{duplicate\_records}}$ (Redundant Records):** $N_{\text{duplicate\_records}} = N_{\text{raw}} - N_{\text{unique}}$.
- **$N_{\text{duplicate\_candidates}}$ (Candidate Collision Groups):** Distinct clusters of candidate records flagged by `duplicate_candidate_records()` requiring manual review.
- **$N_{\text{eligible}}$ (Eligible Corpus Papers):** Unique candidates that pass all inclusion criteria, quality gates, and have verified lawful full-text access.

#### 3.4.2 API Sorting Verification Warning
Phase 8.2 asserted compound sorting syntax as fact. The audit notes:
- **OpenAlex:** Pinned `sort=publication_date:desc,id:asc` requires verification; OpenAlex compound sort syntax varies across endpoint versions.
- **Crossref:** `sort=published&order=desc` sorts by earliest published date, which may differ from print issue date.
- **Semantic Scholar:** The public Graph API search endpoint (`/graph/v1/paper/search`) has limited sorting parameters on free API tiers.
- **Protocol Safeguard:** The pilot protocol must state that **API server-side sorting parameters are provisional and subject to live endpoint verification**. If an API does not support deterministic server-side sorting, the pipeline will capture the raw response, log the unsorted JSON snapshot with its SHA-256 hash, and apply deterministic client-side sorting by publication date and DOI.

---

### 3.5 Task 5: Primary ($I_{\text{primary}}$) and Sensitivity ($I_{\text{all}}$) Corpora (Finding F-05)

#### 3.5.1 Strict Index Demarcation
- **Primary Index ($I_{\text{primary}}$):**
  - **Eligible:** `journal_article`, `conference_paper` (primary empirical/theoretical research only).
  - **Strictly Excluded:** `review`, `systematic_review`, `report`, `preprint`, `correction`, `retraction_notice`.
  - **Role:** Confirmatory evaluation of the frozen research question (BM25 vs. Dense vs. Hybrid).
- **Sensitivity Index ($I_{\text{all}}$):**
  - **Eligible:** `journal_article`, `conference_paper`, `review`, `systematic_review`.
  - **Strictly Excluded:** `report`, `preprint`, `correction`, `retraction_notice`.
  - **Role:** Secondary sensitivity analysis to evaluate whether review literature shifts retrieval rankings.

#### 3.5.2 Document-Type Eligibility Mapping Table

| Document Type in Data Dictionary | Eligible for $I_{\text{primary}}$? | Eligible for $I_{\text{all}}$? | Corpus Representation & Handling Policy |
|---|---|---|---|
| `journal_article` | **YES** | **YES** | Searchable chunks indexed; canonical primary evidence. |
| `conference_paper` | **YES** | **YES** | Searchable chunks indexed; peer-reviewed proceedings only. |
| `review` | **NO** | **YES** | Excluded from $I_{\text{primary}}$; indexed in $I_{\text{all}}$ for sensitivity analysis. |
| `systematic_review` | **NO** | **YES** | Excluded from $I_{\text{primary}}$; indexed in $I_{\text{all}}$ for sensitivity analysis. |
| `correction` | **NO** | **NO** | Metadata-only. Linked to corrected paper; does not form separate retrieval chunks. |
| `retraction_notice` | **NO** | **NO** | Metadata-only. Linked to retracted paper; retracted papers excluded from all indexes. |
| `report` | **NO** | **NO** | Excluded grey literature under Phase 3 Section 4.2. Retained in discovery log only. |
| `accepted_manuscript` | **Conditional** | **Conditional** | Eligible as proxy for `journal_article` only if VoR is inaccessible and acceptance date is verified. |

#### 3.5.3 Invariant Shared Controls & Sensitivity Interpretation
- The question benchmark, gold claim rubrics, generation prompts, generator model, and evaluation metrics remain **100% identical** across $I_{\text{primary}}$ and $I_{\text{all}}$.
- $I_{\text{all}}$ results are strictly secondary and cannot replace or overwrite $I_{\text{primary}}$ findings.
- If dense retrieval performs better on $I_{\text{all}}$ than $I_{\text{primary}}$, this demonstrates that review articles introduce semantic aggregation artifacts rather than indicating superior primary evidence retrieval.

---

### 3.6 Task 6: Extraction Pilot & Single-Reviewer Calibration (Finding F-06)

#### 3.6.1 20-Paper Extraction Pilot Protocol
- **Stratification:** 5 standard 2-column papers, 5 mathematical/physics papers, 5 data-dense table papers, 3 graphic/conference papers, and 2 scanned/OCR papers.
- **Threshold Integrity:** No numerical Character Error Rate (CER) or Word Error Rate (WER) thresholds are invented. Numerical acceptance cutoffs remain **OPEN** until empirical distributions from the 20-paper sample are established.

#### 3.6.2 Single-Reviewer Calibration Integrity
- The 10% re-screening sample after a 14-day washout measures **intra-rater temporal consistency only**.
- It must **never** be described as inter-rater reliability, dual screening, or independent validation.
- Single-reviewer screening is explicitly declared as a methodological limitation in study reporting.

---

## 4. Decision Table Requiring Researcher Approval

```
=============================================================================================================================================
DECISION TABLE FOR RESEARCHER APPROVAL
=============================================================================================================================================
ID     Decision Topic             Recommended Policy                              Options / Alternatives Considered     Status
---------------------------------------------------------------------------------------------------------------------------------------------
DEC-01 Core Window                2024–2026 based on formal VoR year.             Option A: Strict 2024–2026 only.      PROVISIONAL —
                                                                                  Option B: Retrospective 2010–2026.    PENDING SIGN-OFF
                                                                                  Option C: Core + Chaining (Rec).
---------------------------------------------------------------------------------------------------------------------------------------------
DEC-02 Pre-2024 Chaining          Distinct first authors + 100% candidate         Alt A: Lead disjoint + manual audit.  PROVISIONAL —
                                  anti-self-citation; >=2 core primary citing.    Alt B: Distinct first + 100% anti-    PENDING SIGN-OFF
                                  Review citations excluded.                      self-citation (Recommended).
                                                                                  Alt C: ROR institutional separation.
---------------------------------------------------------------------------------------------------------------------------------------------
DEC-03 Date Precedence            VoR Volume > Online-First VoR > Accepted MS.    Option A: Earliest online date.       PROVISIONAL —
                                  Deposit date substitution strictly prohibited.  Option B: Formal VoR issue year (Rec).PENDING SIGN-OFF
                                  Disaggregated date metadata fields.             Option C: Repository deposit date.
---------------------------------------------------------------------------------------------------------------------------------------------
DEC-04 Discovery Sources          Multi-source: OpenAlex, Crossref, S2, OA.       Option A: Single-source (OpenAlex).   PROVISIONAL —
                                  No complete coverage claimed.                   Option B: Multi-source hybrid (Rec).  PENDING SIGN-OFF
---------------------------------------------------------------------------------------------------------------------------------------------
DEC-05 Query Registry & Benchmark 4 Query Families (Q1–Q4) deterministic ordering.Option A: Free text ad-hoc search.   PROVISIONAL —
                                  10 specific known-item papers with DOIs.        Option B: Pinned query families (Rec).BLOCKED (DOIs needed)
---------------------------------------------------------------------------------------------------------------------------------------------
DEC-06 Review Stratification      I_primary: primary research articles only.      Option A: Mix reviews into primary.   PROVISIONAL —
                                  I_all: primary research + review articles.      Option B: Exclude reviews entirely.   PENDING SIGN-OFF
                                  Secondary sensitivity analysis only.            Option C: Stratified dual index (Rec).
---------------------------------------------------------------------------------------------------------------------------------------------
DEC-07 Artifact Preservation      Text-first: captions, structured tables, and    Option A: Multimodal pixel encoding.  PROVISIONAL —
                                  LaTeX/MathML formulas; image pixels excluded.   Option B: Text-first preservation (Rec).PENDING SIGN-OFF
---------------------------------------------------------------------------------------------------------------------------------------------
DEC-08 Extraction Thresholds      Open threshold protocol; numerical cutoffs      Option A: Arbitrary CER cutoff (1%).  OPEN —
                                  established from 20-paper empirical pilot.      Option B: Empirical pilot (Rec).      PENDING PILOT
---------------------------------------------------------------------------------------------------------------------------------------------
DEC-09 Reference List Handling    Metadata only; excluded from retrieval chunks.  Option A: Index reference chunks.     PROVISIONAL —
                                                                                  Option B: Metadata only (Rec).        PENDING SIGN-OFF
---------------------------------------------------------------------------------------------------------------------------------------------
DEC-10 Screening Calibration      Single reviewer + 10% 14-day masked re-screen.  Option A: Claim dual review (False).  PROVISIONAL —
                                  Intra-rater consistency metric only.            Option B: Honest limitation +         PENDING SIGN-OFF
                                                                                  intra-rater calibration (Rec).
=============================================================================================================================================
```

---

## 5. Precise List of Unresolved Blockers

Before researcher sign-off can be completed and before real-paper discovery can be authorized, the following **two blockers** must be resolved:

1. **BLOCKER 1: Specification of the 10 Known-Item Benchmark Papers (DEC-05):**
   - The researcher must provide the verified Titles and DOIs for the 10 landmark 2024 solar-PV papers across the 5 declared subdomains so that Table 2.2.3 in [`phase8_2_signoff_checklist.md`](./phase8_2_signoff_checklist.md) becomes an executable benchmark test set.
2. **BLOCKER 2: Selection of Citation Chaining Rule (DEC-02):**
   - The researcher must formally approve **Alternative B** (Distinct First Authors + 100% Candidate Anti-Self-Citation) or select an alternative rule to replace the unexecutable "corresponding author" API assumption.

---

## 6. Files Changed and Reasons

1. **Created:**
   - [`notes/methodology/phase8_3_final_methodological_challenge.md`](./phase8_3_final_methodological_challenge.md) (this document) — Comprehensive independent methodological challenge report classifying findings, presenting defensible alternatives, and documenting unresolved blockers.
2. **Updated:**
   - [`notes/methodology/corpus_data_dictionary.md`](./corpus_data_dictionary.md) — Disaggregated publication date metadata fields (`formal_publication_year`, `online_publication_date`, `acceptance_date`, `repository_deposit_date`, `year_source`) and added explicit retrieval index eligibility mappings for all document types.
   - [`notes/methodology/phase8_2_signoff_checklist.md`](./phase8_2_signoff_checklist.md) — Updated Table 2.2.3 to explicitly mark known items as awaiting researcher DOIs, incorporated the Alternative B citation chaining rule, and reconciled date disaggregation.

---

## 7. Software and Regression Test Execution

```powershell
# Unit Test Discovery (69 tests across pipeline and corpus workflow)
$env:PYTHONPATH = "src"; .\.venv\Scripts\python -m unittest discover -s tests -q
# Result: Ran 69 tests in 0.812s — OK (0 failures, 0 errors, 0 skipped)

# Synthetic Pilot Smoke Test
$env:PYTHONPATH = "src"; .\.venv\Scripts\python scripts\run_synthetic_pilot.py
# Result: synthetic_technical_smoke_test_passed (2 synthetic docs, 2 questions, 6 condition runs)
```
*Scientific Validity Notice: These test executions verify software mechanics, data schema integrity, and JSONL serialization. They do not constitute scientific validation of the corpus or study outcomes.*

---

## 8. Next Action Required from Researcher

To grant formal protocol sign-off and unlock Phase 9 (Pilot Execution):
1. Review the Decision Table in Section 4 and confirm adoption of **Alternative B** for citation chaining (DEC-02).
2. Provide the 10 specific paper titles and DOIs for the predefined Known-Item Benchmark (DEC-05).
3. Sign off on the itemized checklist in [`notes/methodology/phase8_2_signoff_checklist.md`](./phase8_2_signoff_checklist.md).

**Real-paper discovery remains BLOCKED until these actions are completed.**



---

## Researcher decision update (2026-10-21)

This report is a historical audit snapshot. Subsequent researcher decisions approved DEC-02 Alternative B, approved the v0.2 hypothesis framing, and approved the ten known-item candidates in principle subject to final bibliographic and eligibility checks. These later decisions are recorded in `notes/methodology/protocol_closure_register.md`. They do not authorize the pilot; remaining sign-offs and the candidate eligibility audit are still required.
