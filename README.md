# Vinci Research — Technical Reports

Manuscripts, aggregate evidence packages, and release materials for Vinci Research
technical reports.

## Reports

| No. | Title | Version | Status |
|---|---|---|---|
| 2 | Character Transfer Across Three Model Families | — | in preparation |
| 1 | Transferring Character Post-Training to Mistral 7B | 1.0 | published 13 August 2026 |

## Technical Report No. 2

**Character Transfer Across Three Model Families**
*Reduced unsupported assertions, impaired grounded answering, and a failed
utility-preservation bar*

George Pu, Ayush Naik

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
repository. See each report's reproducibility statement for the exact boundary.

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

Use the `CITATION.cff` in each report directory. Cite the published version, not a
pre-release tag.
