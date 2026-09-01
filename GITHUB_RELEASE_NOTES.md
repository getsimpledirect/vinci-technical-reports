# Technical Report No. 2 — Character Transfer Across Three Model Families

*Reduced unsupported assertions, impaired grounded answering, and a failed
utility-preservation bar*

George Pu, Ayush Naik · 1 September 2026 · DOI [10.5281/zenodo.22236690](https://doi.org/10.5281/zenodo.22236690)

We tested one frozen character post-training recipe across three model families. It reduced
unsupported assertions, but no family preserved grounded-answer accuracy well enough to meet
the pre-registered bar.

Development-tier validation evidence only. Refusal adjustment is Judge-B-only. Capability
preservation was not evaluated. No external audit was performed. The primary holdout remains
sealed. No model checkpoint is recommended for release.

## What is here

The report in Markdown, HTML, DOCX and PDF; publication figures; aggregate result tables;
claim, limitation, provenance and reproducibility statements; citation file, manifest and
checksums.

## What is not

Item-level scored outputs, per-call judge ledgers, exclusion records, analysis locks,
artifact bindings, benchmark prompt and reference text, model weights, and the primary-test
holdout. This is an aggregate-only release: it does not support independent recomputation of
the readout. See Appendix D of the report and `docs/data_access.md`.

## Verifying

```sh
shasum -a 256 -c Vinci-TR2-Character-Transfer-v1.0-public.zip.sha256
unzip -q Vinci-TR2-Character-Transfer-v1.0-public.zip && cd tr2
shasum -a 256 -c checksums.sha256
```

Report text, figures and Vinci-authored tables are CC BY 4.0. Analysis and build code is
Apache 2.0. Benchmark items remain under per-item rights review.
