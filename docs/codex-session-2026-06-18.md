# Codex Session Notes - 2026-06-18

This document captures the key decisions and implementation context from the Codex chat that created this project.

## Original Goal

Build a summer personal-development project that does two things:

- Work through a selected list of terminal tools from Terminal Trove.
- Turn the learning process into a git-tracked, portable development environment with dotfiles, setup scripts, notes, and artifacts.

The intended end state is that the environment can be cloned and continued from another machine.

## Repository Decision

Final repository name:

- Local path: `/Users/mel/Desktop/cli-tools-and-dotfiles`
- GitHub repo: `m3lixir/cli-tools-and-dotfiles`
- Visibility: public

Earlier name candidates included:

- `dev-environment-summer-2026`
- `terminal-dev-lab-2026`
- `portable-dev-environment`
- `dotfiles-and-terminal-tools`
- `dotfiles-toolbox`
- `portable-dotfiles-tools`

The final chosen name was `cli-tools-and-dotfiles`.

## Schedule And Scope

Deadline:

- September 22, 2026

Planned issue count:

- 86 tool-learning issues
- 12 environment setup issues
- 98 total issues

The original list had 87 tool entries, but `resto` appeared twice. It is intentionally tracked once.

## Implemented Project Structure

The initial repo contains:

- `README.md` for goals, schedule, workflow, and bootstrap instructions.
- `Brewfile` for baseline macOS package installation.
- `data/tools.tsv` for the canonical tool list and schedule.
- `data/environment_tasks.tsv` for portable environment work.
- `dotfiles/` for tracked shell, Git, and tool config.
- `scripts/bootstrap.sh` for baseline setup.
- `scripts/link_dotfiles.sh` for safe symlink creation with backups.
- `scripts/verify_environment.sh` for environment checks.
- `scripts/create_issues.py` for GitHub label and issue creation.
- `docs/issue-workflow.md` for issue completion rules.
- `notes/` and `artifacts/` for learning output.

## GitHub Setup

The GitHub repo was created and pushed as:

```text
https://github.com/m3lixir/cli-tools-and-dotfiles
```

Issue creation was completed through GitHub CLI after refreshing the `m3lixir` auth token.

Verified GitHub state:

- Repo is public.
- Default branch is `main`.
- 98 issues exist.
- 86 issues start with `Learn:`.
- 12 issues start with `Setup:`.
- All planned issues have labels.

Relevant labels include:

- `learning`
- `environment`
- category labels such as `ai-cli`, `git-workflow`, `network-api`, and `security-osint`
- schedule labels from `week-01` through `week-13`
- `week-wrap`

## Auth And Git Notes

Two setup issues came up during the session:

- The first local commit attempt failed because global Git signing tried to use GPG from a restricted sandbox. The commit was made with signing disabled for that single commit.
- `gh auth status` initially showed an invalid `m3lixir` token. The stale login was removed and GitHub CLI was re-authenticated with `repo` scope.

The local Git remote is:

```text
origin git@github.com:m3lixir/cli-tools-and-dotfiles.git
```

## Cleanup

An earlier scaffold directory named `/Users/mel/Desktop/dev-environment-summer-2026` was created before the final repo name was chosen. After the project was migrated to `cli-tools-and-dotfiles`, that stale directory was deleted.

## Working Agreements For Future Sessions

- Treat `cli-tools-and-dotfiles` as the source of truth.
- Keep learning notes, artifacts, scripts, and environment changes committed.
- Do not commit secrets, machine-specific credentials, private keys, or unredacted tokens.
- Close each tool issue only after notes and at least one practical artifact or takeaway are committed.
- Prefer improving the bootstrap flow as tools become permanent parts of the environment.

## Suggested Next Steps

1. Start with the week 1 issues.
2. Fill out `notes/codex.md`, `notes/eget.md`, and `notes/shellcheck.md` as the first learning notes.
3. Run `scripts/verify_environment.sh` and use the output to improve the baseline setup.
4. Decide which existing personal dotfiles should be migrated into `dotfiles/`.
5. Keep each week small enough to produce durable setup improvements, not just tool checkmarks.

