#!/usr/bin/env python3
"""Opt-in, public-only Responses API evaluator for World scenario I.

The model can call only the read-only public GitHub functions defined here.
This is a prototype: a successful API run is not consumer ChatGPT certification,
and the public-only data source cannot establish private/account-wide inventory.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

try:
    from .capture_public_portfolio import API_ROOT, CaptureError, fetch_json, fetch_open_pull_requests, mapped_repositories
    from .validate_trace import TraceError, validate_trace
except ImportError:  # direct script execution from this directory
    from capture_public_portfolio import API_ROOT, CaptureError, fetch_json, fetch_open_pull_requests, mapped_repositories
    from validate_trace import TraceError, validate_trace

RESPONSES_URL = "https://api.openai.com/v1/responses"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
MAX_TOOL_CALLS = 16
MAX_TOOL_OUTPUT_CHARS = 12000
OWNER = "mythologyprospector-hub"


class RunnerError(RuntimeError):
    pass


TOOLS = [
    {
        "type": "function",
        "name": "list_mapped_public_repositories",
        "description": "Return the public repository names listed in the checked-out World REPOSITORIES.md map. This is not account-wide inventory.",
        "parameters": {"type": "object", "properties": {}, "required": [], "additionalProperties": False},
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_public_repository_overview",
        "description": "Fetch public repository metadata and its open pull requests. Only mapped public repositories are allowed.",
        "parameters": {
            "type": "object",
            "properties": {"repository": {"type": "string"}},
            "required": ["repository"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_public_issue_or_pull_request",
        "description": "Fetch a current public issue or pull request by number from a mapped public repository. Only read operations are available.",
        "parameters": {
            "type": "object",
            "properties": {
                "repository": {"type": "string"},
                "number": {"type": "integer"},
            },
            "required": ["repository", "number"],
            "additionalProperties": False,
        },
        "strict": True,
    },
]


def api_json(url: str, api_key: str, payload: dict[str, Any]) -> dict[str, Any]:
    request = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=90) as response:
            data = json.load(response)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RunnerError(f"Responses API request failed: {type(exc).__name__}") from exc
    if not isinstance(data, dict):
        raise RunnerError("Responses API returned a non-object response")
    return data


def gh_get(url: str) -> Any:
    return fetch_json(url)


def require_public_repository(repository: str, base: str, get_json=gh_get) -> dict[str, Any]:
    """Fail closed unless GitHub currently confirms this exact repository is public."""
    repo = get_json(base)
    if not isinstance(repo, dict):
        raise RunnerError("Repository metadata was not an object; request refused")
    full_name = repo.get("full_name")
    if (
        repo.get("private") is not False
        or not isinstance(full_name, str)
        or full_name.lower() != repository.lower()
    ):
        raise RunnerError("Repository was not confirmed public; request refused")
    return repo


def run_tool(name: str, args: dict[str, Any], allowed: set[str], map_names: list[str]) -> tuple[str, str]:
    if name == "list_mapped_public_repositories":
        return f"{OWNER}/world", json.dumps({
            "mapped_public_repositories": map_names,
            "coverage_limit": "Map entries only; not account-wide inventory and no private repositories queried.",
        })
    repository = args.get("repository")
    if not isinstance(repository, str) or repository not in allowed:
        raise RunnerError("Requested repository is outside the mapped public-repository allowlist")
    path = repository.split("/", 1)[1]
    base = f"{API_ROOT}/repos/{OWNER}/{path}"
    if name == "get_public_repository_overview":
        repo = require_public_repository(repository, base)
        pulls = fetch_open_pull_requests(repository, gh_get)
        result = {
            "repository": repository,
            "visibility": "public",
            "default_branch": repo.get("default_branch"),
            "pushed_at": repo.get("pushed_at"),
            "updated_at": repo.get("updated_at"),
            "open_pull_requests": [{
                "number": p.get("number"),
                "title": p.get("title"),
                "url": p.get("html_url"),
                "draft": p.get("draft"),
                "updated_at": p.get("updated_at"),
                "head_sha": (p.get("head") or {}).get("sha"),
                "base": (p.get("base") or {}).get("ref"),
            } for p in pulls],
        }
        return repository, json.dumps(result)
    if name == "get_public_issue_or_pull_request":
        # Re-check visibility at point of use; a mapped repository may have changed.
        require_public_repository(repository, base)
        number = args.get("number")
        if not isinstance(number, int) or isinstance(number, bool) or number < 1:
            raise RunnerError("number must be a positive integer")
        item = gh_get(base + f"/issues/{number}")
        if item.get("repository_url", "").rstrip("/").lower() != base.lower():
            raise RunnerError("GitHub returned an item from an unexpected repository")
        result = {
            "repository": repository,
            "number": number,
            "title": item.get("title"),
            "state": item.get("state"),
            "url": item.get("html_url"),
            "updated_at": item.get("updated_at"),
            "body": (item.get("body") or "")[:5000],
            "is_pull_request": "pull_request" in item,
            "merged": None,
        }
        if "pull_request" in item:
            pr = gh_get(base + f"/pulls/{number}")
            result["merged"] = pr.get("merged")
            result["draft"] = pr.get("draft")
            result["head_sha"] = (pr.get("head") or {}).get("sha")
            result["base"] = (pr.get("base") or {}).get("ref")
        return repository, json.dumps(result)
    raise RunnerError("Tool name is not allowlisted")


def bounded_tool_payload(evidence_id: str, result: dict[str, Any]) -> str:
    """Encode valid JSON even when the full evidence payload exceeds the model-input cap."""
    payload = {"evidence_id": evidence_id, "result": result}
    encoded = json.dumps(payload)
    if len(encoded) <= MAX_TOOL_OUTPUT_CHARS:
        return encoded
    preview = json.dumps(result, ensure_ascii=False)
    return json.dumps({
        "evidence_id": evidence_id,
        "truncated": True,
        "original_result_chars": len(preview),
        "preview": preview[: max(0, MAX_TOOL_OUTPUT_CHARS // 2)],
        "note": "Result preview truncated for model input; full result is preserved in the runner artifact.",
    })


def output_text(response: dict[str, Any]) -> str:
    chunks = []
    for item in response.get("output", []):
        if item.get("type") == "message":
            for content in item.get("content", []):
                if content.get("type") == "output_text" and isinstance(content.get("text"), str):
                    chunks.append(content["text"])
    return "\n".join(chunks)


def function_calls(response: dict[str, Any]) -> list[dict[str, Any]]:
    return [item for item in response.get("output", []) if item.get("type") == "function_call"]



def validate_mapped_inventory(trace: dict[str, Any], map_names: list[str]) -> None:
    """Require the model inventory to cover the exact mapped-public scope."""
    repositories = trace.get("repositories")
    if not isinstance(repositories, list):
        raise RunnerError("Model trace repositories must be a list")
    observed = []
    for repo in repositories:
        if not isinstance(repo, dict) or not isinstance(repo.get("name"), str):
            raise RunnerError("Every inventory entry must have a repository name")
        if repo.get("map_status") != "mapped":
            raise RunnerError(
                "Mapped-public-only inventory cannot classify entries as unmapped"
            )
        observed.append(repo["name"])
    expected = set(map_names)
    actual = set(observed)
    missing = sorted(expected - actual)
    unexpected = sorted(actual - expected)
    if missing or unexpected or len(observed) != len(actual):
        details = []
        if missing:
            details.append("missing mapped repositories: " + ", ".join(missing))
        if unexpected:
            details.append("repositories outside map: " + ", ".join(unexpected))
        if len(observed) != len(actual):
            details.append("duplicate repository names")
        raise RunnerError("Inventory does not match mapped public-repository scope (" + "; ".join(details) + ")")


def validate_ranked_item_grounding(trace: dict[str, Any], ledger: list[dict[str, Any]]) -> None:
    """Require every ranked work item to resolve to a fetched public issue or PR."""
    by_id = {entry.get("id"): entry for entry in ledger if isinstance(entry, dict)}
    comparison = trace.get("portfolio_comparison")
    items = comparison.get("ranked_items") if isinstance(comparison, dict) else None
    if not isinstance(items, list):
        raise RunnerError("Portfolio comparison ranked_items must be a list")
    for item in items:
        if not isinstance(item, dict):
            raise RunnerError("Each ranked work item must be an object")
        item_id = item.get("id")
        refs = item.get("evidence_refs")
        if not isinstance(item_id, str) or not isinstance(refs, list):
            raise RunnerError("Each ranked work item needs an id and evidence references")
        grounded = False
        for ref in refs:
            entry = by_id.get(ref)
            if not entry or entry.get("tool") != "get_public_issue_or_pull_request":
                continue
            payload = entry.get("result")
            repository = entry.get("repository")
            number = payload.get("number") if isinstance(payload, dict) else None
            if not isinstance(payload, dict) or payload.get("state") != "open":
                continue
            if payload.get("is_pull_request") is True and payload.get("merged") is True:
                continue
            if isinstance(repository, str) and isinstance(number, int) and item_id == f"{repository}#{number}":
                grounded = True
                break
        if not grounded:
            raise RunnerError(
                f"Ranked item {item_id!r} must use id '<owner>/<repo>#<number>' and cite a fetched issue or pull request for that exact item"
            )



SOURCE_CHECK_FIELDS = {"repository", "number", "title", "state", "url", "updated_at", "is_pull_request", "merged", "draft", "head_sha", "base"}


def validate_source_checks(trace: dict[str, Any], ledger: list[dict[str, Any]]) -> dict[str, str]:
    """Verify explicit source facts against fetched payloads; never grade prose judgments."""
    by_id = {entry.get("id"): entry for entry in ledger if isinstance(entry, dict)}
    comparison = trace.get("portfolio_comparison")
    items = comparison.get("ranked_items") if isinstance(comparison, dict) else None
    if not isinstance(items, list):
        raise RunnerError("Portfolio comparison ranked_items must be a list")
    for item in items:
        if not isinstance(item, dict):
            raise RunnerError("Each ranked work item must be an object")
        item_id = item.get("id", "<unknown>")
        refs = item.get("evidence_refs")
        checks = item.get("source_checks")
        if not isinstance(refs, list) or not isinstance(checks, list) or not checks:
            raise RunnerError(f"Ranked item {item_id!r} needs non-empty source_checks alongside evidence_refs")
        for check in checks:
            if not isinstance(check, dict):
                raise RunnerError(f"{item_id}: each source check must be an object")
            ref = check.get("evidence_ref")
            field = check.get("field")
            if ref not in refs:
                raise RunnerError(f"{item_id}: source check must cite one of the item's evidence_refs")
            if field not in SOURCE_CHECK_FIELDS or "expected" not in check:
                raise RunnerError(f"{item_id}: source check needs an allowed field and expected value")
            entry = by_id.get(ref)
            if not entry or entry.get("tool") != "get_public_issue_or_pull_request":
                raise RunnerError(f"{item_id}: source check {ref!r} is not a fetched issue/PR result")
            payload = entry.get("result")
            if not isinstance(payload, dict):
                raise RunnerError(f"{item_id}: source check {ref!r} has no source payload")
            actual = entry.get("repository") if field == "repository" else payload.get(field)
            expected = check["expected"]
            if type(actual) is not type(expected) or actual != expected:
                raise RunnerError(f"{item_id}: source check failed for {field!r} in {ref!r}; expected {expected!r}, source has {actual!r}")
    return {
        "identity_and_reference_validity": "verified",
        "declared_source_facts": "verified",
        "ranking_impact_and_dependency_judgments": "human_review_required",
    }


def run_evaluation(candidate_sha: str, map_path: str, api_key: str, model: str, output_path: str,
                   post_json=api_json, get_json=gh_get) -> dict[str, Any]:
    if not SHA_RE.fullmatch(candidate_sha):
        raise RunnerError("candidate SHA must be a full 40-character commit SHA")
    if not api_key.strip():
        raise RunnerError("OPENAI_API_KEY is required; no API request was made")
    if not model.strip():
        raise RunnerError("WORLD_EVAL_MODEL must be explicitly configured")
    names = mapped_repositories(Path(map_path).read_text(encoding="utf-8"), OWNER)
    allowed = set(names)
    ledger: list[dict[str, Any]] = []
    call_count = 0
    trace = None
    failure = None
    last_model_text = None
    started = datetime.now(timezone.utc).isoformat()
    prompt = (
        "Run World Factory scenario I as an evidence-driven read-only evaluator. "
        "You may use only the provided read-only tools. Inspect the mapped public portfolio; "
        "compare at least two real active work items from current tool evidence, including blockers, "
        "dependencies, impact and verification; choose a ranked recommendation with tradeoffs; "
        "complete one useful read-only action. Do not claim account-wide or private-repository coverage: "
        "this runner can inspect only public repositories in REPOSITORIES.md. State that this is an "
        "important unverified limitation. Return ONLY a JSON object matching the trace validator: "
        "schema_version=1, scenario_id='I', candidate_sha, inventory_scope='mapped_public_repositories_only', tool_results (use each evidence id returned "
        "by tools), repositories (each entry name, map_status, lifecycle, evidence_refs), map_reconciliation "
        "(complete, unmapped_repositories, mapped_repositories_missing_from_inventory, notes), "
        "portfolio_comparison (ranked_items with id, rank, eligible, reason, tradeoffs, evidence_refs, source_checks; "
        "unknowns), completed_action (status='completed', kind='read_only', description, evidence_refs). "
        "Each ranked work item id must be exactly '<owner>/<repo>#<issue-or-PR-number>' and cite a successful get_public_issue_or_pull_request result for that exact item. " 
        "Each repository entry must cite a successful result for that repository. Each ranked item must include non-empty source_checks with evidence_ref, field, and expected; cite one of that item's evidence_refs and assert an exact source payload value. Allowed fields: repository, number, title, state, url, updated_at, is_pull_request, merged, draft, head_sha, base. Ranking, impact, and dependency judgments remain human_review_required, not machine-verified. Do not invent evidence IDs. "
        "Use lifecycle='unresolved' when authorization/lifecycle is not established. For unmapped repositories, "
        "do not invent account-wide data; list only what the available evidence supports."
    )
    request_input: Any = prompt
    previous_id = None
    try:
        while True:
            payload: dict[str, Any] = {
                "model": model,
                "input": request_input,
                "tools": TOOLS,
                "tool_choice": "auto",
                "parallel_tool_calls": False,
                "max_output_tokens": 6000,
            }
            if previous_id:
                payload["previous_response_id"] = previous_id
            response = post_json(RESPONSES_URL, api_key, payload)
            previous_id = response.get("id")
            if not previous_id:
                raise RunnerError("Responses API response had no id")
            calls = function_calls(response)
            if not calls:
                text = output_text(response)
                last_model_text = text
                try:
                    trace = json.loads(text)
                except json.JSONDecodeError as exc:
                    raise RunnerError("Model did not return a valid JSON trace") from exc
                break
            outputs = []
            for call in calls:
                call_count += 1
                if call_count > MAX_TOOL_CALLS:
                    raise RunnerError("Tool-call limit exceeded")
                name = call.get("name")
                try:
                    args = json.loads(call.get("arguments", "{}"))
                except json.JSONDecodeError as exc:
                    raise RunnerError("Model supplied malformed tool arguments") from exc
                if not isinstance(args, dict):
                    raise RunnerError("Tool arguments must be a JSON object")
                repository, raw = run_tool(name, args, allowed, names)
                result_id = f"e{len(ledger) + 1:03d}"
                result = {
                    "id": result_id,
                    "tool": name,
                    "repository": repository,
                    "status": "ok",
                    "read_only": True,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "arguments": args,
                    "result": json.loads(raw),
                }
                ledger.append(result)
                tool_payload = bounded_tool_payload(result_id, result["result"])
                outputs.append({
                    "type": "function_call_output",
                    "call_id": call["call_id"],
                    "output": tool_payload,
                })
            request_input = outputs
        if not isinstance(trace, dict):
            raise RunnerError("Model trace must be a JSON object")
        trace["candidate_sha"] = candidate_sha
        trace["scenario_id"] = "I"
        trace["schema_version"] = 1
        trace["tool_results"] = [
            {k: item[k] for k in ("id", "tool", "repository", "status", "read_only", "timestamp")}
            for item in ledger
        ]
        trace["runner_metadata"] = {
            "started_at": started,
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "model": model,
            "tool_call_count": call_count,
            "scope": "mapped public repositories only",
            "private_repositories_queried": False,
            "consumer_chatgpt_certified": False,
        }
        validate_mapped_inventory(trace, names)
        validate_ranked_item_grounding(trace, ledger)
        evidence_grades = validate_source_checks(trace, ledger)
        trace["evidence_grades"] = evidence_grades
        validation = validate_trace(trace)
        validation.extend([
            "Direct source-field checks matched the fetched ledger payloads.",
            "Ranking, impact, and dependency judgments remain human-review-required.",
        ])
        result = {
            "status": "public_only_trace_structure_pass",
            "candidate_sha": candidate_sha,
            "model": model,
            "report": trace,
            "model_response_text": last_model_text,
            "tool_ledger": ledger,
            "validation_notes": validation,
            "limitations": [
                "Trace structure/reference validation is not semantic truth validation.",
                "The runner does not enumerate the account's complete repository inventory.",
                "Private-repository lifecycle/authorization and consumer ChatGPT behavior remain untested.",
            ],
        }
    except Exception as exc:
        failure = f"{type(exc).__name__}: {exc}"
        result = {
            "status": "failed",
            "candidate_sha": candidate_sha,
            "model": model,
            "started_at": started,
            "failed_at": datetime.now(timezone.utc).isoformat(),
            "error": failure,
            "model_response_text": last_model_text,
            "tool_ledger": ledger,
            "limitations": [
                "Failure is not a readiness pass.",
                "Only mapped public repositories are in scope.",
                "Consumer ChatGPT behavior remains untested.",
            ],
        }
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if failure:
        raise RunnerError(failure)
    return result


def main(argv: list[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate-sha", required=True)
    parser.add_argument("--map", default="REPOSITORIES.md")
    parser.add_argument("--output", default="artifacts/scenario-i-api-run.json")
    args = parser.parse_args(argv)
    api_key = os.environ.get("OPENAI_API_KEY", "")
    model = os.environ.get("WORLD_EVAL_MODEL", "")
    try:
        result = run_evaluation(args.candidate_sha, args.map, api_key, model, args.output)
        print(f"API evaluation completed; trace structure status: {result['status']}.")
        print("This does not certify account-wide inventory or consumer ChatGPT behavior.")
        return 0
    except (OSError, RunnerError, CaptureError, TraceError) as exc:
        print(f"API EVALUATION FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
