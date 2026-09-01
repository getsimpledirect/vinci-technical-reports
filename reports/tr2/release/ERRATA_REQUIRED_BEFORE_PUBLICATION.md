# Errata Applied

## E1 - Exchange-rate unit label

**Status:** corrected in the manuscript and package tables. The source research record still requires the same correction; see Appendix D.

The internal readout labelled approximately `0.3`, `1.5`, and `0.3` as “ACC points lost per UAR point gained.” The values were calculated as UAR gain divided by ACC loss, the reciprocal of the label.

The cost-oriented ratios used in this package are:

| Family | Adjusted ACC loss | Adjusted UAR gain | ACC loss per UAR gain |
|---|---:|---:|---:|
| Ministral 3 8B | 41.8 | 14.2 | 2.94 |
| OLMo 3 7B | 11.8 | 17.7 | 0.67 |
| Qwen3 8B | 19.7 | 6.5 | 3.03 |

The correction does not change the ordering or the pivot decision. It changes the stated unit and prevents the prose from asserting the inverse arithmetic.

## E2 - Mechanism wording

Avoid “the mechanism works.” The bank shows that the intervention moved the measured response-policy frontier. It does not isolate a causal mechanism.

Use:

> The frozen intervention reduced unsupported assertions across the tested families, but the complete utility-preservation bar was not met.

## E3 - Public bundle completeness

**This guard remains in force at version 1.0.** The release includes aggregate tables only. Do not describe it as a complete reproducibility bundle until sanitized item-level scored outputs, exclusions, analysis locks, artifact bindings, and judge ledgers are exported directly from the private repository.

## E4 - Authorship

Author order and the CRediT statement were confirmed by both named authors on 1 September 2026.

## E5 - Licensing

The report, figures, code, benchmark items, and judge metadata do not automatically share one licence. Assign licences only after artifact-class and per-item rights review.

## E6 - Stale generated LaTeX in the published archive

**Status:** present in the published version 1.0 archive; corrected in the repository after
publication. The archive itself is immutable and was not altered.

`source/latex/Vinci_Technical_Report_No_2.tex` is generated from
`Vinci_Technical_Report_No_2_pdf.md` by the Pandoc command in `source/BUILD.md`. The copy
inside the published archive is the version 0.9 generation: it reads "Version 0.9", carries
"publication draft" and the pre-1.0 authorship sentence, and titles Appendix D "Publication
Corrections Required Before Version 1.0".

It contradicts every other artifact in the same archive. The Markdown, HTML, DOCX and PDF are
all version 1.0 and agree with each other.

**Why it survived.** The file is a build intermediate, so version sweeps excluded it on the
reasoning that the build regenerates it. It was regenerated — on the machine that produced the
archival PDF, and never returned to the repository. `checksums.sha256` covers it, so the
package verifies as internally consistent: a checksum establishes that a file is unmodified,
not that it is correct.

**Effect.** None on any rendering a reader opens. It misleads only someone rebuilding from
`source/`, who would produce a version 0.9 title block from a version 1.0 package.

**Correction.** Regenerated in the repository from the canonical Markdown. The published
archive and its DOI are unchanged; see the divergence note in the top-level README.
