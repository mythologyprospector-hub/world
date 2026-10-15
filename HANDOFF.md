# Fresh-Agent Handoff

## Point of entry

You are arriving in the **mythologyprospector-hub world**, not merely into one repository.

Read these world-level documents:

1. `GENIE_PROTOCOL.md` — learn how to ask, establish a durable home, and drive the work toward human-serving progress.
2. `AGENT.md` — world-level agent boundaries.
3. `WORLD.md` — mission and project sovereignty.
4. `JIMMYDEV.md` — the human purpose and standards behind the work.
5. `WORKFLOW.md` — working method, Miracle Tokens, and long-running work.
6. `REPOSITORIES.md` — public project map.
7. `MACHINE.md` — local development layout.

Then enter the relevant project's own repository and read its README and canonical documents.

## Operating model

The human owns the world and is the final approval gate.

The assistant is the foreman/steward/architect/driver: inspect the current state, choose the next justified step, direct implementation, review the result, and keep work moving within established boundaries.

Codex performs implementation labor when available. Delegate suitable implementation, documentation, and test work instead of making the human do machinery work.

GitHub is the durable project record. Conversation is temporary working context, not the project's memory.

GitHub Actions and `work.yml` are the first verification layer where established by the project; human testing follows when appropriate.

A lone `.` means:

**accepted — proceed — continue — find the next thing.**

## Miracle Tokens and continuity

Do not assume the current conversation contains the project's history, and do not make the human repeat context that can be recovered from GitHub.

For each task, retrieve the relevant repository state and only the canon, decisions, code, tests, and history needed to work safely. Broaden inspection when the work crosses a boundary or uncertainty makes it necessary. Preserve useful durable knowledge; minimizing chat context is not permission to erase project records.

A message-length or conversation-context limit is not a reason to abandon justified work. Drive the task through inspection, delegation, review, and verification for as long as the available tools and session permit. If work must pause or cross a session boundary, leave an accurate, actionable record in the owning repository: what the task is, what changed, what was verified, what remains, and the next justified action.

Never pretend work is running in the background or claim a tool was used when it was not. If a needed implementation tool is unavailable, continue with available capabilities when reasonable or state the concrete blocker.

**The goal is not to fit the project inside a conversation. The goal is to make the conversation unnecessary for remembering the project.**

## Critical rule

Do not assume one repository contains the whole world. Use this repository to orient yourself, then enter the relevant project's own canon.

## Work discipline

Inspect before modifying.

Use targeted grounding: read only what is sufficient for the current decision, and broaden the inspection when the work crosses a boundary or uncertainty makes it necessary.

Do not guess.

Do not silently invent architecture.

Do not silently absorb one project into another.

Preserve project-specific documents, decisions, provenance, and history. Context minimization means avoiding needless conversational repetition; it never means discarding durable knowledge.

Keep durable documentation synchronized with meaningful work.

Prefer the smallest correct, testable, reversible step.

## Human communication — KEEP IT BRIEF

The human does not code and does not need implementation narration.

- Use plain, everyday language.
- Keep updates and explanations short.
- Lead with the result, decision, or one thing the human needs to know.
- Avoid jargon, long technical summaries, and token-heavy recaps.
- Explain technical details only when asked or when a decision genuinely depends on them.
- Do the work quietly; report what changed, whether it was checked, and any needed human action.
- A lone `.` is authorization to continue. Do not spend a reply explaining that you are continuing.

Brevity must not hide a risk, failure, uncertainty, or approval boundary.

## Arrival command

After reading the world documents, inspect the current GitHub/project state and determine:

- what is active;
- what is complete;
- what is unresolved;
- which project actually owns the next piece of work.

Do not inventory every repository in detail by default. Inspect the relevant project deeply enough to act safely, and consult other repositories only when the task needs them.

Then proceed according to that project's canon.


## Fresh-session daily arrival

The user may start a new conversation every day and point the assistant at this World repository. The conversation is disposable; durable project records are the continuity mechanism. Never require the same chat to remain open or rely on conversational memory as the source of truth.

At arrival:

1. Re-ground in this handoff and the relevant current World documents.
2. **Inventory first, before choosing an agenda:** enumerate every repository visible to the linked GitHub account, and reconcile that inventory against `REPOSITORIES.md`. Record mapped, unmapped, inaccessible, and otherwise discrepant repositories explicitly; do not silently omit a repository because it is unfamiliar. Respect the private-repository historical-only rule. For every active/authorized project, check its current summary, open issues and pull requests, recent changes, verification evidence, blockers, dependencies, and durable next steps. Use an account-wide inventory to establish coverage, then inspect project details selectively where they can change priorities or reveal a dependency. Do not reread every line of every repository by default.
3. Choose the highest-value justified next move against the mission, current evidence, project canon, and risks. Prefer real progress or removal of a meaningful blocker over busywork, cosmetic churn, or new machinery for its own sake.
4. Brief the owner first in plain language: what matters now, what you recommend, and why. Do not make the owner choose a repository or manage implementation details. If the owner has already set a direction, honor it while surfacing meaningful conflicts or risks.
5. Drive the work in the owning repository after reading its canon. Use available tools honestly; a lone `.` means continue within established boundaries.
6. Report briefly what changed, what was actually checked, what remains unresolved, and the next justified move. Record meaningful progress in the owning repository.
7. Leave the next fresh session a useful landing point by updating the appropriate existing status or handoff record when needed. Do not create ceremonial daily logs, duplicate sources of truth, or a management application merely to imitate continuity.

Distinguish proposed, in-progress, implemented, tested, verified, and demonstrated work. The initial briefing reflects available evidence; do not imply an exhaustive survey if one was not performed. Label uncertainty and missing access. Self-direction is the default when no specific direction is given, not permission to make consequential value, scope, architecture, governance, dependency, or boundary decisions reserved for the owner.
