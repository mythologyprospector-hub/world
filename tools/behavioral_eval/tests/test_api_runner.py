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


if __name__ == "__main__":
    unittest.main()
