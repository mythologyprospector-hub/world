"""Adversarial tests for exact-item evidence binding in source checks."""
import unittest

from tools.behavioral_eval.api_runner import RunnerError, validate_source_checks


class SourceCheckIdentityTests(unittest.TestCase):
    def _trace(self, item_id, evidence_ref):
        return {
            "portfolio_comparison": {
                "ranked_items": [{
                    "id": item_id,
                    "evidence_refs": ["e001", "e002"],
                    "source_checks": [{
                        "evidence_ref": evidence_ref,
                        "field": "state",
                        "expected": "open",
                    }],
                }],
            },
        }

    def _ledger(self, repository, number):
        return [{
            "id": "e002",
            "tool": "get_public_issue_or_pull_request",
            "repository": repository,
            "result": {"number": number, "state": "open"},
        }]

    def test_source_check_rejects_different_issue_number(self):
        trace = self._trace("mythologyprospector-hub/world#41", "e002")
        ledger = self._ledger("mythologyprospector-hub/world", 42)

        with self.assertRaisesRegex(RunnerError, "exact ranked item"):
            validate_source_checks(trace, ledger)

    def test_source_check_rejects_different_repository(self):
        trace = self._trace("mythologyprospector-hub/world#41", "e002")
        ledger = self._ledger("mythologyprospector-hub/episteme", 41)

        with self.assertRaisesRegex(RunnerError, "exact ranked item"):
            validate_source_checks(trace, ledger)

    def test_source_check_rejects_malformed_ranked_item_identity(self):
        trace = self._trace("mythologyprospector-hub/world", "e002")
        ledger = self._ledger("mythologyprospector-hub/world", 41)

        with self.assertRaisesRegex(RunnerError, "exact repository and positive item number"):
            validate_source_checks(trace, ledger)


if __name__ == "__main__":
    unittest.main()
