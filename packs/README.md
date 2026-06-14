# Packs — the marketplace of importable knowledge

Beyond the method itself, the larger vision is a **marketplace of importable knowledge
packs**: units of curated knowledge an adopter can pick, import into their own memory store,
and evolve. This folder is where pack *definitions* will eventually live. It does **not**
build any packs yet — it sets out what a pack is and how the catalog is meant to work.

## The core idea: a unit of importable knowledge

In the reference memory store, knowledge is grouped into **concepts** — named domains, each a
bundle of rules / patterns / anti-patterns. The marketplace idea is simply: **each such
concept is an importable "pack."** Pick what you want, import it as a *starting point*, and
fork it. Software knowledge is a living thing — packs are seeds others evolve, not truth
handed down.

The reference memory store already has the primitives for this: export, import, and
provenance tracking. The kernel — "a concept is an importable unit" — largely exists. The
**neutral interchange format** that makes a pack portable (rather than a memory-store-internal
dump) is the real product standard; its shape is **settled** — a pack is a directory with a
`pack.yaml` manifest plus one markdown file per rule (front-matter `type · concepts · provenance
· version` + a markdown body). A single-file export is generated from that directory for runtimes
that prefer one blob.

## Two tiers, different positioning

| Tier | What it is | Positioning |
|---|---|---|
| **The method pack** | The Atlas method (`workspace-architecture`) — this repository | Flagship, **universal**, free/open. The adoption driver. You're sharing a *methodology*, and it must carry **zero** firm-specific baggage. |
| **Pattern packs** | Opinionated, firm-flavored collections of dev patterns (e.g. a testing pack, a web-framework pack, a service-layer pack) | **Starting points**, not truth. Forkable, versioned, evolve. Each is one firm's way of doing a thing; another firm has their own or doesn't do that thing at all. |

> **What a pattern pack looks like (by example, not by inclusion).** The reference author's
> memory store also holds dev-pattern concepts — things like a service-layer pattern, a
> SQL-style convention, a typed-error pattern, framework-specific rules. **Those are examples
> of what a pattern pack *is*; their content is deliberately *not* in this method repo.** The
> method ships clean: it tells adopters to seed *their own* pattern packs, never to inherit
> the reference author's. That separation is the whole reason the method was extracted out of
> the entangled memory store in the first place.

## What this repo deliberately does *not* ship

- **No firm-specific programming patterns.** No web-framework conventions, no CMS or
  micro-framework specifics, no firm testing-naming schemes, no product names. The method
  describes *roles and disciplines*; concrete patterns are the adopter's to seed.
- **No requirement to adopt any one memory store or IDE.** Reference implementations are
  named; none are mandated.

## Licensing

**Everything here is MIT, public, and not monetized** — the method pack and any pattern pack
alike. The two tiers differ in **content and positioning only** (how universal vs. how
opinionated), never in license or price.

## Versioning

A pack carries a **semver** (the friendly handle, e.g. `workspace-architecture@1.3.0`) and
**each rule carries its own version**, so an import can record exactly which rule-versions it
pulled and support partial forks. This rides on the memory store's existing provenance
primitives rather than a parallel system.

## Status

This folder is a **placeholder for the catalog**. The pack definitions, the catalog/landing
that lists them, and the interchange-format spec/adapters that make them portable are all
future work.
