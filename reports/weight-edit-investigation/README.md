# Weight-edit investigation: sanitized aggregate evidence

Prepared 9 November 2026. This directory accompanies the weight-edit investigation article. It contains newly authored aggregate data, explanation and calculation code. It includes only whitelisted aggregate-summary excerpts, not complete receipts, item-level benchmark records, model weights, or third-party public source files.

## What the files establish

- `data/public-author-aggregates.json`: 37 public author-reported benchmark aggregates, attributed through exact public citations. These are sample-mean accuracy, not best-of-n or pass@k. Qwen and Gemma have different protocols and must not be pooled.
- `data/local-paired-aggregates.json`: 16 reported local paired contingency tables. These were transcribed from partial private reader evidence and secondary private audit summaries. Some margins were uniquely recovered from rounded source rates and n; residual contingency cells were derived. They are not raw per-item evidence. The two MATH random comparisons have secondary-summary support, not an embedded original reader. Four both-uncut tables select items after observed outcomes and are diagnostic subsets, not unbiased ability estimates.
- `data/completion-diagnostics.json`: 14 reported Qwen arm summaries. Reader-reported cap hits and token medians do not establish the configured token maximum. Null means unknown, never zero. Four random-arm diagnostic counts omitted by the normalized source were restored only where explicitly printed in the retained aggregate excerpts, with row-level correction notes. Other missing diagnostics remain unknown; absence is not a successful check.
- `data/source-excerpts.json`: seven sanitized aggregate-summary excerpts, linked from paired/diagnostic rows. Only reviewed summary lines were retained. Notification wrappers, identities, paths, URLs, decision-record references and unnecessary answer-letter histograms are excluded. Authenticity and complete-run evidence have not been independently verified. Random-control original readers are not present.
- `data/context-and-limits.json`: explicit missing settings, artifact/evaluation-linkage limits and an incomplete 500-item Piccolo test. Its missing counts, gain and interval remain null; it cannot be combined with the separate 239-item selection holdout.
- `data/recomputed-statistics.json`: independently checkable arithmetic from those aggregate tables. This is not an independent model run, rescoring of generations, proof of dataset pairing, or a reproduction of the original editing recipe.

Edited-arm names are receipt labels. A separate recorded artifact reconstruction does not establish which exact weights, tokenizer, template or effective configuration a particular evaluation loaded. Artifact-to-evaluation linkage is unverified. Local configured token caps and thinking settings remain unknown, including thinking mode on the 239-item holdout. Original training overlap for that holdout is unchecked. Full item manifests, raw outputs, scorers and continuation rules are not supplied.

Initial and completion-control CSQA/ARC rows are separate evaluations. Identical or fresh items across stages have not been established. Those controls change inference as well as weights; token budgets are close rather than identical. They do not identify the causal share of the MATH gain, and a direct MATH completion control remains missing. Reused edited-arm outputs make the two MATH random comparisons additional controls, not independent edited-model reruns.

## Reported intervals and reproducible calculation

Reported 95% paired-bootstrap intervals are preserved in `reported_95_percent_ci_pp`. The original records report 10,000 resamples, but complete original ordered records and RNG/quantile implementations are unavailable. No historical RNG is invented or recreated here.

`calculations.py` separately enumerates the empirical paired-bootstrap distribution using floating-point arithmetic: each of n draws contributes -1, 0 or +1 according to the observed reference-only, tied and comparison-only frequencies. It reports the 2.5th/97.5th percentiles under `recomputed_empirical_bootstrap_95_percentiles_pp`. This is an empirical-bootstrap interval, not an exact-coverage interval. Finite-draw reported endpoints may differ. Do not replace reported source intervals with this calculation without making that methodological change explicit.

The script also calculates exact two-sided McNemar p values as a secondary paired diagnostic. These calculations are conditional on the chosen edit and sample and do not account for candidate selection, adaptive looks, training overlap or multiple comparisons. Crossing zero is not proof of equivalence. Zero observed regressions is limited to its evaluated sample.

## Recalculate and verify

Use Python 3 with only its standard library, from this directory:

```sh
python3 calculations.py --check
python3 calculations.py --json
```

The check exercises every supplied aggregate, rejects deliberately wrong margins, an invented cap, invented linkage, a non-public citation, an out-of-bounds cap count and an invented missing result. It also checks identical-arm and all-improved numerical controls, compares the stored recalculation, and verifies the SHA256 manifest covers the complete directory except the manifest itself. The JSON command writes only to standard output; neither command makes network calls or launches a model.

## Public author sources and attribution

Rikiya Takehi, Jayden Teoh, Alex Zhang and Omar Khattab authored [Sparks of Weight-Space Programming](https://rikiyat.github.io/blog/weight-space-programming/). The original public protocol, benchmark results, negative Gemma follow-up and exact released-edit manifest are cited in `data/public-sources.json` at repository commit `4d09ba6d6a7e891dd8063974dfe81b3d78e3494f`. Public author-reported values are kept separate from local measurements. The public release documents missing harness/intermediate material; an incomplete local recipe reconstruction does not invalidate the authors' released-checkpoint results or prove their claims false.

This subset redistributes no complete private receipts, third-party public source documents, third-party code, benchmark item text or weights. Its rights statements concern only the newly authored subset; no license or publication right is granted for underlying models, datasets, private source material or third-party works. Public citations retain the original authorship. This directory does not assert contributor credits, independent release approvals, a report number, or a DOI.
