#!/usr/bin/env sh
# Regenerate llms-full.txt — the entire Atlas framework concatenated in reading order,
# for LLMs that ingest a single file (llmstxt.org convention).
#
# It is GENERATED from the markdown (the single source of truth). Do not edit llms-full.txt
# by hand — re-run this script after changing any doc:  sh build-llms-full.sh
set -eu
cd "$(dirname "$0")"

DOCS="README.md \
method/README.md \
method/01-the-atlas.md \
method/02-stores-model.md \
method/03-atlas-anatomy.md \
method/04-spec-lifecycle.md \
method/05-discipline.md \
method/06-bootstrap.md \
method/07-optional-git-versioning.md \
STRUCTURE.md"

OUT=llms-full.txt

{
  echo "# Atlas — full text"
  echo
  echo "> A tool-agnostic, spec-driven framework for running large, multi-repo, AI-assisted projects."
  echo
  echo "Every document in this repo, concatenated in reading order. GENERATED from the markdown"
  echo "by build-llms-full.sh — do not edit by hand; re-run that script after changing the docs."
  for f in $DOCS; do
    echo
    echo "================================================================================"
    echo "# FILE: $f"
    echo "================================================================================"
    echo
    cat "$f"
    echo
  done
} > "$OUT"

echo "Wrote $OUT — $(wc -l < "$OUT" | tr -d ' ') lines, $(wc -c < "$OUT" | tr -d ' ') bytes"
