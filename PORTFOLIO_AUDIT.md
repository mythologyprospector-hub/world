# Portfolio Audit Snapshot

**Snapshot date:** 2026-10-17  
**Status:** Remote evidence inventory completed within the stated scope; factory readiness remains **UNVERIFIED**.  
**Purpose:** Give a fresh World session a durable, evidence-bounded account of the current public portfolio, its open proposals, and the next justified follow-ups.

This is a dated snapshot, not canon, a readiness certificate, or authorization to merge, implement, run live evaluations, or resume held work. Check current main branches, PR heads, and workflow evidence before acting. The running findings log is [World issue #25](https://github.com/mythologyprospector-hub/world/issues/25).

## Scope and limits

The audit reviewed GitHub repository metadata, current main-branch documents, selected PR diffs and metadata, and available workflow evidence. It also reviewed private-repository metadata and governance documents only where needed for status and privacy boundaries.

- No source code was changed by the audit.
- No tests were executed by the audit.
- No live model/API evaluation or billable API call was made.
- No local filesystem, checkout, or worktree inventory was available.
- No live Organs host/runtime inspection was performed.
- No personal source records or private staging lanes were opened.
- Private repository identities, paths, and project-level details are intentionally omitted from this public report.

The World repository map is intentionally public-only. That is a scope choice, not proof of account-wide or private-repository completeness.

## Current public portfolio baseline

| Repository | Current main SHA | Role and observed state | Open PRs at snapshot |
|---|---|---|---|
| World | 07874c39eac15eae1d0760d4b730cacd68af5315 | World-level orientation and portfolio audit. Readiness remains unverified; issue #25 is the running audit log. | [#17](https://github.com/mythologyprospector-hub/world/pull/17), [#18](https://github.com/mythologyprospector-hub/world/pull/18), [#19](https://github.com/mythologyprospector-hub/world/pull/19), [#20](https://github.com/mythologyprospector-hub/world/pull/20), [#22](https://github.com/mythologyprospector-hub/world/pull/22), [#24](https://github.com/mythologyprospector-hub/world/pull/24), [#26](https://github.com/mythologyprospector-hub/world/pull/26) |
| Project Seed | 140b55cfa55ed1f80c64d6d65f98bd1f1e48ad66 | Shared operating constitution and project-seed propagation. Several proposals are open; PR #7 has a confirmed static false-negative path, and PR #16 combines a useful sequencing correction with a separate authorization change. | [#4](https://github.com/mythologyprospector-hub/project_seed/pull/4), [#7](https://github.com/mythologyprospector-hub/project_seed/pull/7), [#9](https://github.com/mythologyprospector-hub/project_seed/pull/9), [#16](https://github.com/mythologyprospector-hub/project_seed/pull/16) |
| Episteme | 414709ba48e3a6d3fa9d8ea17c67d846de02d925 | Scientific discovery engine. Canonical Phase 28 documentation is internally inconsistent; PR #43's current source regresses the safer mainline planner-payload boundary. | [#29](https://github.com/mythologyprospector-hub/episteme/pull/29), [#30](https://github.com/mythologyprospector-hub/episteme/pull/30), [#43](https://github.com/mythologyprospector-hub/episteme/pull/43), [#59](https://github.com/mythologyprospector-hub/episteme/pull/59), [#62](https://github.com/mythologyprospector-hub/episteme/pull/62) |
| Praxis | 679c8348980590728386f6655af397a2d30f97d2 | Human-centered solution-discovery engine. Canonical documents preserve the human decision gate and explicit evidence admission. One Seed-sync PR is open. | [#6](https://github.com/mythologyprospector-hub/praxis/pull/6) |
| Renaissance | 5837e4555158a417ae7c38e89ecbc9e711237ac7 | Foundational, evolving constitutional layer. Its proposed constellation audit is stale as a current inventory and contains public/private-boundary and visibility-consistency problems. | [#13](https://github.com/mythologyprospector-hub/renaissance/pull/13) |
| Organs | 76fe42259f43414afc6a825556180d70c24b8f73 | Runtime infrastructure. Canonical scope wording conflicts across Organs and Renaissance documents; live host/runtime state is unverified. | [#17](https://github.com/mythologyprospector-hub/organs/pull/17) |
| Wonderweave | 73fcfbdd867f4f03c4e1072cfac871c00694567d | Proposed game canon and experimental first-mystery materials. No human playtest has been conducted; the owner’s current hold remains in force. | [#7](https://github.com/mythologyprospector-hub/wonderweave/pull/7), [#11](https://github.com/mythologyprospector-hub/wonderweave/pull/11), [#14](https://github.com/mythologyprospector-hub/wonderweave/pull/14), [#15](https://github.com/mythologyprospector-hub/wonderweave/pull/15) |


The report's own draft PR, World #27, was opened after this portfolio inventory was captured and is intentionally not counted in the pre-existing PR list above.
Open PRs are proposals, not canonical state. A passing documentation workflow does not prove behavioral readiness. The listed public repositories had no repository-level rulesets returned by the inspected API, and each main branch reported unprotected; organization-level ruleset enforcement could not be inspected, so effective higher-level enforcement remains unverified.

## Confirmed discrepancies

### 1. Readiness and authorization are not yet reconciled

- World PR #19 claims to coordinate readiness changes from #17 and #18, but its current diff omits #18's human-gate and observational-learning changes.
- PR #19 also proposes broad standing builder authorization across accessible repositories. That is a distinct governance change and conflicts with the existing rule that private repositories are historical/reference-only unless specifically reactivated. It must not be treated as a mechanical sequencing fix.
- Project Seed PR #16 correctly proposes allowing read-only portfolio discovery before readiness passes while keeping downstream selection and implementation blocked. Its diff also changes private-repository authorization, and its base is stale relative to current main. Those decisions must be separated before acceptance.
- The mandatory/optional status of readiness scenarios A–H is not explicitly settled. Same-session tabletop observations are not fresh-session acceptance evidence.

### 2. World's proposed trace validator has evidence-integrity gaps

Static review of World PR #22 found:
- A completed action can satisfy “read-only” and “belongs to an inventoried repository” using different evidence records.
- A non-read-only ledger entry elsewhere in a trace can escape rejection if the action still cites a separate read-only result.
- The purported pass fixture contains an unmapped repository entry, while the integrated mapped-inventory gate rejects non-mapped entries in this mode. The trace-only fixture is therefore not a coherent end-to-end known-good fixture.
- The PR description's “latest verification” section names an older head and run than the current PR head. Exact-head fixture workflow evidence exists, but it does not repair these static gaps or certify readiness.

The trusted-runner isolation in PR #24 is an opt-in proposal. Its available workflow evidence covers documentation/orientation checks, not a live API evaluation or a dedicated security-specific test of dispatch behavior. No API evaluation was run.

### 3. Project Seed verifier proposal can accept an unterminated loop

Static review of PR #7 found that its manifest parser can reach end-of-file without seeing the required loop terminator and still accept the manifest. The existing tests do not include a missing-terminator fixture. This is a confirmed false-negative path in the proposed verifier, not evidence that the installed Seed is corrupt.

### 4. Episteme Phase 28 status and PR #43 need reconciliation

- Canonical Phase 28 documentation labels the phase complete while retaining normative language that the capability is missing, proposed, and not ready to implement. This is a documentation discrepancy, not proof that the underlying implementation is broken or that scientific validity is established.
- PR #43 forwards raw evaluation and consequence records to the planner. Current main instead uses an allowlisted evaluation-feedback boundary and explicitly avoids forwarding raw records, result IDs, and numeric values. PR #43 therefore regresses the safer mainline boundary. Keep it draft; do not run a live blinded evaluation on this head.
- PR #59 has current-head test evidence, but a prior blinded live acceptance attempt failed. No new live run was performed.

### 5. Organs scope differs across canonical documents

Organs GOAL.md says the project exists solely to provide runtime infrastructure for Renaissance. Organs README.md describes shared runtime plumbing for the wider project world. Renaissance's Organs alignment document also states a Renaissance-only purpose. This is a scope/authority wording discrepancy; it does not prove runtime failure and does not authorize universal integration. The owner must settle the intended relationship.

### 6. Wonderweave sequencing remains on hold

Wonderweave PR #15 describes cold-start player testing as the next task. The owner's current instruction is to hold Wonderweave playtesting pending progress on an external dependency. The hold takes precedence. The player draft remains experimental, proposed canon is not approved canon, and no human playtest has occurred.

### 7. Public/private information boundaries need owner review

The audit found private or historical repository identities disclosed in multiple public surfaces: public Project Seed documents and workflow configuration, a public World issue body, public historical PR metadata, and Renaissance's proposed constellation audit. The public Renaissance audit also labels multiple entries private, contains an internal visibility-status/action contradiction, and no longer matches the current accessible repository inventory.

This report deliberately does not repeat those identities. The running log records affected public surfaces and evidence in sanitized form. The findings concern disclosure of identities, paths, or historical project context; they do not establish that private file contents are publicly readable. Do not blindly remove operational references or rewrite historical records. Owner review must decide what should remain public and how to preserve necessary automation and provenance safely.

### 8. Historical repository lifecycle is unresolved

A repository referenced in prior project context is absent from the current accessible inventory; exact metadata lookup returned 404 and name search returned no result. This does not prove deletion. It may have been renamed, moved, deleted, or become inaccessible. Do not guess a replacement or restore it without evidence.

## Evidence freshness and limits

- World PR #19's documentation/link check passed, but that is not behavioral evidence.
- World PR #22 has exact-head fixture workflow evidence; its description also retains a verification summary for an older head. No live model/API run occurred.
- World PR #24's available exact-head workflow evidence is documentation/orientation validation, not security-specific dispatch validation.
- World PR #26 is a documentation-only proposal; its workflow does not implement rolling collection or prove fresh-session behavior.
- Project Seed PR #16 lacks exact-head evidence for its current proposal. PR #7's historical workflow result does not cover the missing-terminator case.
- Seed-sync PRs are open review proposals. Episteme #62, Organs #17, and Praxis #6 have reported exact-head checks; Renaissance #13 and Wonderweave #14 had no PR-triggered workflow run found in the inspected evidence.
- This audit did not run any tests. Existing CI results were inspected as historical evidence, not reproduced.
- Local worktrees, uncommitted changes, and the live Organs installation were not inspected. GitHub state cannot establish local cleanliness or live runtime health.
- Public repository listing and the public World map do not establish that every historical or private project is current, accessible, or authorized for work.

## Readiness decision

**Factory readiness: UNVERIFIED.**

The remote portfolio inventory and current proposal review are complete to the limits above, but the acceptance gate is not passed. Fresh-session behavior remains unverified; required scenario status needs to be explicit; the proposed inspector has known fixture/validation gaps; and organization-level enforcement is unknown.

Therefore:
- Keep downstream project selection and implementation blocked until readiness evidence and the portfolio comparison are complete.
- Do not merge open PRs merely to make the proposal set look coherent.
- Do not run billable model/API evaluations without separate explicit approval.
- Keep Wonderweave playtesting and implementation on hold until the external dependency advances and the owner explicitly resumes that work.

## Recommended follow-up order

1. **Owner privacy review:** decide which public identity/path disclosures are intentional; then make a coordinated, approved correction while preserving operational behavior and provenance.
2. **Resolve authorization and sequencing separately:** reconcile World #17/#18/#19 and Project Seed #16 without granting blanket access to private repositories.
3. **Repair and qualify the validators:** add missing-terminator coverage to Project Seed #7; make World trace predicates bind to one valid evidence record; reconcile the fixture and integrated inventory gate; test both known-good and deliberately defective cases.
4. **Resolve Episteme's payload and status boundaries:** keep PR #43 draft until it follows the current allowlisted contract; reconcile Phase 28 documentation; do not substitute fixture tests for live blinded acceptance.
5. **Settle Organs scope:** reconcile GOAL, README, and Renaissance alignment language; inspect organization-level ruleset enforcement before relying on GitHub as a technical approval gate.
6. **Run a genuinely fresh-session readiness evaluation** only after the required scenarios and test fixtures are explicit and the owner authorizes the evaluation mode. Record exact commit, run, scope, and limitations.
7. **Only after readiness and portfolio comparison pass,** recommend a bounded next project step for owner approval. Wonderweave remains held until its dependency and resume authorization are confirmed.

## Audit trail

The running evidence log, including exact source revisions, classifications, and bounded follow-ups, is [World issue #25](https://github.com/mythologyprospector-hub/world/issues/25). This report is a sanitized public snapshot; private-repository identities and personal source material are intentionally excluded.
