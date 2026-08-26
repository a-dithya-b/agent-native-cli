# Structured Output

## Principle

When an agent needs to inspect command results, prefer stable, machine-readable output over prose or uncontrolled terminal output.

## Useful forms

- key-value summaries
- JSON
- line-oriented records
- stable exit codes

Example:

```text
status=degraded
error_count=12
latest_error="connection refused"
```

## Design rules

- Keep schemas small.
- Keep field names stable.
- Avoid mixing human commentary into machine output.
- Separate diagnostics from the primary result when practical.
- Use exit status for success/failure instead of forcing the agent to infer it from text.

Structured output is most useful when the result feeds another agent decision.
