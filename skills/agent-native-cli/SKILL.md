---
name: agent-native-cli
description: Design and improve CLI, scripts, Make targets, and tool interfaces for AI coding agents. Use when a repository exposes repetitive shell workflows, noisy command output, fragile multi-step operations, or tooling that could be made more deterministic, discoverable, structured, and token-efficient.
---

# Agent-Native CLI

Treat the command/tool boundary as an interface for an agent, not just a way to expose shell commands.

## Core approach

When designing or reviewing a workflow:

1. Identify repeated multi-step operations.
2. Move mechanical, deterministic work out of the model and into scripts, Make targets, or higher-level CLI commands.
3. Give the agent a small, semantic command surface.
4. Minimize output crossing the tool → model boundary.
5. Return only information needed for the agent's next decision.
6. Use structured output when the agent needs to inspect fields or make decisions.
7. Use exit codes and explicit failure semantics for machine-detectable outcomes.
8. Keep commands discoverable and composable.
9. Preserve human usability; do not optimize for agents by making normal development harder.

## Important distinction

Optimize both sides of the boundary:

```text
Action compression:
agent → one semantic command → many deterministic operations

Observation compression:
many lines of tool output → small decision-relevant result → agent
```

Short commands alone are not enough. A command that returns thousands of irrelevant lines can still be expensive for an agent.

## Design checklist

For each candidate command, consider:

- Is the operation deterministic enough to move outside the model?
- Can several low-level commands become one semantic operation?
- What is the smallest useful input surface?
- What output does the agent actually need?
- Can stdout be reduced without hiding important failures?
- Should the result be structured?
- Are exit codes meaningful?
- Is the command safe and explicit about side effects?
- Can the agent discover how to use it without reading implementation details?

## References

Read these when relevant:

- `references/command-abstraction.md`
- `references/compact-output.md`
- `references/structured-output.md`
- `references/deterministic-workflows.md`

## Do not over-engineer

Prefer existing repository mechanisms first. A Make target, shell script, package script, or small CLI command is often enough. Do not introduce a framework merely to satisfy this skill.
