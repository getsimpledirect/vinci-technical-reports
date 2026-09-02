# FAQ

## Did P-BREVE make Qwen3.8-27B better?

The study did not establish that. The configured one-epoch recipe missed its efficiency target, and the original correctness evaluator was later condemned.

## Did the fine-tune reduce overthinking?

A two-epoch screen showed lower code-task token use under `xhigh`, but an untrained `medium` serving control reproduced the termination shift. The matched-effort correctness comparison was underpowered. The trained contribution was not identified cleanly.

## Does 0/20 cap hits prove the true rate is zero?

No. Zero of twenty has a two-sided 95% upper bound of 16.8%. The report uses the observed count and its limitation.

## Why is runtime pass not correctness?

Visible tests can be satisfied by programs specialized to the tested inputs. The original bank accepted trivial programs that did not implement the intended function. Runtime checks are useful for repair and retry; they must not automatically become the scientific score or RL reward.

## Was the replacement evaluator better?

Yes, materially. Its protected certification channel rejected all 322 broad shortcut probes. It still accepted near-miss, partial, and independently generated mutant programs, so it remained unqualified.

## Why are there two different 21-of-40 values?

Under one AST mutation population, 19 tasks leaked and the complementary 21 did not show a leak. Across two detection methods, seven prior tasks plus fourteen newly adjudicated tasks outside that set yield a separate lower bound of at least 21 tasks with known flaws. Same number, different construction and opposite polarity.

## Is P-BREVE-02 this study?

No. This is P-BREVE-01-R2. P-BREVE-02 remains reserved for a future locked-recipe reproduction on a Western 24–32B base.

## Are model weights or protected tests released?

No. The release is the report, aggregate evidence, source bindings, and evaluator-integrity standard.
