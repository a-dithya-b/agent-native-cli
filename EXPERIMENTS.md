# Experiments

## Experiment 001 — Agent-native command surface

### Objective

Compare an agent performing a fixed engineering task directly through shell commands against the same agent using an agent-native command surface created with the Skill.

### Task

The agent was asked to:
1. Run tests
2. Check coverage
3. Audit dependencies for vulnerabilities
4. Check DB migration status

The same task list was used for both scenarios. The task was repeated two additional times after the initial run to simulate repeated work.

### Conditions

- Model: Claude Opus 5
- Mode: auto
- Baseline: no Makefile / agent-native command surface; direct repository tooling
- Agent-native: Makefile / command surface created after applying the Agent-Native CLI Skill
- Both sessions used the same task list
- JSONL transcripts were captured and analyzed independently

### Aggregate transcript results

| Metric | Baseline | Agent-native | Reduction |
|---|---:|---:|---:|
| Bash calls | 14 | 9 | 35.7% |
| Commands generated | 117 | 43 | 63.2% |
| Command characters | 3,428 | 924 | 73.0% |
| Tool-output bytes | 30,955 | 9,419 | 69.6% |
| Estimated tool-output tokens | 7,739 | 2,355 | 69.6% |
| Agent output tokens | 6,410 | 2,961 | 53.8% |
| Cache-read tokens | 598,386 | 390,245 | 34.8% |
| Cache-created tokens | 51,232 | 41,304 | 19.4% |

Tool-output tokens were estimated at 1 token per 4 UTF-8 bytes.

### Question A — initial discovery (round 1)

| Metric | Baseline | Agent-native |
|---|---:|---:|
| Bash calls | 10 | 7 |
| Commands generated | 52 | 23 |
| Command characters | 1,589 | 536 |
| Tool-output bytes | 21,464 | 8,445 |
| Estimated tool-output tokens | 5,365 | 2,111 |
| Agent output tokens | 4,745 | 1,958 |
| Exploration calls | 2 | 3 |
| Mechanical calls | 8 | 4 |

### Question B — repeated work (rounds 2–3 combined)

| Metric | Baseline | Agent-native |
|---|---:|---:|
| Bash calls | 4 | 2 |
| Commands generated | 65 | 20 |
| Command characters | 1,839 | 388 |
| Tool-output bytes | 9,491 | 974 |
| Estimated tool-output tokens | 2,374 | 244 |
| Agent output tokens | 1,665 | 1,003 |
| Exploration calls | 0 | 0 |
| Mechanical calls | 4 | 2 |

### Individual repeated rounds

#### Round 2

| Metric | Baseline | Agent-native |
|---|---:|---:|
| Bash calls | 2 | 1 |
| Commands generated | 34 | 10 |
| Command characters | 977 | 194 |
| Tool-output bytes | 4,937 | 487 |
| Estimated tool-output tokens | 1,235 | 122 |
| Agent output tokens | 989 | 319 |

#### Round 3

| Metric | Baseline | Agent-native |
|---|---:|---:|
| Bash calls | 2 | 1 |
| Commands generated | 31 | 10 |
| Command characters | 862 | 194 |
| Tool-output bytes | 4,554 | 487 |
| Estimated tool-output tokens | 1,139 | 122 |
| Agent output tokens | 676 | 684 |

### Observations

- The agent-native interface reduced generated command volume substantially.
- Tool-output volume fell substantially, especially during repeated work.
- The agent-native agent used fewer mechanical Bash calls.
- The interface changed the agent's task decomposition from reconstructing low-level procedures toward invoking semantic capabilities.
- Round 3 agent output tokens were essentially unchanged despite much smaller command and tool-output volume, suggesting that the savings are not simply caused by making the agent's final response shorter.

### Limitations

- One repository
- One model/configuration
- Agent behavior is nondeterministic
- Tool-output token counts are estimates
- Cache behavior complicates direct cost interpretation
- Different execution paths can introduce confounding factors
- Results do not establish generality or causality

### Next

Experiment 002: independent repository and stack, using the same baseline-vs-agent-native methodology.
