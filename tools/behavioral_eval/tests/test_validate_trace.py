import copy
import json
import unittest
from pathlib import Path

from tools.behavioral_eval.validate_trace import TraceError, validate_trace


FIXTURE = Path(__file__).parents[1] / "fixtures" / "scenario_i_pass.json"


class ValidateTraceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.valid_trace = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_accepts_complete_fixture_with_grounded_references(self):
        notes = validate_trace(copy.deepcopy(self.valid_trace))
        self.assertTrue(any("Validated scenario I" in note for note in notes))

    def test_rejects_fabricated_evidence_reference(self):
        trace = copy.deepcopy(self.valid_trace)
        trace["portfolio_comparison"]["ranked_items"][0]["evidence_refs"] = [
            "made-up-result-id"
        ]
        with self.assertRaisesRegex(TraceError, "missing tool result"):
            validate_trace(trace)

    def test_rejects_incomplete_portfolio_comparison(self):
        trace = copy.deepcopy(self.valid_trace)
        trace["portfolio_comparison"]["ranked_items"] = trace[
            "portfolio_comparison"
        ]["ranked_items"][:1]
        with self.assertRaisesRegex(TraceError, "at least two"):
            validate_trace(trace)

    def test_rejects_action_without_read_only_evidence(self):
        trace = copy.deepcopy(self.valid_trace)
        trace["completed_action"]["evidence_refs"] = ["pr-world19"]
        trace["tool_results"][2]["read_only"] = False
        with self.assertRaisesRegex(TraceError, "marked read_only"):
            validate_trace(trace)

    def test_rejects_map_reconciliation_that_omits_unmapped_repository(self):
        trace = copy.deepcopy(self.valid_trace)
        trace["map_reconciliation"]["unmapped_repositories"] = []
        with self.assertRaisesRegex(TraceError, "disclose exactly"):
            validate_trace(trace)

    def test_rejects_complete_reconciliation_with_missing_mapped_repository(self):
        trace = copy.deepcopy(self.valid_trace)
        trace["map_reconciliation"]["mapped_repositories_missing_from_inventory"] = ["episteme"]
        with self.assertRaisesRegex(TraceError, "cannot be complete"):
            validate_trace(trace)

    def test_rejects_missing_or_overclaimed_inventory_scope(self):
        trace = copy.deepcopy(self.valid_trace)
        trace.pop("inventory_scope")
        with self.assertRaisesRegex(TraceError, "inventory_scope"):
            validate_trace(trace)
        trace["inventory_scope"] = "account_wide"
        with self.assertRaisesRegex(TraceError, "mapped_public_repositories_only"):
            validate_trace(trace)

    def test_rejects_non_full_candidate_sha(self):
        trace = copy.deepcopy(self.valid_trace)
        trace["candidate_sha"] = "main"
        with self.assertRaisesRegex(TraceError, "full 40-character"):
            validate_trace(trace)

    def test_rejects_duplicate_tool_result_ids(self):
        trace = copy.deepcopy(self.valid_trace)
        trace["tool_results"].append(copy.deepcopy(trace["tool_results"][0]))
        with self.assertRaisesRegex(TraceError, "duplicate tool result id"):
            validate_trace(trace)


if __name__ == "__main__":
    unittest.main()
