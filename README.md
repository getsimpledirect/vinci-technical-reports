# Vinci Research — Technical Reports

Manuscripts, aggregate evidence packages, and release materials for Vinci Research
technical reports.

## Reports

| No. | Title | Version | Published | DOI |
|---|---|---|---|---|
| 3 | [Runtime Pass Is Not Correctness](reports/tr3/) | 1.0 | 1 September 2026 | [10.5281/zenodo.22241477](https://doi.org/10.5281/zenodo.22241477) |
| 2 | [Character Transfer Across Three Model Families](reports/tr2/) | 1.0 | 1 September 2026 | [10.5281/zenodo.22236690](https://doi.org/10.5281/zenodo.22236690) |
| 1 | Transferring Character Post-Training to Mistral 7B | 1.0 | 13 August 2026 | — |

## Technical Report No. 3

**Runtime Pass Is Not Correctness**
*A Negative Reasoning-Efficiency Post-Training Result and Verifier Audit on Qwen3.8-27B*

George Pu · 1 September 2026 · Version 1.0

**DOI** [10.5281/zenodo.22241477](https://doi.org/10.5281/zenodo.22241477) ·
**Report page** https://www.getsimpledirect.com/research/papers/runtime-pass-is-not-correctness

A conservative SFT+DPO recipe missed every reasoning-efficiency target, a serving control
reproduced the apparent improvement on untrained weights, and the executable evaluator used
to measure correctness accepted 24 of 24 deliberately incorrect shortcut programs. No model
checkpoint, evaluator bank, or release candidate resulted.

Development-tier evidence on one model lineage. The replacement verifier bank is **not
qualified**. The superseded adequacy claim is **withdrawn**. Reported rates characterise the
audited evaluation set and do not estimate ordinary product traffic. Appendix E records what
was closed before release and states plainly what was not performed: no independent
statistical review, no independent verifier or code review against the production path, and
no external peer review or audit.

The bound research records sit in a private repository; each is identified exactly by commit
and blob SHA in `reports/tr3/data/evidence_bindings.json`.

## Technical Report No. 2

**Character Transfer Across Three Model Families**
*Reduced unsupported assertions, impaired grounded answering, and a failed
utility-preservation bar*

George Pu, Ayush Naik · 1 September 2026 · Version 1.0

**DOI** [10.5281/zenodo.22236690](https://doi.org/10.5281/zenodo.22236690) ·
**Report page** [getsimpledirect.com/research/papers/character-transfer-across-three-model-families](https://www.getsimpledirect.com/research/papers/character-transfer-across-three-model-families) ·
**PDF** [reports/tr2/report/Vinci_Technical_Report_No_2.pdf](reports/tr2/report/Vinci_Technical_Report_No_2.pdf)

> We tested one frozen character post-training recipe across three model families. It
> reduced unsupported assertions, but no family preserved grounded-answer accuracy well
> enough to meet the pre-registered bar.

### Scope of the evidence

Development-tier validation evidence only. Refusal adjustment is Judge-B-only. Capability
preservation was not evaluated. No external audit was performed. The primary holdout
remains sealed. No model checkpoint is recommended for release.

### What this repository contains

- the report in Markdown, HTML, DOCX, and PDF;
- publication figures;
- aggregate machine-readable result tables;
- claim, limitation, provenance, and reproducibility statements;
- a citation file, package manifest, and checksums.

### What it does not contain

- model weights or adapters;
- the encrypted primary-test holdout, its prompts, labels, or custody key;
- provider credentials or unredacted provider responses;
- item-level scored outputs and per-call judge ledgers;
- validation benchmark prompt and reference text — see [docs/data_access.md](docs/data_access.md).

Independent recomputation of the published summary is not yet possible from this
repository. Report No. 2 is an aggregate-only release: three items remain open and are
recorded in its Appendix D — the public tables have not been regenerated from the frozen
scored artifacts, sanitized item-level labels and judge ledgers have not been exported, and
the benchmark-item rights review is not complete. See `reports/tr2/release/REPRODUCIBILITY.md`
for the exact boundary.

## Verifying a release

The published package is on Zenodo under the DOI above. To check a download:

```sh
shasum -a 256 -c Vinci-TR2-Character-Transfer-v1.0-public.zip.sha256
unzip -q Vinci-TR2-Character-Transfer-v1.0-public.zip && cd tr2
shasum -a 256 -c checksums.sha256
```

`reports/tr2/` in this repository tracks the published package. It is **not** byte-for-byte
identical to the archive on Zenodo, and the difference is recorded rather than silent.

**Divergence from the published version 1.0 archive — three files.**
`source/latex/Vinci_Technical_Report_No_2.tex` is a Pandoc-generated build intermediate, and
the copy inside the published archive is the version 0.9 generation: it reads "Version 0.9"
and carries the pre-1.0 Appendix D. Every other artifact in that archive — Markdown, HTML,
DOCX, PDF — is version 1.0 and self-consistent, so nothing a reader opens is affected; only a
rebuild from `source/` would be. It has been regenerated here, which also changes
`checksums.sha256` and `manifest.json`, the two files that describe it. See erratum E6.

The archive on Zenodo is immutable and was not altered. Verify a download against **its own**
`checksums.sha256`, which is internally consistent; the repository's copy describes the
repository. A checksum establishes that a file is unmodified, not that it is correct — this
erratum is exactly that distinction.

## Licensing

| Material | Licence |
|---|---|
| Report text, figures, and Vinci-authored tables | [CC BY 4.0](LICENSE-CC-BY-4.0) |
| Analysis and build code | [Apache 2.0](LICENSE) |
| Validation benchmark items | Controlled access — see [docs/data_access.md](docs/data_access.md) |
| Upstream model checkpoints | Governed by their own upstream licences; not redistributed here |

Licences do not inherit across artifact classes. Nothing here relicenses upstream models,
prompt sources, or third-party benchmark material.

## Citing

Use the `CITATION.cff` in each report directory, and cite the published version rather than
a pre-release tag.

> Pu, G., & Naik, A. (2026). *Character Transfer Across Three Model Families: Reduced
> unsupported assertions, impaired grounded answering, and a failed utility-preservation
> bar* (Version 1.0). Vinci Technical Report No. 2. https://doi.org/10.5281/zenodo.22236690
