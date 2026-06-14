# Repository structure

This repo holds the **Atlas framework** as a tool-agnostic, formal write-up. It is structured
so it can later be rendered as a small documentation site (and emit an `llms.txt` index)
without reorganization.

## Layout

```
atlas/
├── README.md                 ← landing / index for the whole repo
├── STRUCTURE.md              ← this file
│
└── method/                   ← THE FRAMEWORK, split into focused, self-contained files
    ├── README.md             ← overview + reading order + role↔reference-impl map
    ├── 01-the-atlas.md       ← the Atlas model (what / why)
    ├── 02-stores-model.md    ← the stores model, described by role
    ├── 03-atlas-anatomy.md   ← files of record, naming, per-repo orientation
    ├── 04-spec-lifecycle.md  ← workitem lifecycle + status values
    ├── 05-discipline.md      ← small deliverable specs, review, ship criteria
    ├── 06-bootstrap.md       ← bootstrap recipe + orientation-file template
    └── 07-optional-git-versioning.md  ← the optional symlink/git mechanic
```

## Why the framework is split into files

It is one document conceptually, but it has genuinely distinct parts that get read and linked
independently (the stores model vs. the lifecycle vs. the bootstrap recipe). Splitting keeps
each part skimmable and makes cross-links precise.

## Toward a documentation site / `llms.txt`

Each `method/` file is **self-contained and rule-shaped**, with a single clear topic and a
stable filename. That makes it straightforward later to:

- render the folder as a static documentation site (one page per file, in reading order), and
- emit an `llms.txt` that indexes the files so an LLM can pull the framework directly.

No site tooling exists yet — this is the target the current layout is meant to grow into
cleanly, without moving files around.
