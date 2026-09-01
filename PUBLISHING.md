# Publishing a technical report

Written after publishing Report No. 2 on 1 September 2026, from what actually went wrong.

`reports/tr2/PUBLICATION_CHECKLIST.md` is a good checklist and it was followed. Everything
below is what the checklist did not catch. Two defects still reached the published archive,
several guards passed their own tests while being wrong, and three approvals arrived before
the thing they approved existed. None of that is visible from a list of items to tick.

Read this alongside the checklist, not instead of it.

---

## The order that matters

Most steps can happen in any order. These four cannot.

**1. Check arXiv endorsement before anything else, if you intend to post there.**
It has the longest lead time by an order of magnitude — everything else is hours, this can be
days, because it depends on another person agreeing. Log in, start a submission, select the
category. You will be told immediately. Report No. 2 discovered this at the end, after
everything else was staged.

**2. Reserve the DOI before the build, not after.**
It is the only ordering constraint in the whole sequence. A DOI minted afterwards cannot go
inside the archival PDF, so the document never carries its own identifier. Zenodo reserves
ahead of publishing; do it first, hand the identifier to whoever builds.

**3. Generate the manifest and checksums LAST, and make it an invariant, not a reminder.**
Report No. 2 shipped a manifest generated before two files were added. `shasum -c` passed
anyway, because it cannot detect files it was never told about. Build order must be: finalize
every file → generate manifest → generate checksums → verify the manifest count equals the
tree → only then create the archive. A checklist line saying "regenerate at the end" is what
failed; a script that refuses to package a tree the manifest does not cover is what works.

**4. The irreversible steps go last, and there are exactly two.**
Publishing the Zenodo record and flipping the repository public. Everything before them can be
undone. Publishing makes files immutable — a record can gain a new version but can never lose
or replace a file. Flipping visibility publishes the **entire git history**, not the current
tree, so audit the history first: every blob, not just HEAD.

---

## The failure that repeats: a green check certifying the wrong property

This is the single most useful thing to carry forward.

Two defects reached the published Report No. 2 archive. Both were covered by
`checksums.sha256`, and in both cases the checksums verified.

- The manifest was stale, so two files were uncovered. Verification passed because it only
  checks the files it lists.
- `source/latex/…No_2.tex` shipped as the previous version's text. Verification passed because
  the file was unmodified since the manifest was written — which is all a checksum asserts.

**A checksum establishes that a file is unmodified. It never establishes that the file is
correct.** Before trusting any green check, ask what property it actually certifies, and
whether that is the property you care about.

The same shape appeared repeatedly:

- A rebuild reproducing the tables byte-for-byte proved the transcription was stable. It could
  not prove the numbers matched the source data, because the build script contained no data —
  every value was a literal. The rebuild was a control that could not fail on the question it
  appeared to answer.
- A test asserting a filename was present on a remote record passed whether that name held the
  new bytes or the old ones.

---

## Generated files are not exempt from review — they are the likeliest to be wrong

`source/latex/…No_2.tex` is produced by Pandoc. Every version sweep deliberately skipped it,
reasoning that the build regenerates it. The build did regenerate it — on the machine that
produced the PDF, and it never came back to the repository. The stale copy shipped.

Two rules follow:

- **Sweep every file type, not a chosen list.** The sweep that missed this filtered on
  `.md`, `.cff`, `.json`, `.csv`, `.txt`. The defect was in `.tex` and a second one in `.py`.
- **A generated file is only regenerated if the regeneration lands in the repository.**
  If someone else runs the build, the output must come back, or the source of record diverges
  from what shipped.

---

## Approvals must name the artifact they approved

Three approvals arrived before the artifact existed.

- A reviewer approved the report twice before any release candidate had been committed.
- A co-author's approval was recorded, then the manuscript changed substantively — an appendix
  rewritten, a section replaced — and the report nearly printed "both authors reviewed and
  approved the final manuscript". That sentence would have been false, permanently, under a
  DOI, about a named person.

**Record what was actually approved, and bind it to bytes.** A recorded approval should name a
commit or a checksum. When the artifact changes after approval, either re-ask or narrow the
claim to what remains true. Report No. 2 narrowed it: "Both authors confirmed the author order
and this contribution statement" — verifiable, and it does not overstate.

Review the **candidate**, not the draft. A review of the draft certifies an artifact that will
not exist at publication.

---

## Claim discipline is per-surface, not per-document

`release/CLAIMS.md` defines permitted wording, forbidden claims, and required qualifiers. The
non-obvious part is where they have to appear.

**Every surface that can be read alone needs the full scope statement.** Not the manuscript —
the manuscript is fine. The surfaces that travel: the README, the FAQ, each launch-copy block,
each follow-up notice, the citation file's abstract, the Zenodo description, the model card,
the research-index card. Report No. 2's scope sentence was missing its sixth clause at source,
so every surface that copied it inherited the gap.

**Headlines and slugs are the surfaces that travel furthest.** A carefully qualified body does
not help when search results, social previews and screenshots carry only the title. Report
No. 1's article body was correct and its headline was not; the headline is what needed
narrowing.

