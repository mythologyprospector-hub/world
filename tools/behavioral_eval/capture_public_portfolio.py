#!/usr/bin/env python3
"""Capture a live, read-only snapshot of the public repositories in REPOSITORIES.md.

This is repository evidence for evaluation, not an account-wide inventory or a
model-behavior test. Private repositories are intentionally never queried.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

SHA_RE = re.compile(r"^[0-9a-f]{40}$")
MAP_RE = re.compile(r"^\|\s*\*\*([A-Za-z0-9_.-]+)\*\*\s*\|", re.MULTILINE)
API_ROOT = "https://api.github.com"


class CaptureError(RuntimeError):
    """Raised when a complete public snapshot cannot be collected."""


def mapped_repositories(map_text: str, owner: str) -> list[str]:
    names = MAP_RE.findall(map_text)
    if not names:
        raise CaptureError("REPOSITORIES.md contains no recognizable repository rows")
    if len(names) != len(set(names)):
        raise CaptureError("REPOSITORIES.md contains duplicate repository names")
    return [f"{owner}/{name}" for name in names]


def fetch_json(url: str) -> Any:
    request = Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "world-read-only-evidence-capture",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with urlopen(request, timeout=20) as response:
            return json.load(response)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise CaptureError(f"GitHub API request failed for {url}: {exc}") from exc


def collect_snapshot(
    repositories: list[str],
    candidate_sha: str,
    captured_at: str | None = None,
    get_json=fetch_json,
) -> dict[str, Any]:
    if not SHA_RE.fullmatch(candidate_sha):
        raise CaptureError("candidate_sha must be a full 40-character commit SHA")
    captured_at = captured_at or datetime.now(timezone.utc).isoformat()
    records = []
    for full_name in repositories:
        repo = get_json(f"{API_ROOT}/repos/{full_name}")
        if repo.get("full_name", "").lower() != full_name.lower():
            raise CaptureError(f"GitHub returned an unexpected repository for {full_name}")
        if repo.get("private") is not False:
            raise CaptureError(f"{full_name} is not confirmed public; refusing to capture it")
        pulls = get_json(
            f"{API_ROOT}/repos/{full_name}/pulls?state=open&per_page=100"
        )
        if not isinstance(pulls, list):
            raise CaptureError(f"GitHub returned an invalid pull-request list for {full_name}")
        records.append({
            "name": full_name,
            "visibility": "public",
            "default_branch": repo.get("default_branch"),
            "pushed_at": repo.get("pushed_at"),
            "updated_at": repo.get("updated_at"),
            "open_pull_request_count": len(pulls),
            "open_pull_requests": [
                {
                    "number": pr.get("number"),
                    "title": pr.get("title"),
                    "url": pr.get("html_url"),
                    "draft": pr.get("draft"),
                    "updated_at": pr.get("updated_at"),
                    "head_sha": (pr.get("head") or {}).get("sha"),
                    "base": (pr.get("base") or {}).get("ref"),
                }
                for pr in pulls
            ],
        })
    return {
        "schema_version": 1,
        "evidence_kind": "live_public_repository_snapshot",
        "captured_at": captured_at,
        "candidate_sha": candidate_sha,
        "coverage": {
            "scope": "public repositories named in the checked-out REPOSITORIES.md",
            "repository_count": len(records),
            "account_wide_inventory": False,
            "private_repositories_queried": False,
            "assistant_behavior_tested": False,
        },
        "repositories": records,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--map", default="REPOSITORIES.md", help="World public repository map")
    parser.add_argument("--owner", default="mythologyprospector-hub", help="GitHub owner")
    parser.add_argument("--candidate-sha", required=True, help="Full 40-character tested commit SHA")
    parser.add_argument("--output", default="artifacts/public-portfolio-evidence.json")
    args = parser.parse_args(argv)
    try:
        names = mapped_repositories(
            Path(args.map).read_text(encoding="utf-8"), args.owner
        )
        snapshot = collect_snapshot(names, args.candidate_sha)
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
        print(
            f"Captured {len(snapshot['repositories'])} mapped public repositories; "
            "private/account-wide coverage and assistant behavior remain untested."
        )
    except (OSError, CaptureError) as exc:
        print(f"PUBLIC EVIDENCE CAPTURE FAILED: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
