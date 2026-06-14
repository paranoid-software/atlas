# The stores model

The heart of the method is a fixed answer to one question: **"where does this piece of
knowledge go?"** Get that right and an agent never has to guess, never duplicates, and
never loses a decision between sessions.

Knowledge is sorted by **two axes**:

- **Scope** — is it *universal* (true for any project), *project-specific* (true for this
  one project), or *transient* (true right now)?
- **Audience** — does *every* tool need it, or only the primary agent you drive the
  project with?

## The four stores (by role)

| Store (role) | Holds | Read by | Reference impl |
|---|---|---|---|
| **Orientation file** | Project orientation (what the product is, each repo's purpose/stack) **+ standing project-specific decisions & conventions** (durable choices true of *this* project that don't generalize) **+ footguns** | The primary agent; the relevant slice is passed to delegated sub-agents via prompt | `CLAUDE.md` at the Atlas root (Claude Code) |
| **Memory store** | **Universal** rules, patterns, and anti-patterns that hold across *all* your projects | **Every** agent, in any tool, querying it live over MCP | a shared MCP memory server queried by all agents — e.g. coco; alternatives: mem0, or any cross-tool rule store an agent can query over MCP |
| **Skill / cheat-sheet store** | Domain cheat-sheets that **point into** the memory store — never duplicate its content | The primary agent | Per-skill files (Claude Code skills) |
| **Forced-discipline store** | Behavior injected on events (e.g. "load STATUS at session start") so discipline doesn't depend on an agent remembering | The primary agent | Event hooks (Claude Code hooks) |

Two of these are required and two are strengtheners:

- **Required: the orientation file + the memory store.** Project-specific orientation in a
  plain file at the Atlas root; universal knowledge in a **shared memory store that every
  agent reaches over MCP**. Both are part of the framework — with these two, the method works.
- **Strengtheners: skills + hooks.** If your primary tool supports reusable cheat-sheets
  and event automation, use them to make the discipline automatic. If it doesn't, the
  method still holds — you just apply the same discipline by hand.

**On the memory store — the framework requires the *role*, recommends MCP, and names no
tool.** The universal layer must live in a store that **all of your agents can query live,
across tools** — and MCP is the recommended way to expose it, so the same universal knowledge
is one query away for every agent regardless of which one is running. A memory store of this
kind is **required**; the specific tool is **your choice and optional**. **coco** is one MCP
memory server that plays this role; **mem0** is another; any cross-tool, agent-queryable rule
store works.

> The method does **not** use per-tool config files (`.cursorrules`, `GEMINI.md`,
> `AGENTS.md`, symlinked entrypoints, …). They were rejected as unmaintainable: the memory
> store covers the universal layer cross-tool, and project orientation reaches other agents
> through the primary agent's delegation prompt.

## What the framework is — and what it deliberately is not

Atlas defines a **methodology and a discipline**. It is **project-agnostic**: it says *where
each kind of knowledge belongs* and *how work flows from idea to shipped*, never what your
product is.

So, deliberately:

- **The framework is not itself a memory, and it does not store a project's knowledge in a
  pile of files.** Unlike spec-driven-development approaches that accrete a file-based
  "project memory," Atlas keeps the durable **universal** layer in a shared, agent-queryable
  **memory store** (required, over MCP), and keeps project-specifics **lean**: orientation +
  standing decisions in one file, current state in a regenerable digest, and buildable work as
  specs. The Atlas files are **planning and orientation artifacts, not a knowledge dump.**
- **The framework names roles, not products.** A memory store is required; *which* one is your
  call. The same holds for the primary agent and the optional strengtheners.

## The critical boundary: the memory store is universal-only

This is the rule people get wrong, so it gets its own section.

**The memory store holds only cross-project, universal knowledge** — patterns,
anti-patterns, behavior rules, decisions that would be true for an unrelated project too.
It is **not** a per-project description dump.

Every project has many decisions that are **durable and real but project-specific**: stack
choices, "we use X here," product-specific architecture. These are **neither universal**
(so not the memory store) **nor transient** (so not status). They live in the project's
**orientation file**. Pushing them into the shared memory store would turn it into a
per-project description dump and make it useless to every other project.

> **The test:** *Would this be true for a different, unrelated project?*
> **Yes →** memory store. **No →** orientation file.

## Where new knowledge goes — the decision tree

When something worth persisting appears, route it:

1. **Product description** (how the system works) → *not memory.* Lives in code or docs in
   the member repos.
2. **Task-scoped instruction** ("for this one case, do X") → apply now, persist nothing.
3. **Where we are right now / current work** → the project's **status digest**
   (`STATUS.md`) — and every line there must trace to a workitem artifact (see
   [04-spec-lifecycle.md](04-spec-lifecycle.md)).
4. **A standing project-specific decision or convention** (stack choice, "we use X here,"
   product architecture, a footgun) → the project's **orientation file**. *Not* the memory
   store.
5. **A universal, cross-project pattern / rule / anti-pattern** → the **memory store** —
   ideally staged first in an optional **candidates file** for a dedicated curation session,
   then promoted (or promoted directly if you don't keep a staging file).
6. **A buildable workitem** (feature / fix / refactor / a plan handed over by another
   tool) → a **SPEC** (shape it as a DRAFT first if still undecided), indexed in the
   backlog. *No coding without a SPEC.*
7. **A known divergence from a memory-store rule that applies here** → the **deviations
   file**.

## No autonomous writes

Writes to any persistent store — the memory store, the orientation file, skills, hooks —
require **explicit human approval**. New universal rules are promoted only in a dedicated
curation session, never mid-task — optionally *staged* in a candidates file in between. This
is what keeps the stores from drifting out from under you.

> **If your tool has an autonomous file-memory feature** (one that writes its own memory
> files as it goes), **turn it off.** It will duplicate the memory store with
> uncontrolled, autonomous writes — exactly the drift this model exists to prevent. The
> reference tool exposes a single setting for this (`autoMemoryEnabled: false`); whatever
> your tool calls it, disable it and let the deliberate stores be the only memory.
