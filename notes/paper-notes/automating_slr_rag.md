# Automating Systematic Literature Reviews with Retrieval-Augmented Generation

## Screening disposition

- **Full text:** Obtained from the [MDPI-hosted article asset PDF](https://mdpi-res.com/d_attachment/applsci/applsci-14-09103/article_deploy/applsci-14-09103.pdf) for *Applied Sciences* 14(19), article 9103; 17 pages.
- **overlap_level:** Low
- **relevance_decision:** Include-Context
- **confidence:** High
- **Decision basis:** This is a review and proposed framework. It discusses retrieval methods and prior systems, but does not implement or experimentally compare retrievers or evaluate downstream QA.

## Forensic method audit

| Item | Finding | Evidence locator |
|---|---|---|
| A. Scientific-literature corpus? | Scientific/RAG literature is the review topic. No experimental source corpus is defined; the review's search and selection protocol and screened-record count are not reported. | Scope, pp. 1–2; review body §§2–4, pp. 3–10 |
| B. Solar/PV corpus? | Not reported; no solar/PV-specific experimental corpus is described. | Article scope and proposed framework, pp. 1–15 |
| C. BM25 retrieval? | BM25 is described as an example of a sparse retriever, not used in an author-run system. | §2.1.1, pp. 3–4 |
| D. Dense retrieval? | Dense retrievers are discussed as a method category. Stage 2 of the proposed framework suggests a dense or parse retriever to re-rank screened articles; this is a proposal, not an experiment. | §2.1.1, pp. 3–4; §5, Stage 2, p. 13 |
| E. Hybrid retrieval? | No hybrid system is implemented/evaluated by this paper. Prior-art combination of BM25 and DPR followed by reranking is described as the Re2G method. | §2.1.4, p. 5 |
| F–H. BM25-only, dense-only, hybrid arms? | No author-run retrieval arms of these types. | No experimental methods/results; framework is proposed in §5, pp. 11–14 |
| I–N. Same corpus, questions, preprocessing, generator, prompt, retrieval as sole variable? | Not applicable to a controlled experiment in this paper; no such experiment is reported. | Article structure and §5, pp. 11–14 |
| O. Retrieval metrics? | Not reported for an author-run experiment. | No author-run evaluation; §5, pp. 11–14 describes work needed for future implementation/evaluation |
| P. Downstream answer-quality metrics? | Not reported for an author-run experiment. | No author-run evaluation |
| Q. Faithfulness? | Not evaluated by this paper. | No author-run evaluation |
| R–T. Citation precision, citation recall/completeness, evidence attribution? | Not evaluated by this paper. Citation-related prior work is discussed, but no author-run citation/evidence scoring is reported. | Prior-work discussion §3, pp. 8–10; proposed synthesis framework §5, pp. 13–14 |
| U. Unanswerability/abstention? | Not reported as an author-run evaluation. | No author-run evaluation |
| V. Statistical comparison? | Not reported; the paper proposes a framework and future studies rather than reporting a controlled experiment. | §5 Future Work, p. 14; §6, pp. 14–15 |

The review describes retrieval granularity as document-, chunk-/passage-, and token-level in its background discussion (§2.1.3, pp. 4–5). The proposed SLR workflow has four stages—literature search, screening, data extraction, and information synthesis (§5, pp. 11–14). Neither description constitutes a tested retrieval pipeline.

## Comparison with the proposed study

- **Retrieval-only comparison:** None by this paper. BM25, dense methods, and a BM25+DPR reranking example are methodological background.
- **System-level RAG comparison:** None by this paper. Systems mentioned in the review are prior work, not experimental conditions in this article.
- **Downstream QA comparison:** None by this paper. The proposed framework describes SLR automation and synthesis; no benchmark is run.
- **Evidence/citation evaluation:** No author-run evidence or citation metric.
- **Exact proposed controlled three-arm design:** Not performed or established.

The article offers contextual discussion of RAG components and a proposed SLR workflow. It does not materially challenge the proposed controlled comparison of BM25, dense, and hybrid retrieval for evidence-grounded QA over a common solar-PV literature corpus.
