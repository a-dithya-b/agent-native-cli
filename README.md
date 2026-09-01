# Agent-Native CLI

### Make coding agents better at repeatable work.

Coding agents are great at making decisions. They are less interesting when they have to repeatedly reconstruct the same mechanical procedure:

```text
inspect → remember commands → run several steps → parse noisy output → repeat
```

**Agent-Native CLI** is a portable Skill that teaches coding agents to turn those procedures into small, deterministic, agent-friendly commands.

> **Let the agent decide what to do. Let deterministic tooling handle how to do it.**

## Install

Install the Skill from this repository with the Agent Skills CLI:

```bash
npx skills add a-dithya-b/agent-native-cli --skill agent-native-cli
```

Run that from the repository where you want to use the Skill. The CLI will let you choose a supported coding agent and installs the Skill for that project.

For Claude Code specifically:

```bash
npx skills add a-dithya-b/agent-native-cli --skill agent-native-cli --agent claude-code
```

To install it globally instead of per-project, add `--global`.

You can also use the Skill manually by opening [`skills/agent-native-cli/SKILL.md`](skills/agent-native-cli/SKILL.md) and giving it to your coding agent.

## Why this exists

A repository often already knows how to perform a task. The problem is that an agent may still have to rediscover the sequence of commands, invoke each step, and process routine output every time.

The idea is to create a better interface at the agent/tool boundary:

```text
Instead of:
agent → many shell commands → lots of output

Prefer:
agent → one meaningful command → useful result
```

This is not about replacing the shell or standardizing on Make. Make, npm scripts, Python scripts, shell scripts, and small CLIs can all remain the implementation mechanisms. The Skill is about designing the interface the agent uses to reach them.

## Try it

The Skill is self-contained and does not require a framework or runtime.

**[Open `SKILL.md`](skills/agent-native-cli/SKILL.md)** and give it to your coding agent.

Then ask the agent to review a repository and identify repetitive workflows that could benefit from a better command interface.

The Skill works with existing repository mechanisms. It does not require you to adopt Make, replace your CLI, or introduce new infrastructure.

## Help test the idea

This project is intentionally an open experiment. **The most useful contribution right now is running the Skill on a repository we haven't tested and reporting what happened.**

Try it on a real codebase, compare the workflow with and without the Skill, and [submit an experiment report](CONTRIBUTING.md).

Both positive and negative results are useful. In particular, we're interested in cases where:

- the Skill clearly reduces procedural work
- the effect is small or disappears
- the agent creates its own abstraction without the Skill
- a command surface makes things worse
- a workflow is difficult to make agent-friendly

The goal is to learn **when and why** agent-native interfaces help, not to collect only favorable results.

## What it teaches

The Skill focuses on two sides of the agent/tool boundary:

**Action compression** — turn a known multi-step procedure into one semantic operation.

**Observation compression** — return a small, decision-relevant result instead of making the agent process pages of routine output.

The agent should still make the decisions. The repository should handle the known procedure.

## What we've seen so far

We've run the approach on two different repositories: a Python project and a TypeScript backend.

In the initial task execution, the agent-native interface reduced procedural work in both experiments, although the size of the effect varied.

### Experiment 001

| | Without the Skill | With the Skill |
|---|---:|---:|
| Bash calls | 10 | 7 |
| Commands generated | 52 | 23 |
| Tool output | 21.5 KB | 8.4 KB |
| Agent output tokens | 4,745 | 1,958 |

### Experiment 002

| | Without the Skill | With the Skill |
|---|---:|---:|
| Bash calls | 28 | 21 |
| Commands generated | 119 | 83 |
| Command characters | 5,107 | 2,104 |
| Agent output tokens | 10,774 | 6,918 |

The repeat phase of Experiment 002 was not a clean comparison because the baseline agent created its own reusable `qa.sh` wrapper during the first run. That is exactly the kind of behavior this project needs to account for: agents can create abstractions themselves, and not every repository benefits equally from a pre-designed interface.

These are small, practical experiments—not a benchmark or a claim that the Skill will produce the same improvement everywhere. Repository tooling, workflows, and agent behavior all matter.

**[Read the experiments](experiments/README.md)**

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

## What's next?

The current goal is validation, not productization. We want to understand which interface patterns consistently help across repositories, workflows, coding agents, and models.

Community experiments can help answer that faster than building more infrastructure prematurely.

## License

MIT
