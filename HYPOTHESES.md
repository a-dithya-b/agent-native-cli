# Hypotheses

These are working hypotheses, not established facts.

## H1 — Less procedural work

An agent-native command surface can reduce the amount of procedural reasoning required for repetitive engineering workflows.

**Status:** Preliminary support

Both initial experiments showed fewer commands and shell interactions in the agent-native condition. The second experiment also showed fewer debugging interactions.

## H2 — Action compression

Higher-level deterministic commands can reduce the amount of command construction and tool interaction required from an agent.

**Status:** Preliminary support

The effect appeared in both a Python repository and a TypeScript backend, although its size varied.

## H3 — Observation compression

Commands designed to return compact, decision-relevant output can reduce the amount of information an agent has to process.

**Status:** Preliminary support, with variation

Experiment 001 showed a large reduction in tool output. Experiment 002 showed a smaller reduction, suggesting that the benefit depends on the workflow and repository.

## H4 — Repeated work

A reusable deterministic interface should be particularly useful when an agent performs the same procedure repeatedly.

**Status:** Plausible, not yet cleanly established

Experiment 001 showed a strong repeated-work effect. In Experiment 002, the baseline agent independently created and reused a `qa.sh` wrapper, making the repeat comparison confounded.

## H5 — Generalization

The design pattern is useful across different repositories, stacks, and workflows.

**Status:** Early support

The approach has now been used on a Python repository and a TypeScript backend. More real-world use will be more informative than trying to establish a universal percentage improvement.

## H6 — Practical usefulness

A better agent-facing interface can make common repository workflows easier for agents to discover, execute, and reuse without hiding meaningful decisions.

**Status:** Preliminary support

The experiments show reduced procedural interaction while preserving the underlying verification work. Real-world usage is the next useful test.
