# Experiment 001

## Objective

Determine whether an agent-native command surface changes agent behavior and reduces command/tool-output volume for common repository maintenance tasks.

## Task

The agent was asked to:

> Run the tests, check coverage, audit the dependencies for vulnerabilities, and check the DB migration status.

The same task was repeated two additional times after the initial run.

## Model / agent

- Agent: Claude Code
- Model: `claude-opus-5`
- Mode: `auto`

## Conditions

### Baseline

The repository had no agent-native Make command surface. The agent was free to use the repository's existing tooling and shell commands.

### Agent-native

The same repository was given an agent-native command surface generated using the Agent-Native CLI Skill. The agent was free to use that interface.

## Control

The task wording was kept the same across conditions. The agent was not told that token efficiency was being measured or instructed to prefer one condition's mechanism.

## Data

Claude Code JSONL transcripts were captured for both sessions and analyzed independently.

The raw transcripts are retained outside this repository's source tree for the current experiment.

## Reproducing the analysis

The transcript analyzer used for this experiment is available at [`scripts/analyze_claude_transcripts.py`](../../scripts/analyze_claude_transcripts.py).

```bash
python scripts/analyze_claude_transcripts.py \
  --baseline /path/to/baseline.jsonl \
  --agent-native /path/to/agent-native.jsonl \
  --output-dir /tmp/transcript-analysis
```

It writes a Markdown comparison report plus CSV and JSON details for each Bash call. Tool-output token counts are estimates based on UTF-8 byte size; the default estimator is 4 bytes per token and can be changed with `--bytes-per-token`.

## Limitations

- One repository.
- One model/configuration.
- Agent behavior is non-deterministic.
- Tool-output token counts in the current analysis are estimates based on 1 token per 4 UTF-8 bytes.
- Cache-token accounting complicates direct interpretation of total token usage.
- Three executions are insufficient to establish general statistical significance.

## Result

See `results.md` for the observed measurements and interpretation boundaries.
