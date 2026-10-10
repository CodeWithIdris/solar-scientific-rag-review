# Methodological Screening Protocol

Project title, unchanged for this audit stage:

Evaluating Retrieval Strategies for Evidence-Grounded Question Answering over Solar Energy Scientific Literature

## Purpose

This protocol defines a reproducible literature screening system for auditing papers that may inform a study of lexical, dense, and hybrid retrieval strategies for evidence-grounded question answering over solar photovoltaic scientific literature.

This is a literature audit protocol, not a finalized research design. The screening process must not claim novelty, decide the final research gap, invent information not present in papers, or classify papers as relevant based only on keyword matches.

## Source Library

Primary BibTeX library:

`literature/bib/Solar Scientific RAG.bib`

PDF storage location:

`literature/pdfs/`

Screening records:

`screening/screening_matrix.csv`

## Controlled Values

Use controlled values wherever possible. If a controlled value is insufficient, add a short free-text note and preserve the underlying evidence location.

### Boolean / Unknown Fields

Use:

- `Yes`
- `No`
- `Unclear`
- `Not assessed`

### Overlap Level

Use exactly one:

- `None`
- `Low`
- `Moderate`
- `High`
- `Critical`

### Relevance Decision

Use exactly one:

- `Include-Core`
- `Include-Context`
- `Potentially-Relevant`
- `Exclude`

### Confidence

Use exactly one:

- `High`
- `Medium`
- `Low`

### Recommended Retrieval Type Values

Use one or more if explicitly supported:

- `Lexical`
- `Dense`
- `Hybrid`
- `Reranking`
- `Other`
- `None`
- `Unclear`

### Recommended Domain Values

Use one or more if explicitly supported:

- `Solar PV`
- `Solar energy`
- `Energy`
- `Scientific literature`
- `Biomedical literature`
- `Legal`
- `General domain`
- `Other`
- `Unclear`

## 1. Inclusion Criteria

A paper may be included when full-text evidence supports one or more of the following:

1. It studies retrieval-augmented generation, retrieval-based question answering, evidence-grounded question answering, citation-supported generation, or closely related systems.
2. It evaluates retrieval methods relevant to RAG or evidence-based QA, including lexical, dense, hybrid, fusion, reranking, chunking, passage retrieval, or document retrieval.
3. It evaluates evidence grounding, citation accuracy, source attribution, answer faithfulness, retrieval quality, or related methodological outcomes.
4. It uses or evaluates scientific literature corpora, especially peer-reviewed articles, abstracts, full texts, proceedings papers, technical papers, or domain-specific scholarly datasets.
5. It concerns solar photovoltaic or solar energy scientific literature, methods, terminology, or domain-specific evidence needs.
6. It provides transferable methodology for building, evaluating, or auditing RAG systems over scientific literature even if it is outside the solar PV domain.

## 2. Exclusion Criteria

Exclude a paper when full-text evidence establishes that it is outside the methodological scope. Common exclusion reasons include:

1. No retrieval component relevant to QA, RAG, evidence attribution, citation, or literature search.
2. No question answering, answer generation, evidence-grounded generation, or citation-supported response task.
3. No evaluation of retrieval, grounding, citation accuracy, evidence attribution, or answer faithfulness.
4. Purely application-domain solar PV paper with no relevant retrieval, QA, RAG, or evidence-grounding methodology.
5. Purely engineering, materials science, or photovoltaic performance study with no information retrieval or QA component.
6. General AI or NLP paper that does not evaluate retrieval or evidence-grounded QA.
7. Tutorial, opinion, editorial, news article, blog post, or non-scholarly item unless retained only as background context.
8. Duplicate bibliographic record or unavailable full text after reasonable effort.

Do not exclude solely because a paper is outside solar PV. Non-solar papers may be important context if they provide directly relevant RAG, retrieval, citation, grounding, or scientific-literature QA methodology.

## 3. Determining Relevance

Relevance must be determined from explicit evidence in the paper, preferably from the methods, experiments, datasets, evaluation, and results sections.

Use the following decision rules:

- `Include-Core`: The paper directly evaluates RAG, retrieval-based QA, evidence-grounded QA, citation-supported QA, or retrieval strategies over scientific literature, and includes methods or metrics substantially relevant to the proposed study.
- `Include-Context`: The paper does not directly overlap with the full proposed study but provides important background, transferable evaluation methods, retrieval methods, RAG architecture patterns, citation evaluation, solar PV domain context, or scientific-literature corpus context.
- `Potentially-Relevant`: The record appears plausibly relevant, but full-text evidence is incomplete, ambiguous, unavailable, or not yet reviewed. This category should trigger full-text verification.
- `Exclude`: Full-text evidence shows the paper does not meet inclusion criteria, or the paper is a duplicate or inaccessible after reasonable effort.

