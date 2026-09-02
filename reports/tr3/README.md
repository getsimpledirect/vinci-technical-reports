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

This directory contains the frozen artifacts of the published Vinci Technical Report No. 3 and a separately identified, unpublished repository-forward correction candidate. It records corrections without changing the immutable GitHub and Zenodo v1.0 release. The report describes a negative reasoning-efficiency post-training result and a positive evaluator-audit result. The configured one-epoch SFT+DPO recipe did not establish a training-attributable efficiency gain. A stronger screened effect could not be attributed cleanly to trained weights after a serving-effort control. The original executable evaluator accepted trivial non-solutions; its replacement improved substantially but still failed independent qualification.

## Start here

- `report/Vinci_Technical_Report_No_3_v1.0.pdf` — immutable historical v1.0 PDF; it retains the disclosed pre-finalization language and is not the corrected candidate.
- `report/Vinci_Technical_Report_No_3_v1.0.3-candidate.pdf` — corrected, unpublished candidate built from the canonical manuscript.
- `report/Vinci_Technical_Report_No_3.docx` — editable review copy.
- `report/Vinci_Technical_Report_No_3.html` — self-contained web copy.
- `source/report_body.md` — sole editable manuscript authority.
- `report/Vinci_Technical_Report_No_3.md` — generated human-readable copy.
- `release/CLAIMS.md` and `release/LIMITATIONS.md` — public claim boundary.
- `release/DATA_AND_PROVENANCE.md` — source bindings and derived-quantity rules.
- `release/PUBLICATION_CHECKLIST.md` — completed publication state and remaining optional actions.
- `web/` — research page, blog, newsroom, newsletter, FAQ, and launch posts.
- `arxiv/Vinci_TR3_arXiv_v1.0.3_candidate_source.zip` — corrected, deterministic arXiv source candidate; not submitted by this repair.

## Included

- Report in Markdown, PDF, DOCX, and self-contained HTML.
- Six reproducible scientific figures in PNG, SVG, and vector PDF.
- Two social cards and one launch-banner image.
- Machine-readable headline, serving-control, evaluator, claim-disposition, and evidence-binding tables.
- Vinci Eval Integrity 0.1 in JSON and human-readable form.
- Release notes, citation files, licences, public-export policy, reproducibility guide, Zenodo metadata, arXiv metadata and upload checklist, endorsement request copy, and GitHub release copy.
- Build sources, arXiv sources, package manifest, and SHA-256 checksums.

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

Package revision 1.0.3 corrects the repository-forward manuscript and package authority; it is not a new publication. The historical v1.0 PDF is preserved byte-for-byte and its known semantic divergence is recorded rather than concealed. Run `bash source/rebuild_all.sh --check` to verify both identities, or `bash source/rebuild_all.sh --write` to regenerate the corrected derivatives, candidate PDF, and inventories. Neither mode publishes, tags, uploads, or creates a Zenodo version.
