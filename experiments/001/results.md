# Experiment 001 — Results

## Question A — initial discovery (round 1)

| Metric | Baseline | Agent-native | Reduction |
|---|---:|---:|---:|
| Bash calls | 10 | 7 | 30.0% |
| Commands generated | 52 | 23 | 55.8% |
| Command characters | 1,589 | 536 | 66.3% |
| Tool-output bytes | 21,464 | 8,445 | 60.7% |
| Estimated tool-output tokens | 5,365 | 2,111 | 60.6% |
| Agent output tokens | 4,745 | 1,958 | 58.8% |

### Classification

| Classification | Baseline | Agent-native |
|---|---:|---:|
| Exploration | 2 | 3 |
| Test Execution | 2 | 0 |
| Coverage | 0 | 1 |
| Dependency Audit | 2 | 2 |
| Migration | 4 | 1 |
| Debugging | 0 | 0 |

### Token accounting

| | Baseline | Agent-native |
|---|---:|---:|
| Input tokens | 22 | 16 |
| Output tokens | 4,745 | 1,958 |
| Cache-read tokens | 405,504 | 267,025 |
| Cache-created tokens | 46,993 | 40,159 |
| Cache tokens | 452,497 | 307,184 |

## Question B — repeated work (rounds 2–3 combined)

| Metric | Baseline | Agent-native | Reduction |
|---|---:|---:|---:|
| Bash calls | 4 | 2 | 50.0% |
| Commands generated | 65 | 20 | 69.2% |
| Command characters | 1,839 | 388 | 78.9% |
| Tool-output bytes | 9,491 | 974 | 89.7% |
| Estimated tool-output tokens | 2,374 | 244 | 89.7% |
| Agent output tokens | 1,665 | 1,003 | 39.8% |

### Classification

| Classification | Baseline | Agent-native |
|---|---:|---:|
| Exploration | 0 | 0 |
| Test Execution | 0 | 0 |
| Coverage | 2 | 2 |
| Dependency Audit | 2 | 2 |
| Migration | 2 | 2 |
| Debugging | 0 | 0 |

### Token accounting

| | Baseline | Agent-native |
|---|---:|---:|
| Input tokens | 8 | 6 |
| Output tokens | 1,665 | 1,003 |
| Cache-read tokens | 192,882 | 123,220 |
| Cache-created tokens | 4,239 | 1,145 |
| Cache tokens | 197,121 | 124,365 |

## Individual repeated rounds

### Round 2

| Metric | Baseline | Agent-native | Reduction |
|---|---:|---:|---:|
| Bash calls | 2 | 1 | 50.0% |
| Commands generated | 34 | 10 | 70.6% |
| Command characters | 977 | 194 | 80.0% |
| Tool-output bytes | 4,937 | 487 | 90.1% |
| Estimated tool-output tokens | 1,235 | 122 | 90.1% |
| Agent output tokens | 989 | 319 | 67.7% |

### Round 3

| Metric | Baseline | Agent-native | Reduction |
|---|---:|---:|---:|
| Bash calls | 2 | 1 | 50.0% |
| Commands generated | 31 | 10 | 67.7% |
| Command characters | 862 | 194 | 77.5% |
| Tool-output bytes | 4,554 | 487 | 89.3% |
| Estimated tool-output tokens | 1,139 | 122 | 89.3% |
| Agent output tokens | 676 | 684 | -1.2% |

## Interpretation boundary

The measurements show substantial reductions in command volume and observed tool-output volume in this experiment. They do not establish general performance improvements, causal attribution beyond the tested conditions, or a product opportunity.

The most notable observation is that repeated work retained the effect: the agent-native condition used substantially fewer commands and much less tool output in rounds 2–3.

Tool-output token values are estimates, not tokenizer-derived counts.
