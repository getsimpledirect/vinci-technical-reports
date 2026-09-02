# Public Claims

## Permitted headline

> The configured P-BREVE-01-R2 SFT+DPO recipe did not establish a training-attributable reasoning-efficiency gain on Qwen3.8-27B, and the executable evaluators used in the program did not earn qualification for model selection or optimization.

## Supported, bounded statements

1. **One-epoch intervention:** reasoning reduction versus base was −10.9% at seed 1729 (longer) and +4.9% at seed 2718 (shorter), against a +20% target at both seeds. The DPO increment over SFT was −0.6% and +0.6%.
2. **Serving control:** on a screened executable-code shard, untrained base at `medium` effort sharply reduced termination failures and token consumption relative to `xhigh`. The formal matched-effort correctness comparison remained underpowered.
3. **Original evaluator:** 24/24 deliberately wrong shortcut programs passed; the nominal 80 code tasks represented eight content-distinct problems repeated ten times.
4. **Replacement evaluator:** broad shortcut discrimination improved, but 7/157 near-miss or partial programs and 52/1,862 independently generated wrong mutants still passed certification.
5. **Affected-task lower bound:** the cross-method lower bound is 7 previously identified tasks plus 14 newly adjudicated tasks outside that set, or at least 21/40 tasks with a known certification flaw. This is not the same quantity as the complementary 21/40 tasks with no detected AST leak under one population.
6. **Portfolio disposition:** no model, evaluator bank, or release candidate resulted.

## Prohibited or unsupported wording

Do not say:

- “P-BREVE improved Qwen correctness.”
- “The adapter solved overthinking.”
- “Medium effort is proven equivalent to the fine-tune.”
- “Safety was preserved.”
- “The replacement bank is qualified.”
- “Half of code tasks are wrong in production.”
- “The mutation false-accept rate estimates deployed model behaviour.”
- “P-BREVE-02 failed.”

`P-BREVE-02` remains reserved for a future locked-recipe Western-base replication.
