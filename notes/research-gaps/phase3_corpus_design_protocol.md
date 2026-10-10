# Phase 3 — Solar-PV Scientific Literature Corpus Design and Construction Protocol

## Status and scope

**Protocol stage:** design only. This document does not authorize large-scale document downloading, final corpus construction, indexing, embedding generation, benchmark construction, or experimental evaluation.

**Frozen research question (reproduced without modification):**

> How do BM25, dense, and hybrid retrieval strategies, compared under identical corpus, question-benchmark, preprocessing, generator, prompt, and evaluation conditions, affect retrieval quality, answer quality, and evidence attribution in question answering over solar-PV scientific literature?

The same corpus snapshot, document versions, extracted content, metadata policy, and shared chunk store must be supplied to BM25, dense, and hybrid arms. Corpus selection must not favor any retrieval arm or be tailored using final benchmark questions, answers, or evidence labels.

Decision labels used below:

- **FROZEN:** fixed by the research question or governing study constraints.
- **PROVISIONAL:** recommended policy requiring approval and explicit confirmation before collection.
- **OPEN:** no value is selected; this protocol states how it must be resolved and when it must be frozen.
- **DEFERRED:** intentionally assigned to a later phase.

## 1. Phase 3 objective

Specify a reproducible and auditable protocol that determines:

1. what solar-PV scientific literature is eligible;
2. where and how eligible records are discovered;
3. how candidate records are screened, deduplicated, and version-resolved;
4. how lawful, usable full text is acquired;
5. how document quality, metadata, extraction, and provenance are checked;
6. how a fixed, versioned common corpus is released for the three retrieval strategies.

The benchmark and question/evidence annotations are not designed or created in this phase.

## 2. Corpus scope

The intended corpus is scientific literature substantially concerned with solar photovoltaic (solar-PV) technology, systems, performance, or directly relevant scientific/technical analysis.

The corpus is a text-first retrieval corpus. It includes source-faithful full text and structured text representations only where those can be extracted and traced reproducibly. It is not a general solar-energy library, an energy-policy corpus, a web-search index, a multimodal image corpus, or a collection of all records containing a PV keyword.

The study's conclusions will apply to the documented sampling frame and included documents, not to all solar-PV research or every language, region, technology, or publication venue.

## 3. Domain definition

### 3.1 Eligible subject matter

A document is in scope when its research question, methods, results, or analysis substantively concern photovoltaic conversion or PV systems. Potentially eligible subjects include:

- photovoltaic materials, cells, devices, manufacturing, and cell/module efficiency;
- silicon, thin-film, organic, perovskite, tandem, bifacial, and other PV technologies;
- module and array performance, thermal behavior, degradation, reliability, and failure;
- PV system design, integration, operation, control, monitoring, diagnostics, and fault detection;
- PV generation forecasting and resource assessment when directly focused on PV output or deployment;
- PV-related techno-economic, environmental, lifecycle, or sustainability analysis when photovoltaic systems are the analyzed technology;
- methods or measurement studies whose primary evaluation is on PV systems/materials or whose output directly supports PV research.

### 3.2 Out-of-scope subject matter

Exclude documents where “solar” refers only to solar thermal, solar fuels, photosynthesis, astronomy, or general insolation without a substantive PV research contribution; general renewable-energy work without separable PV analysis; generic power-system work mentioning PV only as one incidental example; and unrelated expansions of “PV.”

For mixed-technology studies, include only if PV is a substantive study object and the relevant evidence is not merely incidental. Record the rationale and any technology-specific separability.

### 3.3 Operational screening question

At title/abstract and full-text stages, ask:

> Would the document's principal research question, method, results, or evaluated application still be substantially about photovoltaic technology or a PV system if incidental uses of the words “solar,” “energy,” “renewable,” and “PV” were removed?

This question guides, but does not replace, the explicit eligibility checklist in Section 13. A “yes” requires recorded evidence (e.g., aim, methods, results); vague topical resemblance is not sufficient.

## 4. Document-type policy

### 4.1 Recommended primary policy — PROVISIONAL

The primary corpus should include full-text, peer-reviewed:

- original research articles in scholarly journals;
- full research papers in peer-reviewed conferences;
- systematic reviews and other scholarly review articles with substantive PV research synthesis;
- methodological or technical research articles with evaluated methods/results directly relevant to PV.

Systematic reviews and research reviews are included as scientific documents, but their document type is explicitly tagged and can be reported as a separate stratum or sensitivity subset. They must not be misrepresented as primary experiments.

### 4.2 Categories excluded from the primary corpus — PROVISIONAL

| Document type | Primary policy | Reason |
|---|---|---|
| Preprints without a peer-reviewed version | Exclude from primary corpus; retain discovery record and link to any later version | Review status and version stability differ; including both can duplicate evidence and vary quality status |
| Theses/dissertations | Exclude | Different review, length, structure, and document granularity; difficult to compare with article corpus |
| Books/book chapters | Exclude | Different publication and full-text access regimes; heterogeneous chapter/document units |
| Standards | Exclude | Normative rather than research-literature evidence; distinct update and authority characteristics |
| Technical/government/industry reports | Exclude from primary corpus | Grey-literature status and publication processes differ; could form a separately justified extension, not silently mixed |
| Patents | Exclude | Legal disclosure documents, not peer-reviewed scientific articles |
| Dataset records/data-only objects | Exclude as corpus documents; preserve linked dataset metadata where useful | Not comparable full-text research articles |
| Web pages, vendor pages, news, blogs | Exclude | Not stable peer-reviewed scientific literature |
| Abstract-only conference records/posters | Exclude | Insufficient full text for passage-level evidence retrieval |
| Editorials, letters, news items, calls, corrigenda without research content | Exclude unless a correction/retraction notice is needed for status | Not substantive research evidence |

If a preprint later has a peer-reviewed publication, apply the version policy in Section 16 and use one primary document record. If a peer-reviewed conference paper has a journal extension, do not automatically include both.

### 4.3 Decision status and resolution

Peer-reviewed journal/conference research and reviews as eligible types is **PROVISIONAL**. Confirm the policy before systematic screening, based on the research question, access/licensing feasibility, and whether review articles are needed for intended question coverage. Any change after screening begins requires a new protocol version and re-screening of affected records.

## 5. Publication-period policy

### 5.1 Options and methodological consequences

