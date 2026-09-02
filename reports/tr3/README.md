# Vinci Technical Report No. 3 — Publication Package

## Runtime Pass Is Not Correctness

**Version:** 1.0  
**Date:** 1 September 2026  
**Author:** George Pu  
**Evidence tier:** development-tier evidence  
**Review status:** internal review only; external peer review not performed  
**Model release:** none  
**Evaluator release:** none qualified by this study  
**Report licence:** CC BY 4.0  
**Build-script licence:** Apache-2.0

This package contains the complete public release candidate for Vinci Technical Report No. 3. It reports a negative reasoning-efficiency post-training result and a positive evaluator-audit result. The configured one-epoch SFT+DPO recipe did not establish a training-attributable efficiency gain. A stronger screened effect could not be attributed cleanly to trained weights after a serving-effort control. The original executable evaluator accepted trivial non-solutions; its replacement improved substantially but still failed independent qualification.

## Start here

- `report/Vinci_Technical_Report_No_3_v1.0.pdf` — archival report.
- `report/Vinci_Technical_Report_No_3.docx` — editable review copy.
- `report/Vinci_Technical_Report_No_3.html` — self-contained web copy.
- `report/Vinci_Technical_Report_No_3.md` — canonical human-readable manuscript.
- `release/CLAIMS.md` and `release/LIMITATIONS.md` — public claim boundary.
- `release/DATA_AND_PROVENANCE.md` — source bindings and derived-quantity rules.
- `release/PUBLICATION_CHECKLIST.md` — external publication actions.
- `web/` — research page, blog, newsroom, newsletter, FAQ, and launch posts.
- `arxiv/Vinci_TR3_arXiv_v1.0_source.zip` — arXiv-ready XeLaTeX source archive.

## Included

- Report in Markdown, PDF, DOCX, and self-contained HTML.
- Six reproducible scientific figures in PNG, SVG, and vector PDF.
- Two social cards and one launch-banner image.
- Machine-readable headline, serving-control, evaluator, claim-disposition, and evidence-binding tables.
- Vinci Eval Integrity 0.1 in JSON and human-readable form.
- Release notes, citation files, licences, public-export policy, reproducibility guide, Zenodo metadata, arXiv metadata and upload checklist, endorsement request copy, and GitHub release copy.
- Build sources, arXiv sources, QA logs, package manifest, and SHA-256 checksums.

## Deliberately excluded

- Model weights, adapters, or a purported release candidate.
- Protected or encrypted benchmark content, hidden certification cases, custody material, or keys.
- Private raw completions, provider credentials, unredacted API responses, or unpublished per-episode traces.
- Any claim that the replacement bank is qualified, that safety was broadly preserved, or that the reported rates estimate ordinary product traffic.

## Canonical identities

- Research evidence cutoff: `7cdfb4b68b7265be7f6c7299b107ff9d924f2a2d`
- Evidence tree: `getsimpledirect/vinci-gpu-research` @ `7cdfb4b68b7265be7f6c7299b107ff9d924f2a2d`, directory `p-breve-01-r2/` (private repository; per-record blob SHAs in `data/evidence_bindings.json`)
- Intended report page: https://www.getsimpledirect.com/research/papers/runtime-pass-is-not-correctness
- Intended public repository location: https://github.com/getsimpledirect/vinci-technical-reports/tree/main/reports/tr3
- Release tag: `tr3-v1.0.0`

The ZIP SHA-256 is detached beside the archive and is intentionally not written back into the package, avoiding a circular checksum.
