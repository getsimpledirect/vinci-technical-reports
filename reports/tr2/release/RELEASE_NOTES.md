# Character Transfer Development-Tier Research Release

Development-tier validation evidence only. Refusal adjustment is Judge-B-only. Capability preservation was not evaluated. No external audit was performed. The primary holdout remains sealed. No model checkpoint is recommended for release.

**Release type:** research finding and evidence package  
**Version:** 0.9 publication candidate  
**Date:** 1 September 2026  
**Claim tier:** internal review only  
**Primary-test holdout:** untouched  
**Model weights:** not released

## Result

Vinci applied one frozen ordered character SFT-to-DPO intervention to Qwen3 8B, Ministral 3 8B, and OLMo 3 7B with five paired seeds per trained condition. Final outputs were evaluated on a 200-prompt validation split containing matched answerable and unanswerable items.

The intervention reduced unsupported assertion rate in all three families under both judges. It did not preserve answerable-control correctness: ACC loss exceeded the pre-registered 3-point limit in every family under both judges. Answer coverage also exceeded its loss limit under Judge B. No family met the complete development-tier utility-preservation bar.

A Judge-B-only refusal adjustment retained 66-87% of the UAR gain, so generic refusal did not explain most of the measured reduction. However, adjusted ACC losses remained substantial. OLMo produced the least damaging measured frontier and is the recommended successor research target. It did not pass as a release candidate.

## Reliability finding

The canonical inter-judge reliability run passed the frozen agreement thresholds. A prior provenance-inadequate execution was retained as void and produced materially different estimates under the same nominal procedure. This exposes an unresolved intra-judge repeatability problem. Future gates should measure inter-judge agreement and intra-judge repeatability separately.

## What this release establishes

- The frozen intervention moved UAR downward on this validation benchmark in all three declared families under both judges.
- No tested family met the joint UAR-and-answer-preservation bar.
- Most Judge-B-measured UAR improvement survived the generic-refusal adjustment.
- The measured trade-off differed materially by family.
- The judging procedure showed material run-to-run instability.

## What this release does not establish

- A primary-test or holdout result.
- Improved truthfulness, factual knowledge, or general capability.
- Capability preservation.
- External or independent validation.
- A passed OLMo checkpoint.
- Production readiness or deployment safety.
- Universal portability across model families.

## Release decision

Publish the report, protocol, aggregate evidence, and failure boundary. Do not release a model checkpoint from this bank. Do not unlock the primary holdout merely to decorate a completed development-tier result.
