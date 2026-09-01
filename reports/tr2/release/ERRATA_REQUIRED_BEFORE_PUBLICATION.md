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
