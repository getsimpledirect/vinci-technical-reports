# Research Page Copy - Technical Report No. 2

## Registry card

**VINCI PROVA · TECHNICAL REPORT · SEPTEMBER 2026**

### Character Transfer Across Three Model Families

**Verdict:** Does not meet the pre-registered utility-preservation bar  
**Evidence tier:** Development  
**Review:** Internal only  
**Primary holdout:** Untouched  
**Model release:** None

One frozen character SFT-to-DPO recipe reduced unsupported assertions in all three tested families, but grounded-answer accuracy deteriorated beyond the allowed limit in every family.

**Actions:** Read report · View evidence package · View protocol · View corrections

## Research record detail

### Question

When one explicit behavioural SFT-to-DPO intervention is held fixed, does it produce a consistent and useful response-policy change across independently developed model families?

### Answer

Not under the complete pre-registered bar. Unsupported assertion rate declined in Qwen3 8B, Ministral 3 8B, and OLMo 3 7B under both judges. Answerable-control correctness declined too much in every family, and answer coverage also violated its limit under Judge B.

### Key result

- 3 model families.
- 5 paired seeds per trained condition.
- 0 families met the complete bar.
- 66-87% of Judge-B-measured UAR gain survived the generic-refusal adjustment.
- Primary-test holdout untouched.
- No checkpoint recommended for release.

### Interpretation

The intervention moved the unsupported-assertion/grounded-answering frontier. It did not demonstrate improved truthfulness or utility-preserving portability. OLMo produced the least damaging measured frontier and motivates a successor experiment that optimizes answer preservation explicitly.

### Reliability note

The provenance-complete inter-judge reliability artifact passed. A prior provenance-inadequate execution produced materially different estimates under the same nominal judging procedure, exposing a separate judge-repeatability problem.

### Limitations shown above the fold

Development-tier validation evidence only. Refusal adjustment is Judge-B-only. Capability preservation was not evaluated. No external audit was performed. The primary holdout remains sealed. No model checkpoint is recommended for release.

## SEO and metadata

**Page title:** Character Transfer Across Three Model Families | Vinci Technical Report No. 2

**Meta description:** Vinci tested one frozen character post-training recipe across Qwen3, Ministral, and OLMo. Unsupported assertions declined, but no family preserved grounded-answer accuracy well enough to meet the pre-registered bar.

**Suggested slug:** `character-transfer-across-three-model-families`

**Open Graph title:** We tested one character recipe across three model families. None met the bar.

**Open Graph description:** Development-tier evidence from 30 trained runs and three baselines. UAR improved; grounded-answer accuracy fell too far. The primary holdout remains untouched.

## Structured-data draft

```json
{
  "type": "technical-report",
  "program": "Vinci Prova",
  "status": "complete",
  "evidenceTier": "development",
  "claimTier": "internal-review-only",
  "verdict": "does-not-meet",
  "modelReleaseEligible": false,
  "holdoutStatus": "untouched",
  "authors": ["George Pu", "Ayush Naik"],
  "publishedAt": "1 September 2026",
  "reportUrl": "https://www.getsimpledirect.com/research/papers/character-transfer-across-three-model-families",
  "bundleUrl": "https://doi.org/10.5281/zenodo.22236690"
}
```
