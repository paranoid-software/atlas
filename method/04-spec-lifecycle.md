# The SPEC lifecycle

Everything buildable enters as a **SPEC**: one feature, one fix, one refactor, or a plan handed
over by another tool — turned into a small, deliverable specification *before any code is
written*.

## The rule: no coding without a SPEC

1. **Nothing gets coded without a SPEC.** A loose plan — even a good one from another agent — is
   converted into a `SPEC_NNNN_<SLUG>.md` first.
2. **`DRAFT_*.md` is the optional shaping stage**, for an item still being decided. A DRAFT
   either **graduates to a SPEC** or is **discarded** — it is never a destination.
3. **The backlog indexes the open SPECs/DRAFTs** — one line each, nothing else.
4. **A closed SPEC moves to `_archived/`**, with its findings file.

## What a SPEC is — and is not

A SPEC is the **what** plus its **route**: the goal, its acceptance criteria, its repos, its
boundaries, and a **Plan** — the ordered steps that deliver it. The fixed shape (template in
[06-bootstrap.md](06-bootstrap.md)): `created` · `repos` · **What** · **Acceptance** · **Out of
scope** · **Plan**. Nothing else.

**Never in a SPEC:**
- **state** — status, progress, where-we-are → `STATUS.md → Active`;
- **checkboxes** — that's progress, not plan;
- **the how** — the technique of each step; decided live, its record is the code;
- **code** — no fenced blocks, diffs or signatures; reference a path instead;
- **findings** — blockers, misconceptions, wrongly-posed parts → its findings file;
- **archaeology** — no "previously", "changed from", attempts or dead ends
  ([05-discipline.md](05-discipline.md));
- **session notes**.

A SPEC that grows any of these is **contaminated — strip it**. That is what lets any agent open a
SPEC and read only *what we are doing and in what order*.

## Findings — beside the SPEC, never in it

**`SPEC_NNNN_FINDINGS.md`**, the SPEC's companion (same number), keeps what you learn while
resolving it — something that blocks it, a misconception that can't be resolved within it,
something wrongly posed in the SPEC itself — so it isn't lost and doesn't turn the SPEC into a
log. Create it on the first finding.

It is a **record, not a checklist: findings never hold a SPEC open.** A finding worth pursuing
becomes its own DRAFT or SPEC; the file is archived with its SPEC.

## Status values

```
READY  →  IN PROGRESS  →  IN REVIEW  →  CLOSED  →  _archived/
```

| Status | Meaning |
|---|---|
| **READY** | Shaped and buildable; not started. |
| **IN PROGRESS** | Being implemented, on its branch ([05-discipline.md](05-discipline.md)). |
| **IN REVIEW** | Implementation finished; a reviewer other than the implementer verifies the work **in the code**, not in the agent's report. |
| **CLOSED** | The independent review verified the work in the code, a commit exists, and **the human said close**. The SPEC moves to `_archived/`. |

**The lifecycle ends at the code.** Push, PR, merge, release or deploy are not the framework's
business — they depend on the project and nothing in the Atlas can verify them. A SPEC closed
too early goes back to the root as **IN REVIEW**.

## Picking up a SPEC, and leaving it

A fresh agent resumes in two reads: its block in **`STATUS.md → Active`** (**Done / Next /
Blocked** — where we left off), then the **SPEC** (what we are doing). Continue from **Next**.

Before stopping or handing off, **rewrite that Active block** to the current state — never append
to it. That is the checkpoint `/atlas-sync` refreshes.

## The how is decided live

The Plan gives the route; the **how** of each step is settled at execution time: the agent
**proposes** an approach, the **human approves**, then it executes. Plan mode, where the tool has
one, makes this a natural gate — and the cheapest review there is, catching a wrong approach
before any code exists.

**Nothing about the how is written down.** The general way of working already lives in the
memory store; what remains is step-specific and its record is **the code**. No `PLAN_*.md`, no
`TASKS_*.md`, no design notes per step. A how-decision with standing value graduates to
`CLAUDE.md` (project-specific) or the memory store (universal).

## The deviations registry

`DEVIATIONS.md` runs **independently** of the SPEC flow. It records explicit, deliberate
divergences from a memory-store rule *that applies to this Atlas* — a rule you'd be expected to
follow but deliberately (or for now) don't, with the reason. A divergence may also spawn a SPEC
to resolve it.

It is **not** a list of out-of-domain rules that simply don't apply — you don't enumerate what
the project *isn't*. (A memory-server project doesn't record "I'm not a web app.")