| Option | Consequence |
|---|---|
| A. Strictly 2024–2026 | Produces a current, bounded literature sample and aligns with the working search period. It may omit foundational PV knowledge, longer-term degradation/reliability studies, and established methods; some question types could be difficult to support. |
| B. Broader fixed publication window | Improves historical and technical coverage but increases volume and risks mixing literature eras, document versions, and evolving terminology. The start year must be justified rather than chosen for convenience. |
| C. 2024–2026 discovery core plus eligible earlier foundational papers | Preserves a recent discovery frame while allowing demonstrably relevant earlier work. It risks subjective “foundational” selection and citation-network bias unless earlier-paper inclusion has a strict, logged rule. |

### 5.2 Recommended policy — PROVISIONAL, not yet frozen

Use **Option C** as the working recommendation:

1. The systematic database search covers publication years 2024–2026, with the exact final search date recorded and the 2026 range ending on that date.
2. Earlier papers may enter only through a documented backward/forward citation-chaining step from already eligible core records or a predeclared domain-specific seminal-work source.
3. Earlier candidates must meet the same domain, document-type, language, full-text, status, and quality criteria as core records.
4. Tag every included pre-2024 document as `foundational_earlier=true`, record the citation-chain/source and reason, and report the number and proportion separately.
5. Do not use benchmark questions, gold answers, or test evidence to identify or include earlier papers.

The earlier-paper rule must be converted into a precise, auditable procedure before collection. If that rule cannot be applied consistently, choose Option A or B before collection rather than relying on informal judgement. The final publication-period decision and exact boundaries are **OPEN** until protocol approval; once approved, freeze before discovery starts.

## 6. Language policy

### 6.1 Recommended primary policy — PROVISIONAL

English-language full text only for the primary experiment. This supports consistent tokenization, dense model/query encoding, generation, human evaluation, and benchmark annotation. English-only is a scope limitation, not a claim that English represents all solar-PV research.

Non-English records may be logged during discovery, but are excluded from the primary corpus with `non_english_full_text` as primary exclusion reason unless a separately designed multilingual experiment is approved before collection.

### 6.2 Translation

Machine- or human-translated documents should not be mixed into the primary corpus without a separately justified translation protocol. Translation can alter terminology, numbers, units, symbols, and the relative effectiveness of lexical versus dense retrieval. Translation therefore changes a controlled input and may be a confound. Translation is excluded from the primary protocol; a multilingual/translated extension is **DEFERRED**.

Language-identification tool, handling of bilingual documents, and threshold for classifying document language are **OPEN**. Resolve using a pilot sample and manual verification before screening at scale; freeze before final corpus inclusion.

## 7. Full-text policy

### 7.1 Requirement

Usable full text is mandatory for inclusion in the primary retrieval corpus. Abstract-only and metadata-only records are discovery records only and must not be indexed as corpus documents. This follows from the study's passage-level evidence retrieval and evidence-attribution objectives.

A usable full text must:

- represent the selected document version completely enough to contain substantive methods/results/discussion;
- be legally obtained and retained/processed for the research use;
- permit extraction of traceable text beyond metadata/abstract;
- preserve enough structure and locators to support reliable evidence attribution.

### 7.2 Accepted source formats

Accepted input formats may include publisher or repository PDF, machine-readable HTML/XML, or a lawful author/institutional manuscript. Prefer structured HTML/XML when it is the authoritative/legitimate version and preserves document structure; retain or link to the corresponding source file and version.

The accepted format ranking, preservation format, and whether both PDF and structured text are retained are **OPEN** and must be fixed in the acquisition protocol.

### 7.3 Difficult or unavailable documents

| Condition | Handling |
|---|---|
| Paywalled/inaccessible full text | Do not bypass access controls. Check lawful institutional access, author/institution repository, or publisher-authorized copy. If still unavailable, exclude with `full_text_inaccessible`; retain discovery metadata and attempt log. |
| Abstract only | Exclude from primary corpus with `abstract_only`; preserve record in screening log. |
| Scanned PDF | OCR may be used only under a predeclared OCR and quality-control protocol. If required content is not reliably recoverable, exclude with `unusable_scanned_text`. |
| Corrupted/malformed file | Retry lawful source acquisition; if unresolved or unusable, exclude with `corrupt_or_unusable_full_text`, retain hashes and error log. |
| Partial full text | Exclude if substantive sections or evidence locations are missing; record what was available. |
| Supplementary material | Treat as a separately linked item under the same eligibility and access policy; inclusion in searchable corpus is OPEN and must be decided before collection. |

Never silently discard problematic files. Every failed retrieval, OCR, parsing, or QC case receives a status and reason.

## 8. Discovery sources

Separate record discovery, metadata validation, and full-text acquisition. No source is presumed to offer unrestricted programmatic access.

| Role | Candidate sources | Intended use and constraints |
|---|---|---|
| Reproducible broad discovery | OpenAlex; Crossref | Search bibliographic metadata, DOI, venue, year, concepts/fields where supported. Record API version/endpoint, query, filters, retrieval date, pagination, and response snapshots. Respect rate limits and terms. |
| Scholarly discovery/citation chaining | Semantic Scholar; Google Scholar; Web of Science/Scopus if licensed | Supplementary discovery and citation chaining, not a presumed comprehensive or unrestricted API. Record exact query/date and export method; obey site/database access terms and institutional license. |
| Domain/venue discovery | IEEE Xplore; ScienceDirect; SpringerLink; ACM Digital Library; relevant society/publisher indexes | Search relevant peer-reviewed venues and validate publication/version metadata. Search access may require subscription; record coverage, query syntax, access route, and limitations. |
| Biomedical subset where directly relevant | PubMed | Use only for directly relevant PV-health/materials/environmental research indexed there; not as a primary PV discovery source. |
| Preprint/repository discovery | arXiv; institutional repositories; publisher-authorized repositories | Locate versions and full text, but preprint-only records remain excluded under the provisional document-type policy. Use to link versions or obtain a lawful manuscript for a peer-reviewed record. |
| Full-text acquisition | Publisher open access; publisher subscription access; institutional repository; author manuscript where lawful; recognized open repositories | Acquire only under applicable terms. Record version, URL, access date, license and permitted retention/use. |

### 8.1 Source selection

Before collection, select a primary reproducible metadata/discovery source set and a supplementary source set. Avoid treating Google Scholar results as a complete database or scraping where prohibited. A source can be used for citation chasing or validation without being an automated primary source.

Exact providers, access mode, licensed coverage, API versions, and source ranking are **OPEN**. Resolve before search execution; freeze the source set and access method in the protocol.

## 9. Search strategy

### 9.1 Search construction principles

