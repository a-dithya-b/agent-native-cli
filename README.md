# Agent-Native CLI

### Make coding agents better at repeatable work.

Coding agents are great at making decisions. They are less interesting when they have to repeatedly reconstruct the same mechanical procedure:

```text
inspect → remember commands → run several steps → parse noisy output → repeat
```

**Agent-Native CLI** is a portable Skill that teaches coding agents to turn those procedures into small, deterministic, agent-friendly commands.

The idea is simple:

```text
Instead of:
agent → many shell commands → lots of output

Prefer:
agent → one meaningful command → useful result
```

The shell, Make, npm scripts, Python scripts, and small CLIs can still do the work. The Skill is about designing the interface the agent uses to reach them.

## Why use it?

A good agent-facing command surface can:

- reduce repeated command construction
- keep deterministic work out of the model
- return only information the agent needs to make its next decision
- make common repository workflows easier to discover and reuse
- preserve normal developer workflows

It is especially useful for things like tests, builds, linting, migrations, releases, checks, audits, and other multi-step repository procedures.

## Try the Skill

The Skill is self-contained and does not require a framework or runtime.

**[Open `SKILL.md`](skills/agent-native-cli/SKILL.md)** and give it to your coding agent.

Then ask the agent to review a repository and identify repetitive workflows that could benefit from a better command interface.

The Skill works with existing repository mechanisms. It does not require you to adopt Make, replace your CLI, or introduce new infrastructure.

## What it teaches

The Skill focuses on two sides of the agent/tool boundary:

**Action compression** — turn a known multi-step procedure into one semantic operation.

**Observation compression** — return a small, decision-relevant result instead of making the agent process pages of routine output.

The agent should still make the decisions. The repository should handle the known procedure.

## Does it actually help?

We tried the approach on two different repositories: a Python project and a TypeScript backend.

In the initial task execution, the agent-native interface produced fewer shell interactions and substantially less command construction in both experiments.

In the first experiment, for example:

| | Without the Skill | With the Skill |
|---|---:|---:|
| Bash calls | 10 | 7 |
| Commands generated | 52 | 23 |
| Command characters | 1,589 | 536 |
| Tool output | 21.5 KB | 8.4 KB |
| Agent output tokens | 4,745 | 1,958 |

In the second experiment, the initial run showed a smaller but still clear reduction in procedural work: **28 → 21 Bash calls**, **119 → 83 generated commands**, and **5,107 → 2,104 command characters**.

These are small, practical experiments—not a benchmark or a claim that the Skill will produce the same improvement everywhere. Repository tooling, workflows, and agent behavior all matter.

The useful result so far is simpler: **when work is deterministic and repeated, giving an agent a better interface to that work can reduce the effort needed to perform it.**

[Read the experiments](experiments/001/results.md)

## What's in the repository?

```text
skills/agent-native-cli/
├── SKILL.md
└── references/
    ├── command-abstraction.md
    ├── compact-output.md
    ├── structured-output.md
    └── deterministic-workflows.md
```

The references explain the ideas behind the Skill, but you can start with `SKILL.md` alone.

## The principle

> **Let the agent decide what to do. Let deterministic tooling handle how to do it.**

If a repository has a procedure an agent keeps reconstructing, make that procedure a capability the agent can discover and reuse.

## License

MIT
