# Multi-level retrieval with representation alignment enhances cross-document evidence synthesis for scientific knowledge generation

## Targeted full-text retrieval outcome

**Full text unavailable after final targeted retrieval attempt.**

This final pass was limited to the exact registered article; no unrelated papers were searched or added. The attempted routes were: ScienceDirect full-text page and article endpoint (blocked/error; no full text); DOI resolution (redirected to Elsevier landing page, not full text); Elsevier article API (metadata only, marked non-open-access); OpenAlex (closed access, no repository full text); Semantic Scholar (no open-access PDF); Crossref (bibliographic metadata only); Google Scholar exact-title query (two versions, ScienceDirect and an ACM abstract/metadata record); exact-title web search and author-name plus exact-title search (no legitimate full-text copy found); institutional-repository query for the exact title at Communication University of China (no matching manuscript surfaced); and the ACM-linked record (HTTP 403). No legitimate open-access copy linked from these scholarly records was located.

Bibliographic identifiers: ScienceDirect PII `S1568494626000979`; DOI `10.1016/j.asoc.2026.114649`; *Applied Soft Computing* 191 (2026), article 114649.

## What the accessible publisher abstract establishes

The abstract describes:

- a scientific-literature cross-document QA/evidence-synthesis task;
- a multi-level retrieval system (document filtering and element ranking);
- contrastive-learning embeddings and evidence elements including text, tables, formulas, and figures;
- SciLitQA, described as containing more than 50,000 QA pairs;
- experiments against existing RAG models and public benchmarks, with retrieval accuracy and knowledge-synthesis quality discussed.

These are abstract-level statements only. The full-text source-paper count, domain coverage, exact retrieval models, baseline configuration, generator, prompts, preprocessing, metrics, and statistical methods cannot be verified from accessible evidence. The abstract does not establish whether BM25-only, dense-only, or hybrid downstream-QA arms exist.

## Requested methods check (A–V)

| Item | Finding from accessible evidence |
|---|---|
| A. Scientific-literature corpus? | Yes at the task/benchmark level: the publisher abstract describes scientific-literature QA. Exact source corpus and document count are not established. |
| B. Solar/PV domain? | Not reported in the accessible abstract. |
| C. BM25? | Not reported. |
| D. Dense retrieval? | Contrastive-learning embeddings are described as part of multi-level retrieval; exact model and any dense-only experimental arm are not established. |
| E. Hybrid retrieval? | Not reported. |
| F. BM25-only arm? | Not established. |
| G. Dense-only arm? | Not established. |
| H. Hybrid arm? | Not established. |
| I. Same corpus across arms? | Not established. |
| J. Same question benchmark across arms? | Abstract mentions SciLitQA and public benchmarks, but same benchmark conditions across retrieval arms are not established. |
| K. Same preprocessing? | Not established. |
| L. Same generator? | Not established. |
| M. Same prompt? | Not established. |
| N. Retrieval as sole changed variable? | Not established. |
| O. Retrieval metrics? | The abstract mentions retrieval accuracy; exact metrics and per-condition scores are not available. |
| P. Downstream answer-quality metrics? | The abstract claims improved knowledge-synthesis performance against existing RAG models; metric definitions and conditions are not available. |
| Q. Faithfulness? | Not reported in accessible abstract. |
| R. Citation precision? | Not reported in accessible abstract. |
| S. Citation recall/completeness? | Not reported in accessible abstract. |
| T. Evidence attribution? | Multi-element evidence synthesis is described; a formal attribution metric is not reported in accessible abstract. |
| U. Unanswerable/abstention evaluation? | Not reported in accessible abstract. |
| V. Statistical comparison? | Not reported in accessible abstract. |

## Type of overlap and screening decision

- **Retrieval-only comparison:** Not established from the accessible abstract.
- **System-level RAG comparison:** Yes, the abstract describes an MC-RAG system and comparisons with existing RAG models; detailed conditions unavailable.
- **Downstream QA comparison:** The abstract describes cross-document scientific QA and knowledge-synthesis experiments; matched BM25/dense/hybrid QA arms are not established.
- **Evidence/citation evaluation:** Multi-element evidence is part of the stated task; citation precision/completeness and evidence-attribution evaluation are not established.
- **Exact proposed controlled experiment:** Not established. Shared solar-PV corpus, question benchmark, preprocessing, generator, prompt, and retrieval-only treatment contrast cannot be verified.

- **overlap_level:** High potential topical/system overlap; exact design unresolved
- **relevance_decision:** Include-Core
- **confidence:** Medium for the abstract-level task/system facts; Low for the unresolved experimental-control details

## Final RQ-freeze relevance

The abstract establishes a neighboring scientific-literature cross-document QA/RAG task, a large benchmark, and retrieval experiments. It does **not** report the exact lexical, dense, and hybrid arms; common experimental controls; a solar/PV corpus; or joint per-arm retrieval and evidence-grounding outcomes. Therefore, the abstract alone is not sufficient evidence to change the proposed RQ or to claim that the controlled three-arm design has already been performed. The record remains an unresolved-but-bounded literature-access limitation; do not infer the missing experimental methodology.
