# Atlas anatomy — the files of record

Every Atlas keeps a fixed set of planning files at its root (never inside a member repo).
The **fixed scaffold** is created empty at bootstrap, so every Atlas has the same skeleton
from day one and an agent always knows where each thing goes. The **per-workitem** files
appear as work arrives.

## The fixed scaffold (always present)

| File | Role |
|---|---|
| **`CLAUDE.md`** *(orientation file)* | Project orientation + standing project-specific decisions & conventions + footguns. Static — changes only when an orientation fact or a standing decision changes. |
| **`STATUS.md`** | Where the project is *now*, in **three fixed sections that never mix**: **What it is** (one line) · **Active** (the in-flight board — one block per SPEC in progress/review with its status and a short *where-we-left-off* note: Done / Next / Blocked) · **Recently shipped** (a short rolling window into `_archived/`). Holds no rules and no decisions. |
| **`BACKLOG.md`** | The **queue**: one line per open workitem (`SPEC_*` / `DRAFT_*`) **not yet in flight**, index-only — no bodies, no rules, no decisions. `READY` = in the backlog and not yet in `STATUS → Active`. |
| **`DEVIATIONS.md`** | Explicit, documented divergences from a memory-store rule *that applies here* — "the rule says X; here we do Y because …". Not a catalog of rules that simply don't apply. |
| **`_archived/`** | Where shipped SPECs go — the project's shipped history. Holds **only shipped SPECs**, plus a `README.md` explaining the folder. |
| **`.claude/settings.local.json`** *(tool-local settings)* | Tool-local settings for the primary agent (permissions, additional readable directories). Machine-specific; not portable. No event hooks here — those live tool-global. |

> All files of record are **current-state snapshots, rewritten in place — never logs**.
> History lives only in git and `_archived/` (see [05-discipline.md](05-discipline.md) §5).

## Optional files

| File | Role |
|---|---|
| **`CANDIDATES.md`** *(candidates file)* | Staging area for universal rules aspiring to the memory store, awaiting a dedicated curation session. **Optional** — add it only if you run a memory-store promotion workflow (you stage universal rules here, then promote them in a dedicated curation session). Teams that don't keep a shared memory store, or promote rules directly, can skip it. |

> The candidates file's **role** is "staging for universal-rule promotion." `CANDIDATES.md`
> is the neutral default; name it to match your memory store if you prefer.

## The per-workitem files (appear as work arrives)

| File | Role |
|---|---|
| **`SPEC_NNNN_<SLUG>.md`** | A buildable workitem. Created when a workitem appears (not pre-created at bootstrap). See lifecycle. |
| **`DRAFT_*.md`** | An item still being shaped on its way to a SPEC. Created on demand. A DRAFT either graduates to a SPEC or is discarded — it is never a destination. |

## The two living files: `CLAUDE.md` vs `STATUS.md`

These two are easy to confuse, so the split is strict:

- **`CLAUDE.md` is the static "what / why."** What the product is, what each repo
  contributes, the standing decisions. It changes only when an orientation fact or a
  standing decision changes.
- **`STATUS.md` is the living "where are we now."** Three fixed sections that **never mix**:
  - **What `<topic>` is** — one line.
  - **Active** — the **in-flight board**: one block per SPEC currently `IN PROGRESS` or
    `IN REVIEW`, with its status and a short **resume note — where we left off** — in 2–4
    bullets: **Done** / **Next** / **Blocked**. This is the *single home* of in-flight state
    (it is **not** in the SPEC). Each block is **rewritten to the current state, never
    appended as a log**, and a SPEC **leaves Active the moment it ships**.
  - **Recently shipped** — a short rolling window (last N) pointing into `_archived/`. The
    full history is `_archived/`, never this section.

  Every line traces to an artifact (an Active block to its SPEC, a shipped line to
  `_archived/`). **Routine actions (commits, ad-hoc ops) are never status.** No rules, no
  decisions.

The **structured workitem artifacts are the authoritative record**; `STATUS.md` is the
at-a-glance view over them — plus the one thing only it holds: the **Active resume notes**,
which you keep current at every checkpoint. "Recently shipped" and the one-liner are
*derived*; the Active blocks are *maintained* (refreshed via the "sync" command when you stop
or hand off). Ideally `STATUS.md` is injected automatically at the start of every session so
an agent never starts cold. (Reference implementation: a session-start hook cats `STATUS.md`
into context; a "sync" command refreshes it. Both are tool affordances — wire up whatever
your tool offers, or do it by hand.)

## The per-repo orientation block

Inside `CLAUDE.md`, **every symlinked repo gets a standard block** so any agent understands
the territory cold. Group repos by role when there are many. Each block is:

- **Role** — core product / reference / infrastructure / tooling
- **Contributes** — one paragraph: what this repo holds and does for the project
- **Stack** — languages / frameworks / key libraries
- **Cadence** — how it releases or deploys (or "reference only: read, don't modify")

> Fill these from each repo's own README (or package description). If it's missing or
> ambiguous, **ask** — don't infer the repo's purpose from its file layout.

## Adding or removing a repo from an existing Atlas

The set of symlinked repos is part of the Atlas's reality, so changing it is a **sync, not a
re-init**. Bootstrapping (`atlas-init` in the reference impl) is one-time and refuses to run on
an already-scaffolded Atlas; adding or removing a repo afterward is handled by the **sync**
operation, because a repo change *is* an orientation-fact change.

When the symlink set changes, the sync reconciles the artifacts to it:

- **Repo added** (new symlink) → add its **per-repo orientation block** to `CLAUDE.md` §1
  (read its README; ask if ambiguous), and add its real target path to the tool-local
  settings' readable-directories list.
- **Repo removed** (symlink gone) → flag the now-stale orientation block and its settings
  entry, and **ask before deleting** them.
- **Mismatch** between the symlinks present and the orientation blocks (or a multi-root
  workspace file, if you keep one) → surface it; don't silently guess.

This keeps the rule simple: **new Atlas → bootstrap; any later change to the repo set (or the
status) → sync.**

## Naming conventions

- **SPECs: `SPEC_NNNN_<SLUG>.md`** — a 4-digit zero-padded sequence (per-Atlas, assigned at
  creation, never reused) so the name reflects creation order, then an `UPPER_SNAKE` slug.
  Created/ship dates live *inside* the file, not in the name. E.g.
  `SPEC_0001_PROVENANCE_DECOUPLING.md`.
- **DRAFTs: `DRAFT_<SLUG>.md`** — same spirit, for items still being shaped.
- **Legacy files predating this naming are left as-is** — history is not renamed.

Each thing has exactly one home: orientation + standing decisions in `CLAUDE.md`, universal
rules in the memory store, current state in `STATUS.md`, buildable work in a `SPEC_`, known
divergences in `DEVIATIONS.md`, shipped history in `_archived/`.
