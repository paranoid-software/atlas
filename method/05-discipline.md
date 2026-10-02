# The discipline

The Atlas tells you *where things live*. The discipline is the handful of rules that keep
AI-driven work honest — method-level, regardless of language, framework or product.

## The cadence

The suggested flow of work. It is what turns steady work into good software, in any kind of
project — and what breaks first under pressure.

1. **Something rubs** — a bug, an idea, a friction found while working.
2. **Decide** what to do about it, in conversation.
3. **Write a bounded SPEC** ([04](04-spec-lifecycle.md)).
4. **Create its branch** — the human creates `spec/NNNN-<slug>` from `develop` in each repo
   the SPEC touches.
5. **Step by step** — for each Plan step the agent proposes the how, the human approves, the
   agent executes. What is learned on the way goes to the findings file.
6. **Independent review** in the code.
7. **The human commits on the SPEC branch and closes the SPEC.** After the close — done by
   the human, never a condition to close — the branch returns to `develop`; `main` only ever
   receives `develop`.

**Drift signals.** An agent that sees one says so **once**, then follows the human's call —
nothing blocks:

- code is requested and there is no SPEC in `STATUS → Active`;
- more than one SPEC is in progress, and not paused, in the same repo;
- work happens outside the SPEC's branch, or on `main`;
- a step is coded without its how approved;
- a close is asked without an independent review or a commit.

### When something interrupts

| Situation | What to do |
|---|---|
| **Urgent bug in the middle of a SPEC** | Pause the SPEC (below). The fix is a minimal SPEC — What, one criterion, one step — on its own branch (`git switch -c spec/MMMM-<slug> develop`). Close it, then resume. |
| **A new idea** | One line in the backlog, or a DRAFT. Not acted on now. |
| **The SPEC is wrongly posed** | A finding, and the SPEC is corrected. |
| **The SPEC turns out too big** | Split it: what is done closes, the rest becomes a new SPEC. |
| **The SPEC is no longer wanted** | Discard it: out of Active or the backlog, its SPEC and findings files deleted, its branch deleted and any paused stash dropped by the human. Never archived. |

**Pausing a SPEC without a commit.** In each repo with changes the human runs
`git stash push -u -m "SPEC_NNNN paused"`, and the SPEC's Active block gains a line
`Paused: <repos> — stash "SPEC_NNNN paused"`. **Resuming:** in each of those repos, `git switch spec/NNNN-<slug>`, then
`git stash pop stash@{n}` — where `n` is the position of `SPEC_NNNN paused` in `git stash list`,
so the right stash comes back even if there are several — and remove the Paused line. The agent
reads `git stash list` and gives the exact commands; the human runs them.

## 1. The human gates

The agent proposes and executes; the human decides at these four points:

1. **create the branch** for a SPEC;
2. **approve the how** of each step before it is coded ([04](04-spec-lifecycle.md));
3. **commit**;
4. **close** the SPEC.

Everything mechanical between the gates is the agent's or the CLI's job.

## 2. One branch per SPEC

Each SPEC works on **`spec/NNNN-<slug>`** in every repo of its `repos:` line, created by the
human **from `develop`**, and returns to `develop` after it is closed (by the human — not a
close condition). **A SPEC never touches
`main`** — `main` only receives `develop`. The Atlas root itself works on `main` only.

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
