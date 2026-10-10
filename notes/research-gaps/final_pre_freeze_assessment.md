# Final Pre-Freeze Assessment

## 1. Screened evidence base

This assessment uses the previously detailed comparators—Solar Intelligence, Lit3R, SQuAI, IRPAPERS, and OpenScholar—and the already-registered records in the focused follow-up. No new records were added and no broad database search was conducted.

Full text or substantial text was inspected for RILS, PeerQA, Solar GenAI, Open Energy, Solar-VLM, Retrieval-Guided PV Inventory, HySemRAG, and Han et al. The registered IOP abstract for Research on PV was available, but its full text was not. Han et al.'s MDPI-hosted full text was obtained and screened as a review/framework, not as an experiment. Wang et al.'s full text remains unavailable after the final targeted attempt across ScienceDirect/Elsevier, DOI resolution, publisher API, OpenAlex, Semantic Scholar, Crossref, exact-title Google Scholar/web search, author-name plus exact-title search, an institutional-repository query, and linked ACM record. Accessible material is limited to publisher highlights/abstract and snippets. Wang's detailed methodology is therefore **Not reported / Not established**, not inferred from the abstract.

Evidence locations below use printed article/report pages where available. For RILS, the source is a 14-page ResearchSquare PDF whose corpus counts conflict internally; the counts are preserved as printed.

| Paper | Corpus/task and domain | Retrieval comparison and controls | Downstream QA/evidence evaluation | Screening result |
|---|---|---|---|---|
| **RILS / Orabi et al.** | Mixed renewable-energy materials, including peer-reviewed journals, reports, and roadmaps; Table 1 lists 4,200 Solar-PV documents. Corpus totals conflict: Table 1 gives 18,000 documents/28,800 passages; later sections give 21,000 documents/32,800 passages. 900 assessment queries, 150 per technology family, including 150 Solar-PV questions. | BM25+Generation, standard dense RAG, and hybrid BM25+dense RILS system conditions are reported. Shared expert-grounded benchmark is described. Exact shared corpus/index conditions, same generator/prompt across every condition, and retrieval as the sole changed factor are not established. | Table 2 compares downstream system outcomes. Retrieval metrics are reported by technology family, not by each baseline retriever. RILS uses NLI claim checking; no per-arm citation precision/completeness is reported. | **High overlap / Include-Core / High confidence.** ResearchSquare PDF, Table 1 p. 6; §§6.2–7.2 pp. 6–7; Fig. 2/§8.1 and Table 2/§8.2 p. 8; Table 3/§9 p. 9. |
| **PeerQA** | 208 papers with 579 annotated questions; broader set includes 12,546 processed questions. Scientific domains include ML, NLP, geoscience, and mixed venues; each question concerns one paper. | BM25, dense, multi-vector, cross-encoder, and sparse evidence retrievers are compared on evidence retrieval. No matched BM25+dense hybrid arm. Same retrieval benchmark is used for model evaluation; the retrieval models are not all carried into downstream QA. | RAG generation uses SPLADEv3 contexts and several LLMs. Reports evidence retrieval MRR/Recall@10, answerability, ROUGE-L, AlignScore, and Prometheus-2. Table 2 lists 112 unanswerable questions. No generated-citation precision/completeness. | **Moderate overlap / Include-Core / High confidence.** NAACL 2025, Table 2 p. 510; §3 pp. 510–512; §4.1/Table 3 p. 513; §4.2/Fig. 3 pp. 514–515. |
| **Solar GenAI** | Solar-PV assistant using mixed Malaysian policy, technical, institutional, and selected research materials; exact corpus count not clearly reported. | Dense cosine retrieval with all-MiniLM-L6-v2. LLM-only vs RAG is evaluated, not BM25/dense/hybrid arms. A fixed benchmark or common generator controls for a retriever comparison are not established. | Reports answer/hallucination observations and response latency. Prompting asks for refusal when information is insufficient, but systematic abstention is not evaluated. No retrieval or citation attribution metrics. | **High domain overlap / Include-Core / High confidence.** IJIC PDF, corpus and processing pp. 2–4; retrieval pp. 3–5; results pp. 6–8; conclusion p. 9. |
| **Open Energy** | OEDI energy datasets, catalog metadata, and supporting documentation; not a scientific-paper corpus. AskOEDI answers data-discovery questions. | BM25/dense/hybrid paper retrieval and matched retrieval arms are not reported. | No controlled scientific QA/citation benchmark established. | **Low overlap / Include-Context / High confidence.** NREL report, report body §§3–5. |
| **Research on PV** | Accessible IOP abstract describes PV forecasting and an expert knowledge corpus; scientific-paper composition is not established. | BM25, dense, hybrid, shared corpus/question conditions, and retriever arms are not reported in the abstract. | Specialized PV-QA is described for knowledge consolidation in forecasting; evidence/citation evaluation is not established. | **Low overlap / Exclude / Medium confidence.** Registered IOP abstract only; publisher full text unavailable. |
| **Solar-VLM** | Solar-PV forecasting using time-series and multimodal inputs, not scientific papers. | Scientific-paper BM25/dense/hybrid retrieval is not reported. | No scientific-literature QA or evidence/citation evaluation established. | **None / Exclude / High confidence.** Registered arXiv full text, abstract and forecasting methods/results. |
| **Retrieval-Guided PV Inventory** | Satellite imagery and rooftop scenes for PV inventory estimation. | Visual-embedding retrieval is not scientific-text retrieval; no BM25/dense/hybrid literature comparison. | No scientific QA, answer generation, or citation/evidence evaluation. | **None / Exclude / High confidence.** Registered arXiv full text, abstract, retrieval method, inventory experiments. |
| **HySemRAG** | Scientific-literature synthesis in geospatial epidemiology; approximately 500–1,300 retrievable full-text documents per ETL run from about 3,400 metadata candidates. Not solar/PV. | Combines semantic search, keyword filtering, and knowledge-graph traversal. BM25 specifically, a fusion formula, and matched retrieval arms are not established. | Literature synthesis and citation verification are described; controlled downstream BM25/dense/hybrid QA and formal citation precision/completeness are not established. | **Moderate overlap / Include-Core / Medium confidence.** arXiv:2508.05666, abstract and system/evaluation sections. |
| **Wang et al., Multi-level Retrieval with Representation Alignment…** | Publisher abstract describes scientific-literature cross-document QA, multi-level retrieval with contrastive-learning embeddings, and SciLitQA (>50,000 QA pairs); source-paper count/domain composition and solar/PV scope are not established. | Abstract mentions retrieval accuracy and comparisons with existing RAG models/public benchmarks. It does not establish BM25-only/dense-only/hybrid downstream arms, matched controls, or citation/evidence metrics. | **High potential topical/system overlap; exact controlled-design overlap unestablished / Include-Core / Medium confidence** for abstract-level facts. Full text unavailable after final targeted retrieval attempt; ScienceDirect PII S1568494626000979. |
| **Han et al., Automating systematic literature reviews with RAG** | Review of RAG/SLR methods; no experimental corpus or author-run QA benchmark. BM25/dense methods discussed as background; framework proposes four SLR stages. | No author-run retrieval comparison, downstream QA, evidence/citation scoring, or statistical comparison. | **Low overlap / Include-Context / High confidence.** MDPI full text, *Applied Sciences* 14(19), article 9103, §§2.1.1, 2.1.4, 3.1, 5. |

