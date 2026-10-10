# HySemRAG: A Hybrid Semantic Retrieval-Augmented Generation Framework

## Focused screening result

Registered arXiv full text inspected. HySemRAG performs scientific-literature synthesis and methodological gap analysis in geospatial epidemiology.

- **Corpus:** scientific articles collected through metadata/full-text processing. The paper describes approximately 500–1,300 retrievable full-text documents per ETL run from about 3,400 metadata candidates; this is a variable ingestion result, not a fixed controlled benchmark corpus.
- **Domain:** geospatial epidemiology; not solar/PV.
- **Retrieval:** semantic search, keyword filtering, and knowledge-graph traversal are combined in a hybrid system. BM25 specifically, exact sparse/dense fusion formula, retriever arms, passage granularity, and top-k are not established.
- **Question/task:** automated literature synthesis and methodological gap analysis. A matched scientific QA benchmark with BM25-only, dense-only, and hybrid conditions is not reported.
- **Evaluation:** extraction/system-session evaluation and citation accuracy/verification are discussed. Retrieval metrics by lexical/dense/hybrid arms and formal generated-citation precision/completeness are not established.
- **Generation and controls:** an LLM-based workflow is described; same-generator comparisons across retrieval strategies are not reported.
- Unanswerable questions, abstention, latency/cost, and inferential comparison of retrieval arms are not reported.

## Relevance to proposed study

- **overlap_level:** Moderate
- **relevance_decision:** Include-Core
- **confidence:** Medium

The work is a meaningful scientific-literature RAG/synthesis and citation-verification comparator, but does not establish the controlled retriever-to-QA comparison or solar/PV domain.

## Evidence locations

arXiv:2508.05666 full text: abstract; ETL/corpus and system/retrieval descriptions; evaluation and citation-verification sections. Corpus counts are per ETL run as described in the text.
