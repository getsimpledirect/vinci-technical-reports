# TR2 v1.0 — Release Runbook

Steps 4 and 5 cannot be undone. Everything before them is reversible.

## State going in

| | |
|---|---|
| Candidate | `reports/tr2/`, this repo |
| Authors | George Pu, Ayush Naik — confirmed 1 Sep 2026, 14:28 ET |
| Claim review | Vikas Grover — internal claim review, not an external audit |
| DOI | `10.5281/zenodo.22236690` — reserved, record still draft |
| Report URL | https://www.getsimpledirect.com/research/papers/character-transfer-across-three-model-families |
| Release tag | `tr-2026-02-v1.0.0` — not yet created |
| Repo | private, no tags |

## 1. Build the PDF — your team

Two commands from `reports/tr2/source/BUILD.md`. Any current XeLaTeX with the ten listed
packages and the Liberation and DejaVu font families. Then set the pin in BUILD.md to the
distribution actually used.

## 2. Assemble — reversible

```sh
./scripts/assemble_release.sh /path/to/Vinci_Technical_Report_No_2.pdf
```

Verifies the PDF is v1.0 and not the draft, installs it, removes the placeholder,
regenerates the manifest **last**, proves it covers the tree, and builds
`dist/…-public.zip` plus its detached `.sha256`. Commit the result.

## 3. Stage the Zenodo record — reversible

Replace the staged v0.9 PDF (md5 `fc68060eea31eda44fc54d1631144af4`) with the v1.0 PDF and
add the ZIP. Confirm the description carries the six-clause scope line. **Do not publish yet.**

## 4. Publish Zenodo — IRREVERSIBLE

Files become immutable; the DOI goes live. A published record can gain a new version but
never lose or replace a file. Before clicking: the PDF title block reads Version 1.0, and
Appendix D reads "Outstanding Evidence Work".

## 5. Flip the repository public — IRREVERSIBLE

```sh
gh repo edit getsimpledirect/vinci-technical-reports \
    --visibility public --accept-visibility-change-consequences
```

This publishes the **entire history**, not the current tree — every commit, branch, draft
release and issue. Review `git log` first.

## 6. Tag and attach — reversible

```sh
git tag -a tr-2026-02-v1.0.0 -m "Technical Report No. 2, version 1.0"
git push origin tr-2026-02-v1.0.0
gh release create tr-2026-02-v1.0.0 \
    dist/Vinci-TR2-Character-Transfer-v1.0-public.zip \
    dist/Vinci-TR2-Character-Transfer-v1.0-public.zip.sha256 \
    --notes-file GITHUB_RELEASE_NOTES.md
```

## 7. Site and launch

Publish the report page at the URL above using `reports/tr2/web/research_page_copy.md` and
`FAQ.md`. Launch copy is in `web/launch_copy.md` — **append the six-clause scope line to any
block published on its own.** Thread item 3 was rewritten to survive being quoted alone;
check the other six variants the same way before posting.

## 8. Report No. 1

Add the dated follow-up notice from `reports/tr1/FOLLOWUP_NOTICE.md` to **three** surfaces:
the Report No. 1 page, the existing Prova model cards, and the launch blog post at
`/blog/we-tested-whether-character-training-transfers-across-model-lineages-it-did`. The
checklist names only the first two. That post's body is correctly hedged, but its headline
— "We tested whether character training transfers across model lineages. It did." — is what
circulates, and it reads as the opposite of the newer finding. Put the notice above the body.
Do not change the slug; inbound links depend on it. Do not label Report No. 1 retracted — the follow-up
narrows the generalization; the original measurements are unchanged.

## What ships undischarged

Checklist blockers A2, A3 and A4 were not met, by decision on 1 September. They are disclosed
in Appendix D. Do not describe this bundle as a complete reproducibility package, and do not
say the tables were regenerated from the frozen artifacts — they were not.
