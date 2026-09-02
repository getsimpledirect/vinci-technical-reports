---
title: "We trained a model to stop overthinking. The evaluator failed first."
author: "George Pu"
date: "2026-09-01"
slug: "runtime-pass-is-not-correctness"
---

# We trained a model to stop overthinking. The evaluator failed first.

Reasoning models can spend thousands of tokens on work that should be short. Sometimes they keep reconsidering until they hit the generation limit and return nothing useful. P-BREVE-01-R2 was our attempt to change that at the weight level.

We trained a small supervised adapter, then used conservative preference optimization. The data was deliberately not “shorter is always better.” More than half of the chosen responses were not shorter than the rejected response. Correctness and verification were supposed to win over brevity.

The one-epoch result was negative from the start. At one seed, the final model produced 10.9% *more* reasoning tokens than base. At the other, it produced 4.9% fewer. Our bar required at least 20% fewer at both seeds. Adding DPO after SFT changed the result by only −0.6% and +0.6%.

We ran one bounded stronger-dose screen. That looked more promising, especially on executable-code tasks. But every arm had been served with an `xhigh` reasoning-effort instruction. When we changed the untrained base model from `xhigh` to the neutral `medium` setting, cap exhaustion on the screened code shard moved from 65% to 0/20 and token consumption collapsed. The formal matched-effort correctness comparison was underpowered, so I am not claiming equivalence. The causal point is narrower: the apparent trained dose response could not be cleanly separated from the serving policy. We retired the adapter.

Then the more important result arrived.

Our original executable-code evaluator accepted 24 out of 24 deliberately wrong shortcut programs. A three-line function could return the right output by branching on input length without reading the actual values. The nominal set of 80 code tasks was really eight problems copied ten times. Two “capability failures” were ambiguous specifications.

That means the evaluator ran. It was deterministic enough. It produced hashes and reports. It still did not measure the thing we thought it measured.

We built a better replacement with visible runtime tests and separate hidden certification. It was a real improvement: 154 of 322 broad shortcuts passed runtime, while none passed certification. But “better” is not “qualified.” Certification still accepted 7 of 157 near-miss or partial programs. A fresh mutation audit generated 1,862 provably wrong programs, and 52 still passed. Nineteen of forty tasks leaked under that one population. Across two detection methods, at least twenty-one of forty tasks had a known certification flaw.

The most important distinction in that paragraph is easy to lose: the mutation document also says twenty-one of forty tasks showed *no* leak under that population. Same number, opposite meaning. Our release package records the derivation of both because a checksum does not protect a reader from a semantic collision.

The report’s reusable output is Vinci Eval Integrity 0.1. It asks seven questions before an evaluator can govern a claim: are the artifacts and statistical units what they say they are; is the contract clear; are runtime and certification actually separate; do wrong solutions fail and valid alternatives pass; are censoring and denominators correct; does production execute the authority named in provenance; and is power measured against the full decision procedure with an independent post-repair population?

A test suite passing is not the same as work being correct. A verifier returning green is not the same as the verifier being valid. Reproducibility tells you that you can reproduce a result; it does not tell you that the result answers the intended question.

We did not get a model release out of P-BREVE-01-R2. We got a negative intervention result, a retired adapter, an unqualified replacement bank, and a much stronger standard for the next program.

That is worth publishing.

## Read the report

- [Technical report](https://www.getsimpledirect.com/research/papers/runtime-pass-is-not-correctness)
- [GitHub release package](https://github.com/getsimpledirect/vinci-technical-reports/tree/main/reports/tr3)

*This post and the underlying technical report are authored by George Pu. The report discloses the AI systems used in implementation, review, analysis packaging, and drafting.*
