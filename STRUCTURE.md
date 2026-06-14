# Repository structure

This repo holds two things: the **Atlas method** (a tool-agnostic write-up) and the seed of a
**marketplace of importable knowledge packs**. This file proposes how the repo is organized and
where future pieces land. It is a **proposal** — it lays out the shape and the reasoning; it does
not build the packs or the catalog.

## Current layout

```
atlas/
├── README.md                 ← landing / index for the whole repo
├── STRUCTURE.md              ← this file
│
├── method/                   ← THE METHOD (the flagship pack), split into focused files
│   ├── README.md             ← method overview + reading order + role↔reference-impl map
│   ├── 01-the-atlas.md       ← the Atlas model (what / why)
│   ├── 02-stores-model.md    ← the stores model, described by role
│   ├── 03-atlas-anatomy.md   ← files of record, naming, per-repo orientation
│   ├── 04-spec-lifecycle.md  ← workitem lifecycle + status values
│   ├── 05-discipline.md      ← small deliverable specs, review, ship criteria
│   ├── 06-bootstrap.md       ← bootstrap recipe + orientation-file template
│   └── 07-optional-git-versioning.md  ← the optional symlink/git mechanic
│
└── packs/                    ← THE MARKETPLACE (catalog seed)
    └── README.md             ← what a pack is, the two tiers, licensing, versioning
```

## Why the method is split into files

The method is one document conceptually, but it has genuinely distinct parts that get read and
linked independently (the stores model vs. the lifecycle vs. the bootstrap recipe). Splitting
keeps each part skimmable, lets `STATUS.md`-style cross-links be precise, and — not
incidentally — makes `method/` read like a **pack already in authoring form**: a directory of
rule-shaped markdown files. That matches the interchange format (a pack directory with a
manifest plus one markdown file per rule).

## Proposed future layout (when packs and the catalog exist)

Nothing below exists yet; this is the **target** the current layout grows into.

```
atlas/
├── README.md                 ← doubles as the catalog landing: method + pack index + format spec
├── STRUCTURE.md
│
├── method/                   ← the method (unchanged in spirit)
│   └── …
│
├── spec/                     ← THE INTERCHANGE FORMAT (the real product standard)
│   ├── README.md             ← the neutral pack schema: type · concepts · body · provenance · version
│   ├── schema/               ← machine-readable schema (JSON Schema / etc.) for the pack format
│   └── adapters/             ← per-runtime importers (coco, mem0, …) — "speakers" of the format
│
└── packs/                    ← pack DEFINITIONS, one directory per pack
    ├── README.md             ← the catalog index (tiers, how to import, versioning policy)
    ├── workspace-architecture/   ← the method, expressed AS a pack (manifest + rule files)
    │   ├── pack.yaml
    │   └── rules/*.md
    └── <pattern-pack>/       ← adopters seed their OWN here; none shipped by this repo
```

Key placements and the reasoning:

- **The method lives in `method/`** as human-grade prose — the readable definition. It is *also*
  expressed as an importable pack under `packs/workspace-architecture/` (manifest + rule files),
  **generated from / kept in sync with** `method/`. The memory store is canonical for now and
  `method/` is the derived render; the canonical role flips to this repo once the pack format
  can round-trip.
- **Pack definitions live under `packs/<name>/`** as a directory — a manifest plus one markdown
  file per rule. This repo ships **only the method pack**; pattern packs are where *adopters*
  seed their own, so the repo demonstrates the slot without filling it with firm-specific
  content.
- **The interchange format lives under `spec/`** because it's a distinct product standard from
  any one pack — the thing every pack and every runtime adapter conforms to.
- **The catalog/landing is `README.md`** (this repo doubles as the marketplace front door):
  explains the method, indexes the packs, points at the format spec, names the reference runtime
  and alternatives.

## What is intentionally absent

- **No `packs/<firm-pattern-pack>/` content.** The method ships clean; firm-specific patterns are
  the adopter's to seed (see [packs/README.md](packs/README.md)).
- **No runtime, no importer code yet.** `spec/adapters/` is a future slot, not present today.
- **No mandated tool.** Reference implementations are named throughout; none are required.
