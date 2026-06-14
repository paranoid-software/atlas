# Atlas

**A tool-agnostic method for running large, multi-repo, AI-assisted projects — and the seed
of a marketplace of importable knowledge packs.**

Atlas is a small set of conventions that let any AI agent, in any tool, on any day, open a
project cold and have complete clarity about what it is, where it lives, where the work
stands, and how work gets shipped. It assumes you drive development with AI agents, but it
requires **no particular agent, IDE, editor, or memory product**. Where a concrete tool
helps, it's named as a *reference implementation* playing a *role* you can swap.

This repository is both the **write-up of the method** and the **catalog** for the packs
built around it.

## Start here

| If you want to… | Go to |
|---|---|
| Understand and adopt the method | **[method/README.md](method/README.md)** — overview + reading order |
| See how this repo is organized (and where future packs land) | **[STRUCTURE.md](STRUCTURE.md)** |
| Understand the marketplace / packs idea | **[packs/README.md](packs/README.md)** |

## The method in one screen

- **The Atlas** — one directory that aggregates all of a project's repos **by symlink** (not
  by copying), so a single-CWD agent sees the whole territory at once while each repo keeps
  its own git, CI, and release cadence. → [method/01-the-atlas.md](method/01-the-atlas.md)
- **The stores model** — a fixed answer to "where does *this* knowledge go?": project
  orientation + standing decisions in an orientation file; **universal** rules in a
  cross-tool memory store; current state in a regenerable status digest; each with exactly
  one home. → [method/02-stores-model.md](method/02-stores-model.md)
- **The SPEC lifecycle** — nothing is coded without a small, deliverable spec; every spec
  travels `READY → IN PROGRESS → IN REVIEW → SHIPPED → archived`.
  → [method/04-spec-lifecycle.md](method/04-spec-lifecycle.md)
- **The discipline** — small deliverable specs and **independent review before "shipped"**
  (never trust an agent's self-report).
  → [method/05-discipline.md](method/05-discipline.md)

Roles map to reference implementations like so (all swappable; only the first two are
essential):

| Role | Reference impl | Alternatives |
|---|---|---|
| Primary agent / tool | Claude Code | Cursor, Codex, Cline, … |
| Cross-tool memory store | coco (MCP memory server) | mem0, any shared rule store |
| Skill / cheat-sheet mechanism | Claude Code skills | any reusable-prompt affordance |
| Forced-discipline mechanism | Claude Code hooks | any event automation |

## The bigger idea: a marketplace of importable knowledge packs

The method currently lives entangled inside a single memory store that is simultaneously
three things: the **tool** (the memory runtime), the **store of the method**, and the
**store of one firm's programming patterns**. Sharing "the memory store with our rules
preloaded" therefore drags firm-specific baggage and forces adoption of one tool. Wrong unit
to share.

Atlas separates them. **The shareable unit is the *method*** — universal, clean, and
tool-agnostic — and, beyond it, a catalog of **packs**: importable, forkable units of
curated knowledge. Two tiers:

- **The method pack** (`workspace-architecture`) — flagship, universal, the adoption driver.
- **Pattern packs** — opinionated, firm-flavored *starting points*; forkable, versioned,
  evolving. **This repo ships none of them** — adopters seed their own.

The crux that makes packs real is a **neutral interchange format** so a pack can be imported
into one memory runtime or another, rather than being a single tool's internal dump. That
format is the actual product standard; runtimes are interchangeable speakers of it. Its
shape is settled below.

## Decisions already made (binding)

These were settled when the method was extracted and are not re-litigated here:

- **The shareable unit is the METHOD, not any one tool.** The memory store is *a reference
  implementation* of one role the method needs (a cross-tool store every agent queries) — not
  a requirement.
- **Stores are described by ROLE; tools are named as implementations.** "You need a memory
  store playing role X; we use coco; alternatives exist."
- **Firm patterns never ship.** The method tells adopters to seed their own; zero
  firm-specific programming content in what's shared.
- **Source-of-truth direction is memory-store → doc** (derived, tool-abstracted) for now,
  flipping to this-repo-canonical once the pack interchange format can round-trip.
- **The method lives here, versioned**, not floating inside an unversioned aggregator
  directory.
- **Versioning an Atlas itself is OPTIONAL.** It works fine unversioned; if you opt in, there's
  a clean symlink/git recipe. → [method/07-optional-git-versioning.md](method/07-optional-git-versioning.md)

## Design decisions (settled)

1. **Interchange format** — a pack is a **directory**: a manifest plus one markdown file per
   rule (a single-file export is generated from it).
2. **Pack versioning** — **per-rule version + a rolled-up pack semver**, on the memory
   store's provenance primitives.
3. **Licensing** — **MIT, public, no monetization**; the method/pattern tiers differ in
   content and positioning only, never in license or price.
4. **Canonical source** — **memory store now, this repo later**: coco stays canonical and
   this repo is the derived render until the interchange format can round-trip, then this
   public repo becomes canonical and coco imports the method back.

## Explicitly not in scope here

- No memory store preloaded with firm concepts (an optional starter seeded with *only* the
  method is the most any runtime should carry publicly).
- The method is not welded to any one memory store, IDE, or tool.
- No firm-specific programming patterns are imported into this repo.

---

> **Status.** This is the first real draft of the method, rendered tool-agnostically from an
> operational practice. It is a writing/structuring artifact — nothing here is executable. The
> method's canonical home is the memory store for now, flipping to this repo once the pack
> interchange format can round-trip (decision 4 above).