Searches use focused photovoltaic concept families and selected technical terms. Do not combine every possible term into one opaque query. Search syntax is adapted to source capabilities while preserving conceptual coverage. Search fields should prefer title/abstract/keywords where available; full-text search is used only when its behavior and coverage are documented.

Use search blocks for:

- PV technology identity;
- technical application/topic;
- publication date and document type, when supported by the source.

Search strategy should be broad enough to retrieve varied PV subdomains but must be followed by substantive relevance screening; a keyword hit alone is not sufficient for inclusion.

### 9.2 Search date and period

The working core period is 2024–2026. For each actual run, record date, timezone, source-specific date semantics, and exact upper bound. If search execution occurs after 2026, do not silently extend the window; approve a protocol amendment before searching.

### 9.3 Search execution and update

Run a pilot of source-specific query syntax on a small, recorded sample before the approved search. Inspect a sample of hits and known eligible records for retrieval failures. Amend queries only before the formal search, record rationale and version, then execute the frozen query set. A later update is a new search run with a new date/version and a preserved prior result set.

## 10. Search-query registry

The following are **candidate templates**, not verified live queries or completed searches. Field codes and syntax must be adapted and tested per source before formal execution. Save the exact executed string and a frozen query-registry row for every source/query/run.

### 10.1 Candidate core query families

**Q1 — Broad PV identity**

```text
("photovoltaic" OR "photovoltaics" OR "solar PV" OR "solar photovoltaic"
 OR "PV module" OR "PV cell" OR "solar cell")
```

**Q2 — PV systems and performance**

```text
("photovoltaic" OR "solar PV" OR "solar photovoltaic")
AND
("PV system" OR "module performance" OR "PV performance" OR efficiency
 OR degradation OR reliability OR operation OR monitoring)
```

**Q3 — PV materials and devices**

```text
("photovoltaic" OR "solar cell" OR "PV cell")
AND
(material OR silicon OR perovskite OR tandem OR bifacial
 OR "thin film" OR "organic photovoltaic")
```

**Q4 — PV forecasting, resources, diagnosis**

```text
("photovoltaic" OR "solar PV" OR "PV system")
AND
(forecasting OR prediction OR "resource assessment" OR diagnosis
 OR fault OR failure OR thermal OR lifecycle OR techno-economic)
```

Q2–Q4 are separate focused searches, not mandatory universal strings. Terms may be revised based on source syntax and a pre-search pilot; any revision receives a new query version.

### 10.2 Source-specific adaptation examples

Examples below illustrate structure only; source field names and Boolean support must be verified:

```text
TITLE-ABS-KEY((photovoltaic OR photovoltaics OR "solar PV" OR "solar photovoltaic")
AND (performance OR efficiency OR degradation OR reliability OR materials))
AND PUBYEAR > 2023 AND PUBYEAR < 2027
```

```text
title,abstract,keywords: (photovoltaic OR photovoltaics OR "solar PV")
AND (module OR cell OR system OR degradation OR forecasting)
Year: 2024-2026
```

For OpenAlex/Crossref-style APIs, store the exact API filter/parameter string and request URL, not merely a human-readable summary. For publisher databases, store field restrictions, filter settings, result count, and export date.

### 10.3 Mandatory query registry fields

Each executed search row records:

```text
search_run_id
query_id
query_version
source_name
source_role
exact_query_string
field_restrictions
date_filters
document_type_filters
language_filters
execution_timestamp_and_timezone
source/API/version
page_or_cursor_parameters
result_count_reported_by_source
records_exported
export_file_hash
searcher
notes/deviations
```

Store raw exports or lawful response snapshots and their hashes. Do not claim these candidate queries have been executed.

## 11. Corpus-size rationale

### 11.1 Working target — PROVISIONAL

Retain approximately **500–1,000 unique, eligible scientific documents** as a planning range, not a quota or stopping rule. The actual corpus size is constrained by eligibility, lawful full-text access, extraction quality, domain coverage, and reproducibility. Do not inflate the corpus to reach a number.

### 11.2 Recommended target logic

Use a **source-constrained, coverage-aware yield** rather than a rigid fixed count or unlogged saturation claim:

1. Define the source set, search window, and queries before counting eligible papers.
2. Screen every retrieved unique candidate using the same criteria.
3. Report counts at discovery, deduplication, screening, full-text access, QC, and final inclusion stages.
4. Assess topic, document-type, year, geography, and technology coverage among eligible full-text records.
5. If the initial yield is below the planning range, do not relax criteria silently; evaluate whether additional approved sources/query families or a narrower inferential scope are justified.
6. If yield exceeds feasible processing capacity, apply a documented sampling procedure after eligibility screening and before benchmark construction, preserving strata and random seed; do not cherry-pick based on anticipated question evidence.

The final target, feasibility cap, and any sampling/stopping procedure are **OPEN**. Resolve with a pilot search yield, extraction-resource estimate, retrieval-index feasibility, and coverage profile. Freeze before large-scale collection. Do not use benchmark outcomes to determine corpus size.

### 11.3 Size evidence

The pilot should estimate candidate volume, unique/full-text yield, document length and extraction burden, major-topic distribution, and technical feasibility. A power calculation for downstream questions does not directly determine corpus size; benchmark size and corpus coverage are related but distinct decisions.

## 12. Topic-coverage strategy

Track subject labels to diagnose concentration and omissions. Candidate labels:

- materials/cells/devices;
- modules and module performance;
- systems/design/operation/integration;
- efficiency and performance;
- degradation/reliability/failure;
- forecasting/resource assessment;
- diagnostics/fault detection;
- manufacturing;
- thermal behavior;
- techno-economic/environmental/lifecycle;
- emerging technologies (e.g., perovskite, tandem, bifacial, organic).

A document may receive multiple tags, with one primary topic for summary tables. Define a short annotation guide and multi-label procedure before screening. Do not impose arbitrary equal quotas across topics; prevalence and source coverage may differ substantially. Report the realized distribution and address underrepresented areas as limitations.

Whether to use stratified sampling to cap a very large yield is **OPEN**. If needed, predefine strata and sampling probabilities based only on corpus metadata/topic tags, not benchmark questions or retrieval performance.

## 13. Inclusion criteria and screening checklist

Include a candidate only when all required items are satisfied:

