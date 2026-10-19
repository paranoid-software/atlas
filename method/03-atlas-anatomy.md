# Atlas anatomy — the Atlas's own files

An Atlas root holds three kinds of entries: **sources**, each a symlink; the **Atlas's own
files**; and a **declared workbench's files**. Telling them apart takes no guessing:
**anything starting with `_`, the uppercase `.md` files, `.vscode/` and `.gitignore` belong to
the Atlas; `.claude/` belongs to a workbench the Atlas declares; everything else is a source.** The Atlas's own files are never a tool's rule files.

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
| **`.vscode/settings.json`** | Editor git settings, so every git source shows in Source Control (below). Relative paths — the same on every machine, versioned. The Atlas's own: it follows from having git sources, not from the workbench the Atlas is worked with. |
| **`.gitignore`** | Keeps only the Atlas's own files under git, never the symlinks nor a workbench's folder ([07-sharing-an-atlas.md](07-sharing-an-atlas.md)). Ready from day one, whether or not the Atlas is ever shared. |

### A workbench's files

A **workbench** is an editor or agent the Atlas is worked with. The Atlas **declares** its
workbenches in `_settings/atlas.toml` (`[workbenches.<name>]`), once, as it declares its
sources; `atlas workbench add <name>` declares one and writes its files from the declared
sources, `atlas workbench drop <name>` undeclares it, `atlas workbench list` shows them. A
workbench's files are **per machine, never versioned**: `atlas link` and `atlas unlink` keep
them current for the workbenches declared, `atlas doctor` reports one that is missing or
stale, and on another machine the same `atlas workbench add` rebuilds them. One workbench
exists:

| Workbench | Its file | What it holds |
|---|---|---|
| **`claude`** | `.claude/settings.local.json` | The real path of each source as a readable directory, for Claude Code. |

An Atlas with no workbench declared is complete: the CLI, the files of record and the editor
settings are the whole method.

> All the Atlas's files are **current-state snapshots, rewritten in place — never logs**.
> History lives only in git and `_archived/` (see [05-discipline.md](05-discipline.md) §7).

### `_settings/atlas.toml`

```toml
version = 1                              # the Atlas model version this Atlas follows

[sources.log-daemon]
remote = "git@github.com:me/log-daemon.git"

[sources.infra]                          # a folder of repos: each direct child that is a repo

[sources.infra.repos.gke-logy]
remote = "https://dev.azure.com/acme/infra/_git/gke-logy"

[sources.infra.repos.gke-n8n]
remote = "https://dev.azure.com/acme/infra/_git/gke-n8n"

[sources.specs]                          # not in git: the name is all there is

[plugins]                                # none by default

[plugins.coding-rules]                   # this Atlas's coding-rules source
source = "mcp:coco"                      # or "file:CODING_RULES.md"
```

It declares **which sources the Atlas has**, never **where** they live: the location is the
symlink itself, chosen by each person on their machine and never versioned.

### Editor git settings

VS Code–family editors (VS Code, Cursor, the Claude Code desktop Code tab) don't follow
symlinks when looking for repos, so without help no source shows in Source Control — and if
the Atlas itself is versioned, a file opened through a symlink is attributed to the Atlas's
repo. `.vscode/settings.json` fixes both: `git.scanRepositories` lists every source, or each
nested repo of a folder of repos (relative paths, through the symlinks), and
`git.autoRepositoryDetection` is `true`, since the list is only read when detection scans
sub-folders. When sources still don't show, the CLI's README says how to check it.

## Plugin files

A plugin's files exist only in an Atlas that enables it. The `coding-rules` plugin — the Atlas's
choice of shared coding-rules memory ([02-stores-model.md](02-stores-model.md)) — is enabled with
`atlas plugin add coding-rules <source>`, which declares it in `_settings/atlas.toml` and creates:

| File | Role |
|---|---|
| **`CODING_RULES_CANDIDATES.md`** | Universal rules found while working, in force in this Atlas from the moment they are staged, and promoted to the source in a dedicated session with the human's approval — never written straight to the source. Brought to the agent at session start. |
| **`CODING_RULES_DEVIATIONS.md`** | Deliberate divergences, in this Atlas, from a rule of the source: "the rule says X; here we do Y because …". Brought to the agent at session start. |

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
*derived*; the Active blocks are *maintained* (rewritten at the checkpoint, when you stop or
hand off). `atlas orient` prints what a session reads first — the method's orientation, the
coding rules in force, `atlas status` and `STATUS.md` — so an agent in any workbench, or a
human in a terminal, never starts cold. `atlas status` prints the Atlas's state as its files
and sources show it — the Active SPECs, any SPEC out of place, each source's branch and
uncommitted changes, the paused SPECs — so a fresh session starts from both: where the
conversation was left and where the code is. `atlas sync` does the checkpoint's mechanics —
the doctor's report, the lint, a missing stamp, a closed SPEC still in Active — and leaves the
Done / Next / Blocked lines to whoever writes them. (In Claude Code, a session-start hook
injects `atlas orient` into context and `/atlas-sync` runs `atlas sync` and writes the
blocks.)

## The source orientation block