## 2. Studies with the closest methodological overlap

1. **RILS** is the closest energy-domain system comparison. It reports BM25+Generation, standard dense RAG, and hybrid BM25+dense RILS conditions on a 900-query renewable-energy assessment benchmark with 150 Solar-PV questions. It reports both retrieval and downstream system outcomes. However, it is a mixed-technology corpus, has conflicting corpus totals, bundles system changes beyond retrieval, and does not establish matched generator/prompt controls or per-arm formal citation metrics.
2. **IRPAPERS** is the direct retrieval-level precedent: BM25-only, dense-only, and hybrid text retrieval are compared under common scientific-page corpus and question conditions. Its downstream QA experiments do not carry those three text retrievers forward as matched generator arms.
3. **PeerQA** is the closest scientific QA/evidence retrieval benchmark complement. BM25 and dense/sparse retrievers are evaluated against author-annotated evidence, and answerability/generation are evaluated separately. Its downstream RAG uses SPLADEv3-retrieved contexts, not matched QA arms for each retrieval model.
4. **Lit3R, OpenScholar, and SQuAI** establish substantial scientific QA, synthesis, retrieval, or evidence/citation evaluation methods. None of the screened records establishes the proposed combination of a retrieval-only independent variable, common downstream conditions, and a solar-PV scientific-paper corpus.
5. **Solar Intelligence and Solar GenAI** establish solar-domain RAG applications. Their screened methods do not show the specified controlled BM25/dense/hybrid downstream evidence comparison.

## 3. Retrieval-level comparisons already established

