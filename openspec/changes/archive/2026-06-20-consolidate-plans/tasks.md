<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
SPDX-FileContributor: https://redtux.github.io/commitizen-spdx-changelog/credits/

SPDX-License-Identifier: Apache-2.0
-->

## 1. Update fully completed plans (status: done)

- [x] 1.1 Update `docs/plans/02-scaffolding.md` — add SPDX header,
    `description:`, `status: done`, `## Tasks` with `- [x]` items, and
    `## See also` cross-links
- [x] 1.2 Update `docs/plans/03-design.md` — add SPDX header, `description:`,
    `status: done`, `## Tasks` with `- [x]` items, cross-links, and inline
    key-architecture summary
- [x] 1.3 Update `docs/plans/04-pyproject.md` — add SPDX header, `description:`,
    `status: done`, key-decisions log, and `## Tasks` with `- [x]` items
- [x] 1.4 Update `docs/plans/06-ci-cd.md` — add SPDX header, `description:`,
    `status: done`, `## Tasks` with completed `- [x]` items plus one `- [ ]` for
    PyPI trusted-publisher setup (marked external)

## 2. Update partially completed plans (status: partial)

- [x] 2.1 Update `docs/plans/01-problem-and-goal.md` — add SPDX header,
    `description:`, `status: partial`, reformat pending tasks under
    `## Tasks > ### Remaining` with `- [ ]` checkboxes, move done items under
    `### Completed`
- [x] 2.2 Update `docs/plans/05-tests.md` — add SPDX header, `description:`,
    `status: partial`, integrate fixture-difference notes, split `## Tasks` into
    `### Completed` and `### Remaining`
- [x] 2.3 Update `docs/plans/07-reuse-and-smoke-test.md` — add SPDX header,
    `description:`, `status: partial`, list remaining verification tasks with
    exact commands under `## Tasks > ### Remaining`

## 3. Update pending plans (status: pending)

- [x] 3.1 Update `docs/plans/08-release.md` — add SPDX header, `description:`,
    `status: pending`, reformat as actionable `## Tasks` checklist
- [x] 3.2 Update `docs/plans/09-doc-generation.md` — add SPDX header,
    `description:`, `status: pending`, order tasks by dependency with priority
    notes

## 4. Finalize index and lint

- [x] 4.1 Update `docs/plans/index.md` — add status column, ensure all 9 plans
    are linked and descriptions match updated plan metadata
- [x] 4.2 Run `uv run mdformat openspec/changes/consolidate-plans/` to format
    all new artifacts
- [x] 4.3 Run `uv run mdformat docs/plans/` to format all updated plan files