1. **Scientific literature:** scholarly research/review publication under the approved document-type policy.
2. **Solar-PV relevance:** substantive PV focus evidenced in objective, methods, results, or analysis.
3. **Scientific content:** contains methods, evidence, results, or substantive scholarly synthesis useful for domain QA.
4. **Publication period:** meets the frozen core/earlier-paper policy and has a verified publication date.
5. **Document type:** meets the frozen policy; peer-review status verified where applicable.
6. **Language:** meets the frozen language policy.
7. **Full text:** complete enough and lawfully available in an accepted format.
8. **Usability:** content can be extracted or faithfully represented with traceable locations.
9. **Version identity:** selected primary version is identifiable and linked to duplicates/related versions.
10. **Integrity status:** not retracted under the policy; correction/expression-of-concern status checked and recorded.

### Screening stages

- **Title/abstract screening:** exclude clearly irrelevant records; uncertain cases advance to full-text screening.
- **Full-text screening:** record a yes/no/unclear result for every criterion, supporting locator/text note for topical relevance, and one primary disposition.
- **Quality/status screening:** assess publication type, peer-review evidence, retraction/correction status, completeness, and extraction reliability. Do not score scientific “quality” using journal prestige or citation counts as a substitute for relevance/integrity.

Recommended reviewer procedure is two independent screeners for title/abstract and full text, with disagreements reconciled by discussion or third-party adjudication. This is **PROVISIONAL**; if staffing makes dual review infeasible, record the alternative, measure a duplicate-screened calibration sample, and document reliability/limitations before large-scale screening.

## 14. Exclusion criteria and reason codes

Each excluded record has exactly one **primary** exclusion reason; secondary notes may record additional issues.

| Primary reason code | Use when |
|---|---|
| `not_solar_pv_focused` | PV is incidental or document is about another solar/energy topic |
| `not_scientific_literature` | Not a scholarly research/review document |
| `outside_publication_period` | Outside the approved date/earlier-paper rule |
| `unsupported_document_type` | Document type excluded by policy |
| `non_english_full_text` | Full text fails approved language scope |
| `abstract_only` | No substantive full text is available |
| `full_text_inaccessible` | Lawful full-text routes exhausted or access unavailable |
| `corrupt_or_unusable_full_text` | File/text remains unusable after documented recovery/QC |
| `insufficient_scientific_content` | No substantive evidence/methods/results/synthesis for QA |
| `unrelated_pv_term` | “PV” or similar term is unrelated to photovoltaics |
| `duplicate_record` | Redundant database record for same document/version |
| `duplicate_version_not_selected` | Alternate version linked to retained primary version |
| `retracted` | Retraction policy requires exclusion |
| `insufficient_pv_focus_mixed_study` | Mixed study contains no separable/substantive PV component |
| `other_protocol_reason` | Only for a reason not covered above; requires explanatory note and protocol review |

Where several reasons apply, use a predeclared reason precedence (e.g., duplicate record first for record-level duplicates; otherwise scope, type/date/language, full-text/access, usability/status) and retain secondary notes. Do not classify exclusion reason post hoc to favor a desired corpus profile.

## 15. Deduplication protocol

### 15.1 Record-level duplicate detection

Normalize and compare, in order:

1. DOI (case/URL/prefix normalization);
2. PMID, arXiv ID, publisher/article ID, repository ID;
3. normalized title plus author and year;
4. fuzzy title similarity for candidate pairs only, followed by human verification;
5. file and text hashes for identical files or extracted text.

Do not automatically merge records solely because titles are similar. Preserve all source records and create explicit `duplicate_of` or `related_version_id` links.

### 15.2 Similar but distinct documents

Conference and journal versions, corrections, translations, and substantially revised manuscripts are reviewed as related versions, not assumed duplicates. A journal extension may contain materially new work; include both only if the document-type policy, research scope, and anti-duplication rule explicitly allow it and the relationship is recorded. The default primary-corpus policy is one canonical version per underlying work.

### 15.3 Required audit fields

Record match method, compared identifiers, normalized title, adjudication, retained canonical record, linked alternatives, reviewer, date, and rationale. Preserve original bibliographic records and source-specific IDs.

Deduplication thresholds and fuzzy-match tooling are **OPEN**; calibrate on a manually reviewed candidate-pair sample, measure false merge/split cases, and freeze before automated large-scale resolution.

## 16. Version-resolution protocol

### 16.1 Primary version hierarchy — PROVISIONAL

For a peer-reviewed work with multiple copies, select one canonical primary full text in this order where lawful and usable:

1. corrected publisher version of record;
2. publisher version of record if no correction is indicated;
3. accepted manuscript in a lawful institutional/author repository when the publisher version is unavailable or its use is restricted;
4. preprint only if it is the sole version and the study's approved document-type policy is amended to permit it.

Record all known versions and links, but do not index multiple versions of the same work in the primary corpus by default. Use one `document_id` for the work and version-specific `version_id` values.

### 16.2 Specific cases

- **Preprint vs published article:** retain the peer-reviewed published version as canonical; preserve preprint ID/link and differences if known. If no published version exists, exclude under the provisional policy.
- **Accepted manuscript vs publisher version:** use the publisher version if lawfully available and usable; otherwise use the accepted manuscript and record this choice.
- **Corrected article:** use the corrected version; preserve correction notice and prior version link.
- **Retraction:** exclude retracted works from the primary evidence corpus; preserve metadata/status in a separate exclusion register.
- **Expression of concern:** provisional exclusion pending status clarification, or inclusion only after documented adjudication before corpus freeze. The handling rule is **OPEN** and must be finalized before screening.
- **Journal extension of conference paper:** retain one version unless the extension is demonstrably distinct and a preapproved policy permits both; log overlap and rationale.

All version rules must be applied consistently before corpus freeze. No silent replacement or overwrite is allowed.

## 17. Retraction and correction policy

Check Crossref/Crossmark where available, publisher pages, and a recognized retraction-status source before corpus freeze. Record query/date/source and status.

- Exclude papers formally marked retracted at freeze time from the primary corpus.
- If corrected, include the corrected version and record correction metadata.
- For expressions of concern or unresolved integrity notices, quarantine from the primary corpus until adjudicated under a documented rule.
- Recheck status shortly before corpus freeze; later status changes create a new corpus version, not a silent edit.
- Exclude duplicate publications according to Section 15 and retain all linked records/status notices.

Retraction-screening sources and exact recheck cadence are **OPEN**; select a feasible, documented set and freeze before final versioning.

## 18. Metadata schema

### 18.1 Required document metadata

