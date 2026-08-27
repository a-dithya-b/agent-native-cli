# Agent-Native CLI — Project Context

## What we're exploring

An **Agent-Native CLI**: a deliberately designed interface between an AI coding agent and the software environment it operates in.

The initial implementation is a portable Agent Skill that teaches agents to identify and create higher-level commands using existing repository mechanisms such as Make targets, scripts, package commands, or small CLIs.

## Core thesis

Raw shell access makes agents repeatedly reconstruct deterministic procedures and consume potentially noisy command output.

An agent-native command surface moves deterministic work out of the model and controls the information crossing the tool → model boundary.

```text
Action compression:
agent → one semantic command → many deterministic operations

Observation compression:
many lines of tool output → small decision-relevant result → agent
```

## Design principles

- Keep the agent responsible for decisions that require context or judgment.
- Move known mechanical procedures into deterministic tooling.
- Prefer small, semantic, discoverable commands.
- Return only information needed for the agent's next decision.
- Prefer structured output when the agent needs to inspect fields.
- Use meaningful exit codes for machine-detectable outcomes.
- Keep detailed diagnostics available without forcing them into every successful response.
- Make side effects explicit.
- Preserve human usability.
- Prefer existing repository mechanisms before introducing new infrastructure.

## Current implementation

The repository contains a portable Agent Skill at `skills/agent-native-cli/SKILL.md` with supporting reference documents covering command abstraction, compact output, structured output, and deterministic workflows.

The intended distribution model is **Skill first**, not product first: people should be able to point compatible coding agents at the Skill and use it against their repositories.

## What has happened so far

1. Defined the Agent-Native CLI concept.
2. Created the Skill.
3. Used the Skill with Claude Code on a real repository.
4. Claude created an agent-oriented Make command surface for tests, coverage, dependency auditing, and migration status.
5. Ran the same task set with and without that command surface.
6. Captured both Claude Code sessions as JSONL and analyzed them independently.

## Current evidence

Experiment 001 provides preliminary evidence that an agent-native command surface can reduce command volume and tool-output volume. Detailed results are recorded separately in `EXPERIMENTS.md`.

This is **not yet evidence of general performance**: the experiment used one repository and one model/configuration. See `HYPOTHESES.md` for what remains unproven.

## Current hypothesis

A well-designed agent-native command surface can reduce procedural reasoning, model-generated command volume, tool interactions, and irrelevant tool output while preserving enough information for the agent to make correct decisions.

## Current stage

**Phase 2 — controlled validation.**

The next step is an independent experiment on a different repository and stack using the same baseline-vs-agent-native methodology.
