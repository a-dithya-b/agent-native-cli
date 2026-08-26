# Agent-Native CLI

An Agent Skill for designing token-efficient, deterministic CLI interfaces for AI coding agents.

## Idea

AI agents often interact with engineering environments through low-level shell commands. This can create unnecessary model output, noisy tool input, fragile multi-step workflows, and repeated reasoning about mechanical operations.

Agent-Native CLI treats the command/tool boundary as an interface that should be designed for an agent.

```text
Human-facing workflow
        ↓
scripts / Make / CLI
        ↓
agent-native interface
        ↓
      Agent
```

The goal is not to replace the shell. It is to expose a small, predictable, discoverable command surface that:

- moves deterministic work out of the model
- minimizes information crossing the tool → model boundary
- returns decision-relevant output
- uses explicit failure semantics
- remains usable by humans

## Skill

The portable skill lives at [`skills/agent-native-cli/SKILL.md`](skills/agent-native-cli/SKILL.md).

The skill can be pointed at a repository or workflow and used to identify or design agent-native commands.

## Status

Early exploration. The next step is to benchmark raw shell workflows against agent-native interfaces on representative coding tasks.

## Principles

- [Command abstraction](skills/agent-native-cli/references/command-abstraction.md)
- [Compact output](skills/agent-native-cli/references/compact-output.md)
- [Structured output](skills/agent-native-cli/references/structured-output.md)
- [Deterministic workflows](skills/agent-native-cli/references/deterministic-workflows.md)

## License

MIT
