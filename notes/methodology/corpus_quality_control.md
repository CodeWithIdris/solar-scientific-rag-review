# Corpus Quality Control and Acceptance Protocol

Status: protocol-level QC plan for a real solar-PV corpus. This does not authorize a final study corpus or final experiment.

## 1. QC objectives

The QC workflow is designed to prevent silent corruption of the corpus and to require explicit resolution of missing, conflicting, or partial data before the corpus is used in any retrieval or QA benchmark.

## 2. Mandatory QC checks

### 2.1 Identifier integrity
- every record has a non-empty title
- every record has an identifier source when possible
- DOI normalization is consistent
- normalized title collisions are reviewed, not silently merged
- duplicate DOI cases are flagged

### 2.2 Metadata consistency
- publication year, DOI, source URL, source name, and document type are all checked for coherence
- conflicting or missing metadata triggers manual review
- if metadata is absent, the record must remain marked `not_assessed` or `not_checked`, not treated as valid evidence

### 2.3 Access and provenance
- source URL and retrieval timestamp are recorded
- access status is recorded
- open-access claims require explicit evidence
- a record without retrieval provenance is not accepted into a final corpus manifest

### 2.4 Extraction quality
- text hash must exist when text is stored
- extraction failures are explicitly logged and never hidden
- partial extraction requires a note explaining the missing content
- figure-, table-, and equation-only extraction without narrative text is flagged

### 2.5 Screening quality
- included records must have evidence-based solar-PV relevance
- excluded records must have explicit exclusion reasons
- ambiguous records must be queued for manual review
- all review decisions must be time-stamped and attributable

### 2.6 Retracted/corrected materials
- retraction or correction status is checked
- retracted or corrected records are excluded or quarantined until review

## 3. Sampling plan

Use a structured QC sample from the candidate set:
- 10% random sample of included records
- 10% random sample of excluded records
- all duplicate candidates
- all failed or partial extraction records
- all retraction/correction flags
- all manual review items

If QC failures exceed a predeclared threshold, the corpus version must be rejected or reworked before it is approved.

## 4. Acceptance criteria

A corpus version is acceptable only if:
- all required fields for the canonical candidate records are present
- duplicate or near-duplicate records are reviewed and resolved
- no silent extraction failure is hidden
- all source URLs and version identifiers are preserved
- all included records have a documented solar-PV relevance reason
- all excluded records have reason codes and evidence pointers
- all retracted/corrected records are marked appropriately

## 5. Manual review queue requirements

Manual review should be required for:
- duplicate DOI/title collisions
- title-based false positives
- ambiguous access or license status
- extraction failures
- ambiguous peer-review status
- preprint-to-journal version ambiguity
- review-article inclusion decisions
- article-level relevance borderline cases

## 6. Change log and version freeze

Any corpus update must produce a new version and a changelog entry describing:
- added records
- removed or excluded records
- merged or deduplicated records
- extraction corrections
- metadata corrections
- reason for the version bump

An approved version may be used only when the QC summary and manifest are both recorded and reproducible.

## 7. Open decisions that remain unresolved

The following are explicitly unresolved and must be decided before final corpus approval:
- exact publication window
- inclusion of review articles and conference papers
- final language coverage
- exact share of open-access versus subscription-only material allowed
- final extraction completeness threshold
- final manual-review sample size and pass criteria
- exact final corpus size target
