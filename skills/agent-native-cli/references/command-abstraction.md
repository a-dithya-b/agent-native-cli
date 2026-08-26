# Command Abstraction

## Principle

Prefer one semantic, deterministic command over repeated low-level commands when the workflow is known.

```text
Agent → deploy-api

instead of

Agent → docker build
      → docker push
      → aws update-service
      → aws wait
```

## Good candidates

- build
- test
- lint
- deploy
- migrate
- inspect
- health checks
- log summaries
- repetitive environment setup

## Design rules

- Keep inputs small and explicit.
- Hide mechanical implementation details.
- Make side effects clear.
- Prefer idempotent operations where practical.
- Make failure detectable without parsing prose.
- Keep the command useful to humans too.

## Goal

Reduce model-generated action sequences and let deterministic tooling perform deterministic work.
