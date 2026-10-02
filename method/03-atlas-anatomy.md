# Atlas anatomy — the Atlas's own files

An Atlas root holds two kinds of entries: **sources**, each a symlink, and the **Atlas's own
files**. Telling them apart takes no guessing: **anything starting with `_`, the uppercase
`.md` files, `.claude/`, `.vscode/` and `.gitignore` belong to the Atlas; everything else is a source.**

The **base set** is created by `atlas init`, so every Atlas has the same skeleton from day one
and an agent always knows where each thing goes. The **per-workitem** files appear as work
arrives.

## The base set

| File | Role |
|---|---|
| **`CLAUDE.md`** *(orientation file)* | Project orientation + standing project-specific decisions & conventions + footguns. Static — changes only when an orientation fact or a standing decision changes. |
| **`STATUS.md`** | Where the project is *now*, in **three fixed sections that never mix**: **What it is** (one line) · **Active** (the in-flight board — one block per SPEC in progress/review with its status and a short *where-we-left-off* note: Done / Next / Blocked, and Paused when it is paused) · **Recently closed** (a short rolling window into `_archived/`). Holds no rules and no decisions. |
| **`BACKLOG.md`** | The **queue**: one line per open workitem (`SPEC_*` / `DRAFT_*`) **not yet in flight**, index-only — no bodies, no rules, no decisions. `READY` = in the backlog and not yet in `STATUS → Active`. |
| **`_archived/`** | Where closed SPECs go — the project's history of work. Holds **only closed SPECs** and their findings files, plus a `README.md` explaining the folder. |
| **`_settings/`** | The Atlas's configuration, in `atlas.toml` (below). Versioned with the Atlas. |
| **`.claude/settings.local.json`** | Claude's settings for this Atlas: the real path of each source as a readable directory. Machine-specific — rewritten by `atlas link`, never versioned. |
| **`.vscode/settings.json`** | Editor git settings, so every git source shows in Source Control (below). Relative paths — the same on every machine, versioned. |
| **`.gitignore`** | Keeps only the Atlas's own files under git, never the symlinks nor `.claude/` ([07-sharing-an-atlas.md](07-sharing-an-atlas.md)). Ready from day one, whether or not the Atlas is ever shared. |

> All the Atlas's files are **current-state snapshots, rewritten in place — never logs**.
> History lives only in git and `_archived/` (see [05-discipline.md](05-discipline.md) §7).

### `_settings/atlas.toml`

```toml
version = 1                              # the Atlas model version this Atlas follows

[sources.log-daemon]
remote = "git@github.com:me/log-daemon.git"

[sources.specs]                          # not in git: the name is all there is

[plugins]                                # none by default
```

It declares **which sources the Atlas has**, never **where** they live: the location is the
symlink itself, chosen by each person on their machine and never versioned.

### Editor git settings

VS Code–family editors (VS Code, Cursor, the Claude Code desktop Code tab) don't follow
symlinks when looking for repos, so without help no source shows in Source Control — and if
the Atlas itself is versioned, a file opened through a symlink is attributed to the Atlas's
repo. `.vscode/settings.json` fixes both: `git.scanRepositories` lists every source (relative
paths, through the symlinks), and `git.autoRepositoryDetection` is set to `true` — the list is
only read when detection scans sub-folders, and Cursor defaults to `openEditors`, which
ignores it. Reload the window after changing it.

To check what the editor actually does, raise the Git log level to Trace (`Developer: Set Log
Level`), reload the window and read the Git output log: its `doInitialScan` line prints the
effective `autoRepositoryDetection`.

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
| **`SPEC_NNNN_FINDINGS.md`** | What was found while resolving that SPEC — blockers, misconceptions that can't be resolved within it, wrongly-posed parts. A record, never a condition to close. Created on the first finding; archived with its SPEC. See lifecycle. |

## The two living files: `CLAUDE.md` vs `STATUS.md`

These two are easy to confuse, so the split is strict:

- **`CLAUDE.md` is the static "what / why."** What the product is, what each source
  contributes, the standing decisions. It changes only when an orientation fact or a
  standing decision changes.
