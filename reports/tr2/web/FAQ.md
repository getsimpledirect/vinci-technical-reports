# Frequently Asked Questions

> **Scope.** Development-tier validation evidence only. Refusal adjustment is Judge-B-only. Capability preservation was not evaluated. No external audit was performed. The primary holdout remains sealed. No model checkpoint is recommended for release.

## Did character transfer fail?

The intervention clearly affected all three model families and reduced unsupported assertions under both judges. The stronger claim failed: none of the families preserved grounded answering well enough to meet the complete pre-registered bar. The right description is a failed utility-preserving transfer claim, not “nothing happened.”

## Why does the report say G1 passed if the research result was negative?

G1 measured whether the two model judges agreed reliably enough under the frozen development-tier procedure. It was a measurement-quality gate, not the intervention success criterion. The judges agreed that the substantive family-level bar was not met.

## Did the models simply refuse more often?

Not entirely. Under Judge B, 66-87% of the UAR improvement survived after removing every generic-refusal item from both paired arms. Generic refusal explained part of the change, but not most of it. The accuracy loss also remained, especially for Ministral and Qwen.

## Did OLMo pass?

No. OLMo failed the answerable-control accuracy limit. It produced the least damaging measured trade-off and therefore motivates a successor experiment. It is not a passed checkpoint or a model release candidate.

## Why not release the best OLMo seed?

The unit of inference was the family across five seeds, not the most flattering checkpoint chosen after results. Selecting one seed now would introduce post-result model selection and convert a failed family-level criterion into a misleading model launch.

## Why not open the primary holdout now?

The holdout is a one-time resource. All current configurations have already failed the development-tier ACC criterion. Opening the holdout would add a more expensive answer to a question that cannot rescue them. It becomes valuable after a prospectively chosen successor candidate exists and the outcome could change a real decision.

## Was capability preserved?

Not evaluated. The required benchmark runs were not part of this bank. Capability preservation must be reported as not evaluated, never passed.

## Was the result externally validated?

No. The program closed at internal-review development tier. A meaningful future external audit would require a fresh blinded set and a reviewer named before results are disclosed.

## Why are there two judge-reliability runs?

The first execution lacked adequate proof of judge identity and temporal label anchoring, so it was preserved as void rather than treated as a valid gate result. The corrected execution added per-call ledgers and pre-analysis label anchoring. The two runs produced materially different estimates, which is itself an important evaluator-reliability finding.

## Does the void run mean the canonical result was rerolled until it passed?

The report’s position is narrower: the first artifact could not establish the frozen independent-judge condition, regardless of whether its number was favourable. The corrected labels were anchored before their result was computed. The run-to-run difference is still disclosed and is why future gates need a prospective repeatability rule.

## Does this overturn Technical Report No. 1?

No. Report No. 1 made a narrow checkpoint-specific observation and explicitly did not establish universal portability. The new study tests a broader claim and does not support it. The follow-up narrows the generalization while preserving the original measurements.

## Are model weights being released?

No. The responsible artifact is the report, protocol, aggregate evidence, and failure boundary. A future model release requires a new protocol and evidence that supports a model-specific claim.

## Can another lab reproduce the result?

Version 1.0 includes the manuscript, figures, and aggregate tables. A full independent recomputation requires the sanitized item-level scored outputs, analysis locks, and judge ledgers to be exported from the private repository. That export is a version-1.0 blocker.
