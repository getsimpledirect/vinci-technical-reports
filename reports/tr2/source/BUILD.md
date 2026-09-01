# Build Instructions

The package uses a small, auditable toolchain:

Pin these exact versions. Figure output is sensitive to the plotting and font stack.

| Component | Pinned version |
|---|---|
| Python | 3.11.x |
| matplotlib | 3.10.8 |
| numpy | 2.5.2 |
| pandas | 2.2.x |
| python-docx | 1.1.x |
| Pandoc | 3.x |
| XeLaTeX | TeX Live 2024 |

XeLaTeX also needs `fontspec`, `microtype`, `booktabs`, `tabularx`, `caption`, `hyperref`,
`fancyhdr`, `titlesec`, `enumitem`, and `seqsplit`, plus the Liberation Serif, Liberation
Sans, and DejaVu Sans Mono font families. LibreOffice is used for DOCX render QA only.

## 1. Regenerate figures and machine-readable tables

From the package root:

```sh
python source/build_figures_and_tables.py
```

This writes figures to `figures/` and aggregate tables to `tables/`.

## 2. Build the archival PDF

```sh
python source/make_pdf_source.py
cd source/latex
pandoc Vinci_Technical_Report_No_2_pdf.md \
  --from=markdown+raw_tex+autolink_bare_uris \
  --to=latex \
  --shift-heading-level-by=-1 \
  --template=vinci_tr2_template.tex \
  --standalone \
  -o Vinci_Technical_Report_No_2.tex
xelatex -interaction=nonstopmode -halt-on-error Vinci_Technical_Report_No_2.tex
xelatex -interaction=nonstopmode -halt-on-error Vinci_Technical_Report_No_2.tex
cp Vinci_Technical_Report_No_2.pdf ../../report/Vinci_Technical_Report_No_2.pdf
```

Render and inspect with any standards-compliant PDF renderer. For example, with Poppler:

```sh
mkdir -p /tmp/vinci-tr2-pdf-render
pdftoppm -png -r 200 \
  report/Vinci_Technical_Report_No_2.pdf \
  /tmp/vinci-tr2-pdf-render/page
```

## 3. Build the editable DOCX

Create the Pandoc intermediate from the Markdown body, then style it:

```sh
pandoc source/Vinci_Technical_Report_No_2_docx.md \
  --from=markdown+autolink_bare_uris \
  --resource-path=. \
  -o report/Vinci_Technical_Report_No_2_unstyled.docx
python source/style_docx.py
```

Render and inspect every page. One portable route is LibreOffice followed by Poppler:

```sh
mkdir -p /tmp/vinci-tr2-docx-render
libreoffice --headless --convert-to pdf \
  --outdir /tmp/vinci-tr2-docx-render \
  report/Vinci_Technical_Report_No_2.docx
pdftoppm -png -r 160 \
  /tmp/vinci-tr2-docx-render/Vinci_Technical_Report_No_2.pdf \
  /tmp/vinci-tr2-docx-render/page
```

The unstyled DOCX is an intermediate and should not be included in the final release bundle.

## 4. Build self-contained HTML

```sh
python source/make_html_source.py
pandoc source/Vinci_Technical_Report_No_2_html.md \
  --from=markdown+raw_html+autolink_bare_uris \
  --to=html5 \
  --standalone \
  --toc --toc-depth=3 \
  --metadata title='Character Transfer Across Three Model Families' \
  --metadata author='George Pu; Ayush Naik' \
  --metadata date='1 September 2026' \
  --css=source/vinci_report.css \
  --resource-path=. \
  --embed-resources \
  -o report/Vinci_Technical_Report_No_2.html
```

## 5. Build manifest and checksums

```sh
python source/build_manifest.py
sha256sum -c checksums.sha256
```

## Reproducibility boundary

These commands reproduce the publication artifacts from the package sources. They do not
independently recompute the scientific results: `build_figures_and_tables.py` carries the
analysis values as literals and reads no scored artifact. Regenerating the tables therefore
demonstrates stable transcription, not correspondence to the frozen evidence. See Appendix D
of the report.

**What reproduces byte-for-byte.** The machine-readable tables in `tables/` reproduce
byte-identically under the pinned environment above.

**What does not.** Figures reproduce from the same source data and plotting code, but byte
identity is not guaranteed across matplotlib or FreeType versions. Text metrics under
`bbox_inches="tight"` change the output canvas by fractions of a point, which changes the
file without changing the plotted data. Compare figures visually, not by hash.
