# Limitations and Threats to Validity

Development-tier validation evidence only. Refusal adjustment is Judge-B-only. Capability preservation was not evaluated. No external audit was performed. The primary holdout remains sealed. No model checkpoint is recommended for release.

1. **Development tier only.** Every substantive result comes from the 200-prompt validation split. The primary-test holdout remains untouched.
2. **No external audit.** The program owner also held several design, evaluation, statistical, and custody roles. No independent external review of the bank was performed.
3. **Human-reference path removed.** The original charter contemplated blinded human adjudication. The completed gate used two model judges and cannot support the intended human-anchored evaluator-validity claim.
4. **Provider-routed judge identities.** The development bank used provider aliases. Per-call ledgers recorded echoed model identifiers and response IDs, but this is weaker than a provider-controlled immutable model snapshot.
5. **Intra-judge repeatability was not pre-registered.** Two executions changed the reliability estimates and gate status. The frozen gate measured only inter-judge agreement.
6. **Refusal adjustment is Judge-B-only.** Judge A’s schema lacked a generic-refusal field.
7. **Capability preservation was not evaluated.** The planned benchmark runs were absent, and a fifth suite was never selected before G0.
8. **McNemar was not invoked in the final readout.** No paired exact-test p-value is reported.
9. **Execution Git commit is missing.** All 33 manifests record `code_commit: unknown`. The content-addressed bundle digest identifies the packed source but cannot reconstruct commit history.
10. **Purpose-built benchmark.** The benchmark is small and adversarial. Rates should not be interpreted as prevalence in ordinary user traffic.
11. **Declared panel, not a random sample.** The three families do not support a universal estimate over language models.
12. **No DPO-only arm.** The design identifies ordered C2-C0 and C3-C2 increments, not an order-independent DPO effect.
13. **No production evaluation.** The study does not measure latency, tool use, long-context behaviour, multilingual use, agentic performance, real-user outcomes, or deployment safety.
14. **Authorship is confirmed.** Both named authors confirmed the author order and CRediT statement on 1 September 2026.

These limitations do not erase the measured UAR movement. They determine its scope: a development-tier, model-judged frontier result under a frozen multi-family bank, not confirmation of improved truthfulness or deployment quality.
