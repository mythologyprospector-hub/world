import json
import tempfile
import unittest
from pathlib import Path

from tools.behavioral_eval.api_runner import (
    RunnerError,
    function_calls,
    output_text,
    run_evaluation,
    run_tool,
    validate_mapped_inventory,
)

SHA = "a" * 40
MAP = "# Public map\n| Repository | Description |\n| **world** | coordination |\n| **episteme** | science |\n"


class ApiRunnerTests(unittest.TestCase):
    def test_missing_api_key_fails_before_network(self):
        with tempfile.TemporaryDirectory() as d:
            map_path = Path(d) / "REPOSITORIES.md"
            map_path.write_text(MAP)
            with self.assertRaisesRegex(RunnerError, "OPENAI_API_KEY"):
                run_evaluation(SHA, str(map_path), "", "model", str(Path(d) / "out.json"),
                               post_json=lambda *a, **k: self.fail("network should not run"))

    def test_rejects_unmapped_repository(self):
        with self.assertRaisesRegex(RunnerError, "allowlist"):
            run_tool("get_public_repository_overview", {"repository": "someone/private"},
                     {"mythologyprospector-hub/world"}, ["mythologyprospector-hub/world"])

    def test_only_expected_function_calls_are_detected(self):
        response = {"output": [
            {"type": "message", "content": [{"type": "output_text", "text": "done"}]},
            {"type": "function_call", "name": "list_mapped_public_repositories", "call_id": "call1"},
        ]}
        self.assertEqual(len(function_calls(response)), 1)
        self.assertEqual(output_text(response), "done")

    def test_bounded_tool_payload_remains_valid_json_when_truncated(self):
        from tools.behavioral_eval.api_runner import bounded_tool_payload, MAX_TOOL_OUTPUT_CHARS

        payload = bounded_tool_payload("e001", {"body": "x" * (MAX_TOOL_OUTPUT_CHARS * 3)})
        decoded = json.loads(payload)
        self.assertEqual(decoded["evidence_id"], "e001")
        self.assertTrue(decoded["truncated"])
        self.assertLessEqual(len(payload), MAX_TOOL_OUTPUT_CHARS)
        self.assertIn("full result is preserved", decoded["note"])

    def test_successful_mock_run_writes_failure_safe_public_scope_trace(self):
        with tempfile.TemporaryDirectory() as d:
            map_path = Path(d) / "REPOSITORIES.md"
            map_path.write_text(MAP)
            out_path = Path(d) / "out.json"
            with self.assertRaisesRegex(RunnerError, "valid JSON trace"):
                run_evaluation(SHA, str(map_path), "test-key", "test-model", str(out_path),
                               post_json=lambda *a, **k: {"id": "resp1", "output": [
                                   {"type": "message", "content": [
                                       {"type": "output_text", "text": "not json"}]}]})
            saved = json.loads(out_path.read_text())
            self.assertEqual(saved["status"], "failed")
            self.assertEqual(saved["tool_ledger"], [])
            self.assertEqual(saved["model_response_text"], "not json")


    def test_successful_mock_tool_round_trip_validates_and_writes_trace(self):
        with tempfile.TemporaryDirectory() as d:
            map_path = Path(d) / "REPOSITORIES.md"
            map_path.write_text("# Public map\n| Repository | Description |\n| **world** | coordination |\n")
            out_path = Path(d) / "out.json"
            trace = {
                "schema_version": 1,
                "scenario_id": "I",
                "candidate_sha": SHA,
                "inventory_scope": "mapped_public_repositories_only",
                "repositories": [{
                    "name": "mythologyprospector-hub/world",
                    "map_status": "mapped",
                    "lifecycle": "unresolved",
                    "evidence_refs": ["e001"],
                }],
                "map_reconciliation": {
                    "complete": True,
                    "unmapped_repositories": [],
                    "mapped_repositories_missing_from_inventory": [],
                    "notes": "The single-entry fixture map reconciles to the single inventoried repository.",
                },
                "portfolio_comparison": {
                    "ranked_items": [
                        {"id": "work-a", "rank": 1, "eligible": True, "reason": "Higher verified impact.",
                         "tradeoffs": "Requires follow-up.", "evidence_refs": ["e001"]},
                        {"id": "work-b", "rank": 2, "eligible": True, "reason": "Useful but less urgent.",
                         "tradeoffs": "Delays a smaller benefit.", "evidence_refs": ["e001"]},
                    ],
                    "unknowns": ["The mock evidence does not establish semantic truth."],
                },
                "completed_action": {
                    "status": "completed",
                    "kind": "read_only",
                    "description": "Listed the mapped public repository.",
                    "evidence_refs": ["e001"],
                },
            }
            responses = [
                {"id": "resp-tool", "output": [{
                    "type": "function_call",
                    "name": "list_mapped_public_repositories",
                    "arguments": "{}",
                    "call_id": "call-list",
                }]},
                {"id": "resp-final", "output": [{
                    "type": "message",
                    "content": [{"type": "output_text", "text": json.dumps(trace)}],
                }]},
            ]
            sent_payloads = []

            def fake_post(url, key, payload):
                sent_payloads.append(payload)
                return responses.pop(0)

            result = run_evaluation(
                SHA, str(map_path), "test-key", "test-model", str(out_path),
                post_json=fake_post,
            )
            saved = json.loads(out_path.read_text())
            self.assertEqual(result["status"], "public_only_trace_structure_pass")
            self.assertEqual(saved["status"], "public_only_trace_structure_pass")
            self.assertEqual(saved["report"]["inventory_scope"], "mapped_public_repositories_only")
            self.assertEqual(saved["tool_ledger"][0]["id"], "e001")
            self.assertEqual(saved["tool_ledger"][0]["read_only"], True)
            self.assertEqual(result["report"]["runner_metadata"]["tool_call_count"], 1)
            self.assertEqual(sent_payloads[1]["previous_response_id"], "resp-tool")
            self.assertEqual(result["validation_notes"][0].startswith("Validated scenario I"), True)


    def test_rejects_trace_that_omits_a_mapped_repository(self):
        trace = {"repositories": [
            {"name": "mythologyprospector-hub/world", "map_status": "mapped"}
        ]}
        with self.assertRaisesRegex(RunnerError, "missing mapped repositories: mythologyprospector-hub/episteme"):
            validate_mapped_inventory(
                trace,
                ["mythologyprospector-hub/world", "mythologyprospector-hub/episteme"],
            )

    def test_rejects_repository_outside_map_and_unmapped_classification(self):
        with self.assertRaisesRegex(RunnerError, "repositories outside map"):
            validate_mapped_inventory(
                {"repositories": [
                    {"name": "mythologyprospector-hub/world", "map_status": "mapped"},
                    {"name": "other/project", "map_status": "mapped"},
                ]},
                ["mythologyprospector-hub/world"],
            )
        with self.assertRaisesRegex(RunnerError, "cannot classify entries as unmapped"):
            validate_mapped_inventory(
                {"repositories": [
                    {"name": "mythologyprospector-hub/world", "map_status": "unmapped"}
                ]},
                ["mythologyprospector-hub/world"],
            )


    def test_runner_rejects_incomplete_inventory_and_saves_failure_artifact(self):
        with tempfile.TemporaryDirectory() as d:
            map_path = Path(d) / "REPOSITORIES.md"
            map_path.write_text(MAP)
            out_path = Path(d) / "out.json"
            incomplete_trace = {
                "repositories": [{
                    "name": "mythologyprospector-hub/world",
                    "map_status": "mapped",
                }],
            }
            responses = [
                {"id": "resp-tool", "output": [{
                    "type": "function_call",
                    "name": "list_mapped_public_repositories",
                    "arguments": "{}",
                    "call_id": "call-list",
                }]},
                {"id": "resp-final", "output": [{
                    "type": "message",
                    "content": [{"type": "output_text", "text": json.dumps(incomplete_trace)}],
                }]},
            ]

            def fake_post(url, key, payload):
                return responses.pop(0)

            with self.assertRaisesRegex(
                RunnerError,
                "missing mapped repositories: mythologyprospector-hub/episteme",
            ):
                run_evaluation(
                    SHA, str(map_path), "test-key", "test-model", str(out_path),
                    post_json=fake_post,
                )

            saved = json.loads(out_path.read_text())
            self.assertEqual(saved["status"], "failed")
            self.assertIn("missing mapped repositories", saved["error"])
            self.assertEqual(saved["tool_ledger"][0]["tool"], "list_mapped_public_repositories")


if __name__ == "__main__":
    unittest.main()
