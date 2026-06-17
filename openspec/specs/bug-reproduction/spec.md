<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>

SPDX-License-Identifier: Apache-2.0
-->

# bug-reproduction Specification

## Purpose

Define the requirements for reproducing the YAML frontmatter bug in commitizen's
built-in `Markdown` changelog format, used by `scripts/reproduce_bug.py`.

## Requirements

### Requirement: Bug reproduction script

The system SHALL provide a script at `scripts/reproduce_bug.py` that reproduces
the YAML frontmatter bug in commitizen's built-in `Markdown` changelog format,
using two independent methods to confirm the issue.

#### Scenario: Regex analysis detects false version

<!-- REUSE-IgnoreStart -->

- **WHEN** the reproduction script analyzes a changelog with YAML frontmatter
    containing `# SPDX-License-Identifier: Apache-2.0`

<!-- REUSE-IgnoreEnd -->

- **THEN** the script SHALL demonstrate that `RE_TITLE` matches the frontmatter
    line as a heading
- **THEN** the script SHALL demonstrate that `search_version` extracts `2.0`
    from `Apache-2.0`
- **THEN** the script SHALL output `>>> BUG CONFIRMED` to indicate the
    regex-level reproduction succeeded

#### Scenario: cz bump dry-run fails with frontmatter-only changelog

- **WHEN** the reproduction script runs `cz bump --dry-run --changelog` against
    a git repo with a changelog containing only YAML frontmatter (no version
    section yet) and a new commit
- **THEN** the command SHALL either fail with a non-zero exit code or produce a
    false version in its output
- **THEN** the script SHALL output `>>> BUG CONFIRMED` indicating the end-to-end
    reproduction succeeded
