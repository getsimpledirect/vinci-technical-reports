# Build

From the package root:

```sh
bash source/rebuild_all.sh --check
```

`source/report_body.md` is the sole editable manuscript. `--check` rebuilds Markdown, HTML, DOCX, arXiv Markdown, TeX, the arXiv ZIP, and the separately named unpublished candidate PDF in a temporary directory, then proves that the committed derivatives match. It verifies the historical v1.0 PDF only by its frozen SHA-256, page count, and disclosed residual markers; that artifact is not claimed to satisfy the corrected semantic contract and is never overwritten.

Use `bash source/rebuild_all.sh --write` after intentionally changing the canonical manuscript. It replaces only corrected generated derivatives, the unpublished candidate PDF, and inventories. It does not need private task content or raw model outputs, and it cannot publish, tag, upload, create a Zenodo version, or replace the historical v1.0 PDF.

Rebuilding the PDF is a separate, explicit future-edition action. A changed PDF must receive a new recorded digest, a visual review, and a documented explanation; this repair does none of those things.
