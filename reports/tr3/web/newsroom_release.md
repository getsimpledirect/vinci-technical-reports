---
title: "Vinci publishes negative reasoning-efficiency result and evaluator audit"
date: "2026-09-01"
---

# Vinci publishes negative reasoning-efficiency result and evaluator audit

**Toronto — 1 September 2026.** SimpleDirect / Vinci Research has published Vinci Technical Report No. 3, *Runtime Pass Is Not Correctness*, a development-tier study of reasoning-efficiency post-training and executable evaluator validity on Qwen3.8-27B.

The P-BREVE-01-R2 program tested a small supervised fine-tuning stage followed by conservative length-debiased Direct Preference Optimization. The configured one-epoch recipe did not meet its frozen token-efficiency target, and the marginal DPO contribution over SFT was approximately zero across the two reported seeds.

A bounded stronger-dose screen initially suggested an executable-code improvement. A subsequent serving-control experiment showed that changing the untrained base model’s reasoning-effort setting reproduced the termination shift, preventing clean attribution to trained weights. The adapter was retired.

The evaluator audit produced the report’s stronger result. The original executable-code bank accepted 24 of 24 deliberately incorrect shortcut programs. A replacement runtime/certification design rejected broad shortcuts at certification but continued to accept some near-miss, partial, and independently generated mutant programs. No model, evaluator bank, or release candidate resulted.

The report introduces **Vinci Eval Integrity 0.1**, a seven-check admission record for evaluator identity, contract clarity, channel separation, bidirectional discrimination, estimand integrity, production-path binding, and exact-procedure power with independent requalification.

The report is sole-authored by George Pu. It is released as development-tier evidence, internally reviewed, without external peer review. The publication package includes the report, reproducible figures, aggregate evidence tables, provenance bindings, claims and limitations, build sources, arXiv metadata, and public communication materials.

Report: https://www.getsimpledirect.com/research/papers/runtime-pass-is-not-correctness  
Source package: https://github.com/getsimpledirect/vinci-technical-reports/tree/main/reports/tr3
