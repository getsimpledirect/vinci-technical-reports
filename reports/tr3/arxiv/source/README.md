# arXiv source

Generated from `source/report_body.md`. Compile with two XeLaTeX passes:

```sh
xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
```

The archive is self-contained and requires no shell escape or external downloads.
