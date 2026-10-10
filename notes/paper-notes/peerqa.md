# PeerQA: A Scientific Question Answering Dataset from Peer Reviews

## Screening scope and source

Focused screen of the registered NAACL 2025 full text, printed pages 508–517 (PDF pages 1–10). The paper evaluates evidence retrieval, answerability, and answer generation, but these are distinct experiments.

## Corpus and questions

- **Scientific corpus:** camera-ready academic papers from ML, NLP, geoscience, and mixed venues, including ICLR, NeurIPS, ARR, ACL, COLING, CoNLL, ESD, ESurf, and F1000. Paper text is extracted with GROBID 0.8 (§3, printed pp. 510–511).
- **Domain:** scientific literature, not solar/PV.
- **Question source:** human-written peer-review questions. InstructGPT is used to decontextualize and decompose questions; questions are manually filtered (§3, pp. 510–511). The underlying questions are not synthetic.
- **Answer/evidence annotation:** paper authors annotate free-form answers and highlight evidence in the final publication. Five CoNLL papers were handled by a senior NLP professor/co-author because the authors could not be reached (§3, p. 512).
- **Counts:** the paper reports 12,546 processed questions and 579 annotated question-answer items from 208 papers; it also releases 11,967 questions without collected answers from 2,623 papers (§3, pp. 511–512). Table 2 (p. 510) reports 112 unanswerable questions. The reported category totals are retained as printed; this note does not attempt to reconcile them.
- **Question types:** eight classes in a 100-question sample—Methods, Data, Implications, Definitions, Comparisons, Analysis, Justification, Evaluation (§3, p. 511 and referenced appendix §O).
- **Multi-document:** no. Questions are focused on one publication. About 30% require combining evidence from more than one location **within that paper** (p. 510).
- **Unanswerable:** yes; questions can be flagged unanswerable for insufficient information, and 112 are listed in Table 2 (p. 510).

## Evidence retrieval (retrieval-level evaluation)

- Section 4.1 (printed p. 513) evaluates answer-evidence retrieval within the relevant paper, at paragraph and sentence levels; a title-prepending variant is also tested.
- Systems include BM25; dense models MiniLM-L12-v2, Contriever, Dragon+, and GTR; multi-vector ColBERTv2; cross-encoder scoring; and sparse SPLADEv3.
- Table 3 (p. 513) reports MRR and Recall@10 across these systems and passage settings.
- These are same-task evidence-retrieval comparisons against annotated gold evidence. A BM25+dense hybrid retrieval arm is not reported.

## Answerability and generation (downstream QA)

- Section 4.2 (printed pp. 514–515) separately evaluates answerability and answer generation using retrieved contexts. Context conditions include gold evidence, SPLADEv3 top-k paragraphs for k ∈ {10, 20, 50, 100}, and full text.
- Answerability models include Llama-3-8B-Instruct, its 32k variant, Mistral-7B-Instruct-v0.2, Command-R, GPT-3.5-Turbo, and GPT-4o.
- The answerability prompt permits a “No Answer” output. Generation is separately run on answerable items without the abstention instruction.
- Metrics include answerability macro-F1, ROUGE-L, AlignScore against author answers and annotated evidence, and Prometheus-2 correctness ratings (pp. 514–515).
- **Control limitation:** retrieval model comparisons are not each carried forward into matched downstream RAG arms. The described RAG conditions use SPLADEv3-retrieved contexts. The paper therefore does not compare BM25-only, dense-only, and hybrid downstream QA under a shared generator/prompt.

## Evidence and citation evaluation

- Annotated evidence sentences/paragraphs are the ground truth for the retrieval task.
- AlignScore compares generated answers against reference answers/evidence; it is an answer-evidence alignment measure, not reported as a named faithfulness metric.
- Generated citations are not evaluated. Citation precision, citation completeness/recall, and claim-to-citation attribution scores are not reported.
- Latency/resource evaluation and inferential statistical comparisons are not reported.

## Comparison with proposed study

### Exact overlap

- Scientific-paper QA, human peer-review questions, author-provided answers and evidence, BM25 and dense retrieval evaluation, retrieval metrics, unanswerable cases, and downstream answerability/generation evaluation.

### Important differences

- Single-paper questions, not cross-document synthesis; no solar/PV corpus.
- Evidence retrieval model comparisons and downstream QA are separate; downstream RAG uses SPLADEv3 contexts, not BM25-only/dense-only/hybrid arms.
- No hybrid BM25+dense retrieval arm, generated citation evaluation, or matched retriever-to-answer/evidence comparison.

## Overlap assessment

- **overlap_level:** Moderate
- **relevance_decision:** Include-Core
- **confidence:** High

PeerQA is a close scientific QA and evidence-retrieval benchmark precedent. It does not establish the proposed controlled three-arm downstream comparison.

## Evidence locations

NAACL 2025, printed pp. 508–517: Table 2 p. 510; §3 pp. 510–512; §4.1 and Table 3 p. 513; §4.2 and Fig. 3 pp. 514–515.