| Field | Description |
|---|---|
| `document_id` | Stable internal identifier for the canonical scholarly work |
| `version_id` | Stable identifier for the specific retained document version |
| `title` | Source title and normalized title in separate fields if normalized |
| `authors` | Ordered author list as published |
| `publication_year` | Verified year for retained version |
| `publication_date` | Full date where available, with source |
| `journal_or_venue` | Journal/conference/venue |
| `document_type` | Controlled vocabulary from approved policy |
| `doi` | DOI where available |
| `other_identifiers` | PMID, arXiv ID, publisher ID, repository ID, etc. |
| `publisher` | Publisher/society/institution |
| `peer_review_status` | Verified/not verified/unknown and evidence |
| `source_database` | Discovery/metadata source(s) |
| `open_access_status` | Status and source/date checked |
| `license_if_available` | License identifier/text or `not reported` |
| `url` | Landing-page URL; do not assume it is a full-text URL |
| `full_text_url` | Lawful full-text source URL |
| `full_text_source_type` | Publisher, repository, accepted manuscript, etc. |
| `version_type` | Version of record, accepted manuscript, preprint, corrected version |
| `retraction_status` | Status, source, check date |
| `correction_status` | Status and linked notice |
| `expression_of_concern_status` | Status and linked notice |
| `abstract` | Abstract as retrieved; retain source and retrieval date |
| `keywords` | Published/indexed keywords, with source |
| `subject_categories` | Source categories and locally assigned multi-label PV topics |
| `language` | Detected/verified language and method |
| `date_added` | First discovery date |
| `date_screened` | Screening date(s) |
| `inclusion_status` | Included/excluded/uncertain/quarantined |
| `exclusion_reason` | One primary code plus optional notes |
| `corpus_version` | Immutable corpus release identifier |
| `foundational_earlier` | Whether pre-core-window inclusion was approved |
| `topic_labels` | Controlled multi-label subject assignment |

### 18.2 Provenance and processing fields

Also record:

```text
search_run_id
query_id/query_version
source_record_id
original_identifier_values
first_seen_source/date
metadata_source/date
full_text_acquisition_method/date
access/permission notes
duplicate_group_id
duplicate_of/related_version_ids
screening_answers and supporting notes
screening_reviewer(s)/adjudicator/date
file_path or controlled object reference
file_format/file_size
file_hash
extraction_tool/version/configuration
text_hash
preprocessing_version
QC status/flags
corpus_version
```

Do not place restricted full-text content in an unrestricted metadata export.

## 19. Full-text acquisition protocol

For each eligible candidate:

1. Resolve canonical DOI/identifier and validate bibliographic metadata.
2. Check publisher full-text availability and license/terms.
3. Check lawful institutional subscription access where available.
4. Check publisher-authorized open-access copy or institutional/author repository.
5. Verify that the downloaded file/version corresponds to the intended work and record version type.
6. Record URL, access date, retrieval mechanism, license/permission information, and file hash.
7. Store the file only in an access-controlled location under applicable terms.
8. If inaccessible, record routes tried and assign `full_text_inaccessible`; do not bypass controls or silently omit.

Accepted input formats, archive retention, provider terms, and full-text storage location are **OPEN**. Resolve with institutional policy and licensing review before acquisition starts.

## 20. Text-extraction protocol

### 20.1 Pipeline

For each retained full text:

1. retain immutable source file and verify file hash;
2. extract document metadata and page/section structure;
3. extract text from PDF, HTML, or XML using a pinned tool/version/configuration;
4. reconstruct reading order and paragraphs, especially for multi-column PDFs;
5. preserve headings, section paths, page numbers, paragraph boundaries, captions, and table/equation identifiers;
6. identify references, footnotes, headers, and footers;
7. create canonical retrieval text without deleting source-faithful text;
8. retain mapping from every text span to document/version/page/section/offset;
9. run automated and manual extraction QC;
10. version the extraction output and hash it.

### 20.2 Error handling

Check multi-column order, ligatures, hyphenation, Greek/special characters, subscripts/superscripts, minus signs, decimal points, ranges, units, equations, tables, footnotes, headers/footers, references, scanned pages, missing pages, and boilerplate.

Use OCR only under a documented, pinned OCR procedure. Compare OCR/extracted output with source pages on the pilot sample. If scientific meaning or locators cannot be recovered adequately, quarantine or exclude with an explicit reason. Do not make silent text “repairs”; all normalization rules must be versioned and reversible to source text.

Extractor/OCR tools, versions, extraction order, and thresholds are **OPEN**. Select by a pilot of structurally diverse documents, checking reading order, source-span traceability, numeric/symbol fidelity, and extraction completeness. Freeze before bulk extraction.

## 21. Tables, equations, and figures policy

The primary experiment is text-first; it is not multimodal retrieval.

### 21.1 Recommended representation — PROVISIONAL

- Include article prose and section headings.
- Include table captions and table contents when they can be extracted as readable, source-linked text without misleading row/column loss.
- Include equation text and nearby explanations only where the equation can be represented faithfully and linked to its location.
- Include figure captions and stable figure identifiers; do not index image pixels or use vision retrieval in the primary experiment.
- Keep references distinguishable from article body; inclusion in retrieval is addressed in Section 22.
- Preserve exclusions/failed extraction for tables, equations, and figures in per-document QC.

If a table/equation cannot be faithfully represented, do not fabricate a text representation. Exclude that object from searchable content and record the limitation; if its loss makes the document materially incomplete for the intended text-first corpus, quarantine/exclude the document under the usability policy.

### 21.2 Status

Whether tables/equations/captions are searchable in the primary corpus, which representations qualify, and whether supplements are included remain **OPEN**. Resolve using pilot extraction/QC and the text-first scope; freeze the policy before bulk extraction. Adding image interpretation or multimodal embeddings would change the experimental scope and is **DEFERRED** to a separately justified extension.

## 22. Reference-list policy

### 22.1 Primary recommendation — PROVISIONAL

Exclude bibliographic reference lists from the searchable retrieval text in the primary experiment. References can create superficial lexical matches, expose titles of relevant papers without their evidence, and alter the apparent value of BM25/dense retrieval independently of scientific-content retrieval. Retain references as structured metadata for deduplication, version linkage, and citation chaining, not as ordinary evidence chunks.

### 22.2 Boundary treatment

Separate in-text citations from reference-list entries where extraction permits. Retain in-text citation markers only if they are part of source-faithful body text; they are not treated as evidence by themselves. A reference section that cannot be separated reliably triggers QC review.

This exclusion is a design choice that may affect literature discovery and retrieval results; confirm it before corpus construction. If included in a sensitivity corpus, report as a separate, explicitly labeled corpus variant, not mixed into the primary corpus.

## 23. Quality-control protocol

### 23.1 Automated checks

For every record/file/text:

