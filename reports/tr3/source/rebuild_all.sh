#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
python3 source/build_figures.py
(
  cd arxiv/source
  xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
  xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
  cp main.pdf ../../report/Vinci_Technical_Report_No_3_v1.0.pdf
)
pandoc source/report_body.md --from=gfm+yaml_metadata_block --standalone --toc --toc-depth=3 --css source/report.css --embed-resources --resource-path . -o report/Vinci_Technical_Report_No_3.html
pandoc source/report_body.md --from=gfm+yaml_metadata_block --reference-doc source/reference.docx --resource-path . --toc --toc-depth=3 -o report/Vinci_Technical_Report_No_3.docx
printf 'Rebuilt public figures and report formats. Regenerate MANIFEST.json and CHECKSUMS.sha256 before release.\n'
