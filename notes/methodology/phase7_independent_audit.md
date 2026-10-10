# Phase 7.1 — Independent Corpus Workflow Audit Matrix and Technical Report

**Project:** Solar Scientific RAG Literature Review  
**Date:** 2026-10-09  
**Status:** AUDIT COMPLETE — TECHNICAL SCENARIO VERIFIED, SCIENTIFIC CORPUS READINESS BLOCKED  

---

## 1. Executive Summary and Governing Constraints

This independent audit evaluates the Phase 7 corpus acquisition and curation workflow implementation ([`src/solar_rag/corpus_workflow.py`](../../src/solar_rag/corpus_workflow.py) and [`src/solar_rag/corpus.py`](../../src/solar_rag/corpus.py)) for correctness, edge cases, data integrity, and reproducibility.

### Frozen Constraints
- **Frozen Research Question:**  
  > *How do BM25, dense, and hybrid retrieval strategies, compared under identical corpus, question-benchmark, preprocessing, generator, prompt, and evaluation conditions, affect retrieval quality, answer quality, and evidence attribution in question answering over solar-PV scientific literature?*
- **Primary Retrieval Arms:** BM25, Dense, Hybrid (reciprocal rank fusion).
- **Readiness Status:**
  - Configuration Schema Validity: **PASS**
  - Software Pipeline Readiness: **PASS** (69 standard-library unit tests passing, synthetic pilot smoke test passing)
  - Scientific Corpus Readiness: **BLOCKED** (no real papers ingested, no live corpus approved)
  - Confirmatory Experiment Readiness: **BLOCKED** (production models, chunking, generator, prompts, and benchmark unapproved)

---

## 2. Independent Audit Matrix