**Numbered social threads must survive being quoted one item at a time.** Item 3 of the launch
thread read as success on its own, corrected only by item 4.

**State the sign convention for every signed metric, once, before first use — and check
the abstract against the tables, not against the prose.**

This has now happened twice, in two reports, in the abstract both times.

- Report No. 2 labelled a column "ACC points lost per UAR point gained" over values computed
  as the reciprocal. Erratum E1.
- The Report No. 3 draft wrote "median reasoning-token **change** was -10.9%" where every
  table in the same document said **reduction**, a quantity signed so that positive means
  fewer tokens. Under "change", -10.9% reads as an improvement; under "reduction" it means
  reasoning got 10.9% longer. The body was correct throughout — one section even says
  plainly that reasoning *increased* — and only the abstract inverted it.

The mechanism is the same both times: the convention was never written down, so every table
applied it correctly and the prose was free to restate it backwards. The abstract is the
worst place for this to survive, because it is the part that gets quoted, indexed, and pasted
into submission metadata, and it is the part most likely to be rewritten by hand late.

Two checks, neither expensive:

- For every signed metric, state the direction once, before first use. One sentence: *reduction
  is signed so that a positive value means fewer tokens; a negative reduction means the quantity
  increased.*
- Verify each number in the abstract against the table or artifact it came from, not against
  the surrounding prose. Prose agreeing with prose is not a check.

Watch for magnitude collisions while you are there. The Report No. 3 draft carries -10.9% and
+10.9% for the same seed in different arms — both as measured, opposite directions, two
sections apart. Flag it in the text; do not renumber measured values to avoid the confusion.

**Watch for the mention-versus-use false positive.** An automated claim review returned ~20
blockers, most of which flagged forbidden phrases inside sentences that *prohibited* them —
"Do not say the holdout passed" flagged for saying "passed". Taken seriously, it would have
required deleting the guardrails. Check whether the phrase is being asserted or forbidden.

---

## Guards that pass their tests and fail reality

Four guards written for Report No. 2 passed their own tests and would have failed on the real
thing:

- A gate requiring `Version 1.0 - 1 September 2026`. The template prints a bullet, not a
  hyphen. It rejected the correct PDF on the first real run.
- A remote-storage check accepting a URL only if it contained a known substring. The live URL
  shape contained neither. It passed only the mock.
- A refusal that ran *after* the uploads it was meant to prevent.
- A delete-by-recorded-id that, when an upload replaced a file under the same key, deleted its
  own upload — and **exited 0**.

**Test the guard against the real artifact, not only the fixture.** Three of these were caught
by review; one was caught by running the gate against the actual delivered PDF.

**And keep a control that proves the test can still fail.** The regression suite now runs the
old, broken script and *requires* it to lose the file. When a fixture changed and the old
script started failing earlier for a different reason, that control went red and reported the
loss of coverage — while every other test stayed green.

---

## Constraints you write become indistinguishable from constraints you inherit

Three times in one day, a self-imposed constraint was escalated as though it were external:

- A pinned toolchain version, added hours earlier as reproducibility hygiene, was treated as a
  hard requirement blocking the build.
- A hold on a release candidate persisted after a later candidate had resolved it.
- An author's own outreach to his own co-author was routed through an approval queue that
  escalated it back to him.

Each was well-intentioned. The check is: **whose decision is this, and where did the
constraint come from?** Read the original document, not the current one — a pin you added
looks exactly like a pin you were given.

---

## What the archive should say about itself

- **State the evidence tier and never let a version number imply promotion.** Version 1.0 means
  the document is final. It does not mean the result was promoted.
- **Keep open items disclosed rather than deleted.** Report No. 2's Appendix D was originally
  a pre-publication correction list. It was reduced to the three items still open and retitled,
  not removed. Deleting it would have removed the disclosure while shipping a version number
  implying closure.
- **Say what reproduces and what does not.** Machine-readable tables reproduce byte-identically
  under a pinned environment; figures do not, because text metrics vary with the font and
  rendering stack. Claiming both is a claim the toolchain cannot keep.
- **When the repository later diverges from the published archive, record it.** The archive is
  immutable. Correcting forward is fine; correcting silently is the thing the immutability was
  supposed to prevent.

---

## The sequence, condensed

```
endorsement check (if posting to a preprint server)   ← longest lead time, do first
reserve DOI                                           ← must precede the build
freeze claims: CLAIMS.md, the scope sentence, every standalone surface
build → verify against the real artifact, not the fixture
regenerate manifest + checksums LAST, verify they cover the tree
package, detached checksum
co-author + reviewer sign-off ON THE CANDIDATE, bound to a commit or checksum
─────────────── everything above is reversible ───────────────
publish the archive        ← irreversible: files become immutable
flip the repository public ← irreversible: publishes the whole history
tag, release, attach assets
site page, launch copy, follow-up notices on every prior surface the result narrows
```

The last line is the one most easily forgotten. A new result that narrows an old one leaves
the old claim live everywhere it was ever stated — the earlier report, its blog post and
headline, its model cards, and any mirror you do not control.
