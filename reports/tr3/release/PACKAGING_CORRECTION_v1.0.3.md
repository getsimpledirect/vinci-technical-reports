# Repository-forward packaging correction v1.0.3

This correction does not change the published scientific record, its reported metrics, its figures, its claim dispositions, or the immutable GitHub and Zenodo v1.0 records. The historical 43-page v1.0 PDF remains byte-identical at SHA-256 `054a4077193a797e8105224e710b0fc78741eb3f465ce1f994d9a1e960a32e1d`. It retains six disclosed pre-finalization statements on pages 20, 29, 38, and 40 and is not claimed to be semantically repaired.

It repairs the repository and any future source package:

- `source/report_body.md` is the sole editable manuscript authority. Markdown, HTML, DOCX, arXiv Markdown, arXiv TeX, and the arXiv ZIP are generated from it.
- Six residual finalize-later instructions are replaced by factual, present-tense bindings in the corrected Markdown, HTML, DOCX, TeX, arXiv source, and separately named `Vinci_Technical_Report_No_3_v1.0.3-candidate.pdf`.
- Stale parallel TeX and the v1.0.1 arXiv archive are replaced. The corrected arXiv archive contains the final funding disclosure, release-precondition language, all six figures, `main.tex`, and `00README.json`; it compiles without text outside the page boundary.
- The deterministic builder cannot overwrite the historical v1.0 PDF and has no network publication, upload, tag, release, or Zenodo-version operation.
- `MANIFEST.json` now has one report version, one package revision, one file count, typed required publication fields, unique entries, explicit exclusions, and exact coverage. `CHECKSUMS.sha256` has unique rows and covers every payload plus the manifest.
- The publication checklist now records what is already public and keeps the optional arXiv submission as an unperformed future decision.
- Zenodo staging metadata is report-owned rather than hard-coded for Report No. 2. TR3 has no active draft deposition, so staging refuses before reading a token or issuing a request.

The earlier package remains independently verifiable against its own inventory. This repository-forward correction records its divergence rather than attempting to rewrite it.

The candidate and arXiv source remain unpublished. Any tag, GitHub release, Zenodo version, arXiv submission, or replacement public PDF requires a separate publication decision.
