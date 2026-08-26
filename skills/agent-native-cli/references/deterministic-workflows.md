# Deterministic Workflows

## Principle

If a workflow is mostly mechanical and its steps are known, encode those steps in deterministic tooling instead of asking the model to reconstruct them on every run.

## Good fit

```text
build → test → package → publish
```

A script or Make target can own this sequence while the agent decides only when and why to invoke it.

## Benefits

- fewer model decisions
- fewer tool calls
- less generated command text
- more repeatable behavior
- easier testing
- clearer failure boundaries

## Keep the agent in control

Do not encode decisions that genuinely require context or judgment. The agent should decide what needs to happen; deterministic tooling should execute known procedures reliably.
