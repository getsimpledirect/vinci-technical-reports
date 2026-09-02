# Repository-forward packaging correction v1.0.3

This correction does not change the published scientific report, its reported metrics, its figures, its claim dispositions, or the immutable GitHub and Zenodo v1.0 records. The accepted 43-page PDF remains byte-identical at SHA-256 `054a4077193a797e8105224e710b0fc78741eb3f465ce1f994d9a1e960a32e1d`.

It repairs the repository and any future source package:

- `source/report_body.md` is the sole editable manuscript authority. Markdown, HTML, DOCX, arXiv Markdown, arXiv TeX, and the arXiv ZIP are generated from it.
- A residual unresolved-draft paragraph is removed from Markdown, HTML, and DOCX so they match the accepted PDF's final state.
- Stale parallel TeX and the v1.0.1 arXiv archive are replaced. The corrected arXiv archive contains the final funding disclosure, release-precondition language, all six figures, `main.tex`, and `00README.json`; it compiles without text outside the page boundary.
- The deterministic builder cannot overwrite the accepted PDF and has no network publication, upload, tag, release, or Zenodo-version operation.
- `MANIFEST.json` now has one report version, one package revision, one file count, explicit exclusions, and exact coverage. `CHECKSUMS.sha256` covers every payload plus the manifest.
- The publication checklist now records what is already public and keeps the optional arXiv submission as an unperformed future decision.
- Zenodo staging metadata is report-owned rather than hard-coded for Report No. 2. TR3 has no active draft deposition, so staging refuses before reading a token or issuing a request.

The earlier package remains independently verifiable against its own inventory. This repository-forward correction records its divergence rather than attempting to rewrite it.
