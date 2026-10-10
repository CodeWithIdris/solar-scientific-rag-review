# Solar Intelligence — Methodological Screening

Screened paper: Jyotsna Singh, "Solar Intelligence," arXiv:2609.13648v1, submitted 12 September 2026.

Screening question: Does the paper perform the proposed experiment: BM25 vs dense retrieval vs hybrid retrieval over the same solar scientific corpus, same question set, same generator, with controlled experimental comparison, retrieval metrics, answer quality, evidence/citation attribution, and statistical comparison?

Overall determination: **PARTIAL overlap**. The paper uses a solar-domain scientific/report corpus and implements BM25, dense retrieval, and hybrid RRF retrieval in one RAG system. However, it does **not** report a controlled BM25-only vs dense-only vs hybrid comparison over the same questions, generator, and corpus.

## 1. Research objective

Classification: **RELATED**

The paper's objective is to build an integrated solar decision-support platform combining structured solar analytics, evidence-grounded scientific question answering, and forecasting. It is related to the proposed study because it includes solar scientific QA and hybrid retrieval, but its primary objective is system integration rather than controlled retrieval-strategy evaluation.

## 2. Corpus

- source: **PARTIAL** — arXiv API, NREL, IEA-PVPS, IRENA, Sandia, NASA POWER, and Biosphere 2 are reported.
- domain: **EXACT** — solar energy and PV are central.
- number of documents: **PARTIAL** — 149 research papers/reports are reported, plus structured datasets.
- document type: **PARTIAL** — research papers and institutional reports are reported; a project document also appears in examples.
- date range: **PARTIAL** — research papers/reports are described as 1994-2026 in text, while Table 1 appears to show 1994-2006; this inconsistency should be preserved.
- preprocessing: **PARTIAL** — PyMuPDF extraction and approximately 500-token chunks with 50-token overlap are reported.

Corpus overlap assessment: **PARTIAL**. It uses a solar scientific/report corpus, but not necessarily the same corpus as the proposed study. The proposed study's corpus is not yet finalized, and this paper includes institutional reports and project documents, not only solar-PV scientific literature.

## 3. Question benchmark

- number: **NOT REPORTED** — no fixed benchmark question count is reported for the RAG QA evaluation.
- source: **PARTIAL** — example user/system queries are shown; no reusable benchmark source is specified.
- construction: **NOT REPORTED** — no systematic construction protocol for a question set is reported.
- question types: **PARTIAL** — semantic, structured, and hybrid query types are described.
- validation: **PARTIAL** — examples are discussed qualitatively; no formal expert validation or benchmark validation is reported.

Question benchmark overlap assessment: **ABSENT** for the proposed controlled experiment. The paper does not establish a same-question-set comparison across retrieval strategies.

## 4. Retrieval architecture

### BM25

Classification: **EXACT** for use of BM25; **ABSENT** for BM25-only experimental arm.

BM25 is implemented as a sparse retrieval index. The paper reports lowercase tokenization and no stemming to preserve domain-specific solar terms.

### Dense retrieval

Classification: **EXACT** for use of dense retrieval; **ABSENT** for dense-only experimental arm.

Dense retrieval is implemented using BGE-small embeddings, reported as 384-dimensional. The abstract also refers to ChromaDB dense embeddings.

### Hybrid retrieval

Classification: **EXACT** for hybrid retrieval use.

The RAG layer dispatches queries to BM25 and dense retrieval in parallel and combines results with reciprocal rank fusion.

### Fusion

Classification: **EXACT**

The paper reports Reciprocal Rank Fusion as the fusion mechanism for BM25 and dense outputs.

### Reranking

Classification: **ABSENT**

No cross-encoder, LLM reranker, or other reranking component is reported.

### Retrieval granularity

Classification: **PARTIAL**

Documents are chunked into approximately 500-token chunks with 50-token overlap. Retrieval appears to operate over chunks, but the paper does not report a granularity comparison.

### Top-k

Classification: **PARTIAL**

Each index returns top-20 candidates before fusion. The number of final contexts passed to the generator is not fully specified as a benchmark variable.

## 5. Generation

Classification: **PARTIAL**

The generator is llama3.2:3b served via Ollama. The paper reports prompt rules requiring citations and no invented numerical values. Structured numeric answers bypass the LLM and are generated deterministically from SQL output. This is related to the proposed common-generator design, but no controlled retrieval comparison using the same generator across BM25-only, dense-only, and hybrid arms is reported.

## 6. Evaluation

### Retrieval

Classification: **ABSENT**

No retrieval benchmark metrics such as Recall@k, Precision@k, MRR, nDCG, MAP, or evidence recall are reported for BM25-only, dense-only, or hybrid retrieval.

### Answer quality

Classification: **PARTIAL**

The paper discusses example outputs and identifies qualitative issues, including omission of relevant evidence and overemphasis of a theoretical claim. It does not report systematic answer accuracy, correctness, relevance, or expert/LLM-judge scoring over a benchmark.

