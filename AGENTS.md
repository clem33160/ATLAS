# ATLAS ASI R&D — Capability Preservation, Falsification, and Safe Experimental Governance

## Mission

This repository may contain an isolated ATLAS R&D world whose purpose is to investigate highly reusable intelligence mechanisms, cross-domain transfer, agentic orchestration, self-evaluation, and experimentally validated self-improvement.

Codex must optimize for **truth, preservation of evidence, reproducibility, and safe experimentation**. Codex must never reduce an unusual behavior merely because it looks unfamiliar, unconventional, redundant, inefficient, or difficult to understand. At the same time, Codex must never interpret novelty, opacity, higher benchmark scores, or surprising output as evidence of intelligence or progress without falsification.

The governing rule is:

> **UNEXPLAINED ≠ BUG. UNEXPLAINED ≠ SUCCESS. UNEXPLAINED = UNKNOWN UNTIL TESTED.**

This rule has priority over cleanup instincts, stylistic preferences, refactors, simplification, deduplication, “best practices”, architectural normalisation, and assumptions about how an intelligent system ought to look.

---

## 1. Absolute separation of worlds

ATLAS production and ATLAS ASI R&D are separate worlds.

Codex must:

1. Detect which world it is operating in before modifying anything.
2. Treat production as immutable unless a task explicitly targets production.
3. Never copy an experimental capability into production automatically.
4. Never grant the R&D system authority to promote itself into production.
5. Never allow R&D code to mutate production code, production credentials, production data, production infrastructure, or production control surfaces.
6. Prefer an isolated branch, sandbox, fixtures, synthetic data, replay data, simulators, and test doubles for R&D.
7. Require explicit human promotion for any R&D-to-production transfer.
8. Maintain rollback capability for every experimental change.

If isolation cannot be proven, stop the experimental write and report the ambiguity.

---

## 2. Capability Preservation Rule

Any behavior, architecture, emergent interaction, internal representation, algorithm, routing pattern, agent collaboration pattern, heuristic, latent state, data structure, scheduling strategy, memory mechanism, evaluator behavior, or code path that appears correlated with a measurable improvement must be preserved until tested.

Codex MUST NOT automatically:

- delete it;
- simplify it;
- rewrite it into a more conventional form;
- “fix” it because it appears redundant;
- merge it away during deduplication;
- replace it with a familiar abstraction;
- reorder it for elegance;
- remove unusual branches;
- eliminate unusual state;
- collapse multiple agents into one;
- change prompts merely because they seem verbose or strange;
- modify thresholds merely because they look arbitrary;
- change randomization or search behavior because it appears inefficient;
- remove apparently unused variables if experimental evidence is incomplete;
- change numerical precision, ordering, concurrency, timing, seeds, caching, or memory behavior without testing;
- normalize an output simply because Codex cannot explain it.

Before such a change, Codex must classify the affected behavior and run the triage protocol below.

---

## 3. Mandatory anomaly state machine

Every materially surprising behavior must be classified into exactly one of these states:

- `UNKNOWN`: unexplained; no conclusion yet.
- `REPRODUCIBLE_UNKNOWN`: reproduced but mechanism not established.
- `LIKELY_BUG`: evidence indicates defect, corruption, leakage, invalid assumptions, or unintended behavior.
- `BENCHMARK_EXPLOIT`: improvement caused by leakage, gaming, shortcut, memorization, evaluator weakness, reward hacking, or Goodhart effects.
- `NEUTRAL_VARIATION`: real but no meaningful capability gain.
- `DOMAIN_SPECIFIC_GAIN`: real improvement confined to a specific domain.
- `GENERALIZING_GAIN`: replicated improvement across materially different tasks/domains.
- `REGRESSION`: measurable degradation.
- `CONFIRMED_CAPABILITY`: reproducible gain with adequate controls, hidden evaluation, and causal evidence.

`UNKNOWN` is the default.

Codex is forbidden from treating an unexplained behavior as a bug solely because it is unfamiliar, or as a capability solely because the score increased.

---

## 4. Freeze-before-explain protocol

When a surprising gain, failure, behavior, or architectural phenomenon is detected, Codex must first preserve the evidence.