- **IRPAPERS:** direct same-corpus/same-question BM25-only vs dense-only vs hybrid text retrieval comparison over 166 scientific papers/3,230 pages and 180 questions. It reports retrieval-level measures including Recall@1/5/20. This is not a downstream three-arm RAG experiment.
- **PeerQA:** BM25, several dense models, multi-vector retrieval, cross-encoder, and sparse retrieval are compared for evidence retrieval over the same paper-specific question/evidence task. It does not report a matched hybrid BM25+dense arm. Retrieval quality is measured with MRR and Recall@10.
- **RILS:** BM25+Generation, standard dense RAG, and hybrid RILS are reported as *system conditions*. Recall@5, Precision@5, MRR, and nDCG@5 are reported by technology family; those results do not establish per-retriever retrieval comparisons.
- **Lit3R and the other screened retrieval systems** report metrics for their own pipelines or component ablations; they do not establish the same three-way comparison as matched downstream QA conditions.

## 4. Downstream RAG/QA comparisons already established

- **RILS** reports downstream system-level scores for BM25+Generation, standard RAG, and RILS on its assessment benchmark. This constrains a broad claim that no energy-domain system comparison of these types exists. It does not establish retrieval as the sole experimental variable or same generator/prompt across all conditions.
- **PeerQA** evaluates answerability and generation using gold, full-text, or SPLADEv3-retrieved contexts. Its retrieval-model comparison is not propagated to matched downstream QA arms.
- **IRPAPERS** evaluates TextRAG/ImageRAG, retrieval depth, and oracle/hard-negative conditions, but does not carry BM25-only, dense-only, and hybrid text retrieval into three matched QA arms.
- **OpenScholar** evaluates scientific synthesis and downstream answer quality using its retrieval pipeline and component ablations; its ablations are not BM25/dense/hybrid strategy arms.
- **Lit3R, SQuAI, and Solar GenAI** establish additional scientific or solar RAG/QA methods, but not the candidate's controlled retrieval-variable experiment.

## 5. Evidence/citation-grounding comparisons already established

- **OpenScholar:** sentence-level citation precision, recall, and F1, plus answer correctness/coverage and expert evaluation.
- **Lit3R:** evidence precision, recall, and F1, alongside retrieval and answer-task metrics.
- **PeerQA:** author-annotated evidence supports evidence retrieval evaluation; AlignScore evaluates answer alignment with reference answers/evidence. This is not generated-citation precision or completeness.
- **RILS:** benchmark responses are annotated for citation accuracy and the RILS pipeline applies an NLI verifier to claims against retrieved passages. Per-system citation precision/completeness and the same citation score across its system conditions are not reported.
- **SQuAI:** faithfulness/relevance and inline citation/support display are reported; the screened evidence does not establish citation precision/completeness.
- **Solar Intelligence and Solar GenAI:** citations or source-grounded outputs appear, but formal citation precision/completeness is not established in the screened methods.

Retrieval recall, evidence retrieval, answer-evidence alignment, faithfulness, and generated-citation precision/completeness are distinct measures and should not be treated as interchangeable.

## 6. Solar/PV-specific studies already established

- **Solar Intelligence** reports a solar-oriented corpus of research papers/reports and structured solar data, and implements BM25, dense BGE-small, and hybrid BM25+dense RRF. It does not compare those as separate downstream QA arms.
- **Solar GenAI** evaluates an offline solar-PV assistant using dense retrieval over mixed policy/technical/research materials, comparing LLM-only with RAG; it does not evaluate retrieval strategy arms.
- **RILS** includes a Solar-PV subset of a mixed renewable-energy corpus and 150 Solar-PV assessment queries. The full corpus is multi-technology and not exclusively peer-reviewed solar-PV papers.
- **Research on PV, Solar-VLM, and Retrieval-Guided PV Inventory** concern PV forecasting or imagery/inventory tasks in the accessible evidence, not scientific-paper QA. The Research on PV full text remains unavailable.

## 7. Remaining methodological distinction

The screened evidence demonstrates retrieval-level strategy comparisons, scientific QA/evidence evaluation, solar/PV RAG applications, and a close system-level energy comparison. The distinction that remains to be tested is narrower:

> Retrieval itself is the independent variable in a matched BM25-only, dense-only, and specified hybrid comparison; the same solar-PV scientific-paper corpus, question benchmark, preprocessing, generator, prompt, and downstream evaluation are maintained; retrieval quality is reported separately from answer quality and evidence/citation attribution.

RILS does not establish that controlled design because its conditions differ at system level and its generator/prompt controls and per-arm citation scores are not established. PeerQA does not establish it because its downstream QA uses SPLADEv3 contexts rather than the retrieval-model arms. IRPAPERS establishes the retrieval-level comparison, not the requested downstream three-arm evidence-grounding comparison.

