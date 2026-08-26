---
name: agent-native-cli
description: Design and improve CLI, scripts, Make targets, and tool interfaces for AI coding agents. Use when a repository exposes repetitive shell workflows, noisy command output, fragile multi-step operations, or tooling that could be made more deterministic, discoverable, structured, and token-efficient.
---

# Agent-Native CLI

Treat the command/tool boundary as an interface for an agent, not just a way to expose shell commands.

## Core approach

When designing or reviewing a workflow:

1. Inspect the repository's existing commands, scripts, CI, and development conventions first.
2. Identify repeated multi-step operations and mechanical work.
3. Move deterministic work out of the model and into scripts, Make targets, or higher-level CLI commands.
4. Give the agent a small, semantic command surface.
5. Minimize output crossing the tool → model boundary.
6. Return only information needed for the agent's next decision.
7. Use structured output when the agent needs to inspect fields or make decisions.
8. Use exit codes and explicit failure semantics for machine-detectable outcomes.
9. Make side effects, required inputs, and destructive behavior explicit.
10. Keep commands discoverable and composable.
11. Preserve human usability; do not optimize for agents by making normal development harder.

## Important distinction

Optimize both sides of the boundary:

```text
Action compression:
agent → one semantic command → many deterministic operations

Observation compression:
many lines of tool output → small decision-relevant result → agent
```

Short commands alone are not enough. A command that returns thousands of irrelevant lines can still be expensive for an agent.

## Agent vs deterministic tooling

Keep the agent responsible for decisions that require context or judgment:

```text
Agent:
what should happen?
when should it happen?
which option is appropriate?

Deterministic tooling:
how should the known procedure execute?
what exact commands are required?
how should known results be summarized?
```

Do not hide meaningful decisions inside scripts merely to reduce model interaction.

## Output contract

Prefer a deliberate separation between the primary agent-facing result and diagnostics:

```text
stdout → compact result / next-decision information
exit code → machine-detectable success or failure
stderr/logs → detailed diagnostics when needed
```

Do not discard actionable errors merely to reduce tokens. Preserve a path to full diagnostics without forcing them into every successful tool response.

## Design checklist

For each candidate command, consider:

- Is the operation deterministic enough to move outside the model?
- Can several low-level commands become one semantic operation?
- What is the smallest useful input surface?
- What decisions still belong to the agent?
- What output does the agent actually need?
- Can stdout be reduced without hiding important failures?
- Should the result be structured?
- Are exit codes meaningful?
- Are side effects explicit and safe?
- Can detailed diagnostics be retrieved separately?
- Can the agent discover how to use it without reading implementation details?
- Does the interface remain convenient for humans?

## Working method

When asked to improve a repository:

1. Inspect before changing.
2. Reuse existing repository mechanisms where practical.
3. Identify a small set of high-value workflows.
4. Implement the smallest useful command surface.
5. Preserve existing behavior and CI unless the task explicitly calls for a change.
6. Document the command contract and discoverability path.
7. Measure the result separately; do not claim token savings without an actual measurement.

## References

Read these when relevant:

- `references/command-abstraction.md`
- `references/compact-output.md`
- `references/structured-output.md`
- `references/deterministic-workflows.md`

## Do not over-engineer

Prefer existing repository mechanisms first. A Make target, shell script, package script, or small CLI command is often enough. Do not introduce a framework merely to satisfy this skill.