### Faithfulness

Classification: **PARTIAL**

The system is designed to ground answers in retrieved evidence and to reduce unsupported responses. However, no formal faithfulness metric is reported.

### Citation/evidence

Classification: **PARTIAL**

The paper displays cited evidence in example outputs. It does not report citation precision, citation recall/completeness, source attribution accuracy, or evidence attribution F1.

### Efficiency

Classification: **RELATED**

The paper describes deployment architecture and local model choices. It does not report controlled retrieval/generation latency, throughput, or cost comparisons for BM25 vs dense vs hybrid.

### Statistical analysis

Classification: **ABSENT**

No statistical tests or confidence intervals are reported for RAG retrieval or QA comparisons.

## 7. Experimental comparisons

Explicit retrieval comparisons performed:

1. **BM25-only vs dense-only**: **ABSENT**.
2. **BM25-only vs hybrid**: **ABSENT**.
3. **Dense-only vs hybrid**: **ABSENT**.
4. **BM25-only vs dense-only vs hybrid over same corpus/question set/generator**: **ABSENT**.
5. **Hybrid retrieval vs no retrieval**: **ABSENT** for a formal experimental comparison.
6. **Structured SQL path vs semantic retrieval path**: **RELATED**, but this is query routing, not retrieval-strategy comparison.
7. **NASA POWER vs Biosphere 2 sensor comparison**: **RELATED**, but this evaluates solar data sources, not document retrieval.
8. **Forecast output inspection**: **RELATED**, but not part of RAG retrieval evaluation.

The paper implements BM25, dense, and hybrid retrieval components, but does not experimentally compare them.

## 8. Main results

Classification: **RELATED**

The paper's relevant RAG results are qualitative examples of semantic and structured query behavior. The semantic example is used to show correct routing, cross-document retrieval, and grounded generation, while also exposing limitations. The paper does not provide quantitative RAG retrieval or answer-quality results.

## 9. Limitations

Reported limitations relevant to this screening:

- Hardcoded Biosphere 2 location.
- NASA POWER data lag.
- Point forecasts rather than uncertainty forecasts.
- No forecast evaluation.
- Need to enlarge the corpus for better QA.
- The semantic QA example shows omitted operationally relevant evidence.
- The semantic QA example foregrounds a theoretical efficiency claim without sufficiently distinguishing it from current commercial efficiency.

Additional methodological limitations for the proposed study:

- No BM25-only retrieval arm.
- No dense-only retrieval arm.
- No controlled hybrid-vs-baseline comparison.
- No question benchmark.
- No retrieval metrics.
- No formal answer-quality metrics.
- No formal citation/evidence attribution metrics.
- No statistical comparison.

## 10. Exact overlap with proposed study

| Proposed component | Classification | Determination |
|---|---|---|
| Solar scientific corpus | PARTIAL | Solar papers/reports are used, but not necessarily the same corpus and not only solar-PV scientific literature. |
| BM25 retrieval | EXACT | BM25 index is implemented. |
| Dense retrieval | EXACT | BGE-small dense retrieval is implemented. |
| Hybrid retrieval | EXACT | BM25 and dense outputs are fused with RRF. |
| Same solar scientific corpus across retrieval arms | NOT REPORTED | Since separate BM25-only/dense-only/hybrid experimental arms are not reported, this cannot be established. |
| Same question set across retrieval arms | ABSENT | No benchmark question set or retrieval-arm comparison is reported. |
| Same generator across retrieval arms | ABSENT | llama3.2:3b is used, but not in a controlled retrieval-arm comparison. |
| Controlled experimental comparison | ABSENT | No controlled BM25 vs dense vs hybrid experiment is reported. |
| Retrieval metrics | ABSENT | No retrieval metrics for document retrieval are reported. |
| Answer quality metrics | PARTIAL | Qualitative answer discussion only; no systematic metric. |
| Evidence/citation attribution metrics | PARTIAL | Citations/evidence are shown, but attribution accuracy is not evaluated. |
| Statistical comparison | ABSENT | No statistical testing for RAG QA/retrieval is reported. |

Final overlap classification: **PARTIAL**, not **EXACT**. Solar Intelligence is the closest screened solar-domain RAG system, but it does not substantially perform the proposed controlled retrieval-strategy experiment.

## 11. Components not addressed

The paper does not address:

- BM25-only retrieval evaluation.
- Dense-only retrieval evaluation.
- Direct BM25 vs dense comparison.
- Direct BM25 vs hybrid comparison.
- Direct dense vs hybrid comparison.
- All-three retrieval comparison under a common corpus/question/generator setup.
- A reusable scientific QA benchmark with reported question count.
- Formal retrieval metrics.
- Formal answer correctness/relevance/faithfulness metrics.
- Citation precision.
- Citation recall or citation completeness.
- Evidence attribution F1 or comparable metric.
- Abstention or unanswerable-question evaluation.
- Question-type-wise retrieval strategy analysis.
- Retrieval granularity ablation.
- Statistical testing across retrieval strategies.

