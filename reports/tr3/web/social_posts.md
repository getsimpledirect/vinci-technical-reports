# Launch Copy

## X — single post

We tried to train Qwen3.8-27B to stop overthinking.

The one-epoch recipe missed its target. A serving control confounded the stronger screened result. Then the evaluator failed: 24/24 shortcut programs passed the original code bank.

We published the failure, not a checkpoint.

https://www.getsimpledirect.com/research/papers/runtime-pass-is-not-correctness

## X — thread

**1/** We published Vinci Technical Report No. 3: *Runtime Pass Is Not Correctness.* It is a negative reasoning-efficiency result and an evaluator audit on Qwen3.8-27B.

**2/** The configured one-epoch SFT+DPO recipe missed the frozen efficiency bar. Signed reasoning reduction was −10.9% at one seed—meaning longer—and +4.9% at the other. The target was +20% at both.

**3/** A two-epoch screen looked better on executable-code tasks. But every arm was served with an `xhigh` effort instruction.

**4/** On untrained weights, switching `xhigh` to neutral `medium` moved cap exhaustion from 65% to 0/20 on the screened shard and cut token use sharply. The matched-effort correctness test remained underpowered, so the trained effect was not cleanly identified.

**5/** The evaluator audit mattered more. The original code bank accepted 24/24 deliberately wrong shortcut programs—including functions that branched on input length without reading the values.

**6/** The nominal 80 code tasks were eight problems copied ten times. Stable execution and clean hashes did not make the instrument valid.

**7/** We built separate runtime and hidden-certification channels. Broad shortcuts passed runtime 154/322 and certification 0/322. Better—but not qualified.

**8/** Certification still accepted 7/157 near-miss or partial programs and 52/1,862 wrong mutants from an independently constructed population.

**9/** The reusable output is Vinci Eval Integrity 0.1: seven checks an evaluator must clear before it governs model selection, optimization, or release.

**10/** No model, bank, or release candidate resulted. We published the report, evidence map, figures, source, and failure boundary instead.

https://www.getsimpledirect.com/research/papers/runtime-pass-is-not-correctness

## LinkedIn — George Pu

We published a model-training result that did not work—and an evaluator result that matters more.

P-BREVE-01-R2 tested whether small SFT followed by conservative preference optimization could make Qwen3.8-27B reason more proportionally and finish work reliably. The configured one-epoch recipe missed its frozen target. A stronger screen appeared to improve executable-code efficiency, but an untrained serving control reproduced the termination shift. We could not attribute the effect cleanly to the adapter.

Then we attacked the evaluator. All 24 deliberately wrong shortcut programs passed the original code bank. The replacement was substantially better, but independent near-miss and mutation populations still found certification gaps.

The conclusion is not that tests are useless. It is that an executable test result is only as strong as the evaluator’s demonstrated discrimination, independence, estimand, and production binding.

The report introduces Vinci Eval Integrity 0.1, a seven-check admission record for evaluators. No model, bank, or release candidate resulted.

We published the failure because a bar is useful only when it can stop you.

https://www.getsimpledirect.com/research/papers/runtime-pass-is-not-correctness

## LinkedIn — company

Vinci Research has published Technical Report No. 3, *Runtime Pass Is Not Correctness*.

The development-tier study reports a negative reasoning-efficiency post-training result on Qwen3.8-27B and an audit showing that executable evaluators can run reliably while failing to distinguish correct implementations from shortcut programs.

No model checkpoint or evaluator bank is released. The package includes the report, reproducible figures, aggregate evidence, source bindings, and Vinci Eval Integrity 0.1.

https://www.getsimpledirect.com/research/papers/runtime-pass-is-not-correctness

## Hacker News

**Title:** Runtime Pass Is Not Correctness: a negative Qwen reasoning-efficiency result and verifier audit

**Submission text:** We tested small SFT + conservative DPO on Qwen3.8-27B, got a null at the frozen one-epoch bar, then found a serving-control confound in the stronger screen. The more useful result was evaluator failure: 24/24 shortcut programs passed the original executable-code bank, and a replacement hidden-certification design still failed independent near-miss and mutation qualification. Report, aggregate evidence, build source, and figures are included; no model or protected test bank is released.
