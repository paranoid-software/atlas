# The Atlas model

## What an Atlas is

An **Atlas** is the folder that keeps the context of a **real software project** — not an
isolated repo. Its **sources** — git repos, folders that aren't in git, docs, references —
each live **once** on the machine and enter the Atlas **by symlink**, next to the Atlas's own
files.

```
my-project/                        (the Atlas)
├── log-daemon/   → ~/code/log-daemon      — a git repo, also linked by other Atlases
├── client-api/   → ~/code/client-api      — a git repo
├── specs/        → ~/clients/acme/specs   — a folder that isn't in git
│
├── CLAUDE.md                ┐
├── STATUS.md                │
├── BACKLOG.md               │  the Atlas's own files
├── SPEC_* / DRAFT_*         │  (see 03-atlas-anatomy.md)
├── _archived/               │
├── _settings/               │
├── .claude/  .vscode/  .gitignore  ┘
```

Editing a file *through* a symlink writes to the source itself. Any agent that opens the
folder sees the whole project at once: what we are doing, and where each source lives.

## Why it exists

1. **Context, first-hand.** A real project is never one repo. The Atlas puts every source of
   the project in one folder with the files that say what is being done, so an agent opening
   it cold understands the project without anyone re-explaining it.
2. **Reuse.** A source lives once and is linked by every Atlas that needs it — the same log
   daemon in three client projects, never three copies. That is how work gets reused across
   projects, and what tooling built around one monolithic project ignores.

> **Naming.** *Atlas*, not "workspace" — "workspace" is overloaded (editor workspace files,
> tenant workspaces, …). An Atlas is a map of the project's territory.

## What an Atlas is *not*

- **Not a monorepo, not a copy.** Sources are linked, never vendored, submoduled or copied;
  each stays authoritative in its own place, with its own git if it has one.
- **Not a product description.** How the system works lives in its sources. The Atlas holds
  **orientation, status and work**.
- **Not a place inside a source.** Planning files never live inside a source: a source shared
  by several Atlases would leak them into all of them.
- **No agent or tool rule files in a source.** A source carries no `CLAUDE.md`, `.claude/`,
  `AGENTS.md` or `.cursorrules`. Claude Code loads a subfolder's `CLAUDE.md` on its own, so
  one inside a source leaks into every Atlas that links it. A source's orientation lives in
  its block in the Atlas's `CLAUDE.md`.
- **Not tied to one machine.** The Atlas's own files are versioned when it is shared; each
  person rebuilds the symlinks on their machine
  ([07-sharing-an-atlas.md](07-sharing-an-atlas.md)).
