"""Atlas — the framework site.

A small Flask app that serves the Atlas framework straight from the markdown files
(the single source of truth):

  - human pages  : GET /                      -> rendered README
                   GET /method/01-the-atlas    -> rendered method page  (etc.)
  - raw markdown : GET /method/06-bootstrap.md -> the raw .md  (what atlas-fetch consumes)
  - llms.txt     : GET /llms.txt               -> generated index   (llmstxt.org)
  - llms-full.txt: GET /llms-full.txt          -> every doc concatenated, in reading order

Nothing is pre-generated: llms.txt / llms-full.txt and the pages are all produced on
request from the same markdown. Add a doc by adding its file and one PAGES entry.
"""
import os
import re

import markdown
from flask import Flask, Response, abort, render_template

BASE = os.path.dirname(os.path.abspath(__file__))

# Reading order + index metadata. Bodies live in the markdown; this is just nav + summaries.
PAGES = [
    {"file": "README.md",                          "url": "/",                       "title": "Overview",              "group": "Start here",
     "summary": "What Atlas is, the framework in one screen, required roles vs. optional tools."},
    {"file": "method/README.md",                   "url": "/method",                 "title": "Method overview",       "group": "The framework",
     "summary": "Reading order and the role-to-reference-implementation map."},
    {"file": "method/01-the-atlas.md",             "url": "/method/01-the-atlas",     "title": "The Atlas model",       "group": "The framework",
     "summary": "An Atlas — a symlink aggregator of a project's repos giving a single-CWD agent the whole territory."},
    {"file": "method/02-stores-model.md",          "url": "/method/02-stores-model",  "title": "The stores model",      "group": "The framework",
     "summary": "Where each kind of knowledge lives; the required shared MCP memory store; the universal-only boundary; the decision tree."},
    {"file": "method/03-atlas-anatomy.md",         "url": "/method/03-atlas-anatomy", "title": "Atlas anatomy",         "group": "The framework",
     "summary": "The files of record, naming, the per-repo orientation block, adding/removing a repo, and the optional candidates file."},
    {"file": "method/04-spec-lifecycle.md",        "url": "/method/04-spec-lifecycle","title": "The SPEC lifecycle",    "group": "The framework",
     "summary": "No code without a SPEC; READY -> IN PROGRESS -> IN REVIEW -> SHIPPED -> archived."},
    {"file": "method/05-discipline.md",            "url": "/method/05-discipline",    "title": "The discipline",        "group": "The framework",
     "summary": "Small deliverable specs; independent review before 'shipped' (never trust an agent's self-report)."},
    {"file": "method/06-bootstrap.md",             "url": "/method/06-bootstrap",     "title": "Bootstrap recipe",      "group": "The framework",
     "summary": "How to stand up a new Atlas, plus the orientation-file template."},
    {"file": "method/07-optional-git-versioning.md","url": "/method/07-optional-git-versioning","title": "Optional git-versioning","group": "The framework",
     "summary": "Versioning an Atlas's own planning files via the symlink-as-pointer mechanic (optional)."},
    {"file": "STRUCTURE.md",                       "url": "/structure",               "title": "Repository structure",  "group": "Reference",
     "summary": "How this repo is organized and how it maps onto the site."},
]
FILE_TO_URL = {p["file"]: p["url"] for p in PAGES}
URL_TO_PAGE = {p["url"]: p for p in PAGES}

# Nav number prefix (e.g. "method/02-stores-model.md" -> "02"); blank for unnumbered pages.
for _p in PAGES:
    _m = re.match(r"(?:.*/)?(\d+)-", _p["file"])
    _p["num"] = _m.group(1) if _m else ""

