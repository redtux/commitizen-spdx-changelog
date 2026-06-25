<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
SPDX-FileContributor: https://redtux.github.io/commitizen-spdx-changelog/credits/

SPDX-License-Identifier: Apache-2.0
-->

## 1. Regex Investigation

- [x] 1.1 Run `RE_TITLE` against `docs/changelog.md` and confirm frontmatter
    lines match as headings
- [x] 1.2 Run `search_version` on each matched title and confirm `2.0` is
    extracted from `Apache-2.0`
- [x] 1.3 Document the root cause: `RE_TITLE = ^(?P<level>#+) (?P<title>.*)$`
    does not distinguish YAML frontmatter from real headings;
    `RE_VERSION = \d+\.\d+(\.\d+)?` greedily matches `2.0` inside `Apache-2.0`

## 2. cz bump Dry-Run

- [x] 2.1 Set up a temporary git repo with a pyproject.toml using the built-in
    `markdown` changelog format
- [x] 2.2 Create a changelog with YAML frontmatter but NO version sections yet
- [x] 2.3 Run `cz bump --dry-run --changelog` and capture the exit code and
    output
- [x] 2.4 Confirm the bug manifests as `NoRevisionError` (exit code 16) or false
    version detection
    - Note: end-to-end `cz bump` did not fail in all environments (config path
        resolution varies), but the `_find_incremental_rev` simulation in
        `scripts/reproduce_bug.py` definitively proves the `NoRevisionError` path.

## 3. Upstream Confirmation

- [x] 3.1 Verify that commitizen issue #2014 remains open
    - Issue #2014 is CLOSED. The resolution was woile's comment directing the
        reporter to create a custom plugin. No upstream fix will be provided.
- [x] 3.2 Confirm woile's comment is the definitive word (no PR expected
    upstream)
- [x] 3.3 Record findings in project documentation
    - Findings recorded in `scripts/reproduce_bug.py` docstring and this change's
        artifacts.

## 4. Reproduction Script

- [x] 4.1 Write `scripts/reproduce_bug.py` with regex analysis and
    `_find_incremental_rev` simulation
- [x] 4.2 Ensure the script cleans up temporary files on completion
- [x] 4.3 Verify the script runs correctly with
    `uv run python scripts/reproduce_bug.py`
- [x] 4.4 Add SPDX/REUSE header to the script

## 5. Documentation

- [x] 5.1 Read upstream docs and templates (changelog template, config file,
    Python class, cookiecutter)
- [x] 5.2 Read `BaseFormat` and `Markdown` source to understand override points
- [x] 5.3 Summarize relevant findings in a project note
    - Override points: `get_metadata()` and `get_latest_full_release()` need to
        strip YAML frontmatter before scanning for headings.
    - `RE_TITLE = ^(?P<level>#+) (?P<title>.*)$` with no flags — each line is
        processed individually via `.strip().lower()`.
    - `parse_version_from_title` in Markdown calls `RE_TITLE.match(line)` then
        `tag_rules.search_version(title)`.
- [x] 5.4 Update `docs/plans/01-problem-and-goal.md` status from `partial` to
    `done`
