# The discipline

The Atlas and the stores tell you *where things live*. The discipline is the handful of
standing rules that keep AI-driven work honest. These are **method-level and universal** —
they hold regardless of language, framework, or product.

## 1. Specs are small and independently deliverable

A SPEC is sized to be **built, reviewed, and shipped as one coherent unit** — not an epic.
If a workitem can't be described, implemented, and verified end-to-end without dragging in
half the system, it is too big: split it into SPECs that each ship on their own.

Small-and-deliverable is what makes the rest of the discipline affordable. Independent
review (below) is only practical when the change under review is bounded. A spec that
sprawls can't be exhaustively reviewed, can't be cleanly reverted, and tends to hide
"done-ish" work behind its own size.

> Rules of thumb: one SPEC should have a single clear "this is what shipped" sentence; it
> should be reviewable in one focused sitting; and it should leave the project in a
> shippable state when it lands, not "shippable once the next three SPECs also land."

## 2. A SPEC is never shipped on an agent's self-report

This is the core ship-discipline rule. An agent's "I'm done" message is **not** evidence
that the work is done. Before a SPEC is SHIPPED:

1. the implementing agent finishes its work, **then**
2. an **independent review** verifies the work against the SPEC — *running the suites and
   exercising the change*, not reading the agent's report, **then**
3. the change is **committed**.

Independent review routinely produces substantial corrections (boundary conditions, error
handling, naming, test coverage, dependency layout). Skipping it — trusting the
self-report — is how subtly-wrong work gets archived as "shipped." See
[04-spec-lifecycle.md](04-spec-lifecycle.md) for the `IN REVIEW → SHIPPED` transition and
the un-archive rule when something was shipped early.

## 3. Start each SPEC from a clean baseline

Before implementing a SPEC, check the **affected repo's** working tree. If it has **staged or
uncommitted changes that aren't part of this SPEC, stop and surface them** — don't build on top
of unrelated work-in-progress. Pre-existing changes mixed into a SPEC pollute its diff: the
change is no longer independently reviewable or cleanly revertable, which breaks the contract
that **a SPEC's commit equals the SPEC's work**.

Resolve it first — the unrelated changes get committed or set aside (a human runs the write), or
they're confirmed to belong to this SPEC — *then* begin. A clean baseline per workitem is what
makes the independent review and a clean revert possible.

## 4. A commit message says what the commit does — nothing else

When you draft a commit message, describe **only what this commit changes**, at a verbosity that
matches the change:

- **Subject** — one imperative line ("Add X", "Fix Y"), ~50 chars, no trailing period.
- **Body** *(only when the change needs it)* — what changed and why, in present terms. A small
  change needs no body.

Leave out:

- **archaeology** — how you got here, dead ends, prior attempts, "previously…", session narration;
- **what is *not* done** — TODOs, "still missing", "next we'll…", caveats about unrelated work.
  The message documents the commit, not the roadmap.

Simple but complete: someone reading the history understands exactly what this commit did —
without the backstory, and without a list of what it didn't do.

> Commit **authorship / attribution** (who runs the commit, signatures, trailers) is a separate
> **project/business policy — not part of this discipline.** This rule is only about the message's
> content.

---

These four are the universal core. Anything more specific — a particular error-handling
pattern, a framework convention, a naming scheme — is **not the framework**: it's a
project-specific choice that belongs in your orientation file, or a universal one that belongs
in your memory store. Not here.
