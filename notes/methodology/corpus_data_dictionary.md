# Corpus Data Dictionary

Status: protocol-level schema for corpus acquisition and curation. This is not a production corpus or benchmark schema and does not represent a final approved scientific dataset.

## 1. Core record schema

Each candidate or corpus record must include the following fields when available.

### Record-level fields

- `record_id`: stable internal identifier, generated from the normalized DOI/title/year hash when available.
- `source_name`: discovery source (e.g., Crossref, OpenAlex, Semantic Scholar, publisher landing page, repository, manual review).
- `source_url`: canonical landing URL or metadata page.
- `search_query`: exact reproducible query string used to discover the record.
- `search_date`: UTC date or timestamp of the retrieval action.
- `title`: title as recorded in source metadata.
- `doi`: normalized DOI string where available.
- `publication_year`: integer publication year when available.
- `authors`: list of author names when available.
- `document_type`: controlled values: journal_article, conference_paper, review, systematic_review, correction, retraction_notice, report.
- `peer_review_status`: not_checked, peer_reviewed, not_peer_reviewed, unclear.
- `full_text_status`: not_checked, not_found, open_access, subscriber_only, partial_text, extracted, not_applicable.
- `license_status`: not_recorded, cc_by, cc_by_sa, other, rights_unclear, no_license_info.
- `retraction_status`: not_checked, not_retracted, retracted, correction_pending, corrected, review_required.
- `correction_status`: same enum pattern as retraction_status.
- `extraction_status`: not_started, successful, partial, failed, not_required.
- `extraction_note`: required when extraction_status is partial or failed.
- `screening_status`: not_assessed, include_core, include_context, potentially_relevant, exclude.
- `relevance_decision`: same as screening_status or a more explicit decision field if used in a downstream manifest.
- `overlap_level`: none, low, moderate, high, critical.
- `confidence`: low, medium, high.
- `duplicate_of`: canonical document record ID if merged after review.
- `version`: record version or revision tag when available.
- `text_path`: local extracted text path when stored.
- `text_sha256`: SHA-256 hash of extracted full text when present.
- `metadata`: free-form additional metadata, source-specific fields, or manual-review notes.

## 2. Required evidence fields

A record used in final corpus curation must include enough evidence to trace the decision:
- why the record was included or excluded
- evidence for solar-PV relevance
- evidence for peer-review status
- evidence for license or access status
- evidence for duplicate/version status
- evidence for failed or partial extraction
- evidence for final canonicalization or merge decisions

## 3. Screening/status field rules

- `screening_status` must be one of the allowed values only.
- `overlap_level` must only use `none`, `low`, `moderate`, `high`, `critical`.
- `confidence` must only use `low`, `medium`, `high`.
- `extraction_status` of `partial` or `failed` requires a concrete `extraction_note`.
- `full_text_status` must be left as `not_checked` if no source access or legal check has been performed.

## 4. Synthetic-data labeling

Any synthetic example record used in software tests must be labeled clearly as synthetic in its metadata and not treated as a real corpus record.

## 5. Manifest fields

A corpus manifest should record the following summary values:
- corpus_name
- version
- search_query
- search_date
- record_count
- screening_status_counts
- extraction_status_counts
- inclusion_count
- open_or_unassessed
- duplicate_candidates
- sha256
- status

## 6. Retention rules

- Do not silently delete failed or partial extraction records.
- Preserve the original discovery record and the reason for retention/exclusion.
- If a record is excluded, keep its exclusion reason and evidence basis in the canonical candidate set or exclusion log.
- If a record is merged due to duplicate detection, preserve the merged-to and merged-from identifiers.

## 7. Open decisions that remain unfixed

This schema is intentionally not a final scientific corpus schema. The following remain open and must be approved before final study use:
- publication window
- language coverage
- review-article inclusion rules
- figure/table extraction standards
- use of preprints and author manuscripts
- final inclusion thresholds and QC acceptance criteria