- required metadata fields present or explicitly marked missing;
- identifiers normalized and internal ID unique;
- file readable and hash recorded;
- extracted text non-empty and page/section locators present where supported;
- abnormal replacement/control-character frequency;
- language consistent with policy;
- repeated header/footer and boilerplate detection;
- suspiciously short/long text relative to document type;
- page-count and extracted-text-count consistency;
- duplicate file/text/chunk detection;
- source-to-extraction traceability;
- retraction/correction/status fields checked.

### 23.2 Manual checks

Use a pilot with varied publishers, document lengths, layouts, and content types. Compare extracted output against rendered/source pages for:

- reading order and paragraph boundaries;
- scientific terms and abbreviations;
- numbers, signs, units, formulas, Greek characters;
- tables, captions, equation representation, and references;
- missing pages/sections and boilerplate;
- locators and evidence traceability.

During screening, record criterion-level decisions and supporting evidence. Use independent double-screening or the approved calibration/adjudication procedure.

### 23.3 Threshold policy

Do not invent arbitrary text-length, OCR-confidence, character-frequency, or extraction-error thresholds. Determine candidate thresholds from pilot distributions and manual error analysis; define which failures require correction, quarantine, or exclusion before bulk processing. Freeze thresholds and QC code before final corpus acceptance.

Quality assessment is not a prestige ranking. Do not exclude a paper solely due to low citation count, venue impact factor, or disagreement with expected findings. Assess integrity, publication status, relevance, completeness, and extractability.

## 24. Contamination controls

Keep discovery, corpus eligibility, and benchmark construction procedurally separate:

- Do not use final benchmark questions, expected answers, or gold evidence to search for, include, exclude, rank, or rebalance papers.
- Do not remove a paper because it fails to support a benchmark answer or a desired result.
- Freeze corpus membership and document versions before Phase 4 benchmark construction begins.
- Phase 4 may identify that a proposed question lacks usable evidence in the frozen corpus; resolve through benchmark eligibility/answerability rules, not by covertly adding a favorable document. Any corpus amendment creates a new corpus version and requires a documented protocol amendment and impact assessment.
- Keep development and test labels/evidence inaccessible to retrieval tuning; the corpus can contain documents needed to answer questions, but gold annotations must remain protected.
- Deduplicate papers, versions, and benchmark question variants; retain provenance of question/document relationships for later leakage analysis.
- Record generator pretraining exposure as an uncertainty; do not claim it is fully preventable.

## 25. Corpus-benchmark interface

Benchmark construction, questions, answers, evidence annotations, and answerability decisions are **DEFERRED to Phase 4**. This phase specifies only corpus-side support and interfaces.

The corpus must expose stable document/version IDs, chunk/span IDs after shared chunking, source locators, and text that can support:

- factual questions;
- comparative questions;
- causal/explanatory questions;
- methodological questions;
- quantitative questions;
- multi-document questions;
- potentially unanswerable questions.

This is a support requirement, not a commitment that the benchmark will contain every type. Phase 4 determines benchmark composition and annotation methodology without changing the frozen corpus. Evidence spans should be traceable to the corpus version, source document, version, page/section, and text offsets. Do not construct questions or answer annotations in Phase 3.

## 26. Corpus-versioning protocol

Use immutable, semantic version labels with a documented manifest. Suggested lifecycle:

```text
corpus_v0.x  discovery and screened candidate snapshots
corpus_v0.y  extraction/QC candidate snapshots
corpus_v1.0  approved frozen experimental corpus
corpus_v1.1+ documented corrections/additions after freeze (new experiment version)
```

The exact naming convention is **OPEN**, but the invariants are frozen:

- a corpus version is immutable once used for final evaluation;
- no in-place replacement, deletion, or metadata correction without a new version;
- each version has a manifest of document/version IDs, file hashes, text hashes, inclusion status, and protocol/code versions;
- changes have a change log, reason, date, approval, and impact statement;
- all experimental runs reference the exact corpus version and manifest hash.

Changes after v1.0 are new corpus releases; results from different releases are not pooled as if they used the same corpus.

## 27. Provenance requirements

For every candidate and included document preserve:

- discovery source, exact search run/query, discovery date, and source record ID;
- original DOI/PMID/arXiv/publisher/repository identifiers;
- metadata source and date;
- source URL and lawful full-text URL/source;
- access route, date, license/permission notes, and version type;
- screening responses, inclusion/exclusion decision, one primary reason, evidence note, reviewer/adjudication;
- duplicate group and linked versions;
- retraction/correction/expression-of-concern checks and sources;
- original file hash, extracted-text hash, extraction tool/version/configuration;
- preprocessing and corpus version;
- QC flags, remediation, exclusions, and manual changes.

Preserve source-to-text mapping for every retrieval passage. Provenance must not depend solely on a mutable URL.

## 28. Bias and validity assessment

| Threat | Can it be mitigated? | Mitigation | Residual limitation |
|---|---|---|---|
| Publication bias | Partly | Search multiple sources; include null/negative results when eligible; do not select by outcomes | Published literature may still overrepresent positive findings |
| Database coverage bias | Partly | Use a reproducible broad metadata source plus approved publisher/domain sources; report source coverage | No database covers all PV literature; licensed sources may be unavailable |
| Open-access bias | Partly | Seek lawful institutional/author manuscripts and record access attempts | Full-text requirement will favor accessible records; inaccessible papers are excluded |
| English-language bias | No within primary English-only scope | Record language exclusions and state scope explicitly | Non-English PV research is not represented |
| Topic bias | Partly | Track multi-label topic distribution; inspect undercoverage; avoid arbitrary quotas | Search vocabulary and full-text yield can still skew subfields |
| Publisher/venue bias | Partly | Search across publishers and metadata services; report included-source distribution | Coverage and quality of indexing differ; subscriptions may constrain discovery |
| Year bias | Partly | Apply fixed date policy and report year distribution; earlier foundational route is logged separately | The 2024–2026 focus underrepresents older work; citation chaining adds selection bias |
| Document-type bias | Yes, but scope-limiting | Apply explicit peer-reviewed article/review policy; tag types | Excludes valuable reports, standards, theses, and preprints |
| Full-text availability bias | Partly | Use lawful author/institution copies; log attempted routes and exclusion counts | Full-text-only retrieval corpus necessarily excludes inaccessible work |
| Duplicate-version bias | Largely | Identifier/title/version deduplication and explicit relationships | Ambiguous conference/journal extensions may require judgment |
| Geographical research bias | Partly | Record study geography/author affiliations when available; report distribution | Metadata and publication-source coverage can obscure geography |
| Technology-generation bias | Partly | Tag technology type/generation; inspect chronological coverage | Older and emerging technologies may be imbalanced under the date policy |
| Peer-review/status error | Partly | Verify venue/version and retraction/correction status from publisher/crossmark sources | Status databases may lag or disagree |
| Extraction-format bias | Partly | Pilot across publishers/layouts; audit OCR/tables/symbols; preserve source mapping | Complex equations, images, and tables may remain poorly represented in text-first corpus |
| Citation-chaining bias | Partly | Restrict earlier-paper pathway; record seed and chain depth; report separately | Citation networks favor already connected and highly cited work |
| Selection-reviewer bias | Partly | Dual screening, calibration, adjudication, decision audit | Human judgments remain necessary for substantive PV focus |

