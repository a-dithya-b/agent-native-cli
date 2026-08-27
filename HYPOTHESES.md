# Hypotheses

These are working hypotheses, not established facts.

## H1 — Procedural reasoning

An agent-native command surface reduces the amount of procedural reasoning required for repetitive engineering workflows.

**Status:** Preliminary support

Experiment 001 showed fewer generated commands and fewer mechanical Bash calls, but this needs replication.

## H2 — Action compression

Higher-level deterministic commands reduce model-generated command volume and tool interactions.

**Status:** Preliminary support

Experiment 001: 117 → 43 generated commands; 14 → 9 Bash calls.

## H3 — Observation compression

Commands designed to return compact, decision-relevant output reduce the amount of information that must cross the tool → model boundary.

**Status:** Preliminary support

Experiment 001: 30,955 → 9,419 output bytes; estimated output tokens 7,739 → 2,355.

## H4 — Repeated-work advantage

The benefit is especially pronounced when the same workflow is executed repeatedly because deterministic tooling prevents the agent from reconstructing the procedure each time.

**Status:** Preliminary support

Experiment 001 rounds 2–3: estimated tool-output tokens fell 90% and generated commands fell 69%.

## H5 — Generalization

The observed effect generalizes across repositories, technology stacks, and workflow types.

**Status:** Unknown

Requires independent experiments.

## H6 — Agent performance

Agent-native interfaces improve practical agent performance beyond token usage, including latency, reliability, retries, and task completion.

**Status:** Unknown

Requires controlled measurement.

## H7 — Product opportunity

There is sufficient recurring value in agent-native interface design to justify tooling beyond a portable Skill.

**Status:** Unknown

Do not optimize for a product until the underlying pattern is validated.
