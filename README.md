# Vinci Research — Technical Reports

Manuscripts, aggregate evidence packages, and release materials for Vinci Research
technical reports.

## Reports

| No. | Title | Version | Published | DOI |
|---|---|---|---|---|
| 2 | [Character Transfer Across Three Model Families](reports/tr2/) | 1.0 | 1 September 2026 | [10.5281/zenodo.22236690](https://doi.org/10.5281/zenodo.22236690) |
| 1 | Transferring Character Post-Training to Mistral 7B | 1.0 | 13 August 2026 | — |

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

`reports/tr2/` in this repository is the published package, byte-for-byte. Its
`checksums.sha256` and `manifest.json` describe the archived release, so nothing under that
path is edited after publication — corrections become a new version, not a rewrite.

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
