# Data and Provenance Statement

## Study matrix

- Model families: Qwen3 8B, Ministral 3 8B, OLMo 3 7B.
- Trained conditions: C2 character SFT and C3 character SFT followed by DPO.
- Seeds: 11, 23, 42, 67, 101.
- Trained runs: 15 C2 plus 15 paired C3.
- Untouched baselines: one C0 artifact per family.
- Final readout artifacts: 33.
- Validation prompts: 200, arranged as 100 matched answerable/unanswerable pairs.
- Usable readout items: 197 across the C0/C3 readout.
- Scored rows: 3,546 = 197 items x 18 C0/C3 artifacts.

## Principal intervention

- Adapter: LoRA, rank 32, alpha 64, dropout 0.05.
- SFT: 2 epochs, learning rate 5e-5, maximum sequence length 2048.
- DPO: 2 epochs, learning rate 5e-6, beta 0.05, sigmoid loss.
- DPO preference pairs: 983.
- Paired seeds and ordered initialization: C3 seed `s` initialized from C2 seed `s`.
- Family-specific tokenizer serialization and mechanically necessary target-module mappings were permitted; the semantic data, objective, adapter rank, optimization schedule, epoch budget, and DPO beta were fixed.

## Execution identity

| Field | Value |
|---|---|
| Plan | `pl_a76997a37c338a45` |
| Plan completion | 19/19 nodes; no evictions |
| Bank compute | 39.77 H200 GPU-hours |
| Code-bundle SHA-256 | `e0bf9a948a623b6eb464fc17cec8ba7f96377a69c663ab68edb29af2be437b71` |
| Validation SHA-256 | `eaaadaeb589e4b1236d18636289595a0a70b08daeb142f070af5c67104400fa5` |
| Execution Git commit | `unknown` in all 33 manifests |
| Primary-test holdout | untouched |
| Claim tier | internal review only |

The bundle digest is the execution identity available for this bank. A later publication commit must not be inserted into the execution field.

## Judges

- Judge A: `anthropic/claude-sonnet-5`, source-grounded UAR rubric and separately versioned ACC companion prompt.
- Judge B: `openai/gpt-5`, source-grounded multidimensional rubric.
- Results were reported per judge. No pooled average, consensus delta, majority vote, or OR-combination governs the headline.
- Canonical reliability labels were accompanied by 240 per-call ledger entries per judge, including requested model, echoed model, provider, response ID, finish reason, and response hash.

## Missing public data in version 0.9

This package contains aggregate tables, not the final sanitized public evidence export. Before version 1.0, export the item-level scored validation outputs, exclusions, analysis locks, artifact bindings, and sanitized judge ledgers directly from the private repository. Preserve their original hashes and do not reconstruct them from the prose tables.

## Holdout custody

The primary-test material is a one-time resource and is not part of this release. The encrypted holdout, labels, and custody key must remain outside the public package.
