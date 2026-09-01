# Vinci Technical Report No. 2 - Publication Candidate Package

## Character Transfer Across Three Model Families

**Version:** 1.0  
**Prepared:** 1 September 2026  
**Evidence tier:** development-tier validation evidence  
**Claim tier:** internal review only  
**Primary-test holdout:** untouched  
**Model release:** none

This package contains Vinci Technical Report No. 2 and its supporting release materials.

The central result is negative but useful: the frozen character SFT-to-DPO intervention reduced unsupported assertions in all three tested model families under both judges, but answerable-control accuracy deteriorated beyond the pre-registered limit in every family. No family met the complete utility-preservation bar. OLMo produced the least damaging measured frontier and motivates a successor experiment; it did not pass as a model release candidate.

## Start here

- `report/Vinci_Technical_Report_No_2.pdf` - archival two-column report.
- `report/Vinci_Technical_Report_No_2.docx` - editable review copy.
- `report/Vinci_Technical_Report_No_2.html` - self-contained web version.
- `report/Vinci_Technical_Report_No_2.md` - canonical manuscript source.
- `PUBLICATION_CHECKLIST.md` - work that must close before version 1.0.
- `release/RELEASE_NOTES.md` - release summary and claim boundary.
- `release/CLAIMS.md` and `release/LIMITATIONS.md` - public claim controls.
- `release/DATA_AND_PROVENANCE.md` - run matrix, hashes, judge provenance, and missing fields.
- `web/` - research-page, launch, FAQ, and Report No. 1 follow-up copy.

## What is included

- Report in Markdown, PDF, DOCX, and self-contained HTML.
- Five publication figures in PNG, SVG, and PDF.
- Machine-readable aggregate result and provenance tables.
- Release notes, claims, limitations, reproducibility, licensing, and citation files.
- Public-export allowlist and denylist.
- Build scripts and source files.
- Package manifest and SHA-256 checksums.

## What is deliberately not included

- Model weights or adapters.
- The encrypted primary-test holdout, its prompts, labels, or custody key.
- Private raw response text.
- Provider credentials or unredacted provider responses.
- Sanitized item-level scored outputs and per-call judge ledgers. Those still need to be exported from the private research repository through the allowlist before a reproducible public evidence bundle exists.
- Capability-preservation results. They were not part of the completed bank.

## Publication status

This is the final version 1.0 document. It is an aggregate-only release: the evidence tier
is unchanged and three items remain open, recorded in Appendix D of the report.

1. Public tables have not been regenerated from the frozen scored artifacts.
2. Sanitized item-level labels and judge ledgers have not been exported.
3. Benchmark-item rights review is not complete; the benchmark is under controlled access.

Development-tier validation evidence only. Refusal adjustment is Judge-B-only. Capability
preservation was not evaluated. No external audit was performed. The primary holdout remains
sealed. No model checkpoint is recommended for release.


## Non-negotiable claim boundary

Permitted headline:

> We tested one frozen character post-training recipe across three model families. It reduced unsupported assertions, but no family preserved grounded-answer accuracy well enough to meet the pre-registered bar.

Do not say that character transfer succeeded, truthfulness improved, the result was externally validated, OLMo passed, the primary holdout passed, or a production model is ready.
