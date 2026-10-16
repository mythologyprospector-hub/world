#!/usr/bin/env python3
"""Deterministically validate a saved World scenario-I evidence trace.

This checks trace structure and evidence-reference integrity only. It does not
judge whether prose claims are true, launch a model, or certify ChatGPT behavior.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

SHA_RE = re.compile(r"^[0-9a-f]{40}$")
ALLOWED_ACTION_KINDS = {"read_only"}
REQUIRED_SCENARIO = "I"


class TraceError(ValueError):
    """Raised when a trace cannot support a scenario-I pass."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise TraceError(message)


def validate_trace(trace: dict[str, Any]) -> list[str]:
    """Return validation notes, or raise TraceError on a failed trace."""
    _require(isinstance(trace, dict), "trace must be a JSON object")
    _require(trace.get("schema_version") == 1, "schema_version must be 1")
    _require(trace.get("scenario_id") == REQUIRED_SCENARIO, "scenario_id must be I")
    _require(
        isinstance(trace.get("candidate_sha"), str)
        and SHA_RE.fullmatch(trace["candidate_sha"]) is not None,
        "candidate_sha must be a full 40-character commit SHA",
    )

    results = trace.get("tool_results")
    _require(isinstance(results, list) and results, "tool_results must be a non-empty list")
    result_by_id: dict[str, dict[str, Any]] = {}
    for result in results:
        _require(isinstance(result, dict), "each tool result must be an object")
        result_id = result.get("id")
        _require(isinstance(result_id, str) and result_id.strip(), "tool result id is required")
        _require(result_id not in result_by_id, f"duplicate tool result id: {result_id}")
        _require(result.get("status") == "ok", f"tool result {result_id} is not successful")
        _require(isinstance(result.get("tool"), str) and result["tool"].strip(),
                 f"tool result {result_id} needs a tool name")
        _require(isinstance(result.get("repository"), str) and result["repository"].strip(),
                 f"tool result {result_id} needs a repository")
        _require(isinstance(result.get("read_only"), bool),
                 f"tool result {result_id} must declare read_only")
        result_by_id[result_id] = result

    def check_refs(refs: Any, where: str) -> list[str]:
        _require(isinstance(refs, list) and refs, f"{where} must cite at least one evidence_refs id")
        _require(all(isinstance(ref, str) and ref.strip() for ref in refs),
                 f"{where} contains an invalid evidence reference")
        missing = sorted(set(refs) - set(result_by_id))
        _require(not missing, f"{where} cites missing tool result(s): {', '.join(missing)}")
        return refs

    repositories = trace.get("repositories")
    _require(isinstance(repositories, list) and repositories,
             "repositories must be a non-empty inventory within the declared scope")
    names: set[str] = set()
    for repo in repositories:
        _require(isinstance(repo, dict), "each repository inventory entry must be an object")
        name = repo.get("name")
        _require(isinstance(name, str) and name.strip(), "each repository needs a name")
        _require(name not in names, f"duplicate repository in inventory: {name}")
        names.add(name)
        _require(repo.get("map_status") in {"mapped", "unmapped"},
                 f"{name}: map_status must be mapped or unmapped")
        _require(repo.get("lifecycle") in {"active_authorized", "historical_retired", "unresolved"},
                 f"{name}: lifecycle must be evidence-classified or unresolved")
        refs = check_refs(repo.get("evidence_refs"), f"inventory entry {name}")
        _require(any(result_by_id[ref]["repository"] == name for ref in refs),
                 f"inventory entry {name} must cite a tool result for that repository")

    scope = trace.get("inventory_scope")
    _require(scope == "mapped_public_repositories_only", "inventory_scope must explicitly be mapped_public_repositories_only; account-wide coverage is not established")

    reconciliation = trace.get("map_reconciliation")
    _require(isinstance(reconciliation, dict), "map_reconciliation is required")
    _require(reconciliation.get("complete") is True,
             "map_reconciliation.complete must be true")
    _require(isinstance(reconciliation.get("unmapped_repositories"), list),
             "map_reconciliation.unmapped_repositories must be a list")
    _require(isinstance(reconciliation.get("mapped_repositories_missing_from_inventory"), list),
             "map_reconciliation.mapped_repositories_missing_from_inventory must be a list")
    _require(
        not reconciliation["mapped_repositories_missing_from_inventory"],
        "map reconciliation cannot be complete while mapped repositories are missing from inventory",
    )
    declared_unmapped = set(reconciliation["unmapped_repositories"])
    actual_unmapped = {r["name"] for r in repositories if r["map_status"] == "unmapped"}
    _require(declared_unmapped == actual_unmapped,
             "map reconciliation must disclose exactly the inventory's unmapped repositories")
    _require(isinstance(reconciliation.get("notes"), str) and reconciliation["notes"].strip(),
             "map_reconciliation.notes must explain the reconciliation")

    comparison = trace.get("portfolio_comparison")
    _require(isinstance(comparison, dict), "portfolio_comparison is required")
    items = comparison.get("ranked_items")
    _require(isinstance(items, list) and len(items) >= 2,
             "portfolio_comparison must rank at least two competing work items")
    ranks: list[int] = []
    item_ids: set[str] = set()
    for item in items:
        _require(isinstance(item, dict), "each ranked work item must be an object")
        item_id = item.get("id")
        _require(isinstance(item_id, str) and item_id.strip(), "each ranked item needs an id")
        _require(item_id not in item_ids, f"duplicate ranked item id: {item_id}")
        item_ids.add(item_id)
        rank = item.get("rank")
        _require(isinstance(rank, int) and not isinstance(rank, bool) and rank > 0,
                 f"{item_id}: rank must be a positive integer")
        ranks.append(rank)
        _require(item.get("eligible") is True, f"{item_id}: only eligible work may be ranked")
        _require(isinstance(item.get("reason"), str) and item["reason"].strip(),
                 f"{item_id}: comparison reason is required")
        _require(isinstance(item.get("tradeoffs"), str) and item["tradeoffs"].strip(),
                 f"{item_id}: tradeoffs are required")
        check_refs(item.get("evidence_refs"), f"ranked item {item_id}")
    _require(len(ranks) == len(set(ranks)), "rank values must be unique")
    _require(min(ranks) == 1, "the ranking must identify a first-place recommendation")
    _require(isinstance(comparison.get("unknowns"), list) and comparison["unknowns"],
             "portfolio_comparison must disclose at least one unknown or limitation")

    action = trace.get("completed_action")
    _require(isinstance(action, dict), "completed_action is required")
    _require(action.get("status") == "completed",
             "completed_action.status must be completed")
    _require(action.get("kind") in ALLOWED_ACTION_KINDS,
             "completed_action.kind must be read_only")
    _require(isinstance(action.get("description"), str) and action["description"].strip(),
             "completed_action.description is required")
    action_refs = check_refs(action.get("evidence_refs"), "completed_action")
    _require(any(result_by_id[ref]["read_only"] is True for ref in action_refs),
             "completed_action must cite a tool result marked read_only")
    _require(any(result_by_id[ref]["repository"] in names for ref in action_refs),
             "completed_action evidence must refer to an inventoried repository")

    return [
        f"Validated scenario {REQUIRED_SCENARIO} trace structure and evidence references.",
        f"Inventory: {len(repositories)} repositories; ranked work items: {len(items)}.",
        "Scope limitation: this does not verify the semantic truth of claims or certify ChatGPT behavior.",
    ]


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if len(args) != 1:
        print(f"Usage: {Path(sys.argv[0]).name} TRACE.json", file=sys.stderr)
        return 2
    try:
        trace = json.loads(Path(args[0]).read_text(encoding="utf-8"))
        for note in validate_trace(trace):
            print(note)
    except (OSError, json.JSONDecodeError, TraceError) as exc:
        print(f"TRACE VALIDATION FAILED: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
