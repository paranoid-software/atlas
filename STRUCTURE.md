# Repository structure

This repo holds the **Atlas framework** as a tool-agnostic, formal write-up. It is structured
so it can later be rendered as a small documentation site (and emit an `llms.txt` index)
without reorganization.

## Layout

```
atlas/
├── README.md                 ← landing / index for the whole repo (also doc page "Overview")
├── STRUCTURE.md              ← this file
│
├── method/                   ← THE FRAMEWORK, split into focused, self-contained files
│   ├── README.md             ← overview + reading order + role↔reference-impl map
│   ├── 01-the-atlas.md       ← the Atlas model (what / why)
│   ├── 02-stores-model.md    ← the stores model, described by role
│   ├── 03-atlas-anatomy.md   ← files of record, naming, per-repo orientation
│   ├── 04-spec-lifecycle.md  ← workitem lifecycle + status values
│   ├── 05-discipline.md      ← small deliverable specs, review, ship criteria
│   ├── 06-bootstrap.md       ← bootstrap recipe + orientation-file template
│   └── 07-optional-git-versioning.md  ← the optional symlink/git mechanic
│
│   # mini-site (zero-build; renders the markdown above, client-side)
├── index.html                ← the site: sidebar (reading order) + client-side md renderer
├── styles.css                ← site styling (responsive, auto dark mode)
├── llms.txt                  ← llmstxt.org index of the docs (served at the site root)
├── llms-full.txt             ← all docs concatenated in reading order (generated)
├── build-llms-full.sh        ← regenerates llms-full.txt from the markdown
├── Dockerfile                ← serves the static site via nginx
├── .dockerignore             ← keeps .git / tooling out of the image
└── .nojekyll                 ← lets GitHub Pages serve the files as-is
```

> `llms-full.txt` is **generated** from the markdown — the single source of truth stays the
> `.md` files. Re-run `sh build-llms-full.sh` after editing any doc to refresh it.

## Why the framework is split into files

It is one document conceptually, but it has genuinely distinct parts that get read and linked
independently (the stores model vs. the lifecycle vs. the bootstrap recipe). Splitting keeps
each part skimmable and makes cross-links precise.

## The mini-site

The repo ships a **zero-build documentation site**. `index.html` renders the same markdown
files client-side (a single pinned dependency, the `marked` parser, from a CDN) with a sidebar
in reading order — so the markdown stays the **single source of truth**; there is no generated,
drift-prone HTML copy. `llms.txt` (llmstxt.org format) sits at the site root so an LLM can pull
the whole framework directly.

### Run it

```bash
# Option A — Docker (nginx)
docker build -t atlas-site .
docker run --rm -p 8000:80 atlas-site
# → http://localhost:8000/

# Option B — any static file server (no Docker)
python3 -m http.server 8000      # serves static files only; no install, no project code
# → http://localhost:8000/

# Option C — GitHub Pages: serve from the repo root; the site and llms.txt work as-is.
```

Each `method/` file is **self-contained and rule-shaped**, with a single clear topic and a
stable filename, so a page-per-file site needs no reorganization and new files appear by adding
one nav entry in `index.html`.
