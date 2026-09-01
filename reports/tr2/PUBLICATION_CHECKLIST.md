# Publication Checklist - Technical Report No. 2

This checklist separates work required to publish the development-tier result from optional follow-up research. Do not hold the report hostage to new experiments, and do not use new experiments to rewrite what the completed bank showed.

## A. Release blockers for version 1.0

- [ ] **Correct the exchange-rate unit in the source record.** The internal readout labelled approximately `0.3`, `1.5`, and `0.3` as ACC loss per UAR gain. Those values were the reciprocal. The cost-oriented ratios are approximately `2.94`, `0.67`, and `3.03` for Ministral, OLMo, and Qwen.
- [ ] **Regenerate every public result table from frozen scored artifacts.** Do not hand-transcribe from the manuscript. Compare generated CSVs byte-for-byte or field-for-field with the report tables.
- [ ] **Export the public evidence set through an allowlist.** Include sanitized item-level labels, exclusions, artifact bindings, analysis locks, and judge-call metadata. Exclude response bodies where rights or privacy are unresolved.
- [ ] **Run the public bundle from a clean environment.** Recompute the aggregate tables and figures and verify all reported fields.
- [ ] **Complete benchmark-item rights review.** Record the source, licence, redistribution status, and redaction decision for every public item.
- [ ] **Confirm authorship.** George Pu and Ayush Naik must confirm author order and the exact CRediT statement.
- [ ] **Assign immutable publication identifiers.** Fill `https://vinci.getsimpledirect.com/research/character-transfer-across-three-model-families`, `https://doi.org/10.5281/zenodo.22236690`, `tr-2026-02-v1.0.0`, publication source commit, and final package SHA-256.
- [ ] **Run independent claim review.** Review the PDF, DOCX, HTML, release notes, research-page copy, FAQ, Report No. 1 notice, and launch copy against `release/CLAIMS.md`.
- [ ] **Run security and privacy review.** Prove that holdout material, keys, credentials, private response text, session transcripts, and internal-only paths are absent.
- [ ] **Update Technical Report No. 1 and the existing Prova model cards.** Add the dated follow-up notice without changing the original measurements.

## B. Mechanical QA

- [ ] PDF renders cleanly in at least one independent renderer.
- [ ] DOCX renders cleanly in LibreOffice and remains editable.
- [ ] HTML opens offline with all figures embedded.
- [ ] All CSV files parse with a strict reader and have stable column order.
- [ ] All JSON files parse and validate against any declared schema.
- [ ] `checksums.sha256` verifies from the package root.
- [ ] No placeholder remains except explicitly permitted public URLs and identifiers.
- [ ] No result table contains pooled judge averages or a consensus delta.
- [ ] Every mention of capability preservation says **not evaluated**, never passed.
- [ ] Every mention of the primary holdout says **untouched** or **sealed**, never passed.

## C. Publication decisions George must explicitly confirm

- [ ] Final title and subtitle.
- [ ] Release date.
- [ ] Whether the report/figures use CC BY 4.0.
- [ ] Whether accompanying code uses Apache 2.0.
- [ ] Whether the validation benchmark is published now, later, or under controlled access after rights review.
- [ ] Whether the public package includes sanitized judge-call response hashes only or additional response metadata.
- [ ] Whether a fresh external audit is commissioned for a future blinded set.

## D. Optional follow-up work - not blockers for this report

- Capability-preservation benchmarks may be run as **post-result supplementary analysis**. They cannot retroactively become a pre-registered criterion-five pass, and the fifth benchmark cannot be selected after results and described as confirmatory.
- McNemar contrasts may be computed as supplementary analysis. They cannot change the frozen development-tier verdict.
- A judge-repeatability study should be prospectively frozen for G1-vNext.
- A successor OLMo experiment should optimize answer preservation explicitly and require fresh compute authorization.
- The primary-test holdout should remain sealed until a pre-registered candidate exists whose outcome could change a decision.

## E. Release command gate

Publish only when sections A, B, and the required decisions in C are complete. Optional work in D belongs to successor programs or clearly labelled supplements.