TAGLINE = "A tool-agnostic, spec-driven framework for running large, multi-repo, AI-assisted projects."
LLMS_INTRO = (
    "Atlas defines a methodology and a discipline, not a product. It is project-agnostic: it says "
    "where each kind of knowledge belongs and how a unit of work travels from idea to shipped. It "
    "requires a primary AI agent and a shared memory store every agent can query over MCP (coco and "
    "mem0 are optional examples of that role); the specific tools are your choice. It does not store "
    "project knowledge in a pile of files the way other spec-driven-development approaches do.\n\n"
    "The canonical content is the markdown in this repo; the files below are the whole framework, in "
    "reading order."
)

ATLAS_VERSION = os.environ.get("ATLAS_VERSION", "dev")   # baked at image build (git SHA); "dev" for bind-mount
ATLAS_BUILT = os.environ.get("ATLAS_BUILT", "")          # build timestamp, set by CI

app = Flask(__name__)


@app.after_request
def _version_header(resp):
    # Every response carries the version, so you can check freshness on any request.
    resp.headers["X-Atlas-Version"] = ATLAS_VERSION
    return resp


@app.route("/version")
def version():
    body = "version: %s\n" % ATLAS_VERSION
    if ATLAS_BUILT:
        body += "built:   %s\n" % ATLAS_BUILT
    return Response(body, mimetype="text/plain")


def read(file):
    path = os.path.join(BASE, file)
    if not os.path.isfile(path):
        abort(404)
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def rewrite_links(html, base_dir):
    """Turn intra-repo .md links into site routes (rendered page if known, raw .md otherwise)."""
    def repl(m):
        href = m.group(1)
        bare = href.split("#")[0]
        if "://" in href or href.startswith("#") or not bare.endswith(".md"):
            return m.group(0)
        target = os.path.normpath(os.path.join(base_dir, bare))
        return 'href="%s"' % FILE_TO_URL.get(target, "/" + target)
    return re.sub(r'href="([^"]+)"', repl, html)


def render_md(file):
    html = markdown.markdown(read(file), extensions=["tables", "fenced_code", "sane_lists"])
    return rewrite_links(html, os.path.dirname(file))


def nav_groups():
    groups = []
    for p in PAGES:
        grp = next((g for g in groups if g["name"] == p["group"]), None)
        if grp is None:
            grp = {"name": p["group"], "items": []}
            groups.append(grp)
        grp["items"].append(p)
    return groups


@app.route("/")
def home():
    return render_page(URL_TO_PAGE["/"])


@app.route("/<path:relpath>")
def any_path(relpath):
    # Raw markdown — only the documented files, by exact path (no traversal).
    if relpath.endswith(".md"):
        if relpath not in FILE_TO_URL:
            abort(404)
        return Response(read(relpath), mimetype="text/markdown")
    # Rendered page.
    page = URL_TO_PAGE.get("/" + relpath)
    if page is None:
        abort(404)
    return render_page(page)


def render_page(page):
    return render_template(
        "page.html",
        content=render_md(page["file"]),
        title=page["title"],
        groups=nav_groups(),
        current=page["url"],
        tagline=TAGLINE,
    )


@app.route("/llms.txt")
def llms_txt():
    out = ["# Atlas", "", "> " + TAGLINE, "", LLMS_INTRO]
    for grp in nav_groups():
        out += ["", "## " + grp["name"]]
        for p in grp["items"]:
            out.append("- [%s](%s): %s" % (p["title"], p["file"], p["summary"]))
    out += ["", "## Full text",
            "- [llms-full.txt](llms-full.txt): Every document above, concatenated in reading order, "
            "for ingesting the whole framework in one fetch."]
    return Response("\n".join(out) + "\n", mimetype="text/plain")


@app.route("/llms-full.txt")
def llms_full():
    out = ["# Atlas — full text", "", "> " + TAGLINE, "",
           "Every document in this repo, concatenated in reading order. Generated on request from "
           "the markdown (the single source of truth)."]
    for p in PAGES:
        out += ["", "=" * 80, "# FILE: " + p["file"], "=" * 80, "", read(p["file"]).rstrip("\n")]
    return Response("\n".join(out) + "\n", mimetype="text/plain")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8088, debug=True)
