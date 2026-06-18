# The Atlas method

A tool-agnostic way to run **large, multi-repo, AI-assisted projects** so that any
agent — in any tool, on any day — can open the project cold and have complete clarity
about *what it is, where it lives, where the work stands, and how work gets shipped*.

The method is small. It is a handful of conventions about **where each kind of
knowledge lives** and **how a unit of work travels from idea to shipped**. It assumes
you drive the project with AI coding agents, but it does **not** require any particular
agent, IDE, editor, or memory product. Where a concrete tool is useful, this doc names
it as a *reference implementation* and tells you what role it is playing, so you can
swap it.

## Why it exists

AI agents are stateless between sessions and blind across tools. Without a discipline
for where knowledge persists, every session re-explains the project, decisions evaporate,
"done" means "an agent said it was done," and a project with several repos becomes
impossible for an agent to hold in its head. The Atlas method fixes that with four moving
parts:

1. **The Atlas** — one directory that aggregates all of a project's repos (by reference,
   not by copying) so a single-CWD agent sees the whole territory at once.
2. **The stores model** — a fixed answer to "where does *this* piece of knowledge go?",
   so orientation, universal rules, current status, and decisions each have exactly one home.
3. **The SPEC lifecycle** — nothing is coded without a small, deliverable spec; every spec
   travels `READY → IN PROGRESS → IN REVIEW → SHIPPED → archived` through one set of files.
4. **The discipline** — small specs, independent review before "shipped," and a few
   standing rules that keep agents from drifting.

## Read in this order

| # | File | What it covers |
|---|------|----------------|
| 1 | [01-the-atlas.md](01-the-atlas.md) | The Atlas model — what an Atlas is and why it exists |
| 2 | [02-stores-model.md](02-stores-model.md) | The stores model — where each kind of knowledge lives, **described by role** |
| 3 | [03-atlas-anatomy.md](03-atlas-anatomy.md) | The files of record at the Atlas root, their naming, and per-repo orientation |
| 4 | [04-spec-lifecycle.md](04-spec-lifecycle.md) | The workitem lifecycle and its status values |
| 5 | [05-discipline.md](05-discipline.md) | Small deliverable specs · review before shipped · clean baseline per SPEC · commit-message hygiene |
| 6 | [06-bootstrap.md](06-bootstrap.md) | The bootstrap recipe — how to stand up a new Atlas |
| 7 | [07-optional-git-versioning.md](07-optional-git-versioning.md) | The **optional** git/symlink versioning mechanic |

## A note on roles vs. reference implementations

Throughout, the framework describes each component by the **role** it plays and then names a
concrete tool that *could* fill it. The roles are what the framework requires; the tools are
optional and swappable. The mapping:

| Role | Reference implementation (optional) | Alternatives exist |
|------|--------------------------|---------------------|
| **Primary agent / tool** *(required)* — the AI coding tool you drive the project with | Claude Code | Cursor, Codex, Cline, any CLI/IDE agent |
| **Cross-tool memory store, over MCP** *(required)* — universal knowledge every agent queries live | coco (an MCP memory server) | mem0, or any cross-tool rule store an agent can query over MCP |
| **Skill / cheat-sheet mechanism** *(strengthener)* — reusable, on-demand guides that *point into* the memory store | Claude Code skills | any tool affordance for reusable prompts |
| **Forced-discipline mechanism** *(strengthener)* — automation that injects behavior on events (session start, etc.) | Claude Code hooks | any event/automation hook your tool offers |

The first two roles are **required**: a primary agent and a **shared memory store every agent
reaches over MCP**. The named tools are only examples — pick your own. The last two are
*strengtheners*: use them if your tool offers them, and degrade gracefully if it doesn't.

> **Provenance.** This framework is the tool-agnostic render of an operational practice that
> originated as the concept `workspace-architecture` in a memory store. This repository is its
> formal, standalone home.
