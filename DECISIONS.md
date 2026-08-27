# Decisions

## 2026-08-27 — Skill first

**Decision:** Start as a portable Agent Skill rather than a standalone product.

**Reason:** The concept can be tested and distributed with low implementation cost. Product direction should follow evidence.

## 2026-08-27 — Agent-native, not Makefile-specific

**Decision:** Treat Makefiles, scripts, package commands, and small CLIs as implementation mechanisms rather than the definition of the concept.

**Reason:** The underlying idea is a deliberate agent/tool interface, not a particular command runner.

## 2026-08-27 — Optimize both sides of the boundary

**Decision:** Evaluate both action compression and observation compression.

**Reason:** Shorter commands alone do not solve the problem if their output remains noisy.

## 2026-08-27 — Measure independently

**Decision:** Do not rely on agents to report token savings or performance improvements.

**Reason:** Raw agent transcripts and independently derived metrics provide stronger evidence.

## 2026-08-27 — Freeze the Skill during experiments

**Decision:** Avoid changing the Skill or treatment interface in response to an experiment while that experiment is being evaluated.

**Reason:** Iterative tuning during measurement makes attribution harder.

## 2026-08-27 — No premature productization

**Decision:** Validate the interface pattern across independent repositories before deciding whether to build tooling or a product.

**Reason:** Current evidence is from a single repository and model configuration.
