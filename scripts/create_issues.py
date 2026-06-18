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


def run_gh(
    args: list[str],
    *,
    check: bool = True,
    input_text: str | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["gh", *args],
        check=check,
        input=input_text,
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


def find_issue(repo: str, title: str) -> dict[str, object] | None:
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
            "number,title,body",
            "--limit",
            "100",
        ]
    )
    issues = json.loads(result.stdout or "[]")
    for issue in issues:
        if issue.get("title") == title:
            return issue
    return None


def issue_exists(repo: str, title: str) -> bool:
    return find_issue(repo, title) is not None


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


def terminal_trove_source_line(source_url: str) -> str:
    return f"- Source: [Terminal Trove]({source_url})"


def insert_or_replace_source_line(body: str, source_url: str) -> str:
    source_line = terminal_trove_source_line(source_url)
    lines = body.splitlines()

    # Preserve every other part of the issue body, including checked boxes and
    # notes, while keeping the source link idempotent.
    for index, line in enumerate(lines):
        if line.startswith("- Source:"):
            lines[index] = source_line
            return "\n".join(lines) + "\n"

    for index, line in enumerate(lines):
        if line.startswith("- Description:"):
            lines.insert(index + 1, source_line)
            return "\n".join(lines) + "\n"

    for index, line in enumerate(lines):
        if line == "## Checklist":
            lines.insert(index, "")
            lines.insert(index, source_line)
            return "\n".join(lines) + "\n"

    lines.append(source_line)
    return "\n".join(lines) + "\n"


def sync_source_links(repo: str, tools: list[dict[str, str]], dry_run: bool) -> int:
    """Sync Terminal Trove links into existing learning issues without recreating them."""

    missing = 0
    updated = 0
    unchanged = 0

    for row in tools:
        source_url = row.get("source_url", "").strip()
        if not source_url:
            print(f"missing source_url: {row['tool']}", file=sys.stderr)
            missing += 1
            continue

        title = f"Learn: {row['tool']}"
        issue = find_issue(repo, title)
        if issue is None:
            print(f"missing issue: {title}", file=sys.stderr)
            missing += 1
            continue

        body = str(issue.get("body") or "")
        new_body = insert_or_replace_source_line(body, source_url)
        if new_body == body:
            unchanged += 1
            print(f"unchanged: #{issue['number']} {title}")
            continue

        updated += 1
        if dry_run:
            print(f"would update: #{issue['number']} {title}")
            continue

        run_gh(
            [
                "issue",
                "edit",
                str(issue["number"]),
                "--repo",
                repo,
                "--body-file",
                "-",
            ],
            input_text=new_body,
        )
        print(f"updated: #{issue['number']} {title}")

    print(f"source link sync complete: {updated} updated, {unchanged} unchanged, {missing} missing")
    return 1 if missing else 0


def tool_body(row: dict[str, str]) -> str:
    tool = row["tool"]
    source_line = ""
    source_url = row.get("source_url", "").strip()
    if source_url:
        # Keep new issues consistent with source links synced onto existing ones.
        source_line = f"\n- Source: [Terminal Trove]({source_url})"

    return f"""## Goal
Build practical familiarity with `{tool}` and decide whether it belongs in the portable dev environment.

## Context
- Category: `{row["category"]}`
- Scheduled: week {row["week"]}, {row["dates"]}
- Description: {row["description"]}{source_line}

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
    reference = ""
    source_url = row.get("source_url", "").strip()
    if source_url:
        reference = f"""
## Reference
- {source_url}
"""

    return f"""## Goal
{row["description"]}
{reference}

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
    parser.add_argument(
        "--sync-source-links",
        action="store_true",
        help="Insert or update Terminal Trove source links on existing learning issues.",
    )
    args = parser.parse_args()

    tools = load_rows(TOOLS_FILE)
    environment_tasks = load_rows(ENV_FILE)

    if args.sync_source_links:
        return sync_source_links(args.repo, tools, args.dry_run)

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
