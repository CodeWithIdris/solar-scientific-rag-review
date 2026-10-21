# Final Protocol Closure Audit — 2026-10-21

**Project:** Evaluating Retrieval Strategies for Evidence-Grounded Question Answering over Solar Photovoltaic Scientific Literature  
**Audit result:** **PASS — protocol closed; execution remains on hold by explicit researcher instruction.**

## 1. Researcher approvals reconciled

The following decisions were recorded in the master protocol closure register, decision register, checklist, manuscript status, and manuscript v0.3:

- **DEC-01:** Core discovery window and pre-2024 citation-chaining scope approved.
- **DEC-02:** Alternative B approved. Distinct first authors and no candidate-author overlap do not establish independent research groups.
- **DEC-03:** Publication-year precedence and prohibition on repository-deposit-date substitution approved.
- **DEC-04:** Multi-source discovery and query logging procedure approved; API pagination/sorting behavior remains pilot-verification work.
- **DEC-05:** Ten-item known-item metadata-discovery benchmark frozen after the approved KI-10 replacement.
- **DEC-06:** Primary and review-inclusive sensitivity-index rules approved.
- **DEC-07:** Text-first extraction scope approved.
- **DEC-08:** Empirical threshold-setting procedure approved; numerical CER/WER thresholds remain dependent on the 20-paper calibration pilot.
- **DEC-09:** Reference-list metadata extraction and exclusion from searchable chunks approved.
- **DEC-10:** Single-reviewer and delayed masked re-screen policy approved; report as intra-rater temporal consistency, not inter-rater reliability.
- **DEC-11:** Retrieval-architecture selection procedure approved; actual model and parameter values remain development-stage decisions.
- **DEC-12:** Generator-selection and freeze procedure approved; actual generator/configuration remain development-stage decisions.
- **DEC-13:** Benchmark-size and category-mix justification procedure approved; final size/mix remain dependent on corpus freeze.
- **DEC-14:** Hypothesis framing approved: directional H1 at retrieval level, cautious downstream comparisons, and exploratory/non-directional H4.

## 2. Known-item benchmark frozen

The ten targets are frozen for **metadata-discovery sensitivity only**, two per subdomain:

| Subdomain | Item IDs |
|---|---|
| Tandem PV | KI-01, KI-02 |
| Silicon technologies | KI-03, KI-04 |
| Module reliability | KI-05, KI-06 |
| PV forecasting | KI-07, KI-08 |
| Emerging PV | KI-09, KI-10 |

**KI-10 replacement:** Tran Ho et al. (2024), “Organic Solar Modules with Good Stability under Ultraviolet Irradiation,” *Solar RRL*, 8(11), article 2400101. DOI: [10.1002/solr.202400101](https://doi.org/10.1002/solr.202400101). The publisher identifies it as an open-access research article first published on 2024-04-06; institutional repository metadata identifies it as peer-reviewed. Publisher record: https://onlinelibrary.wiley.com/doi/10.1002/solr.202400101.

The previous KI-10 life-cycle-assessment proceedings paper has been removed from the frozen list. This replacement preserves five declared subdomains with two items each.

**Important distinction:** a known item can count for metadata-discovery sensitivity without qualifying for the experimental corpus. Every corpus item still requires a separate check of publication type, topical eligibility, and lawful full-text access before ingestion. Do not ingest a paper whose lawful full-text access is not confirmed.

## 3. Closure criteria

- [x] Researcher policy/procedure sign-off recorded.
- [x] DEC-02 qualification about research-group independence retained.
- [x] H1/H2/H3/H4 framing recorded as approved and pre-experimental.
- [x] Ten-item known-item list frozen with five subdomains and two items per subdomain.
- [x] KI-10 replacement and DOI recorded in the checklist and manuscript.
- [x] Full-text corpus eligibility explicitly separated from metadata-discovery sensitivity.
- [x] Manuscript status and claim register reconciled.
- [x] No pilot or confirmatory results claimed.

**Protocol closure: PASS.**

## 4. Execution hold — no pilot run

The researcher explicitly instructed on 2026-10-21: **do not run any pilot yet**. Therefore this closure audit does not authorize execution.

- 300-slot discovery pilot: **NOT RUN — ON HOLD**.
- 20-paper extraction calibration pilot: **NOT RUN — ON HOLD**.
- Real full-text acquisition: **NOT AUTHORIZED**.
- Question-benchmark construction: **NOT AUTHORIZED**.
- Confirmatory retrieval/generation experiment: **NOT RUN**.

Separate explicit researcher authorization is required to lift the execution hold.

## 5. Remaining non-closure dependencies

These are expected later-stage dependencies, not unresolved protocol-sign-off blockers:

1. API pagination, overlap, and server-side sorting checks during the authorized discovery pilot.
2. Numerical extraction thresholds from the authorized 20-paper calibration pilot.
3. Actual retrieval model, chunking/fusion parameters, generator and decoding/context settings through the approved development procedure.
4. Final benchmark size and category mix after corpus freeze and prospective precision/power justification.
5. Per-paper lawful full-text eligibility before experimental-corpus ingestion.

No real-paper corpus was downloaded, no benchmark questions were created, and no retrieval or generation experiment was run as part of this audit.
