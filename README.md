# Atlas

**A spec-driven framework for running large, multi-repo, AI-assisted projects** — so any
agent, in any tool, on any day, can open a project cold and have complete clarity about what
it is, where it lives, where the work stands, and how work gets closed.

Atlas is a small, tool-agnostic set of conventions: **where each kind of knowledge lives**,
and **how a unit of work travels from idea to closed**. It assumes you drive development with
AI agents, but requires **no particular agent, IDE, editor, or memory product**. Where a
concrete tool helps, it's named as a *reference implementation* playing a *role* you can swap.

> **About this repo.** The formal, tool-agnostic write-up of the framework, served as a small
> documentation site (and an `llms.txt`). Official home: **https://atlas.paranoid.software**.
> MIT-licensed, public.

## Start here

| If you want to… | Go to |
|---|---|
| Understand and adopt the framework | **[method/README.md](method/README.md)** — overview + reading order |
| See how this repo is organized | **[STRUCTURE.md](STRUCTURE.md)** |

## The framework in one screen

- **The Atlas** — one directory that aggregates all of a project's repos **by symlink** (not
  by copying), so a single-CWD agent sees the whole territory at once while each repo keeps
  its own git, CI, and release cadence. → [method/01-the-atlas.md](method/01-the-atlas.md)
- **The stores model** — a fixed answer to "where does *this* knowledge go?": project
  orientation + standing decisions in an orientation file; universal rules in the
  **coding-rules source each Atlas chooses** (a plugin: an MCP memory server or a `.md`);
  current state in a regenerable
  status digest; each with exactly one home.
  → [method/02-stores-model.md](method/02-stores-model.md)
- **The SPEC lifecycle** — nothing is coded without a small, deliverable spec; every spec
  travels `READY → IN PROGRESS → IN REVIEW → CLOSED → archived`.
  → [method/04-spec-lifecycle.md](method/04-spec-lifecycle.md)
- **The discipline** — small deliverable specs and **independent review before "closed"**
  (never trust an agent's self-report). → [method/05-discipline.md](method/05-discipline.md)

## Roles and reference implementations

Atlas describes each component by the **role** it plays, then names a concrete tool that fills
it. The tools are swappable and optional; the first two **roles are required**, the last two
are strengtheners.

| Role | Reference implementation (optional) | Alternatives |
|---|---|---|
| Primary agent / tool *(required)* | Claude Code | Cursor, Codex, Cline, … |
| Coding-rules source *(plugin, chosen per Atlas)* | an MCP memory server, e.g. coco | a `.md` file in the Atlas |
| Skill / cheat-sheet mechanism | Claude Code skills | any reusable-prompt affordance |
| Forced-discipline mechanism | Claude Code hooks | any event automation |

## Sharing an Atlas

Git is how an Atlas is shared: its own files go in a repo of their own, the symlinks never do,
and each person rebuilds the sources on their machine. →
[method/07-sharing-an-atlas.md](method/07-sharing-an-atlas.md)

## What this repo is not

- **Not tied to a memory product.** Each Atlas chooses its coding-rules source — an MCP memory
  server such as coco, or a `.md` in the Atlas — or none; the framework assumes none.
- **Not a memory, and not a file-based "project memory."** Unlike spec-driven-development
  approaches that accrete project knowledge into a pile of files, Atlas keeps the durable
  universal layer in the coding-rules source its plugin declares and keeps project-specifics lean
  (orientation + status + specs). It defines methodology and discipline — nothing more.
- **Not a product description.** How a system *works* lives in its own code and docs; Atlas is
  about orientation, decisions, status, and the flow of work.
- **Not firm-specific.** No firm- or product-specific programming patterns — only the
  tool-agnostic conventions any team can adopt.