- **`STATUS.md` is the living "where are we now."** Three fixed sections that **never mix**:
  - **What `<topic>` is** — one line.
  - **Active** — the **in-flight board**: one block per SPEC currently `IN PROGRESS` or
    `IN REVIEW`, with its status and a short **resume note — where we left off** — in 2–4
    bullets: **Done** / **Next** / **Blocked** — plus **Paused** while the SPEC is paused
    ([05-discipline.md](05-discipline.md)). This is the *single home* of in-flight state
    (it is **not** in the SPEC). Each block is **rewritten to the current state, never
    appended as a log**, and a SPEC **leaves Active the moment it closes**.
  - **Recently closed** — a short rolling window (last N) pointing into `_archived/`. The
    full history is `_archived/`, never this section.

  Every line traces to an artifact (an Active block to its SPEC, a closed line to
  `_archived/`). **Routine actions (commits, ad-hoc ops) are never status.** No rules, no
  decisions.

The **structured workitem artifacts are the authoritative record**; `STATUS.md` is the
at-a-glance view over them — plus the one thing only it holds: the **Active resume notes**,
which you keep current at every checkpoint. "Recently closed" and the one-liner are
*derived*; the Active blocks are *maintained* (refreshed via the "sync" command when you stop
or hand off). Ideally `STATUS.md` is injected automatically at the start of every session so
an agent never starts cold. (Reference implementation: a session-start hook cats `STATUS.md`
into context; a "sync" command refreshes it. Both are tool affordances — wire up whatever
your tool offers, or do it by hand.)

## The source orientation block

Inside `CLAUDE.md`, **every source gets a standard block** so any agent understands the
territory cold. The block describes the source's role **in this Atlas** — the same source can
be core in one project and read-only reference in another. Group sources by role when there
are many. Each block is:

- **Role** — core product / reference / infrastructure / tooling
- **Contributes** — one paragraph: what this source holds and does for the project
- **Stack** — languages / frameworks / key libraries
- **Cadence** — how it releases or deploys (or "reference only: read, don't modify")

> Fill these from the source's own README (or package description). If it's missing or
> ambiguous, **ask** — don't infer its purpose from its file layout.

## Sources: declared once, located per machine

`_settings/atlas.toml` says which sources the Atlas has; each machine has its own symlinks.
Two commands keep them in line:

- **`atlas link <name> <path>`** — adds or rebinds a source: creates the symlink, declares the
  source (with its `remote` when it is a git repo), adds it to `.vscode/settings.json` and
  writes its real path to `.claude/settings.local.json`. The creator of an Atlas and whoever
  clones it run the same command.
- **`atlas doctor`** — reports each declared source as **ok**, **missing** (with the exact
  clone and link commands to run) or **broken** (the symlink points nowhere), and flags
  symlinks that aren't declared. It writes nothing.

**The CLI never clones nor runs git**, beyond reading a source's remote — it tells the person
exactly what to run. A new source also needs its orientation block in `CLAUDE.md`, written
with the human.

To drop a source, remove its symlink, its declaration, its `.vscode/settings.json` entry and
its orientation block — asking the human before deleting.

## Naming conventions

- **SPECs: `SPEC_NNNN_<SLUG>.md`** — a 4-digit zero-padded sequence (per-Atlas, assigned at
  creation, never reused) so the name reflects creation order, then an `UPPER_SNAKE` slug.
  Created/close dates live *inside* the file, not in the name. E.g.
  `SPEC_0001_PROVENANCE_DECOUPLING.md`.
- **Findings: `SPEC_NNNN_FINDINGS.md`** — the companion of the SPEC with the same number.
- **DRAFTs: `DRAFT_<SLUG>.md`** — same spirit, for items still being shaped.
- **Legacy files predating this naming are left as-is** — history is not renamed.

Each thing has exactly one home: orientation + standing decisions in `CLAUDE.md`, universal
rules in the memory store, current state in `STATUS.md`, buildable work in a `SPEC_`, which
sources the Atlas has in `_settings/`, closed work in `_archived/`.
