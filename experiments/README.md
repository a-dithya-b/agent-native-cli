# Experiments

These are small real-repository experiments used to validate the idea behind the Skill.

They are intentionally practical rather than benchmark-style studies. The goal is to see whether a better interface helps an agent handle deterministic, repeatable repository work with less procedural effort.

## Results so far

- **[001 — Python repository](001/results.md):** strong reductions in command construction and tool output, including during repeated work.
- **[002 — TypeScript backend](002/results.md):** fewer Bash calls, generated commands, command characters, and debugging interactions during the initial run. The repeat phase was less conclusive because the baseline agent created its own reusable wrapper.

The results support the idea without claiming that the same improvement will occur in every repository or with every agent.