Keyword presence is not enough. Terms such as `solar`, `RAG`, `AI`, `question answering`, `retrieval`, `citation`, or `scientific literature` must be tied to the paper's actual methods, corpus, task, and evaluation before relevance is assigned.

## 4. Determining Methodological Overlap

Methodological overlap should reflect how closely a paper's actual design matches the proposed study's methodological focus:

- Evidence-grounded or citation-aware QA
- RAG or retrieval-augmented generation
- Lexical, dense, hybrid, fusion, or reranked retrieval comparison
- Scientific literature as the corpus
- Solar energy or solar PV as the domain
- Explicit evaluation of retrieval, grounding, citations, evidence attribution, answer faithfulness, abstention, latency, cost, or statistical significance

Assign overlap as follows:

- `None`: No meaningful methodological relationship after review.
- `Low`: Shares a broad topic, domain, or background concept, but not the core retrieval/QA/evidence-grounding methodology.
- `Moderate`: Shares one or two important components, such as scientific-literature RAG or retrieval evaluation, but lacks other central components.
- `High`: Shares several central components, such as RAG over scientific literature with retrieval evaluation and grounding or citation metrics.
- `Critical`: Very close methodological match, such as explicit comparison of lexical, dense, and hybrid retrieval for evidence-grounded or citation-aware QA over solar PV or closely comparable scientific literature.

Required rule:

A paper cannot be classified as methodologically overlapping based only on its title, abstract, or search snippet when the relevant methodology is not explicitly established. Such papers should be marked for full-text verification.

## 5. Handling Uncertainty

Use uncertainty deliberately and visibly.

1. Use `Unclear` when the paper is available but does not explicitly state the needed detail.
2. Use `Not assessed` when the field has not yet been checked.
3. Use `Potentially-Relevant` when a paper may fit but full-text evidence is missing or incomplete.
4. Use `Low` confidence when evidence is based only on title, abstract, metadata, or partial text.
5. Use `Medium` confidence when the relevant section was reviewed but ambiguity remains.
6. Use `High` confidence only when the relevant claim is supported by a specific full-text location.
7. Record what evidence is missing in `limitations`, `methodological_weaknesses`, or `exclusion_reason` as appropriate.

Do not resolve uncertainty by guessing. If a paper does not explicitly report corpus size, top-k, embedding model, reranker, statistical testing, or citation metrics, record `Unclear` or `Not reported`, not an inferred value.

## 6. Rules Against Unsupported Inference

Screeners must not:

1. Infer use of RAG from general discussion of LLMs.
2. Infer dense retrieval from use of embeddings unless retrieval use is explicit.
3. Infer hybrid retrieval from mention of multiple models unless fusion or combined retrieval is explicit.
4. Infer scientific-literature corpus use from a scientific topic alone.
5. Infer solar PV specificity from general renewable-energy or climate language.
6. Infer citation evaluation from the presence of references or generated citations unless citation correctness is evaluated.
7. Infer evidence grounding from retrieval alone unless the answer is evaluated against retrieved evidence or sources.
8. Treat title, abstract, or search-snippet claims as sufficient for final overlap classification when methods are not explicit.
9. Fill missing metric values from common practice in the field.
10. Claim that a paper identifies the same research gap unless the authors explicitly state that gap.

Every substantive methodological entry should be traceable to the paper.

## 7. Recording Evidence Locations in PDFs

Use the `evidence_location` field to record where the classification evidence was found. Prefer precise page and section references.

Recommended format:

`PDF: filename.pdf; pp. X-Y; section: Section Name; evidence: short paraphrase`

Examples:

- `PDF: smith_2024_rag.pdf; p. 4; section: Methods; evidence: compares BM25, dense retrieval, and reciprocal-rank fusion`
- `PDF: lee_2023_qa.pdf; pp. 7-8; section: Evaluation; evidence: reports citation precision and answer faithfulness`
- `PDF unavailable; abstract only; requires full-text verification`

Evidence notes should be short paraphrases, not long copied passages. If a direct quotation is necessary, keep it brief and include the page number.

## Screening Workflow

1. Import records from `literature/bib/Solar Scientific RAG.bib`.
2. Create one row per bibliographic record in `screening/screening_matrix.csv`.
3. Do not classify final relevance until relevant full-text sections have been checked.
4. Use `Potentially-Relevant` and `Low` confidence for records needing full-text verification.
5. Add excluded records to `screening/exclusions.csv` with a specific exclusion reason and evidence location.
6. Add papers with `High` or `Critical` methodological overlap to `screening/critical_papers.csv` after full-text verification.
7. Preserve uncertainty and missing information explicitly.

## Audit Integrity

This screening system is designed to support a rigorous methodological literature audit. It should enable later review of why each paper was included, excluded, or flagged as critical without relying on memory, title-level impressions, or unsupported inference.
