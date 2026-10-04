# Agent Operating Rules

## Scope
This file governs agent behavior at the world level. Individual project repositories remain authoritative for their own implementation and canon.

## Cross-repository lookup
Treat the GitHub world as one connected unit of orientation. When the answer is not present in the current repository, look in the relevant repositories before guessing.

## Private and retired projects
Authorized tooling may see private repositories. Privacy is therefore not an agent authorization boundary by itself. Private project contents must not be surfaced in public world documentation without authorization.

A project explicitly retired by James is historical archaeology only. It is not current architecture or authority. Do not extend, integrate, or revive it unless James explicitly does so. **Akasha is retired historical archaeology.**

## One automatic retry
For a recoverable tool or repository operation failure, retry the same operation **once** automatically.

- Retry only once.
- Re-check current file state/SHA before retrying a write.
- Do not use the retry to bypass permissions, safety restrictions, authorization boundaries, or project canon.
- If the retry fails, stop and report the failure plainly.
- Never claim a change succeeded unless the tool confirms it.

## Public world map
This repository is a public world-level orientation layer. Do not name private repositories in public orientation documents merely to help agents navigate. Private projects remain available through authorized project work when explicitly needed.

## World-level gap question
After checking the current repository and then the relevant repositories across the whole world, if no justified next task can be found, stop inventing work and ask:

**What is this world missing now that this much exists?**

The purpose of the world is to help mankind prosper, flourish, and advance without dystopian, Orwellian, coercive, or dehumanizing systems. This is a guiding objective, not permission to override project canons, evidence, safety boundaries, or human judgment.
