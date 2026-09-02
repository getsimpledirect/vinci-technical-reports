# Reproducibility Guide

## What the package can and cannot rebuild

The package has one editable manuscript, `source/report_body.md`, and one builder, `source/package_release.py`, driven by `source/rebuild_all.sh`. From the package root:

```sh
bash source/rebuild_all.sh --check   # rebuild in a temporary directory; prove the committed derivatives match
bash source/rebuild_all.sh --write   # regenerate the committed derivatives after an intentional manuscript change
```

Both modes regenerate, from `source/report_body.md` and the committed frozen figures:

- `report/Vinci_Technical_Report_No_3.md`, `.html` (self-contained), and `.docx`;
- `arxiv/source/body.md`, `main.tex`, `README.md`, `00README.json`, and the arXiv source ZIP named in `release.conf`;
- the compiled arXiv PDF, committed as the separately named unpublished candidate `report/Vinci_Technical_Report_No_3_v1.0.3-candidate.pdf`;
- `release/Vinci_TR3_PACKAGE_RECEIPT_v1.0.3.json`, `MANIFEST.json`, and `CHECKSUMS.sha256` (`--write` only).

Neither mode regenerates:

- **the six figures.** `figures/` holds frozen PNG, SVG, and PDF files that the builder copies as-is (the PNGs into the arXiv source). `source/build_figures.py` is retained as the record of how they were produced from the frozen result set; it needs NumPy and Matplotlib, is not invoked by the rebuild, and regenerating the figures is not part of the verified path. Byte identity of regenerated figures is not claimed.
- **the machine-readable tables** in `data/`. They are committed inputs, covered by the inventories, not outputs.
- **the historical v1.0 PDF** `report/Vinci_Technical_Report_No_3_v1.0.pdf`. It is the immutable published artifact and is not derivable from the canonical manuscript. The builder verifies it only by its frozen SHA-256 `054a4077193a797e8105224e710b0fc78741eb3f465ce1f994d9a1e960a32e1d`, its 43-page count, and the disclosed residual markers listed in `release/SEMANTIC_CONTRACT.json` and `release/HISTORICAL_V1_PDF_DIVERGENCE.json`; it never writes to it. No reproducibility claim is made for that file.

The builder has no network, upload, tag, release, Zenodo, or arXiv operation.

## Toolchain

The rebuild needs, on `PATH`:

| Tool | Requirement | How it is enforced |
|---|---|---|
| Python 3 | standard library only | — |
| Pandoc | exactly 3.10 | `package_release.py` refuses any other version |
| TeX engine | XeLaTeX if present, otherwise Tectonic | selected at run time; **engine and version are not pinned and not recorded** |
| Poppler | `pdftotext`, `pdfinfo` | required for the semantic, page-count, and page-bounds gates |

`release/Vinci_TR3_PACKAGE_RECEIPT_v1.0.3.json` records the renderer (`pandoc 3.10`) and the SHA-256 of every derivative, but not the TeX engine that compiled the candidate PDF. Markdown, HTML, DOCX, and TeX derivatives depend only on Pandoc 3.10 and are expected to match across hosts. The candidate PDF and the receipt, manifest, and checksum rows that name it depend on the TeX engine, its version, and its font and package sources; a different engine can produce a different candidate PDF digest, which `--check` reports as a stale artifact rather than silently accepting.

Recorded observation, not a portability claim: on 2026-09-02 the committed derivatives at this revision, including the candidate PDF (SHA-256 `0cccfa2716af7d77cb14754182076d55cd2ac6c3a648a1453beab8dbb11df2a2`), were reproduced offline on one macOS host running Pandoc 3.10, Tectonic 0.17.0, and Poppler 26.07.0 from a pre-populated Tectonic bundle cache. That is one host with one cache; it does not establish byte reproducibility on other hosts or with XeLaTeX. The historical v1.0 PDF was produced by the earlier XeLaTeX-based v1.0/v1.0.1 build recorded in `release/Vinci_TR3_BUILD_RECEIPT_v1.0.1.json`, outside this builder.

## Assembling the distributable package

From the repository root:

```sh
scripts/assemble_release.sh tr3 reports/tr3/report/Vinci_Technical_Report_No_3_v1.0.3-candidate.pdf
```

The script checks the supplied PDF against `ASSEMBLY_PDF_SHA256` in `release.conf` and the text, private-use, link-target, and font gates; runs `rebuild_all.sh --write`; re-checks that the PDF the rebuild left in the tree still carries the gated digest (refusing, with no archive written, if the manuscript has drifted from the approved candidate); proves the manifest covers the tree; and writes a deterministic ZIP plus detached checksum under `dist/`. It publishes nothing.

## Scientific recomputation boundary

The public package does not contain protected task text, hidden certification cases, private raw outputs, or provider credentials. It therefore cannot regenerate the original model completions or independently rerun the private graders. It can verify that every published aggregate is bound to an exact source document and derivation.

## Fail-closed rules

A rebuild or public audit must stop if:

- the evidence cutoff or any bound blob SHA differs;
- a ratio is reported without its numerator and denominator;
- the reasoning-reduction sign convention changes;
- one-epoch −10.9% is confused with two-epoch +10.9%;
- either `21/40` appears without `AST-no-leak` or `cross-method known-flaw union`;
- claim `.015` is absent from the frozen registry snapshot;
- an additional scholarly author appears;
- any protected content or credential enters the export.
