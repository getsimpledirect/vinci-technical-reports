---
title: "Runtime Pass Is Not Correctness"
subtitle: "A Negative Reasoning-Efficiency Post-Training Result and Verifier Audit on Qwen3.8-27B"
author: "George Pu"
date: "2026-09-01"
report: "Vinci Technical Report No. 3"
version: "1.0"
slug: "runtime-pass-is-not-correctness"
status: "Development-tier evidence; external peer review not performed"
---

# Runtime Pass Is Not Correctness

## A Negative Reasoning-Efficiency Post-Training Result and Verifier Audit on Qwen3.8-27B

P-BREVE-01-R2 tested whether small supervised fine-tuning followed by conservative length-debiased preference optimization could make Qwen3.8-27B reason more proportionally and finish work more reliably.

It did not earn that claim.

The configured one-epoch recipe missed its efficiency target at both-seed bar. A stronger two-epoch screen looked promising on executable-code tasks, but an untrained serving control reproduced the termination shift by changing the model’s effort setting. The apparent trained effect could not be isolated.

The evaluator audit mattered more. The original executable-code bank accepted all 24 deliberately wrong shortcut programs. A replacement hidden-certification design rejected broad shortcuts, but independent near-miss and mutation populations still found certification gaps. No model, bank, or release candidate resulted.

## Main findings

- **One-epoch null:** −10.9% signed reasoning reduction at one seed meant *longer* output; +4.9% at the other was below the required +20% at both seeds.
- **Serving confound:** base `xhigh` to base `medium` moved cap exhaustion from 65% to 0/20 on the screened code shard and sharply reduced token use.
- **Original evaluator failure:** 24/24 shortcut programs passed; 80 nominal code tasks represented eight repeated problems.
- **Replacement evaluator failure:** certification rejected 0/322 broad shortcuts, but accepted 7/157 near-miss or partial programs and 52/1,862 independently generated wrong mutants.
- **Reusable output:** Vinci Eval Integrity 0.1 turns the failures into seven checks an evaluator must clear before it can govern model selection, optimization, or release.

## Responsible interpretation

This report does not establish that preference optimization cannot reduce overthinking, that Qwen generally overthinks, that `medium` is correctness-equivalent to the fine-tune, that safety was broadly preserved, or that the reported probe rates estimate deployed traffic.

**Download:** [Report PDF](https://github.com/getsimpledirect/vinci-technical-reports/tree/main/reports/tr3/report/Vinci_Technical_Report_No_3_v1.0.pdf)  
**Release package:** [GitHub](https://github.com/getsimpledirect/vinci-technical-reports/tree/main/reports/tr3)  
**Citation:** Vinci Technical Report No. 3, Version 1.0, 1 September 2026.
