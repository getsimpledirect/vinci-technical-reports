# Claims and Public Wording

This file is the release-level claim control. When another document conflicts with it, narrow the wording rather than expanding the claim.

## Supported claims

### Development-tier UAR direction

**Evidence:** C3 UAR was lower than C0 UAR in all three families under Judge A and Judge B on the 200-prompt validation split.

**Permitted wording:**

> The frozen intervention reduced unsupported assertions on this validation benchmark in all three tested families under both judges.

### Complete bar not met

**Evidence:** ACC loss exceeded the 3-point limit in every family under both judges; answer coverage also violated its limit under Judge B.

**Permitted wording:**

> No family met the pre-registered development-tier utility-preservation bar.

### Refusal did not explain most Judge-B UAR improvement

**Evidence:** 66-87% of the raw UAR gain remained after removing generic-refusal items from both paired arms.

**Permitted wording:**

> Most of the Judge-B-measured UAR gain survived the generic-refusal adjustment.

### Family heterogeneity

**Evidence:** Adjusted ACC loss per adjusted UAR point gained was approximately 2.94 for Ministral, 0.67 for OLMo, and 3.03 for Qwen.

**Permitted wording:**

> OLMo produced the least damaging measured frontier and motivates a targeted successor experiment.

### Judge repeatability risk

**Evidence:** Two nominally identical judging executions produced materially different AC1 estimates and changed gate status; the earlier run was void for inadequate provenance.

**Permitted wording:**

> The study exposed a material judge-repeatability risk that the frozen inter-judge reliability gate did not measure.

## Required qualifiers

Every public summary must make clear that:

- results are development-tier and use the validation split;
- the primary-test holdout is untouched;
- the refusal adjustment is Judge-B-only;
- capability preservation was not evaluated;
- no external audit was performed;
- no model checkpoint is recommended for release.

## Unsupported or forbidden claims

Do not state or imply:

- “Character transfer succeeded across three model families.”
- “The models became more truthful.”
- “Factual knowledge improved.”
- “The intervention preserved capability.”
- “The primary holdout passed.”
- “The result was externally or independently validated.”
- “OLMo passed” or “OLMo is the winning release.”
- “The study proves universal portability.”
- “The reported rates measure real-world hallucination prevalence.”
- “G1 PASS means the intervention passed.”

## Recommended headline

> We tested one frozen character recipe across three model families. It reduced unsupported assertions, but no family preserved grounded-answer accuracy well enough to meet the pre-registered bar.
