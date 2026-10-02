# The discipline

The Atlas tells you *where things live*. The discipline is the handful of rules that keep
AI-driven work honest — method-level, regardless of language, framework or product.

## 1. The human gates

The agent proposes and executes; the human decides at these four points:

1. **create the branch** for a SPEC;
2. **approve the how** of each step before it is coded ([04](04-spec-lifecycle.md));
3. **commit**;
4. **close** the SPEC.

Everything mechanical between the gates is the agent's or the CLI's job.

## 2. One branch per SPEC

Each SPEC works on **`spec/NNNN-<slug>`** in every repo of its `repos:` line, created by the
human. The Atlas root itself works on `main` only.

## 3. Specs are small and independently deliverable

A SPEC is sized to be **built, reviewed and closed as one unit** — not an epic. If it can't be
described, implemented and verified without dragging in half the system, split it. Rules of
thumb: one clear "this is what it does" sentence; reviewable in one focused sitting; the project
works when it lands, not "once the next three SPECs also land."

## 4. Never closed on an agent's self-report

An agent's "I'm done" is not evidence. Before a SPEC closes, the work is **verified in the
code by a reviewer other than the implementer** — running the suites and exercising the
change, not reading the agent's report. The review's corrections go into the code.

## 5. Start each SPEC from a clean baseline

Before implementing, check each affected repo's working tree. **Changes that aren't part of
this SPEC → stop and surface them**; they get committed or set aside by the human first. A
SPEC's commit equals the SPEC's work — that is what keeps it reviewable and revertable.

## 6. A commit message says what the commit does — nothing else

- **Subject** — one imperative line ("Add X", "Fix Y"), ~50 chars, no trailing period.
- **Body** *(only when needed)* — what changed and why, in present terms.

Leave out archaeology (how you got here, prior attempts) and what is *not* done (TODOs, "next
we'll…"). Authorship and attribution are project policy, not this rule.

## 7. Only files of record, SPECs and DRAFTs — and no archaeology

The Atlas root holds the files of record, SPECs (with their findings files) and DRAFTs. **No
other kind of planning file** — a north-star, a brief or a plan is either a DRAFT or a SPEC.

Every file of record describes the **current** state or intent and is **rewritten in place —
never appended to**. No "previously…", "changed from X to Y", "attempt 1 failed" — not in
`CLAUDE.md`, a SPEC, `STATUS.md` or the backlog. History has two homes: **git** and
**`_archived/`**.
