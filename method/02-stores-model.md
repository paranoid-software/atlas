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

| Store (role) | Holds | Read by | In Claude Code |
|---|---|---|---|
| **Orientation file** | Project orientation (what the product is, each repo's purpose/stack) **+ standing project-specific decisions & conventions** (durable choices true of *this* project that don't generalize) **+ footguns** | The primary agent; the relevant slice is passed to delegated sub-agents via prompt | `CLAUDE.md` at the Atlas root (Claude Code) |
| **Coding-rules source** *(plugin)* | **Universal** rules, patterns, and anti-patterns that hold across *all* your projects | **Every** agent, querying it before writing code | Declared per Atlas by the `coding-rules` plugin: an MCP server (e.g. coco) or a `.md` file in the Atlas |
| **Skill / cheat-sheet store** | Domain cheat-sheets that **point into** the coding-rules source — never duplicate its content | The primary agent | Per-skill files (Claude Code skills) |
| **Forced-discipline store** | Behavior injected on events (e.g. "load STATUS at session start") so discipline doesn't depend on an agent remembering | The primary agent | Event hooks (Claude Code hooks) |

One is required, one is a plugin each Atlas chooses, and two are strengtheners:

- **Required: the orientation file.** Project-specific orientation in a plain file at the
  Atlas root. With it, the method works.
- **Chosen per Atlas: the coding-rules source.** Each Atlas decides where its shared,
  universal rules come from by declaring the `coding-rules` plugin in `_settings/atlas.toml`
  ([03-atlas-anatomy.md](03-atlas-anatomy.md)): `source = "mcp:<server>"` for an MCP memory
  server every agent can query — coco is one — or `source = "file:<path>"` for a `.md` inside
  the Atlas. The framework assumes no particular source, and an Atlas may declare none.
- **Strengtheners: skills + hooks.** If your primary tool supports reusable cheat-sheets
  and event automation, use them to make the discipline automatic. If it doesn't, the
  method still holds — you just apply the same discipline by hand.

The plugin owns two files at the Atlas root: `CODING_RULES_CANDIDATES.md` (rules staged for
promotion to the source) and `CODING_RULES_DEVIATIONS.md` (deliberate divergences from one of
its rules). At session start the agent is told the source and the deviations in force.

> The method does **not** use per-tool config files (`.cursorrules`, `GEMINI.md`,
> `AGENTS.md`, symlinked entrypoints, …): the coding-rules source covers the universal layer,
> and project orientation reaches other agents through the primary agent's delegation prompt.

## What the framework is — and what it deliberately is not

Atlas defines a **methodology and a discipline**. It is **project-agnostic**: it says *where
each kind of knowledge belongs* and *how work flows from idea to closed*, never what your
product is.

So, deliberately:

- **The framework is not itself a memory, and it does not store a project's knowledge in a
  pile of files.** Unlike spec-driven-development approaches that accrete a file-based
  "project memory," Atlas keeps the durable **universal** layer in the coding-rules source its
  plugin declares, and keeps project-specifics **lean**: orientation +
  standing decisions in one file, current state in a regenerable digest, and buildable work as
  specs. The Atlas files are **planning and orientation artifacts, not a knowledge dump.**
- **The framework assumes no memory.** Which coding-rules source an Atlas uses — if any — is
  that Atlas's choice, declared in its settings.

## The critical boundary: the coding-rules source is universal-only

This is the rule people get wrong, so it gets its own section.

**The coding-rules source holds only cross-project, universal knowledge** — patterns,
anti-patterns, behavior rules, decisions that would be true for an unrelated project too.
It is **not** a per-project description dump.

Every project has many decisions that are **durable and real but project-specific**: stack
choices, "we use X here," product-specific architecture. These are **neither universal**
(so not the coding-rules source) **nor transient** (so not status). They live in the project's
**orientation file**. Pushing them into the shared source would turn it into a
per-project description dump and make it useless to every other project.

