# RILS — RAG-Based Intelligent Literature System for Renewable Energy Assessment

## Screening scope and source

Focused full-text screen of the registered 14-page ResearchSquare PDF. The assessment below is limited to the evidence in that PDF. RILS is a preprint and the document contains internal corpus-size discrepancies; the counts are retained as printed rather than reconciled.

## Corpus and task

- **Corpus:** renewable-energy documents from IRENA, IEA, peer-reviewed journals, and technology roadmaps. The corpus includes six technology families, not just solar PV. Table 1 labels the source set as authoritative institutional or peer-reviewed publications.
- **Solar-PV coverage:** Table 1 lists 4,200 Solar-PV documents and 6,800 passages for 2018–2024. This is a subset within a mixed renewable-energy corpus, not a solar-only corpus.
- **Corpus-count discrepancy:** Table 1 (p. 6) reports 18,000 documents and 28,800 passages. Section 6.2 (p. 6) refers to 21,000 documents; §7.2 (p. 7) and Table 3 (p. 9) report 32,800 passages. These values conflict and are not silently harmonized.
- **Queries:** 900 technology-assessment queries, 150 per technology family, and five query types (180 per type). Domain experts from IRENA and IEA compiled ground-truth responses. Solar PV contributes 150 queries.
- **Task:** structured renewable-technology assessment, including cost, temporal, geographic, and technology-readiness information. It is not established as a benchmark of scientific-literature QA in the same sense as question answering over research papers.
- **Question provenance/validation:** expert-grounded according to §7.1. The paper does not report a peer-review-style question creation protocol or solar-PV expert panel breakdown.
- **Unanswerable cases:** not reported.

## Retrieval architecture and conditions

- Section 6.2 (p. 6) describes a 768-dimensional renewable-energy domain-fine-tuned sentence transformer and FAISS-HNSW indices, partitioned by technology family, plus a master cross-technology index. The exact embedding-model name is not reported.
- Section 6.4 (p. 7) describes primary semantic retrieval followed by metadata-filtered refinement. It also explicitly describes hybrid sparse-dense retrieval combining BM25 keyword matching and dense similarity, with final ranking by a weighted combination; the weights are not reported.
- Reported baseline/system conditions in §7.2 and Table 2 (p. 8): parametric LLM, BM25+Generation, standard RAG without technology-aware partitioning, and RILS. The methods identify dense semantic retrieval for standard retrieval and BM25+dense hybrid retrieval for RILS.
- This is a **system-level** comparison. RILS also changes technology partitioning, query-intent routing, metadata facets, structured generation, and citation verification. The report does not establish that retrieval alone is the experimental variable.
- Table 2 compares the systems on assessment outcomes. It is not a clean BM25-only/dense-only/hybrid retriever ablation with all non-retrieval factors fixed.
- Same benchmark across the system comparisons is described in §7.1–7.2. A shared corpus/index definition for every baseline is not fully specified.
- A 7B-parameter instruction-tuned decoder and structured templates are specified for RILS (§6.5, p. 7). The same generator and prompt across BM25+Generation, standard RAG, and RILS are **not established**.

## Evaluation

- **Retrieval metrics:** Recall@5, Precision@5, MRR, and nDCG@5 are reported by technology family (§8.1, p. 8). Solar-PV Recall@5 is 89%, MRR 0.86, and nDCG@5 0.91. The paper does not establish these as per-arm retrieval results for BM25-only, dense-only, and hybrid.
- **Downstream/system metrics:** Table 2 (§8.2, p. 8) reports accuracy, hallucination, quantitative accuracy, and TRL consistency. The RILS row reports 85% accuracy, 12% hallucination, 79% quantitative accuracy, and 88% TRL consistency.
- **Evidence/citations:** §6.5 (p. 7) describes a post-generation NLI entailment verifier that checks factual claims against retrieved passages and flags unverified claims. Benchmark answers are annotated for citation accuracy (§7.1, p. 7), but separate per-system citation precision, completeness/recall, or generated-citation attribution scores are not reported.
- **Abstention:** not reported.
- **Latency/resources:** §9 and Table 3 (p. 9) report 28 ms average retrieval latency, 2.1 s end-to-end latency, 3.1 GB index memory, hardware, throughput, GPU memory, and training time.
- **Statistical comparison:** no inferential test, confidence interval, or effect-size estimate for the system/retrieval comparisons is reported.

## Comparison with proposed study

### Exact overlap

- A renewable-energy assessment benchmark includes 150 Solar-PV queries.
- BM25+Generation, standard dense RAG, and a BM25+dense hybrid system are reported as evaluation conditions.
- Retrieval and downstream answer/system metrics are both present in the paper.
- Retrieved passages are checked against generated claims with an NLI verifier.

### Important differences

- The corpus is mixed across renewable technologies and document types; it is not a solar-PV-only scientific-paper corpus.
- The conditions are system-level and bundle retrieval with partitioning, routing, metadata filters, generation templates, and verification.
- The report does not establish identical generator/prompt/corpus controls across conditions or the retrieval strategy as the sole independent variable.
- Retrieval metrics are not reported separately for BM25-only, dense-only, and hybrid arms.
- Citation accuracy is part of benchmark annotation, but per-arm citation precision/completeness and evidence-attribution scores are not reported.
- The paper's internal corpus counts conflict.

## Overlap assessment

- **overlap_level:** High
- **relevance_decision:** Include-Core
- **confidence:** High for the methods/results as printed; this is confidence in the report's statements, not independent replication.

RILS materially constrains a broad energy-RAG framing. It does not establish the exact controlled retrieval-only downstream scientific-QA/evidence-attribution design proposed here.

## Evidence locations

ResearchSquare PDF (14 pages): Table 1 p. 6; §§6.2–6.5 pp. 6–7; §§7.1–7.2 p. 7; Fig. 2/§8.1 p. 8; Table 2/§8.2 p. 8; Table 3/§9 p. 9.