Inside `CLAUDE.md`, **every source gets a standard block** so any agent understands the
territory cold. The block describes the source's role **in this Atlas** — the same source can
be core in one project and read-only reference in another. Group sources by role when there
are many. A source's own rule files, when it carries any, are its context and not the
Atlas's — see [01-the-atlas.md](01-the-atlas.md). Each block is:

- **Role** — core product / reference / infrastructure / tooling
- **Contributes** — one paragraph: what this source holds and does for the project
- **Stack** — languages / frameworks / key libraries
- **Cadence** — how it releases or deploys (or "reference only: read, don't modify")

> Fill these from the source's own README (or package description). If it's missing or
> ambiguous, **ask** — don't infer its purpose from its file layout.

For a source that still has no README — empty or planned — the block is written from
what the human says it is. **Contributes** records that purpose in their words; **Stack**
and **Cadence** stay "not decided yet". Revisit the block once the source has a README.
The agent never invents the purpose from whatever files are already there.

## Sources: declared once, located per machine

`_settings/atlas.toml` says which sources the Atlas has; each machine has its own symlinks.
Three commands keep them in line:

- **`atlas link <name> <path>`** — adds or rebinds a source: creates the symlink, declares the
  source (with its `remote` when it is a git repo, stored without credentials: an
  `https://user:token@host/…` origin is declared as `https://host/…`), adds it to
  `.vscode/settings.json` and keeps the declared workbenches' files current (its real path for
  `claude`). A folder
  that is not a repo but whose direct children are is a **folder of repos**: each child is
  declared under the source with its remote, and the editor scans each one. Rebinding
  rescans the folder. The creator of an Atlas and whoever clones it run the same command.
- **`atlas unlink <name>`** — drops a source: removes its symlink, its declaration, its
  `.vscode/settings.json` entries and its entries in the declared workbenches' files. It works on
  whatever is left of the source (missing, broken or undeclared) and never touches the source
  itself.
- **`atlas doctor`** — reports each declared source as **ok**, **missing** (with the exact
  clone and link commands to run) or **broken** (the symlink points nowhere), and flags
  symlinks that aren't declared; in a folder of repos it reports each nested repo
  **missing** (with its clone) or **undeclared** (with the `atlas link` that rescans), and a
  declared remote as **credentials** when it still carries a user or token, with the
  `atlas link` that rewrites it. It also judges each source's orientation block in
  `CLAUDE.md` §1: **unoriented** when the `### <name> — …` heading is not there, and
  **placeholder** when the block still carries the template's `<...>` placeholders; and each
  declared workbench as **workbench** when its file is **missing** or **stale**, with the
  `atlas workbench add` that rewrites it. Those are
  **problems**: the Atlas is not healthy until they are fixed. A present source — or nested
  repo — that carries agent or tool rule files at its top level is a **notice**, **rules**,
  naming the files ([01-the-atlas.md](01-the-atlas.md)): nothing to fix, something the agent
  is told to read with caution. `atlas doctor --json` gives the same report as data, for
  tools, each finding with its `level`. It writes nothing.

Four more carry the work itself:

- **`atlas workbench add|drop|list`** — the workbenches the Atlas declares and their files
  (above).
- **`atlas spec new|start|pause|resume|review|close`** — the SPEC lifecycle's transitions
  ([04-spec-lifecycle.md](04-spec-lifecycle.md)): the stamps, the backlog line, the Active
  block's shell, `_archived/`, Recently closed; never the Done / Next / Blocked judgment.
  `atlas spec lint` reports what a SPEC carries that it should not, and writes nothing.
- **`atlas sync`** — the checkpoint's mechanics; `--check` writes nothing and says what it would.
- **`atlas orient`** — the session's first read: an agent in any workbench, or a person in a
  terminal.
- **`atlas handover <name> --step N`** — the delegated-mode brief, from the Atlas
  ([05-discipline.md](05-discipline.md)).

`atlas ui` shows all of this on a local, read-only page — the doctor's findings in plain words
with their fix commands, the SPECs with search, stats from their stamps — served on
`127.0.0.1` and reading only the Atlas's own files.

**The CLI never clones nor writes to git** — it reads a source's remote, its branches and its
working tree, tells the person exactly what to run, and never edits `CLAUDE.md`. A new source also needs its orientation
block in `CLAUDE.md`, written with the human; a dropped source's block leaves `CLAUDE.md` the
same way.

## Naming conventions

- **SPECs: `SPEC_NNNN_<SLUG>.md`** — a 4-digit zero-padded sequence (per-Atlas, assigned at
  creation, never reused) so the name reflects creation order, then an `UPPER_SNAKE` slug.
  Created/close dates live *inside* the file, not in the name. E.g.
  `SPEC_0001_PROVENANCE_DECOUPLING.md`.
- **Findings: `SPEC_NNNN_FINDINGS.md`** — the companion of the SPEC with the same number.
- **DRAFTs: `DRAFT_<SLUG>.md`** — same spirit, for items still being shaped.
- **Legacy files predating this naming are left as-is** — history is not renamed.

Each thing has exactly one home: orientation + standing decisions in `CLAUDE.md`, universal
rules in the coding-rules source when the Atlas declares one, current state in `STATUS.md`, buildable work in a `SPEC_`, which
sources the Atlas has in `_settings/`, closed work in `_archived/`.
