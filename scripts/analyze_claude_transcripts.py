#!/usr/bin/env python3
"""Compare Bash-tool efficiency between two Claude Code JSONL transcripts.

Usage:
    python scripts/analyze_claude_transcripts.py \
      --baseline /path/to/baseline.jsonl \
      --agent-native /path/to/agent-native.jsonl \
      --output-dir /tmp/transcript-analysis

The tool writes:
  * bash_calls.csv: one row per Bash call, including the paired tool result
  * bash_calls.json: the same detailed data in a typed, lossless structure
  * report.md: initial and repeated-work comparison tables

Token accounting comes from transcript ``message.usage`` fields. Tool-output
tokens are estimates because Claude Code transcripts retain output text, not
the tokenizer result. The estimator uses the configurable bytes-per-token
ratio (default 4.0) and labels all estimates accordingly.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable


TOKEN_RATIO_DEFAULT = 4.0
MECHANICAL_CATEGORIES = ("test execution", "coverage", "dependency audit", "migration")
ROUND_MARKER_RE = re.compile(r"\b(?:pass|round|run)\s+([123])\b", re.IGNORECASE)
HEREDOC_RE = re.compile(
    r"""<<-?[ \t]*(['\"]?)(\w+)\1\r?\n.*?(?:\r?\n\2(?:\r?\n|$)|$)""",
    re.DOTALL,
)

EXPLORATION_RE = re.compile(
    r"\b(?:ls|pwd|tree|find|rg|grep|cat|sed|head|tail|git\s+(?:status|log|diff|branch|show|ls-files)|"
    r"which|where|type|stat|wc)\b",
    re.IGNORECASE,
)
TEST_RE = re.compile(
    r"\b(?:(?:python(?:3)?\s+-m\s+)?pytest\b(?!\.)|tox|nox|unittest|make\s+(?:test|retest)|"
    r"(?:npx\s+)?jest\b(?!\.)|npm(?:\s+run)?(?:\s+--silent)?\s+test\b|"
    r"npm\s+run(?:\s+--silent)?\s+verify(?:\b|:)|node\s+scripts/verify)\b",
    re.I,
)
COVERAGE_RE = re.compile(
    r"(?:--cov(?:age)?(?:Reporters)?\b|pytest-cov|\bmake\s+(?:cov|check)\b|"
    r"diff-cover\s+\S+\.(?:info|lcov|xml)|verify:ci\b|--coverage\b|"
    r"coverage\s+(?:run|xml|report|html)\b)",
    re.I,
)
AUDIT_RE = re.compile(r"\b(?:pip[-_]audit|python(?:3)?\s+-m\s+pip_audit|npm\s+audit|make\s+audit)\b", re.I)
MIGRATION_RE = re.compile(r"\b(?:alembic|make\s+migration)\b", re.I)
DEBUG_RE = re.compile(
    r"\b(?:debug|traceback|stacktrace|diagnos(?:e|tic)|inspect|show\s+.*(?:log|error)|"
    r"printenv|--version)\b",
    re.I,
)
WORK_RE = re.compile(r"\b(?:npm|npx|node|python(?:3)?|make|pip(?:3|x)?)\b", re.I)


@dataclass
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cache_creation_tokens: int = 0

    @property
    def cache_tokens(self) -> int:
        return self.cache_read_tokens + self.cache_creation_tokens


@dataclass
class BashCall:
    session_round: int
    experiment_round: int
    assistant_turn: int
    tool_use_id: str
    command: str
    description: str
    tool_result: str
    is_error: bool
    categories: list[str]
    is_repeated_phase: bool
    command_count: int
    command_characters: int
    tool_output_bytes: int
    tool_output_tokens_estimate: int
    usage: Usage


@dataclass
class TranscriptAnalysis:
    name: str
    source: str
    calls: list[BashCall] = field(default_factory=list)
    assistant_usage: Usage = field(default_factory=Usage)
    assistant_usage_by_round: dict[int, Usage] = field(default_factory=dict)


def integer(value: Any) -> int:
    return value if isinstance(value, int) else 0


def add_usage(target: Usage, source: Usage, multiplier: int = 1) -> None:
    target.input_tokens += multiplier * source.input_tokens
    target.output_tokens += multiplier * source.output_tokens
    target.cache_read_tokens += multiplier * source.cache_read_tokens
    target.cache_creation_tokens += multiplier * source.cache_creation_tokens


def usage_from_message(message: dict[str, Any]) -> Usage:
    raw = message.get("usage") or {}
    return Usage(
        input_tokens=integer(raw.get("input_tokens")),
        output_tokens=integer(raw.get("output_tokens")),
        cache_read_tokens=integer(raw.get("cache_read_input_tokens")),
        cache_creation_tokens=integer(raw.get("cache_creation_input_tokens")),
    )


def text_from_tool_result(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            item if isinstance(item, str) else str(item.get("text", item))
            for item in content
        )
    return "" if content is None else str(content)


INLINE_EVAL_RE = re.compile(
    r"""(?:node|python(?:3)?)\s+-[ec]\s+(['\"]).*?\1""",
    re.DOTALL,
)


def strip_heredocs(command: str) -> str:
    """Remove heredoc bodies so script contents do not inflate counts or labels."""
    return HEREDOC_RE.sub(" <<HEREDOC ", command)


def command_surface(command: str) -> str:
    """Command text used for classification: drop heredoc and -e/-c payloads."""
    return INLINE_EVAL_RE.sub(" ", strip_heredocs(command))


def shell_command_count(command: str) -> int:
    """Estimate top-level executable segments without splitting quoted strings or heredocs."""
    command = strip_heredocs(command)
    segments = 1 if command.strip() else 0
    quote: str | None = None
    escaped = False
    depth = 0
    index = 0
    while index < len(command):
        char = command[index]
        following = command[index + 1] if index + 1 < len(command) else ""
        if escaped:
            escaped = False
        elif char == "\\" and quote != "'":
            escaped = True
        elif quote:
            if char == quote:
                quote = None
        elif char in "'\"":
            quote = char
        elif char == "(":
            depth += 1
        elif char == ")" and depth:
            depth -= 1
        elif depth == 0 and (
            char == ";"
            or char == "\n"
            or (char in "&|" and following == char)
            or (char == "|" and following != "|")
        ):
            segments += 1
            if char in "&|" and following == char:
                index += 1
        index += 1
    return segments


def classify(command: str) -> list[str]:
    """Assign non-exclusive work categories to a Bash command."""
    surface = command_surface(command)
    categories: list[str] = []

    if COVERAGE_RE.search(surface):
        categories.append("coverage")
    if TEST_RE.search(surface) and "coverage" not in categories:
        categories.append("test execution")
    if AUDIT_RE.search(surface):
        categories.append("dependency audit")
    if MIGRATION_RE.search(surface):
        categories.append("migration")
    mechanical = any(category in categories for category in MECHANICAL_CATEGORIES)
    if DEBUG_RE.search(surface) and not mechanical:
        categories.append("debugging")
    is_write = " <<HEREDOC " in surface or bool(re.search(r"\bcat\s+>", surface))
    if not categories and EXPLORATION_RE.search(surface) and not WORK_RE.search(surface) and not is_write:
        categories.append("exploration")
    if not categories:
        categories.append("debugging")

    return categories


def parse_transcript(path: Path, name: str, bytes_per_token: float) -> TranscriptAnalysis:
    analysis = TranscriptAnalysis(name=name, source=str(path))
    pending_calls: dict[str, BashCall] = {}
    assistant_turn = 0
    session_round = 0
    prior_user_prompt: str | None = None
    assistant_turn_by_message_id: dict[str, int] = {}
    assistant_usage_by_message_id: dict[str, Usage] = {}
    assistant_round_by_message_id: dict[str, int] = {}
    latest_experiment_round = 1

    with path.open(encoding="utf-8") as transcript:
        for raw_line in transcript:
            try:
                event = json.loads(raw_line)
            except json.JSONDecodeError:
                continue

            if event.get("type") == "user":
                message = event.get("message") or {}
                content = message.get("content")
                if isinstance(content, str) and content != prior_user_prompt:
                    session_round += 1
                    prior_user_prompt = content
                    # The follow-up prompt is the start of repeat-task execution, not a retry.
                    if session_round == 2 and latest_experiment_round == 1:
                        latest_experiment_round = 2

                for item in content if isinstance(content, list) else []:
                    if item.get("type") != "tool_result":
                        continue
                    call = pending_calls.pop(item.get("tool_use_id", ""), None)
                    if call:
                        call.tool_result = text_from_tool_result(item.get("content"))
                        call.is_error = bool(item.get("is_error"))
                continue

            if event.get("type") != "assistant":
                continue

            message = event.get("message") or {}
            if message.get("role") != "assistant":
                continue

            message_id = str(message.get("id") or event.get("uuid"))
            content_blocks = message.get("content") or []
            round_markers = ROUND_MARKER_RE.findall(json.dumps(content_blocks))
            if session_round == 1:
                experiment_round = 1
            elif round_markers:
                experiment_round = int(round_markers[-1])
                latest_experiment_round = experiment_round
            else:
                experiment_round = latest_experiment_round
            if message_id not in assistant_turn_by_message_id:
                assistant_turn += 1
                assistant_turn_by_message_id[message_id] = assistant_turn
                usage = usage_from_message(message)
                assistant_usage_by_message_id[message_id] = usage
                assistant_round_by_message_id[message_id] = experiment_round
                add_usage(analysis.assistant_usage, usage)
                round_usage = analysis.assistant_usage_by_round.setdefault(
                    experiment_round,
                    Usage(),
                )
                add_usage(round_usage, usage)
            else:
                usage = assistant_usage_by_message_id[message_id]
                previous_round = assistant_round_by_message_id[message_id]
                if round_markers and previous_round != experiment_round:
                    add_usage(analysis.assistant_usage_by_round[previous_round], usage, -1)
                    assistant_round_by_message_id[message_id] = experiment_round
                    round_usage = analysis.assistant_usage_by_round.setdefault(experiment_round, Usage())
                    add_usage(round_usage, usage)

            for content in content_blocks:
                if content.get("type") != "tool_use" or content.get("name") != "Bash":
                    continue
                command = str((content.get("input") or {}).get("command", ""))
                categories = classify(command)
                call = BashCall(
                    session_round=max(session_round, 1),
                    experiment_round=experiment_round,
                    assistant_turn=assistant_turn_by_message_id[message_id],
                    tool_use_id=str(content.get("id", "")),
                    command=command,
                    description=str((content.get("input") or {}).get("description", "")),
                    tool_result="",
                    is_error=False,
                    categories=categories,
                    is_repeated_phase=experiment_round > 1,
                    command_count=shell_command_count(command),
                    command_characters=len(command),
                    tool_output_bytes=0,
                    tool_output_tokens_estimate=0,
                    usage=usage,
                )
                analysis.calls.append(call)
                pending_calls[call.tool_use_id] = call

    for call in analysis.calls:
        call.tool_output_bytes = len(call.tool_result.encode("utf-8"))
        call.tool_output_tokens_estimate = round(call.tool_output_bytes / bytes_per_token)
    return analysis


def metric_rows(analysis: TranscriptAnalysis, rounds: set[int]) -> dict[str, int]:
    calls = [call for call in analysis.calls if call.experiment_round in rounds]
    usage = Usage()
    for round_number in rounds:
        round_usage = analysis.assistant_usage_by_round.get(round_number, Usage())
        usage.input_tokens += round_usage.input_tokens
        usage.output_tokens += round_usage.output_tokens
        usage.cache_read_tokens += round_usage.cache_read_tokens
        usage.cache_creation_tokens += round_usage.cache_creation_tokens
    category_count = Counter(category for call in calls for category in call.categories)
    mechanical = sum(
        1
        for call in calls
        if any(category in call.categories for category in MECHANICAL_CATEGORIES)
    )
    return {
        "Bash calls": len(calls),
        "Commands generated": sum(call.command_count for call in calls),
        "Command characters": sum(call.command_characters for call in calls),
        "Tool-output bytes": sum(call.tool_output_bytes for call in calls),
        "Tool-output tokens (est.)": sum(call.tool_output_tokens_estimate for call in calls),
        "Agent output tokens": usage.output_tokens,
        "Exploration calls": category_count["exploration"],
        "Mechanical calls": mechanical,
        "Debugging calls": category_count["debugging"],
    }


def write_details(analyses: Iterable[TranscriptAnalysis], output_dir: Path) -> None:
    records = [
        {
            "transcript": analysis.name,
            **{
                key: value for key, value in asdict(call).items() if key != "usage"
            },
            "input_tokens": call.usage.input_tokens,
            "output_tokens": call.usage.output_tokens,
            "cache_tokens": call.usage.cache_tokens,
            "cache_read_tokens": call.usage.cache_read_tokens,
            "cache_creation_tokens": call.usage.cache_creation_tokens,
        }
        for analysis in analyses
        for call in analysis.calls
    ]
    (output_dir / "bash_calls.json").write_text(json.dumps(records, indent=2), encoding="utf-8")
    if not records:
        return
    with (output_dir / "bash_calls.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)


def comparison_table(
    baseline: TranscriptAnalysis,
    agent_native: TranscriptAnalysis,
    rounds: set[int],
) -> list[str]:
    baseline_metrics = metric_rows(baseline, rounds)
    agent_metrics = metric_rows(agent_native, rounds)
    lines = [
        "| Metric | Baseline | Agent-native | Delta |",
        "|---|---:|---:|---:|",
    ]
    for label, baseline_value in baseline_metrics.items():
        agent_value = agent_metrics[label]
        lines.append(f"| {label} | {baseline_value:,} | {agent_value:,} | {agent_value - baseline_value:+,} |")
    return lines


def classification_table(
    baseline: TranscriptAnalysis,
    agent_native: TranscriptAnalysis,
    rounds: set[int],
) -> list[str]:
    baseline_calls = [call for call in baseline.calls if call.experiment_round in rounds]
    native_calls = [call for call in agent_native.calls if call.experiment_round in rounds]
    lines = ["| Classification | Baseline | Agent-native |", "|---|---:|---:|"]
    for category in (
        "exploration",
        "test execution",
        "coverage",
        "dependency audit",
        "migration",
        "debugging",
    ):
        lines.append(
            f"| {category.title()} | "
            f"{sum(category in call.categories for call in baseline_calls)} | "
            f"{sum(category in call.categories for call in native_calls)} |"
        )
    return lines


def token_table(
    baseline: TranscriptAnalysis,
    agent_native: TranscriptAnalysis,
    rounds: set[int],
) -> list[str]:
    lines = [
        "| Transcript | Input tokens | Output tokens | Cache-read tokens | Cache-created tokens | Cache tokens |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for analysis in (baseline, agent_native):
        usage = Usage()
        for round_number in rounds:
            round_usage = analysis.assistant_usage_by_round.get(round_number, Usage())
            usage.input_tokens += round_usage.input_tokens
            usage.output_tokens += round_usage.output_tokens
            usage.cache_read_tokens += round_usage.cache_read_tokens
            usage.cache_creation_tokens += round_usage.cache_creation_tokens
        lines.append(
            f"| {analysis.name} | {usage.input_tokens:,} | {usage.output_tokens:,} | "
            f"{usage.cache_read_tokens:,} | {usage.cache_creation_tokens:,} | {usage.cache_tokens:,} |"
        )
    return lines


def _change(baseline_value: int, agent_value: int) -> str:
    delta = agent_value - baseline_value
    if baseline_value == 0:
        return "n/a vs empty baseline"
    percent = 100.0 * delta / baseline_value
    return f"{delta:+,} ({percent:+.0f}%)"


def _lower_is_better(baseline_value: int, agent_value: int) -> bool | None:
    if baseline_value == 0 and agent_value == 0:
        return None
    if baseline_value == 0:
        return False
    return agent_value < baseline_value


def findings_section(baseline: TranscriptAnalysis, agent_native: TranscriptAnalysis) -> list[str]:
    round1_base = metric_rows(baseline, {1})
    round1_native = metric_rows(agent_native, {1})
    repeat_base = metric_rows(baseline, {2, 3})
    repeat_native = metric_rows(agent_native, {2, 3})
    efficiency_keys = (
        "Bash calls",
        "Commands generated",
        "Command characters",
        "Tool-output bytes",
        "Tool-output tokens (est.)",
        "Agent output tokens",
        "Exploration calls",
    )
    round1_wins = sum(
        1 for key in efficiency_keys if _lower_is_better(round1_base[key], round1_native[key])
    )
    repeat_possible = repeat_base["Bash calls"] > 0 or repeat_native["Bash calls"] > 0
    repeat_comparable = repeat_base["Bash calls"] > 0 and repeat_native["Bash calls"] > 0
    lines = [
        "## Findings",
        "",
        "### 1. Does the agent-native interface improve initial discovery efficiency in round 1?",
        "",
    ]
    if round1_wins >= 5:
        lines.append(
            f"Yes. Agent-native is lower on {round1_wins} of {len(efficiency_keys)} round-1 efficiency metrics."
        )
    elif round1_wins >= 3:
        lines.append(
            f"Partially. Agent-native is lower on {round1_wins} of {len(efficiency_keys)} round-1 efficiency metrics; see the table."
        )
    else:
        lines.append(
            f"No clear round-1 efficiency win. Agent-native is lower on {round1_wins} of {len(efficiency_keys)} metrics."
        )
    lines += [
        "",
        "### 2. Does that advantage persist or compound during repeat-task executions in rounds 2–3?",
        "",
    ]
    if not repeat_possible:
        lines.append("Neither transcript contains repeat-task executions in rounds 2–3.")
    elif not repeat_comparable:
        lines.append(
            "Not comparable: one transcript has no round 2–3 Bash calls. "
            "Rounds 2–3 are user-requested repeat-task executions, not retries. "
            "A zero on one side means that session never entered the repeat phase."
        )
    else:
        persist_keys = ("Bash calls", "Command characters", "Tool-output bytes", "Agent output tokens")
        persisted = sum(
            1 for key in persist_keys if _lower_is_better(repeat_base[key], repeat_native[key])
        )
        compounded = 0
        for key in persist_keys:
            if round1_base[key] == 0 or repeat_base[key] == 0:
                continue
            round1_ratio = round1_native[key] / round1_base[key]
            repeat_ratio = repeat_native[key] / repeat_base[key]
            if repeat_ratio < round1_ratio and repeat_native[key] < repeat_base[key]:
                compounded += 1
        if compounded >= 2:
            lines.append(
                "Yes, the advantage compounds. The agent-native/baseline ratio is smaller in rounds 2–3 "
                f"than in round 1 for {compounded} of {len(persist_keys)} core volume metrics."
            )
        elif persisted >= 3:
            lines.append(
                "The round-1 advantage persists in rounds 2–3 but does not clearly compound. "
                f"Agent-native remains lower on {persisted} of {len(persist_keys)} core volume metrics."
            )
        else:
            lines.append(
                "The round-1 pattern does not clearly persist in rounds 2–3. See the repeat-task tables."
            )
    lines.append("")
    return lines


def markdown_report(baseline: TranscriptAnalysis, agent_native: TranscriptAnalysis, ratio: float) -> str:
    lines = [
        "# Claude Code transcript comparison",
        "",
        f"- Baseline source: `{baseline.source}`",
        f"- Agent-native source: `{agent_native.source}`",
        "",
        f"Tool-output tokens are **estimates**, labeled as such in CSV/JSON as `tool_output_tokens_estimate`. "
        f"Claude Code transcripts keep tool output text, not tokenizer counts. The estimator is "
        f"`round(utf8_bytes / {ratio:g})` (UTF-8 bytes / 4 by default). Agent output tokens come from "
        f"`message.usage.output_tokens` and are exact API usage, deduplicated by assistant message ID.",
        "",
        "Cache tokens are extracted separately in `bash_calls.csv` and `bash_calls.json`.",
        "",
    ]
    lines += findings_section(baseline, agent_native)
    lines += [
        "## Question A: initial discovery (round 1)",
        "",
    ]
    lines += comparison_table(baseline, agent_native, {1})
    lines += ["", "### Classification", ""] + classification_table(baseline, agent_native, {1})
    lines += ["", "### Token accounting", ""] + token_table(baseline, agent_native, {1})
    lines += [
        "",
        "## Question B: repeated work (rounds 2–3 combined)",
        "",
    ]
    lines += comparison_table(baseline, agent_native, {2, 3})
    lines += ["", "### Classification", ""] + classification_table(baseline, agent_native, {2, 3})
    lines += ["", "### Token accounting", ""] + token_table(baseline, agent_native, {2, 3})
    lines += [
        "",
        "## Individual repeat rounds",
        "",
    ]
    for round_number in (2, 3):
        lines += [f"### Round {round_number}", ""]
        lines += comparison_table(baseline, agent_native, {round_number})
        lines.append("")
    lines += [
        "## Definitions and caveats",
        "",
        "- Rounds 2–3 are user-requested **repeat-task executions**, never retries.",
        "- Mechanical calls are calls tagged test execution, coverage, dependency audit, or migration.",
        "- Classifications are intentionally non-exclusive except that coverage supersedes test execution.",
        "- Repeated transcript events with the same assistant message ID contribute token usage once; every distinct Bash `tool_use_id` is retained.",
        "- Estimated tool-output tokens are not billed tokenizer counts. Do not treat them as exact.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare Bash usage in Claude Code JSONL transcripts.")
    parser.add_argument("--baseline", type=Path, required=True, help="Baseline transcript JSONL")
    parser.add_argument("--agent-native", type=Path, required=True, help="Agent-native transcript JSONL")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory for report artifacts")
    parser.add_argument(
        "--bytes-per-token",
        type=float,
        default=TOKEN_RATIO_DEFAULT,
        help="Tool-output token estimate divisor; default: 4.0",
    )
    arguments = parser.parse_args()
    if arguments.bytes_per_token <= 0:
        parser.error("--bytes-per-token must be greater than zero")
    for path in (arguments.baseline, arguments.agent_native):
        if not path.is_file():
            parser.error(f"Transcript not found: {path}")

    arguments.output_dir.mkdir(parents=True, exist_ok=True)
    baseline = parse_transcript(arguments.baseline, "Baseline", arguments.bytes_per_token)
    agent_native = parse_transcript(arguments.agent_native, "Agent-native", arguments.bytes_per_token)
    write_details((baseline, agent_native), arguments.output_dir)
    (arguments.output_dir / "report.md").write_text(
        markdown_report(baseline, agent_native, arguments.bytes_per_token),
        encoding="utf-8",
    )
    print(f"Wrote {arguments.output_dir / 'report.md'}")


if __name__ == "__main__":
    main()
