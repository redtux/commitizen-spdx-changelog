<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>

SPDX-License-Identifier: Apache-2.0
-->

## Why

The `docs/plans/` directory contains 9 numbered implementation plans created
during the initial project scaffolding, but they vary widely in quality,
completeness, and structure. Plans 02–06 are largely implemented; Plan 07 is
partially done; Plans 01, 08, and 09 still have pending items. The files lack
consistent frontmatter, titles, task-tracking conventions, and cross-references.
Before we can implement each plan as an independent OpenSpec change, they must
be consolidated into a uniform, self-contained format where each (except the
index) can be actioned independently.

## What Changes

- Rewrite every plan file (`01-*.md` through `09-*.md`) to a consistent
    template: SPDX header, one-line `description:`, `status:`
    (done/partial/pending), `tasks:` block with `- [ ]` tracking, and
    cross-links to other plans
- Update `docs/plans/index.md` to reflect current statuses and add reference
    links
- Mark plans as implementation-ready for independent OpenSpec changes
- Remove any stale or superseded content from individual plans

## Capabilities

### New Capabilities

- `plan-index`: Consolidated index linking all plans with current status badges
- `plan-01-problem-goal`: Updated root-cause analysis and upstream-position
    sign-off, formatted as standalone plan
- `plan-02-scaffolding`: Scaffolding plan trimmed to "completed, reference only"
    with implementation summary
- `plan-03-design`: Architecture reference plan with implementation-complete
    marker and cross-links
- `plan-04-pyproject-toml`: Configuration reference plan with completed tasks
    and key-decision log
- `plan-05-tests`: Test plan with optional `__init__.py` task clarified and
    fixture notes integrated
- `plan-06-ci-cd`: CI/CD plan with pending PyPI-publish task clearly scoped to
    first release
- `plan-07-reuse-smoke`: REUSE and smoke-test plan with remaining tasks
    enumerated and linked to CI/CD
- `plan-08-release`: Release plan formatted as actionable implementation
    checklist
- `plan-09-doc-generation`: Doc-generation plan made self-contained with all 7
    tasks listed and prioitized

### Modified Capabilities

*None — no existing specs to modify.*

## Impact

- `docs/plans/*.md` — all 10 files rewritten
- No source code, tests, or configuration files are affected
- Downstream: none — these are internal planning documents only
