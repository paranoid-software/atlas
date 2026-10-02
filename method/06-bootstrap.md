# Creating an Atlas

An Atlas is created with the `atlas` CLI and grows one source at a time. Every Atlas starts
from the same base set ([03-atlas-anatomy.md](03-atlas-anatomy.md)), so an agent always knows
where each thing goes.

## 1. Create — `atlas init`

In an empty folder, `atlas init` creates the base set of
[03-atlas-anatomy.md](03-atlas-anatomy.md) and nothing else. Its initial contents: `CLAUDE.md`
and `STATUS.md` from the templates below, with no sources and no SPECs; an empty backlog;
`_archived/README.md` saying what the folder holds; `_settings/atlas.toml` with the current
model version and no sources nor plugins; `.claude/settings.local.json` with no readable
directories; `.vscode/settings.json` with `git.autoRepositoryDetection: true` and an empty
`git.scanRepositories`; `.gitignore` with the whitelist of
[07-sharing-an-atlas.md](07-sharing-an-atlas.md).

No SPECs, DRAFTs or plugin files: those appear when there is work or a plugin is enabled.
`atlas init` refuses a folder that is already an Atlas (it has `_settings/atlas.toml`,
`CLAUDE.md` or `STATUS.md`). Settings found in a fresh folder are completed, never replaced —
`.claude/settings.local.json` and `.vscode/settings.json` gain what the Atlas needs — and an
existing `.gitignore` is kept, with a reminder to check it against
[07-sharing-an-atlas.md](07-sharing-an-atlas.md).

## 2. Add sources — `atlas link`

For each source, `atlas link <name> <path>` creates the symlink, declares the source and wires
it into `.vscode/settings.json` and `.claude/settings.local.json`. Then write its orientation
block in `CLAUDE.md` §1 with the human — from the source's README; if there is none or it is
ambiguous, ask. Sources keep being added this way for the life of the Atlas.

## 3. Join an existing Atlas — `atlas doctor`

Clone the Atlas, run `atlas doctor`: it lists every declared source that is missing or broken
on this machine, with the exact commands to get it and link it. Put each source wherever you
like and `atlas link` it. Run `atlas doctor` again until everything is ok.

## The orientation-file template

Copy this skeleton, then fill the `<...>` placeholders. Universal behavior rules are **not**
in this template — they live in the memory store; don't re-add them per Atlas.

````markdown
# <Topic> Atlas — agent instructions

This is the **<topic> Atlas** — the context of the <topic> project. Project orientation +
Atlas-specific glue only. Universal rules and behavior live in the memory store; autonomous
file-memory is off. **Current state & next steps live in [STATUS.md](STATUS.md) — read it
first.**

---

## 1. What lives here — sources and their purposes

Each source is a symlink; where it lives is up to each machine and is never recorded here:

```
<topic>/                           (the Atlas)
├── source-a/   — <one-line purpose>
├── source-b/   — <one-line purpose>
└── source-c/   — <one-line purpose>
```

Editing a file under a symlink writes to the source itself. Changes across sources are
flagged explicitly.

### <source-name> — <role: core product | reference | infrastructure | tooling>
- **Contributes:** <one paragraph>
- **Stack:** <languages / frameworks / key libs>
- **Cadence:** <how it releases — or "reference only: read, don't modify">

---

## 2. How I work in this Atlas
- **Before editing, identify the target source** — most changes belong to exactly one;
  changes across sources are called out explicitly.
- <Atlas-specific tooling notes — environment naming, dev-server entrypoints, lint/format>
- <Atlas-specific footguns unique to this Atlas — generic ones live in the memory store>

---

## 3. <Project domain> — product / architecture
_(no domain conventions yet)_

---

## 5. Conventions we're establishing (Atlas-level, not in the memory store)
_Rules that apply to this Atlas and that we've decided not (yet) to lift into the memory
store. Keep it short; promote to the memory store only after a dedicated session, and only
if they generalize._
- _(empty — fill in as conventions get decided.)_
````

**Applying the template:**

- The **source orientation block** is the heart of §1 — it's what lets any agent
  understand each source without re-explanation.
- §2 = how you work; §3+ = domain; an optional §4 = a separable sub-domain; §5 = conventions
  you're establishing locally. **Section numbers are fixed**: if you omit §4, §5 stays §5 —
  don't renumber. The stable §1/§2/§3/§5 shape is recognizable across Atlases.
- At bootstrap, §3 is a single `_(no domain conventions yet)_` line. **Don't pre-create
  sub-sections** — empty 3.1/3.2 read as "I forgot to fill this in," not "fresh Atlas." Add
  them only when there's real content.
- Don't put current-state / progress in the orientation file — that's `STATUS.md`'s job.

## The SPEC template

A SPEC is the *what* and its *route* (the Plan) — nothing else (see
[04-spec-lifecycle.md](04-spec-lifecycle.md)). Copy this shape; **do not add sections**.

````markdown
# SPEC_NNNN_<SLUG>
created: <date>
repos: <repo-a>, <repo-b>        ← the repos this SPEC may touch

## What
<the change, as behavior / outcome — the goal>

## Acceptance
<observable criteria that make it done — not steps>

## Out of scope
<explicit boundaries>

## Plan
<the ordered steps / milestones that deliver the What — the route, in prose.
 No technique, no code, no checkboxes: the how of each step is decided live, with the human.>
````

**Never add** anything on the "never in a SPEC" list in
[04-spec-lifecycle.md](04-spec-lifecycle.md) — findings go to `SPEC_NNNN_FINDINGS.md` beside it.

## The STATUS.md template

Three fixed sections that never mix. **Active** is the in-flight board — one resume note per
SPEC — **rewritten to the current state at every checkpoint, never appended**.

````markdown
# <Topic> — STATUS (living)

Where this project is now. Standing decisions + orientation live in CLAUDE.md; the
BACKLOG / SPEC_ / _archived artifacts are the record. Refresh with `/atlas-sync`.

_Last updated: <date>_

## What <topic> is (one line)
<one-line product summary>

## Active
_(one block per SPEC in progress / in review — rewritten to the current state, never appended)_

### SPEC_NNNN_<SLUG> — IN PROGRESS
- **Done:** <what is already in place>
- **Next:** <the very next step — where to resume>
- **Blocked:** <what's in the way — omit the line if nothing>
- **Paused:** <repos> — stash "SPEC_NNNN paused" — omit the line if not paused

## Recently closed
_(short rolling window — last N — pointing into _archived/; the full history lives there)_
- SPEC_NNNN_<SLUG> → _archived/ (<date>)
````

A SPEC **leaves Active the moment it closes** and appears under Recently closed; `BACKLOG.md`
holds what is queued and not yet in flight.
