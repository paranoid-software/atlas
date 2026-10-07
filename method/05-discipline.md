# The discipline

The Atlas tells you *where things live*. The discipline is the handful of rules that keep
AI-driven work honest — method-level, regardless of language, framework or product.

## The cadence

The suggested flow of work. It is what turns steady work into good software, in any kind of
project — and what breaks first under pressure.

1. **Something rubs** — a bug, an idea, a friction found while working.
2. **Decide** what to do about it, in conversation — and write the decision right away where
   it belongs: `CLAUDE.md`, the SPEC, its findings or the backlog (except the how of a step,
   whose record is the code). What is not written is lost.
3. **Write a bounded SPEC** ([04](04-spec-lifecycle.md)).
4. **Create its branch** — the human creates `spec/NNNN-<slug>` from `develop` in each repo
   the SPEC touches. With its branch in place, the SPEC enters `STATUS → Active`.
5. **Step by step** — for each Plan step the how is decided and executed: approved by the
   human in **paired** mode, decided by the workbench and reviewed by the principal in
   **delegated** mode (below). What is learned on the way goes to the findings file.
6. **Independent review** in the code.
7. **The human commits on the SPEC branch and closes the SPEC.** After the close — done by
   the human, never a condition to close — the branch returns to `develop`; `main` only ever
   receives `develop`.

**Sessions are disposable.** Every agent session starts blank; what carries the work from one
to the next is the Atlas. So a decision taken in conversation is written the moment it is
taken — except the how of a step, whose record is the code ([04](04-spec-lifecycle.md)) — and
work is cut so a fresh session picks it up from the Atlas alone: one session per SPEC, or per
large block of it, ending with the SPEC's Active block rewritten as the handoff.

**Drift signals.** An agent that sees one says so **once**, then follows the human's call —
nothing blocks:

- code is requested and there is no SPEC in `STATUS → Active`;
- more than one SPEC is in progress, and not paused, in the same repo;
- work happens outside the SPEC's branch, or on `main`;
- in paired mode, a step is coded without its how approved;
- a close is asked without an independent review or a commit.

## Working modes

A SPEC runs in one of two modes. Only the approval of the how changes; the human's other gates
(§1) stay the same in both.

| | **paired** | **delegated** |
|---|---|---|
| Who approves the how | The human, step by step | The principal, reviewing the complete execution and having corrections made |
| The SPEC | May stay open; it is settled in conversation | **Complete** — executable without questions |
| The executing agent stops | At every step | Only on a real blocker or a decision the SPEC doesn't cover |
| The hand-over | — | A precise, self-contained prompt (its contents below). It never sends the workbench to research what the principal already knows. It never prescribes tooling (see Environments and tooling). |

In delegated mode the **principal** is the agent the human talks to (Claude); the
**workbench** is whoever executes — another tool, another session, a subagent. The Atlas
declares its default mode in its orientation file; a SPEC overrides it with a `mode:` line
under `repos:`.

**The hand-over prompt carries:** what to build; the rules; the files to imitate when the
project has them, otherwise the patterns of the coding-rules source; the verification; what to
leave staged; when to stop — a SPEC that conflicts with what the workbench finds is a blocker:
report a finding, never implement around it; and the report expected — what was verified and
with what output, what was assumed, what was not done.

## Environments and tooling

Atlas imposes no language, framework, platform or tooling. How a source is built and run
lives in the source; how work is done on a machine lives in that environment's own rules
(in Claude Code, the user-level `CLAUDE.md` of that machine or container).

An Atlas's orientation file carries no environment tooling rules, and a hand-over prompt
(Working modes) never prescribes tooling.

In any environment the agent looks at where it stands and what is available, and follows
that environment's rules. Where there are none, it proposes carefully and asks the human
before installing or changing anything — it never installs tooling to match a prompt.

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

The agent proposes and executes; the human decides at these points:

1. **approve the SPEC** — the what;
2. **create the branch** for it;
3. **approve the how** of each step before it is coded — in paired mode only; in delegated mode
   the principal reviews instead (Working modes);
4. **commit**;
5. **close** the SPEC.

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
change, not reading the agent's report. The reviewer reads the code against each Acceptance
criterion and hunts for tests that only look like tests, edges left uncovered, silent
assumptions and abstractions nobody asked for. The review's corrections go into the code.

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
