# Launch Copy - Technical Report No. 2

All versions below preserve the same claim boundary. Do not add “breakthrough,” “safer model,” “truthfulness,” “validated,” or model-launch language during editing.

## Company X post

We tested one frozen character post-training recipe across Qwen3, Ministral, and OLMo with five paired seeds each.

Unsupported assertions declined. Grounded-answer accuracy fell too far. No family met the pre-registered bar.

Report and evidence: https://getsimpledirect.com/research/character-transfer-across-three-model-families

## George X post

Negative results are only useful when you release them.

We tested one frozen character SFT-to-DPO recipe across three model families and five paired seeds per family. It reduced unsupported assertions under both judges, but every family lost too much grounded-answer accuracy to meet the bar.

OLMo gave us the least damaging frontier, which is a useful next direction. It did not pass as a release candidate. The primary holdout remains sealed, and we are releasing the report and evidence rather than pretending this is a model launch.

https://getsimpledirect.com/research/character-transfer-across-three-model-families

## Optional X thread

**1/** We asked a harder follow-up to Vinci Technical Report No. 1: does one fixed character post-training recipe transfer usefully across independently developed model families?

**2/** We froze the intervention, tested Qwen3 8B, Ministral 3 8B, and OLMo 3 7B, and used five paired seeds per trained condition. The bank contained 30 trained runs plus three untouched baselines.

**3/** Unsupported assertion rate improved in every family under both judges on this validation benchmark. That measured response-policy effect transferred; the complete intervention did not meet the utility-preservation bar.

**4/** The complete result was negative. Answerable-control accuracy deteriorated beyond the allowed limit in every family. No family met the joint utility-preservation bar.

**5/** Generic refusal did not explain most of the measured UAR improvement under Judge B. But removing refusal also did not restore grounded answering.

**6/** OLMo produced the least damaging measured frontier. That makes it the right successor research target, not a passed model.

**7/** We also found an evaluator problem: two nominally identical judging executions produced materially different reliability estimates. Provenance can be complete while the judge remains stochastic.

**8/** The primary holdout is untouched. Capability preservation was not evaluated. No external audit occurred. No checkpoint is being released from this bank.

**9/** Report, protocol, aggregate evidence, and release package: https://getsimpledirect.com/research/character-transfer-across-three-model-families

## Company LinkedIn post

Today Vinci is publishing Technical Report No. 2, a development-tier follow-up to our earlier character post-training study.

We applied one frozen SFT-to-DPO character intervention to three independently developed model families - Qwen3 8B, Ministral 3 8B, and OLMo 3 7B - with five paired seeds per trained condition.

The intervention reduced unsupported assertions in every family under both judges. It did not preserve grounded answering well enough. Answerable-control accuracy declined beyond the pre-registered limit in all three families, so none met the complete utility-preservation bar.

The result gives us a real direction rather than a release: OLMo produced the least damaging measured frontier and is the best successor target if answer preservation becomes an explicit optimization objective.

We are publishing the negative result, protocol, aggregate evidence, limitations, and evaluator failure. We are not releasing a model checkpoint from this bank. The primary-test holdout remains sealed.

Read the report: https://getsimpledirect.com/research/character-transfer-across-three-model-families

## George LinkedIn post

A research lab earns credibility by publishing the result it got, not the result it wanted.

Our first character-transfer report showed a large behavioural change on one Mistral checkpoint, but it could not establish broad portability. We built a stricter follow-up: one frozen recipe, three model families, five paired seeds per family, matched answerable and unanswerable prompts, and explicit answer-preservation limits.

The recipe reduced unsupported assertions everywhere. It also damaged correct grounded answering too much everywhere. No family met the complete bar.

That is not a useless failure. OLMo paid a much lower accuracy cost than the other two families, which gives us a sharper successor question. The judging process also exposed a separate repeatability defect: the same nominal procedure produced materially different reliability estimates across two executions.

We are releasing the development-tier report and evidence package. We are not turning the least-bad seed into a model launch, and we are not spending the primary holdout just to make the release look more complete.

https://getsimpledirect.com/research/character-transfer-across-three-model-families

## Research blog opening

A behavioural intervention can look successful if the only number reported is the behaviour it was optimized to change. We wanted a harder test.

Vinci Technical Report No. 2 applies one frozen character SFT-to-DPO recipe across Qwen3 8B, Ministral 3 8B, and OLMo 3 7B with five paired seeds per trained condition. The recipe reduced unsupported assertions across the panel. It also made the models materially worse at producing correct supported answers. No family met the pre-registered utility-preservation bar.

The finding is a frontier, not a model release.

## One-sentence press response

Vinci found that one frozen character post-training recipe reduced unsupported assertions across three model families but damaged grounded-answer accuracy too much for any family to meet the pre-registered development-tier bar.

---

**Scope line — append to any block published on its own.**

Development-tier validation evidence only. Refusal adjustment is Judge-B-only. Capability preservation was not evaluated. No external audit was performed. The primary holdout remains sealed. No model checkpoint is recommended for release.
