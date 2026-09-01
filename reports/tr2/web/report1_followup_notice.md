# Dated Follow-Up Notices for Technical Report No. 1

Use the same date and destination URL across every surface.

## Report No. 1 page - full notice

> **Follow-up - 1 September 2026.** This report established a behavioural effect on one Mistral checkpoint and explicitly did not establish general cross-lineage portability. A subsequent frozen three-family development study found that the intervention reduced unsupported assertions across the tested panel but that no family met the combined unsupported-assertion and answer-preservation bar. The original measurements in this report are unchanged; the later result narrows how broadly they should be interpreted. See Vinci Technical Report No. 2: https://getsimpledirect.com/research/character-transfer-across-three-model-families.
>
> Development-tier validation evidence only. Refusal adjustment is Judge-B-only. Capability preservation was not evaluated. No external audit was performed. The primary holdout remains sealed. No model checkpoint is recommended for release.

## Research article - concise notice

> **Research update - 1 September 2026.** Our three-family follow-up found a consistent reduction in unsupported assertions, but every tested family lost too much grounded-answer accuracy to meet the pre-registered bar. The original single-checkpoint measurements remain unchanged. Read Technical Report No. 2: https://getsimpledirect.com/research/character-transfer-across-three-model-families.
>
> Development-tier validation evidence only. Refusal adjustment is Judge-B-only. Capability preservation was not evaluated. No external audit was performed. The primary holdout remains sealed. No model checkpoint is recommended for release.

## Hugging Face model card - top-of-card notice

> **Follow-up evidence - 1 September 2026.** A later frozen study across Qwen3 8B, Ministral 3 8B, and OLMo 3 7B did not confirm utility-preserving portability of this character recipe. Unsupported assertions declined, but no family met the joint answer-preservation bar. This checkpoint remains an experimental artifact and is not recommended for production. Technical Report No. 2: https://getsimpledirect.com/research/character-transfer-across-three-model-families.
>
> Development-tier validation evidence only. Refusal adjustment is Judge-B-only. Capability preservation was not evaluated. No external audit was performed. The primary holdout remains sealed. No model checkpoint is recommended for release.

## GGUF card notice

> **Follow-up evidence - 1 September 2026.** The later three-family Character Transfer study found a real unsupported-assertion reduction but failed its grounded-answer preservation criterion in every family. This conversion remains an experimental research artifact, not a validated or production-recommended model. https://getsimpledirect.com/research/character-transfer-across-three-model-families
>
> Development-tier validation evidence only. Refusal adjustment is Judge-B-only. Capability preservation was not evaluated. No external audit was performed. The primary holdout remains sealed. No model checkpoint is recommended for release.

## Research registry update for Report No. 1

- Keep the original verdict and measurements.
- Add `followUpStatus: qualified`.
- Add `followUpReport: https://getsimpledirect.com/research/character-transfer-across-three-model-families`.
- Replace any present-tense broad statement that the recipe “transfers across lineages” with the narrower historical statement that a behavioural effect was measured on one additional lineage.
- Do not label Report No. 1 retracted. The follow-up narrows the generalization; it does not invalidate the original checkpoint-specific measurements.
