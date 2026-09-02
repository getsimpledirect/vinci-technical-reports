# Vinci Eval Integrity 0.1

Any FAIL or UNVERIFIED check blocks qualified-evaluator language for model selection, optimization, release, or product claims.

## VEI-1 — Identity and statistical independence

- exact artifact/model/authority identities
- semantic-family or cluster metadata
- declared independent unit

Required record fields: `status`, `owner`, `evidence_digest`, `checked_at`, `failure_condition`, and `limitations`.

## VEI-2 — Contract clarity

- prompt-test-reference agreement
- blind independent implementation where applicable
- scored edge cases stated in contract

Required record fields: `status`, `owner`, `evidence_digest`, `checked_at`, `failure_condition`, and `limitations`.

## VEI-3 — Runtime/certification separation

- visible runtime channel used only for repair/retry
- protected score channel not exposed to policy
- separate digests and loaders

Required record fields: `status`, `owner`, `evidence_digest`, `checked_at`, `failure_condition`, and `limitations`.

## VEI-4 — Bidirectional discrimination

- independent wrong-program population
- valid-alternative population
- positive and negative controls

Required record fields: `status`, `owner`, `evidence_digest`, `checked_at`, `failure_condition`, and `limitations`.

## VEI-5 — Estimand, censoring, and retention integrity

- cap exhaustion kept in denominator
- raw completions retained before scoring
- task/family weighting explicit
- adaptive sampling excluded from pooled yield

Required record fields: `status`, `owner`, `evidence_digest`, `checked_at`, `failure_condition`, and `limitations`.

## VEI-6 — Production-path and authority binding

- production selection path exercised
- executed authority digest equals provenance
- fail-closed on missing/mixed identity

Required record fields: `status`, `owner`, `evidence_digest`, `checked_at`, `failure_condition`, and `limitations`.

## VEI-7 — Exact-procedure power and independent requalification

- power simulated against full decision procedure
- cluster variance measured
- post-repair population built by a different method

Required record fields: `status`, `owner`, `evidence_digest`, `checked_at`, `failure_condition`, and `limitations`.
