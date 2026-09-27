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

## What a SPEC is — and is not

A SPEC is the **what** plus its **route**: the goal, its acceptance criteria, its declared
repos, its boundaries, and a **Plan** — the ordered steps/milestones that deliver it. It
carries **no state, no technique, no code, no history.**

**Plan ≠ How.** The **Plan** is the *route*: what gets done, in what order — a decomposition
of the what into deliverable steps. The **how** is the *technique* of each step — pattern,
library, design — and it is decided **live, each iteration**: the agent proposes, the human
disposes. **The how is not documented anywhere — its output is the code** (the diff, the
install, the config) and the general way of working that shapes it already lives in the
memory store as universal rules. Writing the how down again — in the SPEC or anywhere else —
is over-documentation: text that goes stale the moment the code moves, and that takes the
per-step decision away from the human.

**Never in a SPEC:**
- **state** — status, progress, where-we-are → `STATUS.md → Active`
  ([03-atlas-anatomy.md](03-atlas-anatomy.md));
- **checkboxes** (`- [x]`) — that's progress, not plan;
- **the how / technique** → decided live; its record is the code. General working rules
  already live in the memory store;
- **code** — no fenced blocks, diffs, signatures or file-by-file edits, anywhere in the SPEC
  (reference a path instead); code lives in the repo;
- **verification results** → the independent review's report;
- **archaeology** — no "previously", "used to", "changed from", attempts, dead ends
  ([05-discipline.md](05-discipline.md) §5). A SPEC states the current intent, not its history;
- **session notes**.

A SPEC that grows a "Progress", "Verification", "Notes" or "Status" section, a code block, a
checkbox, or a Plan that reads like implementation, is **contaminated — strip it**. Keeping all
of that out is what lets any agent open a SPEC and read only *what we are doing and in what
order*, uncluttered by how far someone got or how they got there.

The fixed shape (template in [06-bootstrap.md](06-bootstrap.md)): `created` · `repos` ·
**What** · **Acceptance** · **Out of scope** · **Plan**. Nothing else.

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

## Picking up a SPEC, and leaving it — resume & checkpoint

The whole point of the SPEC/STATUS split is that **a fresh agent can resume in two reads**:

- **Picking up a SPEC:** read its block in **`STATUS.md → Active`** first — it says *where we
  left off* (**Done / Next / Blocked**) — then read the **SPEC** for *what we are trying to
  do*. Continue from **Next**.
- **Stopping or handing off:** before you leave, **update that SPEC's Active block** so it
  reflects the current state (Done / Next / Blocked). That update **is** the checkpoint that
  `/atlas-sync` refreshes — and what the stop nudge reminds you to do. The block is
  **rewritten to the current state, never appended as a log.**

If a SPEC's Active block is missing or stale, the resume cost is paid by whoever comes next.
Keep it current; keep it short.

## The *how* is decided live — it is never an Atlas artifact

The SPEC's **Plan** gives the route (the ordered steps). The **how** of each step — the
technique, the design — is settled at execution time, in conversation: the agent **proposes**
an approach for the step, the **human disposes**, then it executes. (Tools with a plan mode —
Claude Code, Cursor — make this a natural gate; without one, the agent simply states its
approach and the human approves before coding.) For a non-trivial step this approval is the
**cheap, early review gate** — catching a wrong approach *before* code is written, the same
spirit as never shipping on an agent's self-report.

**Nothing about the how is written down.** Most of it is already given: the **universal
working rules in the memory store** (how you test, structure, name, handle errors) are the
standing how, and every agent queries them live. What remains is step-specific and its
record is **the code itself** — the diff, the installation, the configuration that gets
produced. Do **not** create `PLAN_*.md` / `TASKS_*.md` files, do not write technique or code
into the SPEC's Plan, do not keep design notes per step: that is over-documentation — text
that duplicates the code and rots the moment the code moves. The how is *apply now, persist
nothing*. Its only durable traces are the ones Atlas already keeps: the **code**, a
**how-decision with standing value** (which graduates to `CLAUDE.md` if project-specific, or
to the memory store if universal), and the **archived SPEC** with the *what* and its route.

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
