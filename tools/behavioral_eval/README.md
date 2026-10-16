# Behavioral evaluation trace prototype

This directory contains the first, deliberately limited piece of the World readiness evaluation work: a deterministic validator for a saved scenario-I trace.

## What it checks

- The trace identifies scenario I and pins the exact candidate commit SHA.
- The account inventory is non-empty, classifies each listed repository, cites actual result IDs, and reconciles unmapped repositories.
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
