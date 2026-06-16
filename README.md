# Atlas

**A spec-driven framework for running large, multi-repo, AI-assisted projects** — so any
agent, in any tool, on any day, can open a project cold and have complete clarity about what
it is, where it lives, where the work stands, and how work gets shipped.

Atlas is a small, tool-agnostic set of conventions: **where each kind of knowledge lives**,
and **how a unit of work travels from idea to shipped**. It assumes you drive development with
AI agents, but requires **no particular agent, IDE, editor, or memory product**. Where a
concrete tool helps, it's named as a *reference implementation* playing a *role* you can swap.

> **About this repo.** This is the formal write-up of the framework. The practice originated as
> an operational concept (`workspace-architecture`) kept in a memory store; this repository is
> its standalone, tool-agnostic formalization, served as a small documentation site (and an
> `llms.txt`). Its official home is **https://atlas.paranoid.software**. MIT-licensed, public.

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
  orientation + standing decisions in an orientation file; universal rules in a **shared
  memory store every agent queries over MCP** (required); current state in a regenerable
  status digest; each with exactly one home.
  → [method/02-stores-model.md](method/02-stores-model.md)
- **The SPEC lifecycle** — nothing is coded without a small, deliverable spec; every spec
  travels `READY → IN PROGRESS → IN REVIEW → SHIPPED → archived`.
  → [method/04-spec-lifecycle.md](method/04-spec-lifecycle.md)
- **The discipline** — small deliverable specs and **independent review before "shipped"**
  (never trust an agent's self-report). → [method/05-discipline.md](method/05-discipline.md)

## Roles and reference implementations

Atlas describes each component by the **role** it plays, then names a concrete tool that fills
it. The tools are swappable and optional; the first two **roles are required**, the last two
are strengtheners.

| Role | Reference implementation (optional) | Alternatives |
|---|---|---|
| Primary agent / tool *(required)* | Claude Code | Cursor, Codex, Cline, … |
| Cross-tool memory store, over MCP *(required)* | coco (an MCP memory server) | mem0, any cross-tool rule store agents query over MCP |
| Skill / cheat-sheet mechanism | Claude Code skills | any reusable-prompt affordance |
| Forced-discipline mechanism | Claude Code hooks | any event automation |

## Optional: versioning the Atlas itself

An Atlas works fine unversioned — it's just a folder of symlinks plus planning files. If you
*want* a git history of its planning artifacts, there's a clean symlink/git recipe that
versions the artifacts without touching the member repos. It stays **optional**. →
[method/07-optional-git-versioning.md](method/07-optional-git-versioning.md)

## What this repo is not

- **Not tied to any one agent, IDE, or memory-store product.** The framework names *roles*,
  not products: a primary agent and a shared MCP memory store are **required**, but *which*
  tools fill them are yours to choose (coco, mem0, … are optional examples).
- **Not a memory, and not a file-based "project memory."** Unlike spec-driven-development
  approaches that accrete project knowledge into a pile of files, Atlas keeps the durable
  universal layer in a shared, agent-queryable memory store and keeps project-specifics lean
  (orientation + status + specs). It defines methodology and discipline — nothing more.
- **Not a product description.** How a system *works* lives in its own code and docs; Atlas is
  about orientation, decisions, status, and the flow of work.
- **Not firm-specific.** No firm- or product-specific programming patterns — only the
  tool-agnostic conventions any team can adopt.

---

> **Status.** First real draft of the framework, rendered tool-agnostically from an operational
> practice. It is a writing/structuring artifact — nothing here is executable.
