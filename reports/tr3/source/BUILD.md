# Build

From the package root:

```sh
bash source/rebuild_all.sh --check
```

`source/report_body.md` is the sole editable manuscript. `--check` rebuilds Markdown, HTML, DOCX, arXiv Markdown, TeX, and the arXiv ZIP in a temporary directory, then proves that the committed derivatives match. It also verifies the accepted PDF by its recorded SHA-256, page count, extracted semantic contract, fonts, and links. The PDF is never overwritten.

Use `bash source/rebuild_all.sh --write` after intentionally changing the canonical manuscript. It replaces only generated editable derivatives and inventories. It does not need private task content or raw model outputs, and it cannot publish, tag, upload, create a Zenodo version, or replace the accepted PDF.

Rebuilding the PDF is a separate, explicit future-edition action. A changed PDF must receive a new recorded digest, a visual review, and a documented explanation; this repair does none of those things.