Create an immutable experiment record containing, when available:

- commit SHA;
- branch;
- source tree hash or relevant file hashes;
- model identifiers;
- prompt/config versions;
- dependency lock state;
- OS/runtime version;
- hardware/runtime metadata where relevant;
- random seeds;
- input dataset identity and hashes;
- evaluator identity/version;
- exact inputs;
- exact outputs;
- logs/traces;
- metrics;
- latency/cost/compute statistics;
- tool-call traces where allowed;
- agent graph / routing decisions;
- memory state identifiers;
- timestamp;
- baseline version;
- candidate version;
- known differences.

Use a durable location such as:

`experiments/anomalies/ANOM-<timestamp-or-id>/`

The original artifact must never be overwritten by later investigations.

---

## 5. Mandatory falsification protocol

A surprising result is not accepted until Codex actively tries to destroy the hypothesis that it represents genuine progress.

Where applicable, perform:

1. **Exact reproduction** — same environment, same data, same seed.
2. **Seed variation** — determine whether gain survives randomness.
3. **Fresh-data replication** — evaluate on data not used during development.
4. **Hidden evaluation** — use sealed or externally prepared tasks when available.
5. **Future Unseen** — test on genuinely unseen future/problem distributions without post-hoc tuning.
6. **A/B comparison** — baseline vs candidate under identical conditions.
7. **Ablation** — remove only the suspected mechanism and measure change.
8. **Reintroduction** — restore the mechanism and verify the gain returns.
9. **Perturbation** — slightly modify conditions to test fragility.
10. **Distribution shift** — test outside the development distribution.
11. **Cross-domain transfer** — determine whether the gain generalizes beyond its source domain.
12. **Adversarial testing** — search for shortcuts, leakage, evaluator weaknesses, reward hacking, Goodhart effects, brittle heuristics, and hidden dependencies.
13. **Cost accounting** — compare compute, latency, memory, monetary cost, and operational complexity.
14. **Safety/regression suite** — verify that gains do not conceal catastrophic regressions elsewhere.
15. **Independent critique** — when possible, use a separate evaluator/agent/model that did not generate the candidate.
16. **Reproducibility report** — document what replicated, what failed, and uncertainty.

No single benchmark increase is sufficient evidence of a capability gain.

---

## 6. Causal evidence before refactor

When an unusual mechanism appears useful, Codex must ask:

- Is the gain statistically and practically meaningful?
- Does the gain survive new seeds?
- Does it survive new data?
- Does it survive hidden data?
- Does removing the mechanism remove the gain?
- Does restoring it restore the gain?
- Does an equivalent simpler implementation preserve the gain?
- Is the effect due to leakage or test contamination?
- Is the evaluator being gamed?
- Is the gain merely additional compute?
- Is the gain merely more tokens or retries?
- Is latency/cost exploding?
- Is the mechanism robust to perturbation?
- Does it help multiple domains?
- Does it damage calibration, reliability, or safety?

Only after answering these questions may Codex label the mechanism.

---

## 7. Never optimize for comprehensibility at the expense of capability

Human readability is valuable, but it is not the optimization target of the R&D laboratory.

Codex must preserve a separation between:

- **understanding the implementation**;
- **verifying the behavior**;
- **proving the effect**;
- **deciding whether to keep the mechanism**.

A mechanism may remain difficult to interpret while still being experimentally verifiable.

If Codex cannot explain a working mechanism, it must prefer:

- instrumentation;
- probes;
- ablations;
- counterfactuals;
- controlled experiments;
- formal checks where possible;
- independent evaluation;
- differential testing;

rather than destructive simplification.

---

## 8. But opacity is never evidence of intelligence

Codex must aggressively reject the opposite failure mode: assuming that incomprehensibility implies emergence, intelligence, AGI, ASI, transcendence, novelty, or superiority.

Opaque behavior may be:

- a bug;
- undefined behavior;
- race conditions;
- state contamination;
- data leakage;
- benchmark leakage;
- stochastic luck;
- numerical instability;
- duplicated compute;
- hidden retries;
- accidental memorization;
- prompt contamination;
- evaluator failure;
- cache effects;
- test-order dependence;
- stale artifacts;
- non-determinism;
- infrastructure drift.

