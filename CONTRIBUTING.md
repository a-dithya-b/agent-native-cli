# Contributing

Agent-Native CLI is currently an open experiment. The most useful contributions are experiments, observations, and interface ideas—not just code.

## Run your own experiment

The easiest way to contribute is to use the Skill on a repository you work with and report what happened.

### Suggested methodology

1. Pick a real repository with one or more repeatable engineering workflows.
2. Choose a fixed task set, such as tests, coverage, linting, builds, dependency audits, migrations, or release checks.
3. Run the task with the agent using the repository's existing tooling directly.
4. Apply the Agent-Native CLI Skill and let the agent design a higher-level command surface.
5. Run the same task set again.
6. If practical, repeat the task set to test whether the interface continues to help after discovery.
7. Compare the transcripts independently rather than relying on the agent to report its own results.

You do not need to reproduce the exact setup used in the existing experiments. Be explicit about what changed between conditions.

## What to report

Open an issue using the **Experiment report** template. Useful reports include:

- repository type and stack (avoid private or sensitive details)
- coding agent and model
- task set
- baseline and agent-native conditions
- command/tool interaction counts where available
- tool-output volume where available
- agent output or token measurements where available
- repeated-run results, if tested
- anything surprising, including cases where the Skill did not help
- confounders or limitations you noticed

Raw transcripts are welcome when they can be shared safely, but please remove secrets, credentials, private source code, and other sensitive information first.

## Other contributions

You can also contribute by:

- proposing better principles for agent-facing command interfaces
- improving the Skill or its reference documents
- adding analysis tooling for experiments
- documenting failure modes and counterexamples
- suggesting new experimental methodologies

Prefer small, focused pull requests. For changes to the Skill itself, explain what behavior the change is intended to improve and, where possible, include an example or experiment.

## A note on negative results

Negative results are valuable here. If the Skill makes a workflow slower, noisier, less reliable, or otherwise worse, please report it. We are trying to understand when agent-native interfaces help—and when they do not.

## Scope

This project is deliberately in the validation stage. Please avoid turning the repository into a framework or product implementation unless an experiment or discussion establishes a clear need first.
