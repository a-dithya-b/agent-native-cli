# Experiment 002 — TypeScript backend

A second real-repository experiment to see whether the agent-native approach is useful beyond the first Python repository.

## Task

The agent was asked to run the repository's pre-PR quality checks:

- clean dependency install
- dependency audit
- lint
- production build
- tests and coverage
- diff coverage
- database validation when relevant

The agent had to discover the appropriate commands from the repository and its CI configuration.

## Conditions

**Baseline:** the repository did not have the agent-native interface. The agent was free to use the repository's existing tooling and shell commands.

**Agent-native:** the repository had the command surface created using the Agent-Native CLI Skill.

The same task was used in both sessions. The task was then repeated twice.

## What we observed

During the initial run, the agent-native condition used:

- 25% fewer Bash calls
- 30% fewer generated commands
- 59% fewer command characters
- 10% less tool output
- 36% fewer agent output tokens
- 42% fewer debugging calls

The underlying verification work was still performed. The difference was mainly in the procedural work around discovering, constructing, and debugging the workflow.

## An important caveat

During the repeat phase, the baseline agent created its own `qa.sh` wrapper and reused it. This made the repeat comparison less clean: the baseline had effectively created an abstraction of its own.

For that reason, this experiment should be read as evidence that the approach can reduce procedural work during initial execution—not as proof of a universal advantage for repeated execution.

## Data

Raw Claude Code JSONL transcripts were captured for both sessions and analyzed independently. The raw transcripts are retained outside the repository.

## Interpretation

This is a small real-world experiment, not a benchmark. It supports the idea that agents can benefit from a deliberate interface to deterministic repository workflows, while also showing that results depend on the repository and on what abstractions already exist.

See `results.md` for the measurements and details.
