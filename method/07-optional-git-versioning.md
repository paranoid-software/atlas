# Optional: versioning the Atlas itself (git + symlinks)

**Versioning an Atlas with git is OPTIONAL** — a choice the adopter makes, neither required
nor forbidden by the method. An Atlas works perfectly well unversioned: it's just a folder
of symlinks plus planning files. This section exists only so that *if* you choose to version
it, you do it cleanly. The default stance is **"your call."**

## Reconciling with "an Atlas is a non-git aggregator"

The core model calls an Atlas a *non-git aggregator*, and that stays true in spirit: git
here **never** subsumes the aggregated repos into one history. What this optional mechanic
adds is narrower — the Atlas's **own planning files** (decisions, SPEC evolution, status
over time) are ordinary text worth a history, and they *can* be versioned in their own repo
**without touching or duplicating the member repos**.

So: **the aggregation stays non-git; only the artifacts are optionally versioned.** Opt in
when that history has value (long-lived project, multiple SPECs shipping, decisions worth a
diff); skip it for a throwaway or single-purpose Atlas.

## Why it's safe — git stores a symlink as a pointer, not as contents

A committed symlink is a tiny blob (git mode `120000`) whose entire content is the **target
path string** — git never recurses through it into the linked repo. So `git add` over an
Atlas records the planning files plus one small (~50-byte) pointer blob per symlink, and
**never** the member repos' files, history, or `.git`. Each member repo keeps its own git,
history, and release cadence; nothing is re-sent or embedded.

> Verified empirically (2026-06-13): committing an Atlas with a symlink to a repo tracked
> only the link's path string, never the repo's files.

## The caveat that drives the recipe — version the artifacts, not the pointers

Atlas symlinks are typically **absolute, machine-specific paths** (`/Users/<me>/Code/…`), so
a committed symlink is a dangling pointer on any other machine. The tool-local settings file
has the same problem (machine-specific absolute paths; its `.local` suffix already implies
"untracked"). So **version the text artifacts and ignore the symlinks** (and the local
settings).

## Recipe — whitelist `.gitignore`, then `git init`

Ignore everything, then re-include only the planning artifacts:

```gitignore
/*
!/*.md
!/_archived/
!/.gitignore
# plus any other fixed artifact dirs the method defines
```

Any current **or future** symlink is ignored automatically — zero per-repo maintenance — and
only the planning artifacts are tracked.

**Prefer this whitelist over a hand-maintained blocklist of repo names.** `.gitignore` has
**no "ignore by filetype = symlink" selector** — matching is purely by path/name — so
"deny everything, allow the known artifact set" is the robust, future-proof form. A blocklist
must be edited every time a new repo is symlinked in; the whitelist never does.
