# Behavioral evaluation trace prototype

This directory contains the first, deliberately limited piece of the World readiness evaluation work: a deterministic validator for a saved scenario-I trace.

## What it checks

- The trace identifies scenario I and pins the exact candidate commit SHA.
- The inventory explicitly declares its scope as mapped public repositories only, classifies each listed repository, cites result IDs, and reconciles map entries. It cannot claim account-wide coverage.
- In the API runner, the returned inventory is cross-checked against the exact repository names parsed from the checked-out map; omitted mapped repositories, extra names, duplicates, and `unmapped` classifications are rejected before trace validation.
- The portfolio comparison ranks at least two eligible work items, gives reasons and tradeoffs, cites result IDs, and discloses unknowns.
- A claimed completed action is explicitly read-only and cites a successful read-only tool result.
- Every evidence reference resolves to a result recorded in the same trace.

## What it does not prove

This is **not a model runner**. It does not launch an assistant, query GitHub, inspect whether a cited source actually supports the prose, prove the inventory is complete, or certify consumer ChatGPT behavior. A fabricated result can still be written into a trace; the validator only prevents a report from citing result IDs that are absent from that trace. The fixture is illustrative, not live repository evidence.

The API-runner design remains separate work and requires a supported execution path, credential/data-handling review, and explicit opt-in. This fixture workflow uses no API secret and does not call a model. A pass here means only that the deterministic trace-shape tests pass.

## Run locally

From the repository root:

```bash
python -m unittest discover -s tools/behavioral_eval/tests -v
python tools/behavioral_eval/validate_trace.py tools/behavioral_eval/fixtures/scenario_i_pass.json
```

The test suite includes a complete fixture and negative cases for missing evidence, incomplete comparisons, non-read-only action evidence, incomplete map reconciliation, and an unpinned candidate SHA.


## Live public evidence capture

The workflow also runs `capture_public_portfolio.py` against the checked-out `REPOSITORIES.md`. It queries GitHub's public API for each mapped repository, captures repository metadata and open pull requests, pins the candidate commit SHA, and uploads `public-portfolio-evidence.json` as a 14-day workflow artifact.

Run it locally from the repository root with a full commit SHA:

```bash
python tools/behavioral_eval/capture_public_portfolio.py --candidate-sha <40-character-commit-sha>
```

The collector is read-only and refuses any repository not confirmed public. It deliberately does **not** inventory every repository visible to an account, query private repositories, establish private-repository lifecycle or authorization, run an assistant/model, or prove that an assistant used the collected evidence correctly. A successful capture is a public evidence snapshot, not a readiness pass.


## Opt-in API-runner prototype

`api_runner.py` is an experimental Responses API runner with three read-only public GitHub functions and a hard cap of 16 tool calls. It refuses repositories outside the checked-out public map, records a structured tool ledger, and writes an artifact for success or failure. It has no shell or repository-write tools.

The manual-only workflow `.github/workflows/behavioral-eval-api.yml` requires an explicit confirmation string, a full candidate SHA, an `OPENAI_API_KEY` Actions secret, and a `WORLD_EVAL_MODEL` Actions variable. It does not run on pull requests or ordinary pushes. No API secret is assumed to exist; a missing secret or model setting fails closed.

**Important:** this runner is only a public-portfolio prototype. It cannot establish account-wide inventory completeness, inspect private repositories, or certify consumer ChatGPT. Its trace validator checks structure and reference integrity, not semantic truth. A successful run is evidence for review, not a readiness pass. A live run may incur API charges.