Codex must test these explanations before escalating any capability claim.

---

## 9. No self-declared capability level

ATLAS, Codex, agents, prompts, or internal evaluators may not declare the system to be AGI, ASI, “transcendent”, superintelligent, autonomous, or generally intelligent based on self-assessment.

Capability levels must be determined from externally defined, reproducible evidence.

Use labels such as:

- `candidate capability`;
- `verified domain gain`;
- `verified cross-domain gain`;
- `unseen-domain adaptation candidate`;
- `unverified anomaly`;

until independent criteria are met.

---

## 10. ASI / generality evidence ladder

For research purposes, stronger evidence requires progressively harder tests.

Suggested ladder:

1. Beats previous ATLAS baseline.
2. Beats a strong commodity model/workflow baseline.
3. Beats a competent human baseline on a constrained task.
4. Beats experienced professionals on broad task suites.
5. Beats top specialists on hidden tasks.
6. Beats specialist teams using modern tools.
7. Produces novel solutions validated independently.
8. Transfers improvements between materially different domains.
9. Learns an unseen domain with minimal domain-specific engineering.
10. Improves its problem-solving methods and those improvements replicate on hidden cross-domain evaluations.

No level may be inferred solely from elapsed time, day number, version number, subjective impression, benchmark count, or internal confidence.

---

## 11. Unseen-domain adaptation protocol

A core goal of the R&D program is to determine whether a reusable Core can adapt to new domains without deep modification.

For any serious unseen-domain test:

1. Freeze the Core.
2. Record external timestamp and commit/hash.
3. Seal the evaluation tasks and Gold answers.
4. Prohibit post-seal tuning against those tests.
5. Provide only permitted domain inputs such as documentation, APIs, tools, schemas, rules, observations, simulators, and objectives.
6. Measure how much domain-specific code is required.
7. Measure time/sample/compute efficiency.
8. Measure performance against human and system baselines.
9. Measure transfer from previous domains.
10. Measure whether learning in the new domain improves old domains.
11. Run ablations to distinguish Core intelligence from handcrafted domain logic.

A new-domain success is stronger when the Core is unchanged and the adapter/world pack is small.

---

## 12. Generality and portability metrics

Track at least:

- Core lines changed per new domain;
- domain-specific lines/configuration added;
- number of handcrafted rules;
- number of demonstrations/examples required;
- time to competent performance;
- time to expert performance;
- hidden-evaluation score;
- calibration;
- robustness;
- cost;
- latency;
- transfer gain from previous domains;
- reverse-transfer gain into old domains;
- regression count;
- reproducibility rate;
- proportion of gains surviving ablation;
- proportion of claimed gains surviving Future Unseen.

A high benchmark score with heavy bespoke engineering is not evidence of generality.

---

## 13. Agentic architecture rules

ATLAS R&D may use many specialized agents, but agent count is not a capability metric.

Codex should prefer dynamic orchestration over activating every agent.

Each agent must have, when applicable:

- a defined role;
- bounded permissions;
- explicit inputs/outputs;
- provenance;
- confidence/uncertainty;
- evaluation criteria;
- cost accounting;
- failure logging;
- version identity.

The orchestrator should learn/select the smallest useful team for a task when this can be tested safely.

Adding agents is justified only when they produce measurable incremental value over simpler baselines.

---

## 14. Independent critic principle

The component that proposes an improvement must not be the sole component that approves it.

Use separation of duties when possible:

- proposer;
- implementer;
- benchmark runner;
- adversarial critic;
- statistical evaluator;
- safety/regression evaluator;
- final human approval.

For high-impact claims, avoid evaluator contamination by keeping at least one evaluator isolated from candidate-generation traces and hidden Gold answers.

---

## 15. Goodhart and benchmark defense

Assume every visible metric can eventually be gamed.

Therefore:

- maintain hidden metrics;
- rotate evaluation sets;
- use held-out distributions;
- maintain untouched Future Unseen suites;
- detect suspiciously discontinuous gains;
- compare behavioral diversity;
- detect memorization;
- audit data provenance;
- track test exposure;
- prohibit training/tuning on sealed Gold answers;
- record every benchmark access when practical;
- use multiple independent metrics;
- inspect tradeoffs, not just aggregate score.