The corpus is a documented study sample, not a perfectly representative census of solar-PV research.

## 29. End-to-end corpus workflow

| Stage | Action | Required record/output | Stop/failure rule |
|---|---|---|---|
| 1. Protocol approval | Freeze sources, date/language/type policy, queries, screening rules, and QC design | Approved protocol version and decision log | No formal search before approval |
| 2. Discovery | Execute registered queries and approved citation chaining | Search registry, raw exports, counts, hashes, timestamps | New query requires versioned amendment |
| 3. Metadata collection | Preserve source metadata and normalize identifiers | Candidate-record table and source provenance | Missing key fields flagged for resolution |
| 4. Identifier normalization | Normalize DOI/other IDs and title/author/year fields | Normalized metadata plus original values | Do not overwrite source metadata |
| 5. Deduplication | Exact-ID, file/text, then human-adjudicated fuzzy matching | Duplicate groups, retained canonical record, rationale | Ambiguous pairs go to adjudication |
| 6. Title/abstract screening | Apply checklist independently/approved calibration | Criterion decisions and primary exclusion reason | Uncertain cases advance to full text |
| 7. Full-text retrieval | Obtain lawfully or record routes and failure | Full-text file/version/source, license, hash or access-failure record | Inaccessible documents excluded from primary corpus with reason |
| 8. Full-text screening | Apply all inclusion criteria with evidence notes | Full-text decision table, reviewers, locators | Uncertain cases adjudicated; no silent inclusion |
| 9. Status/version resolution | Select canonical version; check correction/retraction status | Version graph and status record | Retracted excluded; concern quarantined per policy |
| 10. Quality/QC assessment | Validate completeness, source integrity, and usability | Automated reports, manual audit, remediation log | Unusable content quarantined/excluded with reason |
| 11. Text extraction | Run pinned extraction/OCR and preserve structure | Source-mapped extracted text, tool/configuration, hashes | Failed extraction retried or excluded explicitly |
| 12. Text validation | Compare extraction to source and run content checks | QC status, flags, threshold results, corrected version | Failures not silently repaired or omitted |
| 13. Metadata validation | Validate required fields, status, and provenance | Validated metadata with missingness log | Unresolved fields remain marked unknown or block inclusion if required |
| 14. Coverage audit | Summarize year, topic, type, geography, publisher, language | Corpus profile and bias/coverage report | Add sources only via approved amended search; no question-driven additions |
| 15. Corpus freeze | Assign immutable version and manifest | Corpus version, complete IDs, hashes, protocol and code revision | Any later change creates a new version |
| 16. Versioned release | Preserve lawful files/text/manifests and access limitations | Read-only release/archive and change log | Release scope follows licenses; no unauthorized redistribution |

At each stage record input count, output count, exclusions, status, timestamps, scripts/configuration version, operator/reviewer, errors, and hashes where applicable.

## 30. Frozen decisions

1. The frozen research question is not modified.
2. The primary target is solar-PV scientific literature, not general solar/energy material.
3. The identical corpus snapshot and document versions must be used by BM25, dense, and hybrid retrieval.
4. Corpus membership is fixed before final retrieval evaluation; changes create a new corpus version.
5. Corpus selection must not use final benchmark questions, answers, or gold evidence to favor documents.
6. The primary corpus requires usable full text; abstract-only and metadata-only records do not enter the retrieval corpus.
7. Every included/excluded record receives an auditable screening status and every exclusion one primary reason.
8. Every document requires traceable provenance and stable internal identity.
9. Retractions, corrections, duplicates, and versions must be checked and handled explicitly.
10. Phase 3 does not construct the benchmark or run retrieval systems.

## 31. Provisional decisions

| Decision | Working recommendation | Rationale | Must be confirmed before |
|---|---|---|---|
| Document types | Peer-reviewed journal and full conference research papers; include substantive reviews tagged separately; exclude grey literature, patents, standards, theses, books, web pages, and preprint-only works | More consistent scholarly publication type and document structure | Formal search/screening |
| Publication window | Option C: core 2024–2026 discovery plus logged earlier foundational works under a strict route | Preserves current search frame while allowing critical historical coverage | Any search execution |
| Language | English full text for primary experiment; report as limitation | Control of retrieval, generation, and evaluation language | Screening |
| Full text | Mandatory, complete enough for evidence passage retrieval and traceable locators | Required by retrieval and attribution objectives | Acquisition |
| Earlier foundational papers | Citation-chained, separately tagged, same eligibility criteria | Constrains subjective backward expansion | Citation chaining |
| Reference lists | Exclude from searchable body; retain structured for deduplication/chaining | Avoids reference-title lexical matches as pseudo-evidence | Text extraction freeze |
| Tables/equations/figures | Text-first; preserve faithful text/captions where extraction is reliable; no image retrieval | Avoids silently introducing multimodal retrieval | Extraction pilot |
| Corpus size | 500–1,000 as planning range only, source-constrained and coverage-aware | Balances retrieval diversity and processing feasibility without forcing a quota | Large-scale collection |
| Review procedure | Dual screening with adjudication; if infeasible, calibrated duplicate-screening sample and explicit limitation | Reduces subjective inclusion variation | Screening launch |

None of these becomes frozen merely by appearing in this table. Protocol approval must explicitly accept or amend each item.

## 32. Open decisions

