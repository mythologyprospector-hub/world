# Agent Operating Rules

## Scope
This file governs agent behavior at the world level. Individual project repositories remain authoritative for their own implementation and canon.

## Cross-repository lookup
Treat the GitHub world as one connected unit of orientation. When the answer is not present in the current repository, look in the relevant repositories before guessing.

## One automatic retry
For a recoverable tool or repository operation failure, retry the same operation **once** automatically.

- Retry only once.
- Re-check current file state/SHA before retrying a write.
- Do not use the retry to bypass permissions, safety restrictions, authorization boundaries, or project canon.
- If the retry fails, stop and report the failure plainly.
- Never claim a change succeeded unless the tool confirms it.

## Public world map
This repository is a public world-level orientation layer. Do not name private repositories in public orientation documents merely to help agents navigate. Private projects remain available through authorized project work when explicitly needed.
