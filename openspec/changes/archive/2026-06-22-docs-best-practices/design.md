<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
SPDX-FileContributor: https://redtux.github.io/commitizen-spdx-changelog/credits/

SPDX-License-Identifier: Apache-2.0
-->

## Context

The project's `docs/` directory has four Markdown files and a `plans/`
subdirectory. The content is functional but minimal — the landing page is a
single sentence, the API reference is one mkdocstrings block with no prose, and
there is no dedicated usage guide. Google's Documentation Best Practices
emphasize Minimum Viable Documentation, updating docs with code, and writing for
humans first.

## Goals / Non-Goals

**Goals:**

- Transform `docs/index.md` into a welcoming landing page with project overview,
    navigation guidance, and quick-start callouts
- Expand `docs/api.md` with usage context, examples, and explanatory prose
    around the mkdocstrings-generated content
- Create `docs/guide.md` covering installation, configuration, common workflows,
    debugging, and release procedures
- Apply Google's principles: minimum viable content, no duplication, clear
    narrative flow

**Non-Goals:**

- Restructuring or migrating existing `docs/plans/` content
- Adding automated documentation generation tooling
- Changing the mkdocstrings configuration or theme
- Modifying the README.md (already aligned in prior work)

## Decisions

- **Monolithic guide vs. multiple pages**: A single `docs/guide.md` is
    preferable to fragmenting into several small pages. The project is small
    enough that one well-structured guide reduces navigation overhead and keeps
    content easier to maintain (Principle: Minimum Viable Documentation).
- **Examples inline vs. separate file**: Inline examples in `docs/api.md`
    directly alongside the `:::` block keep context close to the API reference.
    No separate examples file is needed (Principle: Documentation is the Story
    of Your Code).
- **Landing page as entry point**: `docs/index.md` should mirror the README
    structure at a high level but focus on documentation navigation rather than
    repeating install/config verbatim (Principle: Duplication is Evil).

## Risks / Trade-offs

- **Staleness risk**: Guide content may drift from the README over time.
    Mitigation: the guide and README should cross-reference each other, and both
    should be updated together when CLI usage or configuration changes
    (Principle: Update Docs with Code).
- **Over-documenting**: A small project risks writing too much too early.
    Mitigation: start with lean content and expand only when contributors
    identify gaps (Principle: Prefer the Good Over the Perfect).