## 8. Threats to the proposed study

| Study | Exact or closest overlap | Remaining distinction |
|---|---|---|
| **RILS** | BM25+Generation, standard dense RAG, and hybrid system; renewable-energy assessment benchmark includes Solar-PV questions; retrieval and answer metrics | System-level rather than retrieval-only control; mixed technology/document corpus; same generator/prompt and per-arm citation metrics not established; corpus counts conflict |
| **IRPAPERS** | Same scientific corpus/questions for BM25-only, dense-only, and hybrid retrieval; retrieval metrics | No matched three-arm downstream QA/evidence attribution; not solar/PV |
| **PeerQA** | Scientific questions, BM25/dense evidence retrievers, human-annotated evidence, unanswerable cases, answerability and generation evaluation | Evidence retrieval is separate from downstream RAG; no matched BM25/dense/hybrid QA arms; not solar/PV |
| **Lit3R** | Scientific QA, hybrid retrieval pipeline, retrieval and evidence precision/recall/F1 | No solar/PV; no isolated matched three-arm retriever comparison |
| **OpenScholar** | Scientific synthesis QA and citation precision/recall/F1 | No solar/PV; no BM25/dense/hybrid retriever arms |
| **SQuAI** | Scientific QA, hybrid retrieval, faithfulness/relevance and supporting citations | No solar/PV; no matched strategy arms or established citation precision/recall |
| **Solar Intelligence** | Solar/PV paper/report corpus, BM25/dense/hybrid implementation, cited QA examples | No separate retriever arms or formal controlled answer/evidence comparison |
| **Solar GenAI** | Solar-PV RAG and answer/hallucination evaluation | Dense-only application; no retrieval metrics or formal citation attribution |
| **HySemRAG** | Scientific-literature synthesis with semantic/keyword/graph retrieval and citation verification | No solar/PV or matched retrieval-strategy downstream comparison |
| **Wang et al.** | Abstract describes scientific cross-document QA, multi-level retrieval, SciLitQA (>50,000 pairs), and comparisons with existing RAG models/public benchmarks | Full text unavailable after final targeted retrieval attempt; matched BM25/dense/hybrid QA arms, solar/PV scope, controls, and evidence/citation scoring are not established |
| **Han et al.** | Review of RAG/SLR methods; BM25 and dense retrieval discussed, and a four-stage framework proposed | No author-run retrieval or QA experiment; contextual overlap only |

Han et al. is resolved as a review/framework and does not establish an author-run controlled experiment. Wang et al. remains a material unresolved threat: its accessible abstract establishes a neighboring scientific-literature QA/RAG task but does not disclose the experimental arms or controls.

## 9. What would NOT constitute a contribution

- Implementing BM25, dense, or hybrid retrieval individually for scientific papers.
- Repeating a BM25-only/dense-only/hybrid retrieval benchmark without distinguishing it from IRPAPERS.
- Building another general scientific-literature RAG or citation-backed QA system without a justified evaluation distinction.
- Applying hybrid retrieval to solar/PV material without a controlled strategy comparison; Solar Intelligence already demonstrates such implementation.
- Reporting only retrieval scores and treating them as evidence of downstream answer or citation quality.
- Reporting only answer correctness or displayed citations without evaluating retrieval and evidence attribution separately.
- Calling RILS a clean retrieval-only three-arm experiment, or describing PeerQA as a matched downstream comparison of its retrieval models.

## 10. What contribution remains defensible

Within the screened evidence, a clearly distinguishable **methodological and empirical contribution** remains possible if the study isolates retrieval strategy under common conditions and measures its effects at both retrieval and downstream evidence-grounding levels on a solar-PV scientific-paper corpus. A documented question/evidence benchmark and appropriate uncertainty/statistical reporting could support that contribution. This is a conditional assessment of the screened records, not a claim about the entire literature.

## 11. Recommended research question

**Freeze the research question as framed below.** Han et al. is a review/framework without an author-run controlled comparison. Wang et al. remains unresolved after the final targeted retrieval attempt, but its abstract establishes only neighboring scientific QA/RAG, a benchmark, and retrieval experiments. The abstract does not establish the lexical/dense/hybrid arms, controlled downstream conditions, solar/PV scope, or joint evidence-grounding outcomes that define the proposed methodological distinction. On the accessible evidence, this is a bounded literature-access limitation rather than sufficient grounds to defer the RQ. Do not infer the missing methods.

## 12. Recommended study design

