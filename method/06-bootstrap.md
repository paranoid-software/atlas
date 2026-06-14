# Bootstrap recipe — standing up a new Atlas

This is the step-by-step for creating the baseline files of a new Atlas. It is written
**tool-agnostically**; where the reference implementation (Claude Code) uses a specific
affordance, that's called out as *reference impl* so you can map it to your tool or do it
by hand.

The recipe assumes **the Atlas directory and its symlinks already exist** — a human creates
those before bootstrapping. The current working directory is the Atlas directory.

> **Reference impl:** the reference author runs this recipe via an `/atlas-init` command,
> and regenerates `STATUS.md` later via `/atlas-sync`. Those are *machinery* that recall
> the definition and apply it — they don't re-encode it. If your tool has reusable
> commands, wire equivalents; otherwise follow the steps directly.

## Prerequisites (a human handles these first)

- The **Atlas directory** exists (reference convention:
  `~/Code/<container>/<topic>/_<topic>-default/`).
- **Symlinks to the real repos** are already in place inside it
  (`ln -s /real/path/to/repo <repo-name>`).
- *(Optional)* an editor multi-root workspace file lives **one level above** the Atlas
  (at the topic folder), listing the symlinks. Putting it inside the Atlas would be
  cyclically redundant.
- **Once-per-machine tool setup is already done** (not per Atlas): autonomous file-memory
  is disabled; any session-start and stop automations are installed tool-global.
  *(Reference impl: `autoMemoryEnabled: false` plus a `SessionStart` hook that injects
  `STATUS.md` and a `Stop` hook that nudges a status re-sync — all in user-global tool
  settings, installed once.)*

## Steps

1. **Discover the symlinks** at CWD and resolve each to its real target path. If an
   optional workspace file exists in the parent topic folder, confirm the two agree. **If
   the workspace file lists folders absent as symlinks (or vice versa), stop and ask the
   human before continuing.**

2. **Recall the method** before creating files — pull the Atlas model, this recipe, and the
   orientation-file template from wherever the canonical definition lives (the memory store
   for the reference author; this document otherwise). Don't reconstruct it from memory.

3. **Create the orientation file (`CLAUDE.md`)** from the template (below). Fill the "what
   lives here" section with the symlinks, each with a **per-repo orientation block** (role ·
   contributes · stack · cadence). Read each repo's own README / package description for the
   content. **If it's missing or ambiguous, ask the human — do not infer it from the file
   layout.** Leave the workflow / domain / establishing-conventions sections mostly as
   placeholders.

4. **Create the tool-local settings** (`.claude/settings.local.json` for the reference tool)
   granting the agent read access to the real symlink target paths. **No event hooks here** —
   those are tool-global, installed once per machine.

   ```json
   {
     "permissions": {
       "allow": [],
       "additionalDirectories": [
         "/real/path/to/repo-1",
         "/real/path/to/repo-2"
       ]
     }
   }
   ```

5. **Create the fixed scaffold — all start empty** so every Atlas has the same skeleton
   from day one:
   - `STATUS.md` — the thin digest (one-line product summary; "Active" and "Recently
     shipped" start empty).
   - `BACKLOG.md` — index only; "Open" starts empty.
   - `DEVIATIONS.md` — starts empty.
   - `_archived/README.md` — explains that the folder holds only shipped `SPEC_NNNN_<SLUG>.md`
     files.

6. **Optionally create `CANDIDATES.md`** (the candidates file) — only if you run a
   memory-store promotion workflow. It stages universal rules for a later curation session;
   starts empty, with the entry format documented inline. Skip it otherwise.

7. **Do NOT pre-create `SPEC_*.md` / `DRAFT_*.md`.** Those are per-workitem, created when the
   first workitem appears — not at bootstrap.

8. **Do NOT touch once-per-machine tool setup** (tool-global settings, skills) during Atlas
   bootstrap.

Done. The Atlas is scaffolded: standing decisions accumulate in the orientation file;
buildable work enters as `SPEC_NNNN_<SLUG>.md` (indexed in the backlog, shipped to
`_archived/`); `STATUS.md` digests it all; and, if you stage universal rules for promotion,
they collect in the optional candidates file.

## The orientation-file template

Copy this skeleton, then fill the `<...>` placeholders. Universal behavior rules are **not**
in this template — they live in the memory store; don't re-add them per Atlas.

````markdown
# <Topic> Atlas — agent instructions

This is the **<topic> Atlas** — a symlink-aggregator project root. Project orientation +
Atlas-specific glue only. Universal rules and behavior live in the memory store; autonomous
file-memory is off. **Current state & next steps live in [STATUS.md](STATUS.md) — read it
first.**

---

## 1. What lives here — symlinks and their purposes

Each top-level entry is a symlink into a real, independent git repo:

```
_<topic>-default/                  (Atlas; not a repo)
├── repo-a/   → <real-path>        — <one-line purpose>
├── repo-b/   → <real-path>        — <one-line purpose>
└── repo-c/   → <real-path>        — <one-line purpose>
```

Editing a file under a symlink writes to the underlying real repo. Cross-repo changes are
flagged explicitly.

### <repo-name> — <role: core product | reference | infrastructure | tooling>
- **Contributes:** <one paragraph>
- **Stack:** <languages / frameworks / key libs>
- **Cadence:** <how it releases — or "reference only: read, don't modify">

---

## 2. How I work in this Atlas
- **Before editing, identify the target repo** — most changes belong to exactly one repo;
  cross-repo changes are called out explicitly.
- <Atlas-specific tooling notes — environment naming, dev-server entrypoints, lint/format>
- <Atlas-specific footguns unique to this Atlas — generic ones live in the memory store>

---

## 3. <Project domain> — product / architecture
_(no domain conventions yet)_

---

## 5. Conventions we're establishing (Atlas-level, not in the memory store)
_Rules that apply to this Atlas and that we've decided not (yet) to lift into the memory
store. Keep it short; promote to the memory store only after a dedicated session, and only
if they generalize._
- _(empty — fill in as conventions get decided.)_
````

**Applying the template:**

- The **per-repo orientation block** is the heart of §1 — it's what lets any agent
  understand each repo without re-explanation.
- §2 = how you work; §3+ = domain; an optional §4 = a separable sub-domain; §5 = conventions
  you're establishing locally. **Section numbers are fixed**: if you omit §4, §5 stays §5 —
  don't renumber. The stable §1/§2/§3/§5 shape is recognizable across Atlases.
- At bootstrap, §3 is a single `_(no domain conventions yet)_` line. **Don't pre-create
  sub-sections** — empty 3.1/3.2 read as "I forgot to fill this in," not "fresh Atlas." Add
  them only when there's real content.
- Don't put current-state / progress in the orientation file — that's `STATUS.md`'s job.
