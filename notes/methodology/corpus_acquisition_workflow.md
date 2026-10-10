# Solar-PV Corpus Acquisition and Curation Workflow

Status: PROTOCOL WORKFLOW ONLY. This workflow governs how a real solar-PV scientific corpus is collected, screened, and documented. It does not authorize final study execution, final corpus approval, or final benchmark construction.

## 1. Frozen decisions and open decisions

Frozen:
- Research question remains unchanged.
- Retrieval strategy remains the manipulated variable.
- BM25, dense, and hybrid are the three primary arms.
- The final corpus must be shared across all arms.
- No final experiment is run from this workflow.

Provisional:
- Use peer-reviewed journal and conference papers as the default eligible document type, with review articles separated into a distinct stratum if included.
- Open-access/full-text availability is preferred but not required for discovery metadata; status must be recorded explicitly.

Open:
- exact publication-period window
- exact search-source mix
- exact eligibility thresholds for review articles, non-journal outputs, and regional or language coverage
- final corpus size and inclusion cutoff
- final extraction method and figure/table policy
- final manual-review queue criteria

Deferred:
- final benchmark construction
- final retrieval technical settings
- final downstream scientific experiment

## 2. Objective

This workflow creates an auditable, versioned, and documented corpus acquisition path for solar-PV literature suitable for downstream retrieval and question answering. It does not imply scientific readiness, benchmark completion, or model approval.

## 3. Sources and reproducible search queries

Use public metadata sources and lawful open-text sources only. Search sources may include:
- Crossref
- OpenAlex
- Semantic Scholar
- Google Scholar (for exact-title or metadata verification, not as a primary full-text source)
- publisher search pages and DOI landing pages
- institutional repositories and author manuscripts where the legal and access-status record is explicit
- curated solar-energy bibliographic databases when available and lawfully accessible

For each search, record:
- source name
- exact query string
- search date/time in UTC
- engine/URL or API call identifier
- query filters used
- page count and result count (when available)
- retrieval provenance and access conditions

Minimum query patterns should be explicit and reproducible, not ad hoc. Example patterns include:
- `"solar photovoltaic" "efficiency" OR "PV" "degradation"` with document-type filters
- `"photovoltaic" AND ("reliability" OR "degradation" OR "module" OR "cell")`
- `"solar PV" AND ("question answering" OR "retrieval" OR "literature review")` only for screening, not final corpus composition

Query strings and parameters must be preserved in a manifest. Exact search results are not proof of eligibility; they are discovery records only.

## 4. Search dates and retrieval timestamps

Each discovery record, metadata fetch, and full-text retrieval must log:
- retrieval timestamp in UTC
- source
- method (API, publisher page, DOI resolution, repository access, manual review)
- access status
- URL or metadata identifier
- observed license or access note if visible

This is required for auditability and later reproducibility checks.

## 5. Inclusion and exclusion criteria

Inclusion must be explicit and evidence-based. It should include:
- peer-reviewed scientific articles or review articles whose central subject is PV technology or PV-relevant scientific analysis
- methodological or systems papers whose methods, experiments, or results directly concern PV performance, reliability, degradation, systems, or materials
- reviews or syntheses when the paper itself is a scientific article and not merely a general survey or non-evidence external commentary

Exclusion must be explicit and recorded:
- non-peer-reviewed or non-scientific materials without an approved reason to include
- general solar/renewable or energy policy materials where PV is incidental
- technical reports, patents, books, editorials, posters, and blog content when the study does not explicitly include them in scope
- duplicate records, retracted/corrected versions, and non-substantive metadata-only entries

If a record is excluded for any reason, capture the reason code and the evidence basis.

## 6. Solar-PV relevance screening

Screening must be performed at three stages:
1. metadata/title/abstract relevance
2. full-text relevance and methodological fit
3. eligibility and corpus-entry decision

At each stage, record:
- screening decision
- evidence basis
- confidence
- reviewer or operator identifier
- date
- unresolved issues

A record is in scope only when the paper’s methods, results, or research question are substantively about photovoltaic science or PV systems, not merely when keywords appear.

## 7. Publication metadata and DOI handling

Required publication metadata:
- title
- authors
- publication year
- DOI if available
- source name / publisher
- source URL or landing page
- document type
- peer-reviewed status
- publication venue if available
- OpenAlex or Crossref identifier when available
- license or access metadata when present

DOI normalization:
- lowercase the DOI
- drop URL prefixes (`https://doi.org/`, `http://dx.doi.org/`, `doi:`)
- preserve the canonical DOI suffix

If DOI conflicts with metadata or title changes, create a duplicate review record rather than silently merging.

## 8. Open-access/full-text eligibility

Eligibility includes a distinction between metadata access and full-text access. A record may be discovered and included in a candidate list without immediate full-text access. Do not claim open access or legal text access without evidence.

Record status values:
- not_checked
- not_found
- open_access
- subscriber_only
- partial_text
- extracted
- not_applicable

Open-access or approved lawful repository copies are preferred; they may be used only when access rights are clear and the source is cited in the manifest.

## 9. Duplicate and version detection

Before inclusion, check for:
- duplicated DOI
- duplicated normalized title
- same authors/year/title with different metadata variants
- preprint and journal-version pairs
- correction and retraction notices
- same article discovered through multiple sources