The frozen RQ retains the distinction from RILS and IRPAPERS by specifying one documented solar-PV scientific-paper corpus and question/evidence benchmark; common preprocessing, generator, prompt, and context budget; BM25-only, dense-only, and a specified hybrid retriever as the retrieval treatment; separate retrieval outcomes from answer and evidence/citation outcomes; and pre-specified statistical comparisons. This is a concise methodological boundary, not an implementation plan or a claim that any component is absent from all prior work.

## 13. Residual uncertainty

1. Wang et al.'s full text remains unavailable after the final targeted retrieval attempt. Routes checked: ScienceDirect article/full-text endpoint, DOI resolution, Elsevier API, OpenAlex, Semantic Scholar, Crossref, exact-title Google Scholar, exact-title web search, author-name plus exact-title search, Communication University of China institutional-site query, ACM-linked record, and open-access links surfaced from these records. Publisher/index metadata indicates closed access or no OA PDF; the ACM record returned HTTP 403. The abstract alone does not establish the proposed controlled comparison.
2. Research on PV was screened from the registered abstract only; any full-text details beyond the abstract remain unverified.
3. RILS reports incompatible corpus totals across Table 1, §6.2, §7.2, and Table 3. The discrepancy is preserved rather than resolved.
4. In RILS, the shared benchmark is described, but shared corpus/index, generator, and prompt controls across all baseline conditions are not fully established.
5. Other metadata-only records remain in the project register outside the ten focused follow-up items; they were not screened in this pass and are not treated as methodological evidence here.
6. This is a bounded screening of registered records and the previously screened set; it does not support a field-wide absence statement.

## 14. Final decision

**A. FREEZE RQ**

The accessible evidence does not provide a sufficiently material methodological threat to prevent freezing the RQ. Wang et al.'s abstract describes scientific cross-document QA/RAG, SciLitQA (>50,000 QA pairs), multi-level retrieval, and retrieval experiments, but it does not report a BM25-only/dense-only/hybrid downstream comparison, matched controls, solar/PV scope, or joint evidence-grounding outcomes. The missing full text is recorded as an unresolved-but-bounded literature-access limitation; no absent method is inferred.

### Final defensible RQ

**How do BM25, dense, and hybrid retrieval strategies, compared under identical corpus, question-benchmark, preprocessing, generator, prompt, and evaluation conditions, affect retrieval quality, answer quality, and evidence attribution in question answering over solar-PV scientific literature?**

### Methodological distinction

The RQ concerns retrieval strategy as the controlled independent variable and evaluates its effects separately at retrieval and downstream answer/evidence-attribution levels on one common solar-PV scientific-literature corpus and question benchmark.

### Three strongest threats considered

| Threat | What the screened evidence establishes | Why it does not close the distinction |
|---|---|---|
| **IRPAPERS** | Direct same-corpus/same-question BM25-only, dense-only, and hybrid retrieval comparison over scientific papers, with retrieval metrics. | This establishes the retrieval-level comparison. It does not carry all three retrievers into matched downstream QA/evidence-attribution arms and is not solar/PV-specific. |
| **RILS** | BM25+Generation, dense RAG, and hybrid system-level conditions on a renewable-energy benchmark that includes Solar-PV questions; retrieval and downstream system outcomes are reported. | The compared conditions are systems, not established as a retrieval-only variable under common generator/prompt controls; the corpus is mixed technology and formal per-arm citation completeness is not established. |
| **PeerQA** | Scientific QA with BM25/dense and other evidence retrievers, author-annotated evidence, unanswerable examples, and separate answerability/generation evaluation. | Retrieval model comparisons are not propagated into matched downstream QA arms for BM25-only, dense-only, and hybrid retrieval; it is not solar/PV-specific. |

OpenScholar, Lit3R, and SQuAI further establish scientific QA and evidence/citation evaluation, but not the specified solar-PV controlled three-arm downstream comparison. Solar Intelligence and Solar GenAI establish solar/PV RAG applications, but not that controlled comparison.

### Confidence and remaining limitations

- **Confidence: Medium.** The core distinction is supported by direct screening of the closest retrieval-level, energy-system, and scientific QA/evidence comparators. Confidence is not high because Wang et al.'s detailed methods remain inaccessible and Research on PV was screened from its registered abstract only.
- The screened set is bounded and cannot establish field-wide absence. The final RQ is defensible relative to the screened evidence; it is not a claim of priority or universal absence.
- For Wang et al., the publisher abstract establishes topical/system adjacency only. BM25, dense-only, hybrid arms, the control design, solar/PV domain, and evidence/citation methods remain **Not reported / Not established**. This residual uncertainty does not, on available evidence, justify holding the RQ open.
