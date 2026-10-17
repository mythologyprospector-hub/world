# World

## Purpose

The mythologyprospector-hub GitHub account contains a constellation of independent projects developed under a common working philosophy.

The projects are not one monolithic application.

They may cooperate through explicit contracts where useful, while retaining separate identities, responsibilities, architectures, and governance.

## World principle

> **Unity without sameness.**

A project can belong to the broader world without becoming a subsystem of another project.

## Mission seriousness

The mission is not rhetorical decoration or an aspirational tagline. It is the serious, governing purpose of this work: to make a real, constructive contribution to the progress and flourishing of humanity by increasing our ability to understand, discover, create, learn, and solve problems.

The scale of that purpose does not justify grandiose claims. No project, model, agent, or contributor should claim progress merely because its architecture is ambitious, its roadmap is long, or its tests pass. Claims of contribution must be earned through observable capability, reproducible evidence, honest limits, and benefit that respects human agency and the well-being of others.

This mission is a direction and a standard of accountability, not a promise that success is guaranteed. Work should remain serious about the aim, humble about what has been achieved, and willing to revise its methods when evidence demands it.

## Shared runtime substrate

**Organs is the shared runtime plumbing for this project world.** Projects should account for Organs when designing or building, and use its published contracts when shared runtime capabilities fit the need. This does not make the world one monolithic application or require every feature to connect directly to an organ. Projects may remain independent and standalone; connections are optional, deliberate, and contract-based. Organs provides common infrastructure, not project meaning, domain truth, or authority.

Before meaningful design decisions, inspect the relevant repositories and their actual capabilities rather than assuming the current project is the whole landscape. Consider reuse, bridges, and independent operation; choose based on evidence and the mission, not a desire to connect everything.

## Orientation model

An arriving agent should think in this order:

```
WORLD
  ↓
PROJECT MAP
  ↓
RELEVANT PROJECT
  ↓
PROJECT CANON
  ↓
CURRENT WORK
```

Do not begin by assuming the repository named in the current conversation is the whole system.

## Durable truth

Conversation is temporary working context.

GitHub repositories are the durable project record.

Important decisions, architecture, status, tests, and handoff information should be recorded in the appropriate repository rather than relying on conversation history.

## Project sovereignty

Each project owns its own:

- purpose;
- boundaries;
- canon;
- architecture;
- roadmap;
- implementation;
- tests;
- decisions.

Cross-project relationships must be explicit and evidence-based.

## Ecosystem integrity and rolling audit

The World has a standing responsibility to help ensure that repositories are **individually correct and collectively coherent**, without forcing them into sameness.

This is not merely a one-time portfolio survey. The intended outcome is a **rolling ecosystem audit**: establish a broad, evidence-backed baseline across all authorized repositories, then continuously refresh that picture so inconsistencies and drift do not quietly accumulate.

The audit is persistent in responsibility, bounded in each run, and honest about coverage. It must not claim that the entire ecosystem is healthy just because a single run passes or some repositories were inaccessible.

### Audit layers

- **Repository-local checks:** each repository validates its own applicable rules, documentation, tests, and deliverables.
- **Change-triggered checks:** run fast, deterministic checks when relevant code, docs, workflows, repository maps, or declared contracts change.
- **Portfolio reconciliation:** periodically revisit the full authorized portfolio to catch missed events, stale evidence, untracked changes, missing repositories, and cross-project drift.
- **Targeted rechecks:** when a source revision, dependency, contract, or finding changes, re-evaluate the affected checks rather than blindly repeating every expensive test.
- **Cross-repository contract checks:** validate only explicitly declared relationships; do not infer that projects must share an architecture or data model.
- **Inspector qualification:** test important checks against known-good and deliberately defective fixtures, and periodically test the audit machinery itself.
- **Finding lifecycle:** preserve traceable evidence and enough history to distinguish newly detected, persistent, resolved, regressed, and unverified findings.

### Evidence and authority

Every finding should state its scope and evidence source, with source revision and capture/check time where available. Use clear outcomes such as **Verified**, **Discrepancy**, and **Unverified**. Missing evidence is not proof of failure; a passing script is not proof of semantic truth.

Begin with report-first, advisory findings. A check may become blocking only after its coverage, failure behavior, false positives, and ability to detect known defects are demonstrated and the policy is approved.

Automate routine detection, not consequential judgment. Do not silently rewrite a project's canon or automatically merge, delete, or otherwise make consequential changes. Ambiguous or consequential findings go to the human gate.

### Coverage, privacy, and cadence

Public and private coverage must be distinguished explicitly. Never expose private repository names or contents in public World artifacts, and never imply that public-only inspection covers private repositories. Use a tiered cadence: fast checks on relevant changes, broader scheduled reconciliation, and deeper tests only when justified, authorized, and safe. Do not introduce billable model/API calls or query private sources beyond existing authorization without explicit approval.

The audit should grow from the existing World executive portfolio/evidence collector, not duplicate it with a second inspector. First map and qualify the current collector, its fixtures, and the related readiness/security work. The broad baseline audit and the rolling cadence are one design: the baseline discovers existing drift; the rolling process prevents the picture from becoming stale.

The staged work and acceptance criteria are tracked in [World issue #25: Establish ecosystem-wide integrity checks without erasing project sovereignty](https://github.com/mythologyprospector-hub/world/issues/25). This principle records the intended direction; it does not claim the inspector or rolling audit is already implemented or verified. The existing World factory-readiness gate remains in force.

## Current philosophy

The world favors:

- human agency;
- explicit boundaries;
- inspectability;
- provenance;
- reproducibility;
- deterministic behavior where practical;
- evidence before assertion;
- small verified steps;
- replaceability rather than unnecessary centralization;
- fun while doing serious work.
