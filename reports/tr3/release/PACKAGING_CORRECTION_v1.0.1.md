# Packaging correction v1.0.1

This packaging-only correction makes no change to the reported scientific values or claim dispositions.

It:

- adds the main PDF that was inadvertently omitted from the v1.0 full-package ZIP;
- repairs the conditional-probability table row so `P(certification pass given runtime pass)` remains one cell across Markdown, HTML, DOCX, PDF, and arXiv source;
- constrains PDF table widths so wide results and appendix tables wrap within the page;
- adds a complete `main.tex` and required figure assets to the arXiv source; and
- regenerates the package manifest and SHA-256 inventory.

The verified PDF is the publication-layout authority. The DOCX remains an editable source whose pagination can vary by Word-compatible renderer.

This correction does not clear any unchecked item in `PUBLICATION_CHECKLIST.md`. In particular, account-side publication, final funding disclosure, exact-artifact approval, and external-review decisions remain separate release actions.
