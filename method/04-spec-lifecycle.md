# The SPEC lifecycle

Everything buildable enters as a **SPEC**. A SPEC is the unit of work: one feature, one
fix, one refactor, or a plan handed over by another tool — converted into a small,
deliverable specification *before any code is written*.

## The rule: no coding without a SPEC

1. **Nothing gets coded without a SPEC.** Every workitem becomes a `SPEC_NNNN_<SLUG>.md`
   before any code is written. A loose plan — even a good one handed over by another agent
   — is **converted into a SPEC first**. You don't code from a loose plan.
2. **`DRAFT_*.md` is the optional shaping stage**, for an item still being decided (open
   questions, placeholders, unknowns). A DRAFT either **graduates to a SPEC** once its
   shape is fully defined, or is **discarded**. It is never a destination.
3. **The backlog indexes the open SPECs/DRAFTs** — one line each, index-only (never item
   bodies, never rules, never candidate universal rules).
4. **A shipped SPEC moves to `_archived/`** (same name). `_archived/` holds *only* shipped
   SPECs.

## Status values

A SPEC travels through these states. The distinction between the last few is the whole
point of the ship discipline (see [05-discipline.md](05-discipline.md)):

```
READY  →  IN PROGRESS  →  IN REVIEW  →  SHIPPED  →  archived
```

| Status | Meaning |
|---|---|
| **READY** | Shaped and buildable; not yet started. |
| **IN PROGRESS** | An agent is actively implementing it. |
| **IN REVIEW** | The implementing agent is *done*; an **independent review** is underway — running the suites and exercising the change, not reading the agent's report. |
| **SHIPPED** | A commit exists. The change is real, reviewed, and committed. |
| **archived** | The SPEC has moved to `_archived/`. This happens **at SHIPPED — after review and commit — never on the agent's say-so.** |

> **"Shipped" is a claim about reality, not about an agent's completion message.** It
> requires, in order: (1) the implementing agent finished, (2) an *independent* review
> verified the work against the SPEC by running and exercising it, and (3) the change was
> committed. Archiving a SPEC or marking status "done" on an agent's self-report alone is
> premature on two counts — independent review routinely produces substantial corrections,
> and uncommitted work is by definition not shipped. If a SPEC was archived early,
> **un-archive it**: move it back to the Atlas root with status IN REVIEW rather than
> "reviewing history."

## Planning the *how* is the tool's job — not an Atlas artifact

A SPEC fixes the **what** (and its acceptance). The **how** — the implementation approach,
and any task breakdown — is planned at the `READY → IN PROGRESS` boundary by **your tool's
plan mode** (e.g. Claude Code's or Cursor's): feed it the SPEC, it produces the approach
(and tasks if it wants), a human approves it, then it executes. For a non-trivial SPEC this
approval is the **cheap, early review gate** — catching a wrong approach *before* code is
written, the same spirit as never shipping on an agent's self-report. A tool without a plan
mode degrades gracefully: the agent states its approach and the human approves before coding.

**This plan is transient and tool-owned — it is never an Atlas artifact.** Do **not** create
`PLAN_*.md` / `TASKS_*.md` files; that is exactly the "pile of files" Atlas avoids. The plan
is a task-scoped instruction → *apply now, persist nothing*. Its only durable traces are the
ones Atlas already keeps: the **code** is the record of how it was built, a **how-decision
with standing value** graduates to `CLAUDE.md`, and the **archived SPEC** records the *what*
that shipped.

## The deviations registry

`DEVIATIONS.md` runs **independently** of the SPEC flow. It records explicit, deliberate
divergences from a memory-store rule *that applies to this Atlas* — a rule you'd be
expected to follow but deliberately (or for now) don't, with the reason. A divergence may
also spawn a SPEC to resolve it.

It is **not** a list of out-of-domain rules that simply don't apply — you don't enumerate
what the project *isn't*. (A memory-server project doesn't record "I'm not a web app.")

## Each artifact's job, recapped

- **`BACKLOG.md`** — the index of *open* work.
- **`SPEC_*` / `DRAFT_*`** — the work itself, one file per item.
- **`_archived/`** — shipped history.
- **`DEVIATIONS.md`** — known, deliberate divergences.
- **`STATUS.md`** — the digest over all of the above (regenerated, never the source of
  truth).
