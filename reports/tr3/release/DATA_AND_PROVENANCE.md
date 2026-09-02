# Data and Provenance

## Research cutoff

The report is bound to the research-record commit `7cdfb4b68b7265be7f6c7299b107ff9d924f2a2d`. This is the evidence cutoff used for claim `.015`, the serving-control correction, the original evaluator audit, the replacement qualification audit, and the blind mutation population.

The publication source is this release package. Do not insert the package build hash into an execution field: many original execution records have their own content-addressed identities and some did not record a Git commit.

## Direct values and derived quantities

Every public ratio must preserve its numerator, denominator, unit, and derivation:

| Rendering | Numerator | Denominator | Derivation |
|---|---:|---:|---|
| `154/322` | runtime-passing broad shortcuts | broad-shortcut population | `154 / 322` |
| `7/157` | near-miss plus partial certification false accepts | near-miss plus partial probes | `(4 + 3) / (121 + 36)` |
| `52/1,862` | wrong mutants accepted by certification | provably wrong mutants admitted | `52 / 1,862` |
| `19/40 AST-leak` | tasks with at least one AST mutant passing | protected tasks | `19 / 40` |
| `21/40 AST-no-leak` | tasks with no detected AST leak | protected tasks | `(40 − 19) / 40` |
| `at least 21/40 known-flaw union` | seven previously identified plus fourteen newly adjudicated outside that set | protected tasks | `(7 + 14) / 40` |

The two `21/40` quantities have opposite polarity and different constructions. Neither may appear without its qualifier.

## Source bindings

See `data/evidence_bindings.csv` and `.json` for exact paths, the cutoff commit, immutable blob SHAs, and stable commit URLs.

## Public reproduction boundary

This package reproduces the manuscript, figures, public aggregate tables, source archives, and checksums from included files. It does not independently re-run the private model episodes or disclose protected benchmark content. Reproduction must fail closed if a source hash, numerator, denominator, unit, or direction convention differs from the manifest.
