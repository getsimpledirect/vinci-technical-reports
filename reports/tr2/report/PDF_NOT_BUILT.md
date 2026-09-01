# The archival PDF is not in this commit

`report/Vinci_Technical_Report_No_2.pdf` was deliberately removed rather than carried
forward. The file present at version 0.9 (md5 `fc68060eea31eda44fc54d1631144af4`) is the
draft: it carries "Version 0.9 - publication draft" on its title block and the old
Appendix D. Shipping it beside version 1.0 sources would invite exactly the substitution
this release is trying to avoid.

Build it from these sources with step 2 of `source/BUILD.md`. That step now passes
`autolink_bare_uris` to pandoc, which is what makes the reference URLs, the DOI, and the
report URL clickable — the template already configures `hyperref`, but pandoc was never
producing links for it to style.

Delete this file once the PDF is built.