A duplicate is not automatically excluded without review. It requires a version-status decision:
- keep one canonical record
- retain alternative source URLs as provenance
- prefer the most complete peer-reviewed version if both are eligible
- preserve the superseded record in a change log

## 10. Retracted papers and corrections

Every candidate record must have:
- retraction_status
- correction_status
- review_required flag if a retraction or correction is suspected

Possible values:
- not_checked
- not_retracted
- retracted
- correction_pending
- corrected
- review_required

Retracted or corrected records must not be silently used as evidence. They are either excluded or separate from the canonical corpus until adjudicated.

## 11. Full-text extraction and extraction failures

When full text is available, record:
- extraction method
- extraction status
- exact source path or URL
- page range coverage
- file format
- text hash
- extraction failures
- missing or inaccessible sections

Required statuses:
- not_started
- successful
- partial
- failed
- not_required

If extraction fails or is partial, do not hide the failure. Record:
- reason code
- missing content type (e.g., equations, tables, figures, OCR issue, scanned PDF, permissions)
- whether manual review is required
- whether the record is retained in the candidate list or excluded

## 12. Tables, equations, figures, captions, and references

The extraction workflow should preserve evidence structure, not only plain text. For each document, record whether:
- tables were extracted
- equations were extracted
- captions were extracted
- figures were identified
- references were parsed or linked
- layout-based or OCR-based extraction was used

This matters because solar-PV scientific evidence often appears in tables, equations, and figure captions. They are not optional metadata. They must be represented in the corpus manifest or flagged as missing.

## 13. Document identifiers and source provenance

Every corpus record should have:
- stable document ID
- canonical title
- DOI
- source URL
- source name
- retrieval timestamp
- access date
- license or access note
- text hash if extracted
- text path if stored locally
- duplicate_of if merged
- version marker or revision identifier

This ensures a record can be traced back to its source and version without guessing.

## 14. Manual review queue

A manual review queue is required for:
- duplicate candidates
- ambiguous title matches
- DOI conflicts
- open-access uncertainty
- extraction failures
- retracted/corrected material
- borderline PV relevance
- review article inclusion decisions

Manual review must record:
- reviewer
- date
- reason for review
- decision
- evidence location
- final status

No record should remain ambiguous without a flag and a review action.

## 15. Corpus versioning and change logs

Each corpus snapshot must have:
- version identifier
- search date and time
- source list and query list
- inclusion and exclusion counts
- manifest hash
- list of record additions, removals, and amendments
- reason for changes
- operator or reviewer who approved the change

Corpus snapshots must be immutable once approved for a given experiment. If a change is required, it becomes a new version rather than silent mutation.

## 16. Quality-control sampling and acceptance criteria

Use quality control at the corpus and extraction level:
- random sample of metadata records for DOI/title/year consistency
- random sample of included/excluded records for screening correctness
- sample of extracted full texts for text completeness and hash validity
- sample of duplicate review resolutions
- sample of extraction partial/failure records

Acceptance criteria:
- no unresolved internal identifier conflicts
- no silent missing DOI/title/year records in canonical corpus entries
- no undisclosed extraction failures in final corpus manifest
- no unreviewed duplicate set remains open
- no record without provenance is accepted into the canonical corpus

## 17. Quality-control reporting

The workflow must create a QC summary with:
- sample size and selection method
- acceptance rates
- failures and reasons
- manual review queue counts
- unresolved items
- whether a corpus version is approved or provisional

## 18. Allowed data handling and ethics

Use public metadata and openly accessible text where lawful and clearly allowed. Do not:
- bypass paywalls or access restrictions
- fabricate an open-access license or claim lawful access without evidence
- store credentials in manifests or source files
- use personal or non-public metadata as a corpus source

Source URLs, access dates, access restrictions, and license notes must be preserved when visible.

## 19. Deferred items and decision process

The workflow leaves unresolved decisions intentionally open. For each open item, record:
- candidate values
- evidence need
- consequence of each option
- proposed decision process
- relevant phase owner

Examples:
- publication-period window
- source mix and search-depth strategy
- whether review articles are included and how they are stratified
- final extraction acceptance threshold
- final manual-review acceptance policy

The workflow is a reproducible collection procedure; it does not finalize the scientific corpus.

## 20. Phase 8 Protocol Finalization Reference

The protocol decisions for corpus acquisition have been formalized in [notes/methodology/phase8_protocol_decision_register.md](./phase8_protocol_decision_register.md):
- **Core Publication Window (DEC-01):** 2024–2026 inclusive, anchored by formal Version of Record (VoR) year.
- **Pre-2024 Foundational Chaining (DEC-02):** Strict algorithmic backward citation chaining ($\ge 2$ independent citations from eligible core papers); tagged `foundational_earlier=true`.
- **Query Registry Families (DEC-05):** Standardized across Q1 (Identity), Q2 (Systems/Degradation), Q3 (Materials/Devices), and Q4 (Forecasting/Diagnostics).
- **Review Article Stratification (DEC-06):** Ingested but tagged with `document_type="review"` to allow separate primary vs review sensitivity analyses.
- **Tables, Equations, Figures & OCR (DEC-07, DEC-08):** Text-first preservation; numerical OCR thresholds remain OPEN pending a 20-PDF extraction pilot.
- **Screening Adjudication (DEC-10):** Primary screener with a 10% stratified calibration re-screening sample.