| ID | Requirement / Capability | Implementation Location | Existing Test Coverage | Additional Tests Added | Actual Observed Result | Verdict | Remaining Risk |
|---|---|---|---|---|---|---|---|
| **REQ-01** | **DOI Normalization & URL Stripping**<br>Normalize resolver URLs (`https://doi.org/`, `http://dx.doi.org/`), `doi:` prefix, whitespace, query strings (`?utm_source=...`), URL fragments (`#page=1`), trailing slashes, and mixed case. | [`src/solar_rag/corpus.py#L34-L42`](../../src/solar_rag/corpus.py#L34-L42) | Single standard DOI test | `DoiAndTitleNormalizationTests.test_doi_normalization_variants` | All 11 URL, prefix, query string, fragment, trailing slash, and case variants normalize to canonical lowercase DOI suffix. | **VERIFIED** | Non-standard publisher resolver domains outside `doi.org` / `dx.doi.org` require manual URL stripping prior to ingestion. |
| **REQ-02** | **Malformed DOI Rejection**<br>Reject non-DOI strings, bare resolver URLs (`https://doi.org/`), bare `doi:`, or strings not starting with `10.`. | [`src/solar_rag/corpus.py#L34-L42`](../../src/solar_rag/corpus.py#L34-L42), [`src/solar_rag/corpus_workflow.py#L72-L74`](../../src/solar_rag/corpus_workflow.py#L72-L74) | None | `DoiAndTitleNormalizationTests.test_doi_normalization_rejects_malformed`, `test_candidate_doi_validation_rejects_malformed_doi` | Non-DOI strings return empty normalized string; candidate validation raises `ValueError("DOI value is present but non-normalizable.")`. | **VERIFIED** | Highly novel unregistered DOI formats with non-`10.` prefixes (if any exist) would be rejected. |
| **REQ-03** | **Missing DOI Handling & Stable Document ID**<br>Generate deterministic stable UUID5 document IDs (`doc-{uuid5}`) anchored by DOI if present, or by `normalize_title(title)|year` if DOI is absent. | [`src/solar_rag/corpus.py#L22-L32`](../../src/solar_rag/corpus.py#L22-L32) | Deterministic test on matching DOI | `StableDocumentIdTests.test_stable_document_id_without_doi_distinguishes_years`, `test_stable_document_id_empty_raises` | Distinct publication years for the same title generate distinct stable IDs. Records with same DOI generate identical IDs regardless of title variants. Missing title and DOI raises `CorpusValidationError`. | **VERIFIED** | Different papers sharing the exact same title, year, and lacking DOIs share an ID if not distinguished by metadata/manual review. |
| **REQ-04** | **Title Normalization & Unicode Edge Cases**<br>Apply Unicode NFKC normalization, whitespace collapsing (tabs, newlines), casefolding (e.g. German eszett `ß` -> `ss`), and ligature decomposition (e.g. `ﬁ` -> `fi`). | [`src/solar_rag/corpus.py#L44-L46`](../../src/solar_rag/corpus.py#L44-L46) | Basic lowercase test | `DoiAndTitleNormalizationTests.test_title_normalization_unicode_and_whitespace` | Unicode ligatures, full-width characters, and whitespace variants normalize consistently without data corruption. | **VERIFIED** | Punctuation differences (e.g. hyphens vs en-dashes) are preserved; fuzzy title matching must require human review. |
| **REQ-05** | **Duplicate Candidate Detection & Review Enforcement**<br>Detect duplicate candidates by normalized DOI (`status: duplicate`) and normalized title (`status: review_required`). Never silently merge or drop uncertain records. | [`src/solar_rag/corpus_workflow.py#L210-L243`](../../src/solar_rag/corpus_workflow.py#L210-L243) | 2 basic tests | `DuplicateDetectionAndScreeningTests.test_same_doi_with_conflicting_metadata_flagged_as_duplicate`, `test_unique_records_produce_no_duplicate_flags` | Conflicting metadata records sharing a DOI are flagged with `kind: doi, status: duplicate`. Shared titles across different records are flagged with `kind: title, status: review_required`. Original source records are preserved. | **VERIFIED** | Large-scale candidate deduplication still requires operator adjudication before final corpus freeze. |
| **REQ-06** | **Publication Year Coercion & Integrity**<br>Coerce valid integers and integer strings (including trimmed whitespace), reject booleans (`True`/`False`), out-of-range years (`<1000` or `>2200`), and non-numeric strings. | [`src/solar_rag/corpus_workflow.py#L125-L141`](../../src/solar_rag/corpus_workflow.py#L125-L141) | None | `PublicationYearCoercionTests.test_publication_year_coercion_valid`, `test_publication_year_coercion_invalid` | Rejects `True`/`False`, floats, invalid date strings (e.g. `"2024-05-01"` without year extraction), and years outside 1000–2200 with descriptive `ValueError`. | **VERIFIED** | Date parsing for complex publisher strings must occur before mapping to `publication_year`. |
| **REQ-07** | **Screening, Peer-Review & License Controlled Vocabularies**<br>Enforce strict controlled vocabularies: `screening_status`, `overlap_level`, `confidence`, `peer_review_status`, `full_text_status`, `license_status`, and `relevance_decision`. | [`src/solar_rag/corpus_workflow.py#L13-L59`](../../src/solar_rag/corpus_workflow.py#L13-L59), [`#L143-L200`](../../src/solar_rag/corpus_workflow.py#L143-L200) | `screening_status` only | `CorpusWorkflowValidationTests.test_peer_review_status_validation`, `test_license_status_validation`, `test_full_text_status_validation`, `test_confidence_validation`, `test_overlap_level_validation`, `test_status_helper_functions` | All controlled fields validate strictly against protocol enums. Arbitrary or fabricated statuses raise `ValueError`. | **VERIFIED** | External harvester scripts must map third-party API strings into these controlled enums. |
| **REQ-08** | **Extraction Quality & Note Requirement**<br>Validate extraction statuses (`not_started`, `successful`, `partial`, `failed`, `not_required`). Enforce mandatory `extraction_note` for `failed` and `partial` extractions. | [`src/solar_rag/corpus_workflow.py#L182-L188`](../../src/solar_rag/corpus_workflow.py#L182-L188) | 1 basic test | `CorpusWorkflowValidationTests.test_failed_and_partial_extraction_require_outcome_note` | Empty/absent `extraction_note` on partial/failed extractions raises `ValueError`. Successful extractions without note pass. Extraction failures never disappear silently. | **VERIFIED** | Successful text extraction does not guarantee scientific completeness (e.g., figure/table fidelity). |
| **REQ-09** | **Retraction, Correction & Review Flags**<br>Check `retraction_status` and `correction_status`. Trigger `review_required="yes"` for `retracted`, `correction_pending`, `corrected`, or `review_required`. | [`src/solar_rag/corpus_workflow.py#L254-L267`](../../src/solar_rag/corpus_workflow.py#L254-L267) | 1 test (retracted only) | `RetractionAndCorrectionTests.test_retracted_and_corrected_documents_are_flagged`, `test_unproblematic_status_does_not_trigger_review` | All actionable statuses (`retracted`, `correction_pending`, `corrected`, `review_required`) trigger `review_required="yes"`. Clean records yield `"no"`. | **VERIFIED** | Retraction databases (e.g., Crossmark, Retraction Watch) must be actively queried during real candidate screening. |
| **REQ-10** | **Source Provenance & Manifest Integrity**<br>Ensure every record tracks `source_name`, `source_url`, `search_query`, and `search_date`. Reconcile manifest counts (`record_count = inclusion + open + excluded`). Compute deterministic SHA-256 fingerprint. | [`src/solar_rag/corpus_workflow.py#L269-L333`](../../src/solar_rag/corpus_workflow.py#L269-L333) | Basic summary test | `ManifestAndProvenanceIntegrityTests.test_manifest_reconciles_all_counts`, `test_manifest_deterministic_hash` | Manifest counts reconcile completely with screening and extraction distributions. Manifest SHA-256 fingerprint is deterministic and immutable. Missing provenance fields raise immediate validation error. | **VERIFIED** | Manifest captures aggregate counts and duplicate candidate records; raw candidate dumps should accompany the manifest. |

---

## 3. Detailed Technical Findings and Defect Corrections

During this independent audit, four concrete implementation defects were identified and corrected:

1. **DOI Normalization Edge Cases (Fixed in [`src/solar_rag/corpus.py`](../../src/solar_rag/corpus.py)):**
   - *Previous Issue:* `normalize_doi` used `value.removeprefix("doi:")` after `value = doi.strip().lower()`. If input was `"DOI: 10.1000/182"`, stripping left leading whitespace (`" 10.1000/182"`). Query parameters (`?utm_source=...`), URL fragments (`#page=1`), and trailing slashes from resolver URLs were retained in the DOI string. Malformed strings without standard DOI syntax were returned unchanged.
   - *Fix Applied:* Updated `normalize_doi` with regex substitution for `doi:\s*`, query strings/fragments removal (`[?#].*$`), trailing slash trimming, and prefix verification requiring `10.`.

2. **Missing Controlled Enum Validation in Candidate Metadata (Fixed in [`src/solar_rag/corpus_workflow.py`](../../src/solar_rag/corpus_workflow.py)):**
   - *Previous Issue:* `validate_candidate_metadata` validated `screening_status`, `overlap_level`, `confidence`, and `full_text_status`, but omitted validation for `peer_review_status`, `license_status`, and `relevance_decision`. Invalid strings were accepted without error.
   - *Fix Applied:* Defined `PEER_REVIEW_STATUS_VALUES`, `LICENSE_STATUS_VALUES`, `RELEVANCE_DECISION_VALUES` and added strict enum membership checks raising descriptive `ValueError`s.

3. **Incomplete Retraction/Correction Review Triggers (Fixed in [`src/solar_rag/corpus_workflow.py`](../../src/solar_rag/corpus_workflow.py)):**
   - *Previous Issue:* `retraction_flags` checked `{"retracted", "correction_pending", "review_required"}`, but omitted `corrected`. Under the protocol ([`notes/methodology/corpus_acquisition_workflow.md#L160-L175`](../../notes/methodology/corpus_acquisition_workflow.md#L160-L175)), corrected papers must be audited to ensure the version of record contains the correction notice rather than uncorrected text.
   - *Fix Applied:* Added `"corrected"` to the review trigger set so that any paper with `correction_status="corrected"` triggers `review_required="yes"`.

4. **Empty String and Whitespace Coercion in Metadata Validation (Fixed in [`src/solar_rag/corpus_workflow.py`](../../src/solar_rag/corpus_workflow.py)):**
   - *Previous Issue:* Whitespace-only `record_id`, `title`, `source_name`, `search_query`, and `search_date` strings were not rejected uniformly before candidate creation.
   - *Fix Applied:* Added mandatory non-empty checks for `record_id`, `title`, `source_name`, `search_query`, and `search_date` in `validate_candidate_metadata`.

---

## 4. Verification and Regression Test Execution

### Test Execution Command
```powershell
$env:PYTHONPATH = "src"; .\.venv\Scripts\python -m unittest discover -s tests -q
```
**Observed Output:**
```text
----------------------------------------------------------------------
Ran 69 tests in 0.432s

OK
```

### Synthetic Pilot Execution Command
```powershell
$env:PYTHONPATH = "src"; .\.venv\Scripts\python scripts\run_synthetic_pilot.py
```
**Observed Output:**
```json
{
  "status": "synthetic_technical_smoke_test_passed",
  "fixture_type": "synthetic_software_validation_only",
  "documents_processed": 2,
  "shared_chunks_created": 2,
  "questions_exercised": 2,
  "condition_runs": 6,
  "scientific_performance_evaluated": false,
  "production_configuration_ready": false
}
```

### CLI Config Validation Command
```powershell
$env:PYTHONPATH = "src"; .\.venv\Scripts\python -m solar_rag.cli validate-config config\experiment.example.json
```
**Observed Output:**
```json
{
  "status": "valid_schema",
  "unresolved_decisions": [
    "benchmark_version_and_split",
    "bm25_analyzer_and_parameters",
    "chunking",
    "context_budget",
    "corpus_version",
    "dense_model_and_encoding",
    "evaluation_rubrics_and_thresholds",
    "generator_and_decoding",
    "hybrid_fusion_and_candidate_budget",
    "latency_protocol",
    "preprocessing_version",
    "prompt",
    "retrieval_cutoffs",
    "retry_and_timeout_policy",
    "shared_controls.benchmark_version",
    "shared_controls.chunking_version",
    "shared_controls.context_budget",
    "shared_controls.corpus_version",
    "shared_controls.evaluation_version",
    "shared_controls.generation_parameters",
    "shared_controls.generator",
    "shared_controls.preprocessing_version",
    "shared_controls.prompt_version",
    "vector_index_and_similarity"
  ],
  "study_execution_ready": false
}
```

---

## 5. Methodological Decisions and Open Issues

The following methodological items remain **OPEN** and must be formally approved before any real scientific literature collection begins:

1. **Publication-Period Window:** Confirmation of the 2024–2026 core discovery window and strict backward/forward citation chaining rules for pre-2024 foundational papers.
2. **Search-Source Mix & API Rate Limits:** Formal selection of primary metadata sources (OpenAlex, Crossref, Semantic Scholar) and lawful full-text repository endpoints.
3. **Review Article Stratification:** Whether review articles are included as a separate stratum or excluded from primary passage-level retrieval.
4. **Figure/Table/Equation Extraction Policy:** Text-first handling policy for multimodal artifacts and OCR quality thresholds.
5. **Deduplication Adjudication Queue:** Procedure for dual-screening title collisions and preprint/journal version reconciliation.

---

## 6. Audit Verdict and Readiness Status

- **Corpus Workflow Implementation Audit Verdict:** **VERIFIED** (All protocol requirements, edge cases, validation rules, and provenance integrity checks implemented and tested).
- **Scientific Corpus Readiness:** **BLOCKED** (No real papers ingested; candidate discovery pending protocol approval).
- **Confirmatory Experiment Readiness:** **BLOCKED** (Retrieval models, prompts, chunking, and expert benchmark pending).

---

## 7. Recommended Next Action

Do **NOT** ingest real papers or run downstream retrieval experiments.  
Proceed to **Phase 8 / Protocol Finalization**:
1. Formally resolve open methodological decisions (publication window, source mix, review article policy).
2. Prepare search query registry and lawful access verification before initializing candidate discovery.

