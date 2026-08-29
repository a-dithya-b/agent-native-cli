# Experiment 002 — Results

## Initial execution

| Metric | Baseline | Agent-native | Reduction |
|---|---:|---:|---:|
| Bash calls | 28 | 21 | 25% |
| Commands generated | 119 | 83 | 30% |
| Command characters | 5,107 | 2,104 | 59% |
| Tool-output bytes | 32,748 | 29,381 | 10% |
| Estimated tool-output tokens | 8,188 | 7,345 | 10% |
| Agent output tokens | 10,774 | 6,918 | 36% |
| Exploration calls | 11 | 9 | 18% |
| Debugging calls | 12 | 7 | 42% |

Mechanical verification calls were unchanged at 5 per session. The underlying checks still had to run; the reduction was mainly in the procedural work around them.

## Repeated executions

The repeat phase was mixed rather than consistently better for the agent-native condition.

| Metric | Baseline | Agent-native |
|---|---:|---:|
| Bash calls | 4 | 6 |
| Commands generated | 15 | 52 |
| Command characters | 2,893 | 2,329 |
| Tool-output bytes | 1,913 | 1,941 |
| Agent output tokens | 2,255 | 2,349 |

The baseline agent created a `qa.sh` wrapper during the first run and reused it for the repeats. This means the baseline had independently created a deterministic abstraction, so the repeat phase is not a clean comparison of raw shell versus agent-native tooling.

## What this suggests

The two experiments point in the same direction during initial workflow discovery: a deliberate command surface can reduce the amount of procedural work an agent has to construct around deterministic tasks.

The size of the effect varies by repository. Experiment 001 showed a larger reduction in tool output; Experiment 002 showed a larger reduction in debugging activity but only a modest reduction in tool-output volume.

That variation is expected. The value of an agent-native interface depends on the repository, its existing tooling, the workflow, and the agent's behavior.

## Limits

- Two repositories are not enough to establish general performance claims.
- Agent behavior is non-deterministic.
- Tool-output token counts are estimates based on UTF-8 bytes / 4, not tokenizer-derived counts.
- Total cost is affected by prompt caching and should not be inferred from command or output volume alone.
- The repeat phase in this experiment was confounded by the baseline agent creating its own reusable wrapper.
- Diff coverage was not meaningfully exercised because there were no relevant changed lines against the comparison base.

The purpose of these experiments is to validate the usefulness of the design pattern, not to claim a universal percentage improvement.
