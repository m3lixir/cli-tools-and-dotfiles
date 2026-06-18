# Issue Workflow

Each tool gets a GitHub issue. The issue is the task, and the repo commit is the evidence.

## Tool Issue Done Criteria

- Install path is recorded.
- Basic help/version command is captured.
- Three realistic workflows are tried.
- A short note exists in `notes/<tool>.md`.
- One artifact or reusable config change is committed.
- Final verdict is recorded: keep, occasional, or skip.

## Environment Issue Done Criteria

- The config or workflow is tracked in Git.
- The setup is documented enough to repeat.
- Verification exists through a command, script, screenshot, or note.
- Secrets are excluded from Git.

## Labels

- `learning`: every tool issue.
- `environment`: every environment setup issue.
- Category labels: `ai-cli`, `git-workflow`, `network-api`, and similar.
- Week labels: `week-01` through `week-13`, plus `week-wrap`.

