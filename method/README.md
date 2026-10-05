# The Atlas method

A way to run **large, multi-repo, AI-assisted projects** so that an agent, on any day,
can open the project cold and have complete clarity about *what it is, where it lives,
where the work stands, and how work gets closed*.

The method is small. It is a handful of conventions about **where each kind of
knowledge lives** and **how a unit of work travels from idea to closed**. It is anchored
in **Claude** (Claude Code) as the primary agent, which delegates work to other agents —
Cursor, Codex, subagents, local LLMs — as workbenches.

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
   travels `READY → IN PROGRESS → IN REVIEW → CLOSED → archived` through one set of files.
4. **The discipline** — small specs, independent review before "closed," and a few
   standing rules that keep agents from drifting.

## Read in this order

| # | File | What it covers |
|---|------|----------------|
| 1 | [01-the-atlas.md](01-the-atlas.md) | The Atlas model — what an Atlas is and why it exists |
| 2 | [02-stores-model.md](02-stores-model.md) | The stores model — where each kind of knowledge lives, **described by role** |
| 3 | [03-atlas-anatomy.md](03-atlas-anatomy.md) | The Atlas's own files, `_settings/`, sources declared vs located, editor git settings, naming |
| 4 | [04-spec-lifecycle.md](04-spec-lifecycle.md) | The workitem lifecycle, what a SPEC is (and is not), Plan ≠ how, and how to resume one |
| 5 | [05-discipline.md](05-discipline.md) | Human gates · branch per SPEC · small deliverable specs · review before close · clean baseline · commit-message hygiene · no archaeology |
| 6 | [06-bootstrap.md](06-bootstrap.md) | The bootstrap recipe — how to stand up a new Atlas |
| 7 | [07-sharing-an-atlas.md](07-sharing-an-atlas.md) | Git as how an Atlas is shared; what is versioned and the `.gitignore` |

## Claude as the anchor

Claude (Claude Code) is the primary agent. `CLAUDE.md`, skills, hooks and commands are
first-class pieces of the framework. Other agents — Cursor, Codex, subagents, local LLMs —
are workbenches Claude delegates to. The memory of rules is the **coding-rules** plugin
each Atlas chooses.
