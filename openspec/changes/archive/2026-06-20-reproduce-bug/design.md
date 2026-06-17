<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>

SPDX-License-Identifier: Apache-2.0
-->

## Context

Commitizen's built-in `Markdown` changelog format (from
`commitizen.changelog_formats.markdown`) uses
`RE_TITLE = ^(?P<level>#+) (?P<title>.*)$` with `re.MULTILINE` to find version
headings. YAML frontmatter lines starting with `#` (e.g.,

<!-- REUSE-IgnoreStart -->

`# SPDX-License-Identifier: Apache-2.0`)

<!-- REUSE-IgnoreEnd --> match this regex. The `search_version`

method then extracts `2.0` from `Apache-2.0` via
`RE_VERSION = \d+\.\d+(\.\d+)?`, producing a false version candidate.

The upstream project (commitizen-tools/commitizen) has confirmed via issue #2014
that a hardcoded frontmatter fix is not wanted — the recommended path is a
custom plugin.

The current project (`commitizen-spdx-changelog`) already has a scaffolding of
the plugin (entry point, stub class), but the bug has never been formally
reproduced and documented in the project's own records.

## Goals / Non-Goals

**Goals:**

- Reproduce the false version detection using the actual commitizen library
- Capture the exact error (`NoRevisionError` exit code 16 or false version
    output)
- Document the root cause with line-level regex analysis
- Provide a shareable reproduction script so any contributor can confirm
    independently
- Update `docs/plans/01-problem-and-goal.md` status from `partial` to `done`
- Verify no upstream fix is expected (issue #2014 remains open)

**Non-Goals:**

- Implementing the plugin fix (scope of Plan 02 onward)
- Modifying the upstream commitizen library
- Making the reproduction script part of CI (just a developer tool)

## Decisions

- **Approach: Python script in `scripts/`** rather than a pytest test, because
    reproduction requires a temporary git repo with tags, which is awkward in
    pytest. A standalone script is simpler and can be run by anyone with
    `uv run python scripts/reproduce_bug.py`.
- **Repo-local temp files in `tmp/`** to avoid leaking into tracked directories.
- **Regex-level reproduction as step 1**, `cz bump` dry-run as step 2:
    demonstrate the root cause before showing the symptom.

## Risks / Trade-offs

- [R] The reproduction script creates a temporary git repo in `tmp/repro/` — if
    execution is killed, leftover files may remain. Mitigation: `shutil.rmtree`
    in `finally` block.
- [R] The script depends on `commitizen>=4.16.3` (already in project
    dependencies). Mitigation: runs via `uv run python ...` which uses the venv.