| OPEN decision | Why it matters | Evidence needed | How resolved | Development use? | Freeze point |
|---|---|---|---|---|---|
| Final publication period and earlier-paper rule | Alters historical coverage and selection bias | Pilot yield/coverage, domain rationale, early-paper yield | Approve Option A/B/C and exact dates/chaining rule; record separately tagged earlier papers | Not a retrieval development-set decision; use discovery pilot only | Before formal search |
| Exact source set and access modes | Determines discovery coverage/reproducibility | API/database capabilities, access and license terms, overlap/yield | Approve primary/supplementary sources and compliant query/export method | No test data; source pilot permitted | Before formal search |
| Final search strings, fields, filters | Query choices determine candidate set | Source syntax tests and known-record retrieval checks | Pilot, revise/version, then freeze query registry | Pilot search only, before formal search | Before formal search run |
| Document-type policy confirmation | Changes scientific evidence population | Research aim, full-text yield, document-type review status | Accept/amend provisional policy; record rationale | No benchmark or retrieval outcomes | Before screening |
| English classification/language detection | Determines language eligibility | Language tool behavior and manual pilot | Choose detection method and bilingual document rule | Pilot may be used | Before screening |
| Full-text formats, lawful storage, retention | Affects access, QC, reproducibility, compliance | Institutional policy, licenses, provider terms | Obtain policy/legal/institutional review; approve storage method | No final corpus needed | Before acquisition |
| Corpus target/cap/stopping and sampling | Affects coverage, feasibility, selection bias | Search yield, processing effort, topic profile | Pilot yield and resource estimate; fixed/saturation/source-constrained rule documented | Discovery pilot only | Before large-scale collection |
| Topic taxonomy and primary labels | Controls representation audit and possible stratification | PV domain expertise and pilot sample | Finalize annotation guide and multi-label rules | Pilot screening sample allowed | Before formal screening |
| Dual screening feasibility and calibration | Affects reliability and workload | Staffing, calibration agreement/disagreements | Confirm two reviewers or alternate calibration design | Pilot screening allowed | Before screening at scale |
| Deduplication fuzzy threshold/tool | False merges/splits alter corpus and version counts | Manually adjudicated candidate-pair sample | Calibrate and freeze threshold plus human review route | Pilot metadata only | Before automated dedup at scale |
| Version hierarchy edge cases | Determines duplicate evidence and canonical source | Publisher/repository policy and version availability | Approve precedence and conference/journal extension rule | Case-by-case review | Before corpus freeze |
| Expression-of-concern policy | Integrity risk and ambiguous status | Publisher/status source evidence and study scope | Approve quarantine/exclude/conditional handling | No benchmark use | Before final screening |
| Retraction/status sources and cadence | Status can change over time | Crossref/Crossmark/publisher source coverage | Select source set and final recheck date | No retrieval dev use | Before corpus freeze |
| Extraction/OCR tooling and versions | Errors can damage evidence and ranking | Diverse publisher/layout pilot; fidelity/locator audit | Compare candidate tools on pilot; define pass/fail/repair criteria | Pilot documents only | Before bulk extraction |
| QC thresholds | Arbitrary thresholds can exclude valid documents | Pilot distributions and manual error analysis | Predeclare thresholds and remedial workflow | Pilot permitted | Before bulk QC |
| Tables/equations/captions/supplements | Impacts text coverage and evidence units | Pilot extraction fidelity and corpus scope | Approve included elements and representation; no images in primary arm | Pilot documents only | Before extraction freeze |
| Reference-list separation | Included references can create misleading matches | Extraction reliability, retrieval rationale | Confirm body/reference parsing and exclusion handling | Pilot extraction only | Before corpus freeze |
| Corpus manifest schema/version naming | Required for immutable reproducibility | Engineering needs and artifact constraints | Approve schema, hashing, access control and naming | Prototype schema only, no final corpus | Before candidate snapshots |

Every resolution must include decision, rationale, evidence, date, responsible person, protocol version, and whether it changes any previously screened record.

## 33. Deferred decisions

- **Phase 4:** benchmark/question-set design, question types and counts, answerability labels, reference answers, evidence-span annotation, annotator qualification, adjudication, and benchmark leakage controls. Phase 4 receives the frozen corpus and its stable document/span provenance; it must not silently alter corpus membership.
- **Phase 5 / implementation planning:** final retrieval-unit/chunk generation and index-build execution according to Phase 2 and the approved corpus protocol. Phase 3 does not create indexes or embeddings.
- **Later evaluation protocol:** generator and prompt details, retrieval/QA metrics, statistical analysis, latency/resource methods, and final test execution, consistent with Phase 1/2.
- Public redistribution of full texts, subject to license and institutional policy; only manifests/hashes/access instructions may be releasable for restricted documents.

## 34. Phase 3 acceptance criteria

Phase 3 is complete only when an independent researcher can determine:

1. what counts as a solar-PV scientific paper and what does not;
2. which document types, publication dates, and languages are eligible;
3. which sources are searched, for what role, with which exact queries and dates;
4. what full text is required and how lawful access failures are handled;
5. how screening decisions, primary exclusion reasons, and disagreements are recorded;
6. how duplicates, preprints, publisher versions, corrections, retractions, and extensions are resolved;
7. what metadata and provenance are preserved;
8. how extraction, OCR, tables/equations/captions, references, and QC are handled;
9. how corpus size and topic representation are justified without question-driven selection;
10. how the corpus is hashed, versioned, frozen, and changed without overwriting;
11. how corpus-level biases and residual limitations are measured and reported;
12. which items remain open, what evidence resolves them, and when they must be frozen.

No formal discovery search or large-scale collection begins until all pre-search OPEN decisions in Section 32 are approved and the protocol version is frozen. Remaining implementation-specific decisions must be resolved before their corresponding processing stage.

## 35. Phase 4 handoff

Phase 4 receives:

- the approved and immutable corpus version and manifest, or—if corpus collection has not yet been authorized—the approved protocol and the explicitly open decisions that block corpus freeze;
- stable `document_id` and `version_id` values;
- source provenance, full-text source/version, file/text hashes, and access restrictions;
- screening decisions, inclusion/exclusion records, and status metadata;
- extraction/QC report, topic/year/document-type coverage, and known limitations;
- source-to-text locators sufficient to map passages to document/version/page/section/offset;
- the exact protocol, search-query registry, and decision log.

Phase 4 is responsible for designing the benchmark/question set and evidence annotations against that fixed corpus, including factual, comparative, causal/explanatory, methodological, quantitative, multi-document, and potentially unanswerable question support as appropriate. Phase 4 must not modify the frozen research question or silently add/remove corpus documents; a corpus change requires a new version and documented amendment.

### Phase 3 → Phase 4 Handoff

**Carry forward the corpus protocol, frozen corpus version or corpus-freeze blockers, immutable manifest, stable IDs and source locators, screening/version/status records, extraction and QC reports, topic-coverage/bias profile, query registry, and all approved decision-log entries. Phase 4 designs questions and evidence annotations only against that documented corpus; benchmark construction must not be used to bias corpus inclusion.**
