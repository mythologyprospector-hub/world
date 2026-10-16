import unittest
from unittest.mock import Mock

from tools.behavioral_eval.capture_public_portfolio import (
    CaptureError,
    collect_snapshot,
    mapped_repositories,
)


SHA = "a" * 40


class CapturePublicPortfolioTests(unittest.TestCase):
    def test_extracts_public_map_rows_only(self):
        text = (
            "# Map\n"
            "| Repository | Description |\n"
            "| **world** | coordination |\n"
            "| **episteme** | science |\n"
        )
        self.assertEqual(
            mapped_repositories(text, "example-org"),
            ["example-org/world", "example-org/episteme"],
        )

    def test_rejects_unpinned_candidate_sha(self):
        with self.assertRaisesRegex(CaptureError, "full 40-character"):
            collect_snapshot([], "main", captured_at="2026-10-16T00:00:00Z")

    def test_collects_public_repository_and_open_pr_evidence(self):
        def get_json(url):
            if url.endswith("/repos/example-org%2Fworld"):
                return {
                    "full_name": "example-org/world",
                    "private": False,
                    "default_branch": "main",
                    "pushed_at": "2026-10-15T12:00:00Z",
                    "updated_at": "2026-10-15T12:30:00Z",
                }
            if url.endswith("/pulls?state=open&per_page=100"):
                return [{
                    "number": 12,
                    "title": "Example change",
                    "html_url": "https://github.com/example-org/world/pull/12",
                    "draft": True,
                    "updated_at": "2026-10-15T12:00:00Z",
                    "head": {"sha": "b" * 40},
                    "base": {"ref": "main"},
                }]
            raise AssertionError(f"unexpected API URL: {url}")

        snapshot = collect_snapshot(
            ["example-org/world"], SHA, "2026-10-16T00:00:00Z", get_json
        )
        self.assertEqual(snapshot["coverage"]["repository_count"], 1)
        self.assertFalse(snapshot["coverage"]["account_wide_inventory"])
        self.assertFalse(snapshot["coverage"]["private_repositories_queried"])
        self.assertEqual(snapshot["repositories"][0]["open_pull_request_count"], 1)
        self.assertEqual(snapshot["repositories"][0]["open_pull_requests"][0]["number"], 12)

    def test_refuses_private_repository(self):
        def get_json(url):
            return {
                "full_name": "example-org/private",
                "private": True,
                "default_branch": "main",
            }

        with self.assertRaisesRegex(CaptureError, "not confirmed public"):
            collect_snapshot(["example-org/private"], SHA, get_json=get_json)


if __name__ == "__main__":
    unittest.main()
