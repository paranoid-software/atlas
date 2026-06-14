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

---

These two are the universal core. Anything more specific — a particular error-handling
pattern, a framework convention, a naming scheme — is **not the method**. It belongs in your
orientation file (if project-specific) or in a *pattern pack* (if it's a reusable,
opinionated starting point). See [../packs/README.md](../packs/README.md).