> **The test:** *Would this be true for a different, unrelated project?*
> **Yes →** coding-rules source. **No →** orientation file.

## Where new knowledge goes — the decision tree

When something worth persisting appears, route it:

1. **Product description** (how the system works) → *not memory.* Lives in code or docs in
   the member repos.
2. **Task-scoped instruction** ("for this one case, do X") → apply now, persist nothing.
3. **Where we are right now / current work** → the project's **status digest**
   (`STATUS.md`) — and every line there must trace to a workitem artifact (see
   [04-spec-lifecycle.md](04-spec-lifecycle.md)).
4. **A standing project-specific decision or convention** (stack choice, "we use X here,"
   product architecture, a footgun) → the project's **orientation file**. *Not* the
   coding-rules source.
5. **A universal, cross-project pattern / rule / anti-pattern** → staged in
   **`CODING_RULES_CANDIDATES.md`**, then promoted to the **coding-rules source** in a
   dedicated curation session, with the human's approval.
6. **A buildable workitem** (feature / fix / refactor / a plan handed over by another
   tool) → a **SPEC** (shape it as a DRAFT first if still undecided), indexed in the
   backlog. *No coding without a SPEC.*
7. **A known divergence from a coding-rules rule that applies here** →
   **`CODING_RULES_DEVIATIONS.md`**.

### Triaging a candidate — when it turns out *not* to be universal

`CODING_RULES_CANDIDATES.md` (step 5) stages things that *aspire* to be universal. It is **not a
destination**: in a curation pass, each candidate resolves to exactly one home. A candidate
that, on reflection, is **not** universal is **re-routed**, not left in `CODING_RULES_CANDIDATES.md`.

> **The one question:** *Should this guide future work in this Atlas, beyond the SPEC that
> introduced it?*

| The candidate turns out to be… | Home |
|---|---|
| Universal — true for an unrelated project too | **coding-rules source** (promote) |
| A standing convention/decision **of this Atlas** | **orientation file** — the "establishing conventions" section (§5) |
| A deliberate divergence from a coding-rules rule that applies here | **`CODING_RULES_DEVIATIONS.md`** |
| Just how one workitem was done, with no standing rule for the future | **leave it in its SPEC**, drop the candidate — once closed, the `_archived/` SPEC is its only record |

The last row is the subtle one: an archived SPEC is the *record of the work*, not where an
agent looks for *standing rules* — orientation comes from `CLAUDE.md` + the status digest,
never from reading archived SPECs. A durable convention buried in an archived SPEC is
effectively lost; promote it to the orientation file. Only knowledge with **no**
future-guiding character stays in the SPEC.

**Worked examples** (generic — your real conventions live in your orientation file or coding-rules source):

- *"Standardize on the project's existing date library; don't add another."* → if it's how
  *any* project should behave, **coding-rules source**; if it's "in **this** Atlas we picked library
  X," **orientation file**.
- *"This layer maps errors to typed results, not exceptions."* → a standing convention of this
  Atlas → **orientation file**.
- *"For `SPEC_0007` we special-cased the legacy importer; don't generalize it."* → scoped to
  that work, no future rule → **stays in the SPEC**.
- *"A coding rule applies here, but a legacy area doesn't follow it yet; new work does."*
  → a known divergence → **`CODING_RULES_DEVIATIONS.md`**.

## No autonomous writes

Writes to any persistent store — the coding-rules source, the orientation file, skills, hooks —
require **explicit human approval**. New universal rules are promoted only in a dedicated
curation session, never mid-task — staged in `CODING_RULES_CANDIDATES.md` in between. This
is what keeps the stores from drifting out from under you.

> **If your tool has an autonomous file-memory feature** (one that writes its own memory
> files as it goes), **turn it off.** It will duplicate the coding-rules source with
> uncontrolled, autonomous writes — exactly the drift this model exists to prevent. The
> reference tool exposes a single setting for this (`autoMemoryEnabled: false`); whatever
> your tool calls it, disable it and let the deliberate stores be the only memory.
