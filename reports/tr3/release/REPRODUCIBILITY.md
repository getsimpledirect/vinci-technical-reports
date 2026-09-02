# Reproducibility Guide

## Rebuild the public package

From the package root:

```sh
bash source/rebuild_all.sh
```

The portable rebuild path uses only included public sources and expects Python 3, Matplotlib, Pandoc, XeLaTeX, and python-docx. `source/build_release_reference.py` preserves the complete environment-specific package assembly for audit.

The release can reproduce:

- the six scientific figures in PNG, SVG, and PDF;
- the PDF, DOCX, HTML, and Markdown report surfaces;
- the machine-readable aggregate data tables;
- the arXiv source ZIP and local preview;
- the package manifest and SHA-256 checksums.

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
