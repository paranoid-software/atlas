# The Atlas model

## What an Atlas is

An **Atlas** is an aggregator directory whose entries are **symlinks to real, independent
repositories**, sitting alongside a small set of its own planning files. It gives an AI
tool a single working directory (CWD) that presents the whole project as one tree, while
every underlying repo keeps its own git history, its own CI, and its own release cadence.

It's called an *Atlas* because it is a **map of the project's repos**: open it and you see
the whole territory at once.

```
_<topic>-default/                 (the Atlas — a directory, not a repo)
├── repo-a/   → /real/path/to/repo-a    — core product
├── repo-b/   → /real/path/to/repo-b    — supporting infrastructure
├── repo-c/   → /real/path/to/repo-c    — reference / read-only
│
├── CLAUDE.md            ┐
├── STATUS.md            │
├── BACKLOG.md           │  the Atlas's own planning files
├── DEVIATIONS.md        │  (its "files of record" — see 03-atlas-anatomy.md)
├── SPEC_*.md / DRAFT_*  │
├── _archived/           ┘
└── CANDIDATES.md           (optional — memory-store staging)
```

Editing a file *through* a symlink writes to the underlying real repo. The Atlas adds no
git layer over those repos — it only **colocates visibility**.

> **Naming.** The term is deliberately **Atlas**, not "workspace." "Workspace" is
> hopelessly overloaded (editor multi-root workspace files, billing/tenant workspaces,
> per-customer workspaces, …). "Atlas" names the concept cleanly so any agent grasps it
> instantly. The reference convention is to name the directory `_<topic>-default/` and
> keep all of a topic's Atlases under one parent folder — but the *name* is a convention,
> not a load-bearing part of the method.

## Why the pattern exists

Two complementary reasons:

1. **The single-CWD constraint.** Most CLI/app AI agents (Claude Code, Codex, Cursor, and
   friends) operate against a single working directory and do **not** honor an editor's
   multi-root workspace format. A symlink Atlas hands the agent one CWD it sees as a
   unified tree, while preserving each repo's independence underneath.

2. **Bringing related / reference repos into reach.** An Atlas is also where you colocate
   repos that aren't direct parts of the product but benefit from being one `cd` away
   during a task: sibling products sharing a framework, supporting infrastructure, guides
   and reference implementations, repos being reviewed or audited, historical codebases.
   Each stays fully independent in git; the Atlas only makes it *visible*.

These projects are large and **always multi-repo** — not single landing pages. The Atlas
exists so that opening one cold, in any tool, gives complete clarity without re-explaining
the project every session.

## What an Atlas is *not*

- **Not a git repo of its own** (by default). The aggregation is non-git: it never folds
  the member repos into a single history. (You *may* optionally version the Atlas's own
  planning files — and only those — without touching the member repos. That mechanic is
  [07-optional-git-versioning.md](07-optional-git-versioning.md), and it stays optional.)
- **Not a monorepo.** Member repos are not vendored, submoduled, or copied. They are
  referenced by symlink and remain authoritative in their own location.
- **Not a place for product description.** How the system *works* lives in code and docs
  inside the member repos. The Atlas holds **orientation, decisions, status, and work** —
  see the stores model next.
