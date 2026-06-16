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
├── Dockerfile                ← python image, serves via gunicorn
└── .dockerignore             ← keeps .git / .venv / tooling out of the image
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
# Docker
docker build -t atlas-site .
docker run --rm -p 8088:80 atlas-site        # → http://localhost:8088/

# Local dev (project venv — never the system Python)
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python app.py                       # → http://localhost:8088/
```

This is the source the machinery points at: `~/.claude/atlas-source` holds the base URL (e.g.
`http://localhost:8088`, later `https://atlas.paranoid.software`) and `~/.claude/atlas-fetch.sh`
fetches `method/*.md` / `llms*.txt` from it.
