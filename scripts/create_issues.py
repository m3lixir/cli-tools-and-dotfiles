#!/usr/bin/env python3
"""Create GitHub issues for the summer dev environment plan."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS_FILE = ROOT / "data" / "tools.tsv"
ENV_FILE = ROOT / "data" / "environment_tasks.tsv"


def run_gh(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["gh", *args],
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def normalize_week(week: str) -> str:
    if week == "wrap":
        return "week-wrap"
    return f"week-{int(week):02d}"


def ensure_label(repo: str, name: str, color: str, description: str, dry_run: bool) -> None:
    if dry_run:
        print(f"label: {name}")
        return

    result = run_gh(
        [
            "label",
            "create",
            name,
            "--repo",
            repo,
            "--color",
            color,
            "--description",
            description,
        ],
        check=False,
    )
    if result.returncode not in (0, 1):
        sys.stderr.write(result.stderr)
        result.check_returncode()


def issue_exists(repo: str, title: str) -> bool:
    result = run_gh(
        [
            "issue",
            "list",
            "--repo",
            repo,
            "--state",
            "all",
            "--search",
            f'in:title "{title}"',
            "--json",
            "title",
            "--limit",
            "100",
        ]
    )
    issues = json.loads(result.stdout or "[]")
    return any(issue.get("title") == title for issue in issues)


def create_issue(repo: str, title: str, body: str, labels: list[str], dry_run: bool) -> None:
    if dry_run:
        print(f"issue: {title} [{', '.join(labels)}]")
        return

    if issue_exists(repo, title):
        print(f"skip existing: {title}")
        return

    run_gh(
        [
            "issue",
            "create",
            "--repo",
            repo,
            "--title",
            title,
            "--body",
            body,
            "--label",
            ",".join(labels),
        ]
    )
    print(f"created: {title}")


def tool_body(row: dict[str, str]) -> str:
    tool = row["tool"]
    return f"""## Goal
Build practical familiarity with `{tool}` and decide whether it belongs in the portable dev environment.

## Context
- Category: `{row["category"]}`
- Scheduled: week {row["week"]}, {row["dates"]}
- Description: {row["description"]}

## Checklist
- [ ] Confirm the current upstream project, docs, and install path.
- [ ] Install or document why it should not be installed globally.
- [ ] Run the help/version command and capture notable options.
- [ ] Try at least three realistic workflows.
- [ ] Add notes to `notes/{tool}.md`.
- [ ] Commit one artifact, config change, alias, script, or practical takeaway.
- [ ] Record verdict: keep, occasional, or skip.
"""


def environment_body(row: dict[str, str]) -> str:
    return f"""## Goal
{row["description"]}

## Scheduled
- Week: {row["week"]}
- Dates: {row["dates"]}

## Checklist
- [ ] Track the relevant config, script, or documentation in this repository.
- [ ] Confirm the workflow can be repeated from a fresh clone.
- [ ] Add verification evidence through a command, note, screenshot, or script update.
- [ ] Confirm secrets and machine-specific values are not committed.
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default="m3lixir/cli-tools-and-dotfiles")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    tools = load_rows(TOOLS_FILE)
    environment_tasks = load_rows(ENV_FILE)

    labels = {
        "learning": ("0e8a16", "Tool learning task"),
        "environment": ("5319e7", "Portable environment setup task"),
    }
    for row in tools:
        labels[row["category"]] = ("1d76db", f"Category: {row['category']}")
        labels[normalize_week(row["week"])] = ("ededed", f"Scheduled for {row['dates']}")
    for row in environment_tasks:
        labels[normalize_week(row["week"])] = ("ededed", f"Scheduled for {row['dates']}")

    for name, (color, description) in sorted(labels.items()):
        ensure_label(args.repo, name, color, description, args.dry_run)

    for row in tools:
        create_issue(
            args.repo,
            f"Learn: {row['tool']}",
            tool_body(row),
            ["learning", row["category"], normalize_week(row["week"])],
            args.dry_run,
        )

    for row in environment_tasks:
        create_issue(
            args.repo,
            f"Setup: {row['title']}",
            environment_body(row),
            ["environment", normalize_week(row["week"])],
            args.dry_run,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
