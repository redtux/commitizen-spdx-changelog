<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>

SPDX-License-Identifier: Apache-2.0
-->

## Context

The `docs/plans/` directory contains 9 implementation plans from the initial
project scaffolding. They were written at different times, to different
standards, and many contain completed tasks alongside pending ones without clear
separation. The AGENTS.md references them, and the OpenSpec workflow expects
each plan to be a self-contained, independently implementable unit. Currently no
plan can be cleanly mapped to an OpenSpec change without manual interpretation.

## Goals / Non-Goals

**Goals:**

- All 9 plan files follow a consistent template with SPDX header,
    `description:`, `status:`, and `tasks:` sections
- Each plan is self-contained: a reader can understand, evaluate, and implement
    it without cross-referencing other plans for basic context
- The index (`docs/plans/index.md`) reflects current status and acts as a
    reliable navigation hub
- Completed plans are marked `done` with implementation-summary sections;
    partial plans clearly distinguish done vs. pending tasks
- Pending tasks use consistent `- [ ]` checklist format for direct OpenSpec task
    import

**Non-Goals:**

- Not implementing any plan's pending tasks — this change is purely
    structural/editorial
- Not changing the plan numbering or topic scope — only the presentation format
- Not introducing new plans or merging existing ones

## Decisions

1. **Template-driven rewrite** — Each plan file gets the same skeleton:

    - SPDX header (matching project convention)
    - `description:` (one-line summary)
    - `status:` (`done` | `partial` | `pending`)
    - Body (existing content, reformatted/consolidated as needed)
    - `## Tasks` section with `- [ ]` checklist for non-done items; `- [x]` for
        accomplished items
    - `## See also` reference-links to related plans
    - Reasoning: uniform structure enables automated processing and reduces
        cognitive load.

2. **Inline completion markers** — For plans with a mix of done/pending tasks
    (e.g., Plan 05, 07), group completed items under a `### Completed`
    subsection and pending items under `### Remaining` within `## Tasks`.
    Reasoning: makes it obvious what work remains without parsing crossed-out
    lines.

3. **status field** — Three-tier:

    - `done`: all tasks complete (Plans 02–04, 06 where PyPI setup is external)
    - `partial`: some tasks remain (Plans 05, 07)
    - `pending`: no work started (Plan 09; Plan 08 is pending publishing)
    - Reasoning: avoids ambiguity of half-implemented plans during future change
        planning.

4. **Reference links over raw URLs** — Standardize all cross-plan references to
    `[label]` reference-style links with definitions at file bottom. Reasoning:
    consistent with project's mdformat conventions.

## Risks / Trade-offs

- [Repetitive format for dense plans] → Plans 02–04 (mostly reference docs) may
    feel padded; mitigate by keeping their body sections concise and allowing
    `## Tasks` to be brief
- [Status changes over time] → Index will drift if plans are later implemented;
    mitigate by making status easy to update (single field) and noting in
    AGENTS.md that plan status should be refreshed after each implementation
    change
