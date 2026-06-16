# Repository structure

This repo holds the **Atlas framework** as a tool-agnostic, formal write-up, plus a small
Flask app that serves it as a site and as machine endpoints — all rendered from the same
markdown.

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
│   # the site — a small Flask app that renders the markdown above (nothing pre-generated)
├── app.py                    ← Flask: pages, raw .md, /llms.txt, /llms-full.txt
├── templates/page.html       ← page layout (sidebar in reading order + content)
├── static/styles.css         ← styling (responsive, auto dark mode)
├── requirements.txt          ← Flask · Markdown · gunicorn
├── Dockerfile                ← python image, serves via gunicorn (shared by dev & deploy)
│
│   # running it
├── docker-compose.yml        ← DEV: bind-mount + auto-reload (live docs)
├── docker-compose.deploy.yml ← example: run the published image (no build)
├── .dockerignore             ← keeps .git / .venv / tooling out of the image
└── .github/workflows/
    └── publish.yml           ← build + push the image to GHCR (on push to main / v* tag / manual)
```

## Why the framework is split into files

It is one document conceptually, but it has genuinely distinct parts that get read and linked
independently (the stores model vs. the lifecycle vs. the bootstrap recipe). Splitting keeps
each part skimmable and makes cross-links precise.

## The site (Flask)

`app.py` serves everything **from the markdown** — there is no generated, drift-prone copy and
no build step. Routes:

| Route | Serves |
|---|---|
| `/`, `/method/<name>`, `/structure` | the doc **rendered to HTML** (server-side), with a sidebar in reading order |
| `/method/<name>.md`, `/README.md`, … | the **raw markdown** (this is what the `atlas-fetch` machinery consumes) |
| `/llms.txt` | the [llmstxt.org](https://llmstxt.org) index, generated from the page manifest |
| `/llms-full.txt` | every doc concatenated in reading order, generated on request |

Adding a doc = drop the `.md` file and add one entry to the `PAGES` list in `app.py` (nav,
routes, llms.txt and llms-full.txt all follow).

### Run it

```bash
# Development — docker-compose.yml (bind-mount + auto-reload): edit any .md, refresh, no rebuild
docker compose up -d            # → http://localhost:8088/
docker compose down

# Local, without Docker (project venv — never the system Python):
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python app.py
```

In development the markdown is read **live from the bind-mount** (each request re-reads the
file). **Deployment uses a separate compose** (no bind-mount) that serves the content **baked
into the image** — there a doc change needs a rebuild. The `Dockerfile` is shared by both;
only the compose differs.

This is the source the machinery points at: `~/.claude/atlas-source` holds the base URL — the
official site **`https://atlas.paranoid.software`**, or `http://localhost:8088` for local dev —
and `~/.claude/atlas-fetch.sh` fetches `method/*.md` / `llms*.txt` from it.

### Published image & CI

`publish.yml` builds the image and pushes it to **GHCR** (`ghcr.io/<owner>/atlas`, multi-arch)
on every **push to `main`**, on `v*` tags, and on manual run. That's all CI does — **build &
push, no deploy**. Anyone can then pull and run it however they like (self-hosted, local, …):

```bash
docker compose -f docker-compose.deploy.yml up -d   # → http://localhost:8088/
```

> First publish: the GHCR package starts **private** — make it public in the repo's *Packages*
> settings if you want anonymous `docker pull`.