## 12. Evidence table

| Claim | Page | Section/table/figure | Supporting quotation or precise paraphrase |
|---|---:|---|---|
| The paper introduces a hybrid retrieval-augmented framework for solar decision support. | 1 | Abstract | The abstract says Solar Intelligence unifies structured solar analytics, evidence-grounded scientific QA, and forecasting in one hybrid RAG framework. |
| Scientific questions are answered using BM25 and dense embeddings fused with RRF. | 1 | Abstract | It states that scientific questions use a hybrid retriever fusing BM25 and ChromaDB dense embeddings via RRF. |
| The generator is llama3.2:3b. | 1 | Abstract | The abstract reports grounded responses through llama3.2:3b. |
| The corpus includes research papers and institutional reports. | 3 | Data Sources / Table 1 | The paper reports 149 research papers and reports, including arXiv papers and reports from NREL, IEA-PVPS, IRENA, and Sandia. |
| The corpus is solar-domain and includes PV-related topics. | 3-4 | Corpus Construction and Table 2 | The arXiv queries include photovoltaic efficiency, PV performance modeling, PV soiling, degradation, inverter MPPT, bifacial panels, and related solar topics. |
| Corpus date range has an inconsistency. | 3 | Data Sources / Table 1 | Text describes 1994-2026; Table 1 appears to show 1994-2006. This should not be normalized without verification. |
| PDFs are extracted and chunked. | 4 | Corpus Construction and Processing | The paper reports PyMuPDF extraction and approximately 500-token chunks with 50-token overlap, yielding 9,496 chunks. |
| BM25 is implemented. | 4 | Corpus Construction and Processing | The paper reports two parallel indices, one of which is BM25. |
| Dense retrieval is implemented with BGE-small. | 4 | Corpus Construction and Processing | The dense index uses BGE-small 384-dimensional embeddings. |
| Each query is sent to both indices. | 4 | Retrieval through query routing | The paper reports parallel dispatch to both indices, each returning top-20 candidates. |
| Fusion uses RRF. | 4 | Retrieval through query routing | Results are fused via Reciprocal Rank Fusion because BM25 and cosine scores are not directly comparable. |
| Query routing distinguishes structured, semantic, and hybrid queries. | 4 | Retrieval through query routing | The classifier assigns routing tags for SQL-only, retrieval-only, or combined numerical/conceptual evidence paths. |
| The LLM is constrained by prompt rules. | 4 | Retrieval through query routing | The paper reports rules to not invent numerical values and to cite claims with markers. |
| Structured numeric answers bypass the LLM for numbers. | 4 | Retrieval through query routing | Numerical answer strings are constructed from SQL output when strongly structured signals are detected. |
| The system technology table lists BM25, BGE-small, RRF, PyMuPDF, and llama3.2:3b. | 7 | Table 4 | Table 4 lists sparse retrieval BM25, dense retrieval BGE-small, fusion RRF, chunking PyMuPDF, and generation llama3.2:3b via Ollama. |
| The paper shows semantic and structured query examples. | 8-10 | Results and Discussion / Query Types and QA Citation Results | The results section gives examples for semantic and structured queries, including cited evidence. |
| The semantic example exposes answer-quality limitations. | 8 | Semantic Query discussion | The paper notes that the answer omitted an operationally relevant temperature-efficiency fact and overemphasized a theoretical conversion ceiling. |
| The paper claims grounded generation without hallucination for the semantic path example, but not a formal metric. | 8 | Semantic Query discussion | It characterizes the example as grounded and not hallucinated, while discussing limitations qualitatively. |
| Structured numeric answers are deterministic from SQL. | 10 | Structured Query discussion | The paper states the numerical answer comes from SQL rather than LLM composition, preventing fabricated values for that path. |
| Forecasting is separate from RAG. | 6 | Forecasting Layer | The paper states the forecasting module operates independently of the RAG pipeline. |
| Deployment is described but not used as retrieval-efficiency evaluation. | 7 | Deployment Architecture | The paper describes FastAPI, Streamlit, cron updates, and an MCP-style manifest. |
| No forecast evaluation is performed. | 13 | Conclusion and Future Work | The paper explicitly says no evaluation of forecasts has been performed. |
| The current system has limitations unrelated to retrieval-arm comparison. | 13 | Limitations | The paper lists hardcoded location, NASA POWER lag, and point forecasts rather than uncertainty forecasts. |
| Corpus enlargement is future work. | 13 | Conclusion and Future Work | The paper states that enlarging the corpus is a next step for better QA. |
| No BM25-only vs dense-only vs hybrid controlled comparison is reported. | Not applicable | Whole paper | Precise paraphrase: the methods describe BM25, dense, and RRF hybrid operation, but the results section does not report separate retrieval arms, a shared benchmark question set, retrieval metrics, or statistical tests. |
