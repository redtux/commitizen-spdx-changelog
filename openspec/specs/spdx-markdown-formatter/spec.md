<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>

SPDX-License-Identifier: Apache-2.0
-->

# spdx-markdown-formatter Specification

## Purpose

Define the behavior contract for the SPDXMarkdown changelog format plugin:

SPDX/REUSE-aware Markdown changelog format plugin for commitizen. Handles
`---`-delimited YAML frontmatter stripping with correct line-index offset
correction, enabling REUSE-compliant changelogs alongside commitizen's
incremental changelog workflow.

## Requirements

### Requirement: Single-file module with isinstance fix

The `SPDXMarkdown` wrapper and `_SPDXMarkdownImpl` implementation SHALL live in
a single file. The `__new__` pattern is necessary (commitizen loads entry points
at import time). The `isinstance` fix is achieved by having `_SPDXMarkdownImpl`
inherit from both `SPDXMarkdown` and `Markdown`.

#### Scenario: isinstance check passes

- **WHEN** a caller runs `isinstance(formatter, SPDXMarkdown)` on an instance
    created via `SPDXMarkdown(config)`
- **THEN** the result SHALL be `True`

#### Scenario: isinstance Markdown check passes

- **WHEN** a caller runs `isinstance(formatter, Markdown)` on an instance
    created via `SPDXMarkdown(config)`
- **THEN** the result SHALL be `True`

### Requirement: Frontmatter stripping preserves line indices

The `get_metadata` and `get_latest_full_release` methods SHALL strip
`---`-delimited YAML frontmatter from the changelog file before delegating to
the parent `Markdown` methods, then shift returned line indices by the number of
frontmatter lines removed.

#### Scenario: Metadata with frontmatter

- **WHEN** a changelog file contains a 7-line frontmatter block followed by
    version headings
- **THEN** `get_metadata` SHALL return correct `latest_version_position` values
    shifted by +7 from the clean-file positions

#### Scenario: No frontmatter

- **WHEN** a changelog file has no `---`-delimited frontmatter
- **THEN** `get_metadata` SHALL return indices identical to the parent
    `Markdown.get_metadata`

### Requirement: Module imports structured for circular-import avoidance

Core commitizen types (`Metadata`, `IncrementalMergeInfo`, `Markdown`) SHALL be
imported after the `SPDXMarkdown` wrapper class definition. The staggered import
order is necessary and produces E402 warnings that are suppressed with
`noqa: E402`. Only `BaseConfig` may remain lazy inside `__init__`.

#### Scenario: Module loads cleanly

- **WHEN** Python imports `commitizen_spdx_changelog.formatters.spdx_markdown`
- **THEN** the entry point SHALL load without circular import errors

### Requirement: Entry point registration

The `pyproject.toml` entry point SHALL remain
`spdx-markdown = "commitizen_spdx_changelog.formatters.spdx_markdown:SPDXMarkdown"`.

#### Scenario: Entry point loads without circular import

- **WHEN** commitizen scans `commitizen.changelog_format` entry points
- **THEN** the `spdx-markdown` entry point SHALL load without errors