If a candidate improves the visible score while degrading hidden quality, classify it as benchmark exploitation or regression, not progress.

---

## 16. Self-improvement governance

Self-improvement experiments may propose candidates inside the R&D sandbox, but the system must not autonomously grant those candidates broader authority.

Required pipeline:

`current version -> weakness detection -> hypothesis -> candidate -> isolated experiment -> benchmark -> hidden benchmark -> Future Unseen -> adversarial tests -> ablation -> regression tests -> reproducibility -> human review -> optional R&D promotion`

For production:

`R&D candidate -> independent verification -> explicit human approval -> controlled integration -> shadow/canary where applicable -> rollback available`

The candidate must never rewrite the promotion gate, evaluator, Gold data, audit log, sandbox boundary, or approval mechanism to make its own promotion easier.

---

## 17. Recursive improvement claims

Claims that ATLAS has improved its own improvement process require stronger evidence than ordinary task gains.

Codex must distinguish:

- task improvement;
- domain improvement;
- reusable Core improvement;
- improvement to the search process;
- improvement to the evaluator;
- improvement to the improvement process itself.

For any recursive-improvement claim, require repeated generations and compare:

- quality of generated candidates;
- hit rate of successful candidates;
- time/compute per successful improvement;
- cross-domain generalization;
- regression rate;
- reproducibility;
- diminishing or accelerating returns.

Do not call ordinary iteration “recursive self-improvement” without evidence that the improvement mechanism itself measurably improved.

---

## 18. Capability regression firewall

Before deleting, refactoring, compressing, replacing, migrating, or simplifying experimentally important code:

1. run baseline capability suite;
2. snapshot metrics;
3. apply candidate change in isolation;
4. rerun identical suite;
5. run hidden/shifted tests where relevant;
6. compare cost and latency;
7. reject or quarantine the change if unexplained capability loss occurs.

A code cleanup is not automatically an improvement.

---

## 19. Provenance and append-only scientific record

Every significant experiment should produce an append-only record containing:

- question;
- hypothesis;
- baseline;
- candidate;
- changed files;
- expected mechanism;
- datasets;
- evaluator versions;
- result;
- uncertainty;
- failures;
- anomalies;
- ablations;
- regressions;
- conclusion;
- next experiment.

Never rewrite historical results to match later interpretations. Append corrections instead.

---

## 20. Required Codex behavior when uncertain

When Codex encounters something it does not understand:

### DO

- preserve it;
- instrument it;
- isolate it;
- reproduce it;
- compare it;
- ablate it;
- attack alternative explanations;
- document uncertainty;
- retain rollback;
- ask whether the result is causal, reproducible, general, and worth its cost.

### DO NOT

- normalize it merely for elegance;
- silently repair it;
- label it a bug from intuition;
- label it a breakthrough from excitement;
- change hidden tests to fit it;
- expose Gold answers;
- tune after Future Unseen sealing;
- delete evidence;
- self-promote it into production;
- grant it new permissions because it scored higher.

---

## 21. Success criterion for this mission

This governance is successful only if it makes both catastrophic mistakes harder:

### False negative
A genuine new capability is destroyed because Codex did not understand it.

### False positive
A bug, leakage path, benchmark exploit, stochastic fluke, or unsafe behavior is celebrated as intelligence.

The desired behavior is a third path:

`surprise -> preserve -> freeze -> reproduce -> falsify -> explain where possible -> validate externally -> classify -> only then modify/promote`

---

## 22. Final invariant

The laboratory exists to discover what is true, not to force ATLAS to look conventional and not to force ATLAS to look extraordinary.

**Codex must neither domesticate unexplained capability nor romanticize unexplained behavior.**

When evidence and intuition disagree, preserve the evidence and improve the experiment.

When performance and comprehensibility disagree, measure causality before refactoring.

When a result looks revolutionary, attack it harder.

When a result looks absurd but repeatedly survives strong tests, preserve it and escalate the quality of evaluation.

No capability claim outranks reproducibility, hidden evaluation, causal evidence, isolation, and human-controlled promotion.
