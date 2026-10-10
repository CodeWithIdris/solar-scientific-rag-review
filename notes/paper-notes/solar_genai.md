# Solar GenAI

## Focused screening result

Full nine-page IJIC PDF inspected. The paper demonstrates a solar-PV RAG application, not a controlled retrieval-strategy study.

- **Corpus/domain:** Malaysian solar-PV policy, technical and institutional material plus selected research publications. It is mixed grey literature and science, not a corpus consisting only of peer-reviewed papers. Exact document count is not clearly reported.
- **Processing/retrieval:** approximately 1,000-character overlapping chunks; 384-dimensional all-MiniLM-L6-v2 embeddings in a persistent vector database with cosine retrieval. BM25, a hybrid retriever, fusion, reranking, and retrieval top-k are not reported.
- **Questions:** representative solar-PV queries; results describe 9 manually labelled hallucinated and 21 non-hallucinated responses (30 response instances). The query-set construction/provenance and expert validation are not reported.
- **Comparison:** LLM-only versus RAG. There are no BM25-only, dense-only, and hybrid RAG arms, and retrieval strategy is not the experimental variable.
- **Generation:** Mistral-7B-Instruct via Ollama, deployed locally with 4-bit quantization. LLM-only versus RAG is evaluated; the generator is not compared across BM25/dense/hybrid retrieval arms because no such arms exist.
- **Evaluation:** answer correctness/hallucination and latency are discussed. Retrieval metrics, faithfulness score, citation precision/completeness, and formal evidence attribution are not reported. Prompt guidance requests abstention for insufficient information, but systematic unanswerable/abstention evaluation is not reported.
- **Statistics:** the paired t-test concerns caching latency, not retrieval strategies or QA/evidence differences.

## Relevance to proposed study

Solar GenAI is direct domain/application context. It does not establish the controlled retrieval-to-answer/evidence design. Treat its demonstration and its evaluation protocol separately.

- **overlap_level:** High
- **relevance_decision:** Include-Core
- **confidence:** High

## Evidence locations

IJIC full PDF (9 pages): abstract/model p. 1; corpus/chunk processing and embeddings pp. 2–3; offline deployment pp. 3–4; evaluation/results and response counts pp. 4–6; limitations/conclusion p. 9.
