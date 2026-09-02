# Packaging correction v1.0.2

This revision carries three editorial corrections to the report text and rebuilds every
derived artifact around the redesigned PDF. No reported scientific value, claim
disposition, figure, or table changed.

## Report text

- **Funding disclosure restored.** v1.0.1 shipped an unfilled template instruction
  ("FUNDING DISCLOSURE REQUIRED: state whether…") in place of a disclosure. The
  instruction is removed and replaced with a statement of fact: the study used
  company-controlled compute funded by SimpleDirect, no external funding was received,
  and no funder had any role in study design, analysis, interpretation, or the decision
  to publish. The section heading again reads "Competing Interests, Funding, and AI
  Assistance".
- **Appendix E replaced.** It previously read "The report should not receive a DOI until
  every item below is closed" above 24 unchecked items, two of which require an
  independent external reviewer and were not performed. Publishing over that text would
  have falsified the report's own stated precondition. It is replaced by "Appendix E.
  Release preconditions", which states what was closed and states plainly what was not
  performed. Nothing is claimed closed that is not.
- **Appendix A.** "This appendix is intended to become machine-checked before
  publication" became "This appendix will be machine-checked in a successor version" —
  the same class of defect, a precondition that publication would falsify.
- A residual drafting instruction in the AI-assistance paragraph ("Other model providers
  should be added if…") is removed.

## Artifacts

- `report/Vinci_Technical_Report_No_3_v1.0.pdf` is the redesigned edition, promised by
  the v1.0 README but absent from every earlier package.
- HTML and DOCX are regenerated from the corrected source. The v1.0.1 DOCX embedded
  **no figures**: its build resolved image paths from the package root, where the
  source's `../figures/` references do not exist, and pandoc only warns. Both formats
  now carry all six.
- `MANIFEST.json` and `CHECKSUMS.sha256` regenerated. `.DS_Store` removed.
- Citation files and Zenodo metadata carry the reserved DOI 10.5281/zenodo.22241477.

## Text-layer note

The redesigned PDF's first build set Inter as the sans face. Inter maps its
case-sensitive punctuation alternates into the Unicode Private Use Area, so the page
rendered correctly while extraction lost characters: `Qwen3.8-27B` came out
`Qwen3.827B`, `P-BREVE-01` came out `PBREVE01`, and the signed headline metrics
`-10.9% / +4.9%` lost both signs. The accepted build sets
`\setsansfont{Inter}[RawFeature={-calt,-case}]` and contains zero private-use code
points. Extracted text is what indexers, screen readers and citation managers receive,
so this was corrected before release rather than after.

This correction does not close any item listed as not performed in Appendix E.
