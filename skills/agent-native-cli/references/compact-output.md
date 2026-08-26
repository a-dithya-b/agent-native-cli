# Compact Output

## Principle

The output of a tool becomes input to the agent. Return the smallest result that preserves the information needed for the next decision.

## Prefer

```text
status=healthy
version=1.4.2
replicas=4/4
```

over thousands of lines of underlying CLI output.

## Techniques

- suppress irrelevant stdout/stderr
- use quiet or summary flags
- filter logs
- select relevant fields
- paginate large results
- summarize deterministic output in scripts
- avoid printing intermediate commands unless needed

## Important

Do not hide actionable errors merely to reduce tokens. Errors, warnings, and state needed for the next decision must remain visible.
