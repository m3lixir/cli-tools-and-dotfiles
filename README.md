# Dev Environment Summer 2026

This repository tracks a summer learning plan for terminal tools and the portable development environment that grows out of it.

Target date: September 22, 2026.

Primary outcome: by the end of the project, the tool list has been explored and the development environment is git-tracked enough to clone onto a new Mac, bootstrap the core setup, link dotfiles, and continue from there.

## Outcomes

- Learn 86 unique terminal tools from the selected Terminal Trove list.
- Track dotfiles, shell helpers, Git defaults, install manifests, and setup notes in Git.
- Capture one practical note or artifact for every tool.
- Maintain one GitHub issue per tool plus environment setup issues.
- End with a reproducible new-machine setup flow.

The original list contains 87 entries. `resto` appears twice, so it is tracked once.

## Repository Layout

- `dotfiles/`: tracked shell, Git, and CLI config files.
- `scripts/bootstrap.sh`: installs baseline Mac development dependencies.
- `scripts/link_dotfiles.sh`: links tracked dotfiles into `$HOME` with backups.
- `scripts/verify_environment.sh`: checks whether the core setup is ready.
- `scripts/create_issues.py`: creates GitHub issues from `data/*.tsv`.
- `data/tools.tsv`: canonical tool learning list and weekly schedule.
- `data/environment_tasks.tsv`: portable environment setup tasks.
- `docs/codex-session-2026-06-18.md`: original planning chat decisions and setup context.
- `notes/`: per-tool and environment notes.
- `artifacts/`: generated screenshots, recordings, exports, and experiments.

## Weekly Learning Schedule

| Week | Dates | Focus |
| --- | --- | --- |
| 1 | Jun 22-28 | Codex, installation helpers, shell quality, and Git ignore basics |
| 2 | Jun 29-Jul 5 | Git workflow, changelogs, gists, and issue/documentation tracking |
| 3 | Jul 6-12 | Markdown reading, editing, and terminal presentations |
| 4 | Jul 13-19 | Code images, terminal screenshots, and CLI recordings |
| 5 | Jul 20-26 | Dotfiles, PATH, file management, restore workflows, and automation |
| 6 | Jul 27-Aug 2 | macOS, Bluetooth, local device, and home/system tools |
| 7 | Aug 3-9 | Hacker News, RSS, and reference reading |
| 8 | Aug 10-16 | Email, messaging, Google Workspace, IRC, and deal tracking |
| 9 | Aug 17-23 | Network diagnostics and local service visibility |
| 10 | Aug 24-30 | LAN discovery, domain intelligence, MQTT, APIs, and load testing |
| 11 | Aug 31-Sep 6 | Logs, web logs, aggregation, highlighting, and repeated commands |
| 12 | Sep 7-13 | Security crawling, fuzzing, CVEs, OSINT, and threat intelligence |
| 13 | Sep 14-20 | Databases, papers, metrics, archiving, galleries, and video tools |
| Wrap | Sep 21-22 | Dashboards, remaining niche tools, final bootstrap review |

## Learning Workflow

Each tool issue should be closed only after:

1. The install path is documented.
2. At least three meaningful commands or workflows have been tried.
3. A note exists in `notes/<tool>.md`.
4. One artifact, config change, alias, script, or practical takeaway is committed.
5. The tool is classified as keep, occasional, or skip.

## Bootstrap Flow

After cloning this repository on a Mac:

```sh
./scripts/bootstrap.sh
./scripts/link_dotfiles.sh
./scripts/verify_environment.sh
```

The dotfile linker backs up existing files before creating symlinks. Secrets and machine-specific values belong in untracked `.env` files, not in tracked dotfiles.

## GitHub Issue Creation

Once GitHub authentication is fixed:

```sh
gh auth login -h github.com
gh repo create m3lixir/cli-tools-and-dotfiles --public --source=. --remote=origin --push
python3 scripts/create_issues.py --repo m3lixir/cli-tools-and-dotfiles
```

This creates one issue per unique tool and one issue per environment setup task.
