<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>

SPDX-License-Identifier: Apache-2.0
-->

## Why

Commitizen's built-in `Markdown` changelog format has no YAML frontmatter
awareness, causing `RE_TITLE` to match `#` lines inside frontmatter as headings.
This makes `search_version` extract false version numbers (e.g., `2.0` from
`Apache-2.0`), which breaks `cz bump --changelog`. Before we can build a fix
(the spdx-markdown plugin), we need to confirm the bug, understand the upstream
position, and document the root cause.

## What Changes

- Reproduce the bug: run `cz bump --dry-run --changelog` against a
    frontmatter-bearing changelog and capture the failure
- Confirm upstream position: verify commitizen issue #2014 remains open and no
    upstream fix is expected
- Document root cause: explain why `RE_TITLE` matches inside frontmatter and how
    `search_version` extracts `2.0` from `Apache-2.0`
- Sign off on plugin approach: confirm that a custom
    `commitizen.changelog_format` entry point is the agreed path
- Review upstream docs and source code (BaseFormat, Markdown) for override
    points

## Capabilities

### New Capabilities

- `bug-reproduction`: Documented, reproducible proof of the YAML frontmatter /
    Markdown changelog bug, including root-cause analysis and a reproduction
    script

### Modified Capabilities

*(none — no existing spec requirements change)*

## Impact

- **Code**: No production code changes — this is purely investigative and
    documentary
- **Docs**: `docs/plans/01-problem-and-goal.md` will be updated from
    `status: partial` to `status: done`
- **Tooling**: A reproduction script `scripts/reproduce_bug.py` will be added so
    any contributor can confirm the issue
