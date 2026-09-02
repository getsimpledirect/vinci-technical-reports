# Vinci Research Note — Runtime Pass Is Not Correctness

We published Vinci Technical Report No. 3, a negative reasoning-efficiency post-training result and evaluator audit on Qwen3.8-27B.

The configured one-epoch SFT+DPO recipe missed its efficiency target. A stronger screened result looked promising on code tasks, but an untrained serving control reproduced the termination shift, so the gain could not be attributed cleanly to trained weights.

The evaluator audit was more consequential. All 24 deliberately wrong shortcut programs passed the original code bank. A replacement hidden-certification design rejected broad shortcuts, but independent near-miss and mutation audits still found gaps. No model, bank, or release candidate resulted.

The report turns those failures into Vinci Eval Integrity 0.1: seven checks an evaluator must clear before it can govern model selection, optimization, or release.

Read the report: https://www.getsimpledirect.com/research/papers/runtime-pass-is-not-correctness
