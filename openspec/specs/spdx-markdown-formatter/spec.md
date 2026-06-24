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

The `SPDXMarkdown` class SHALL directly inherit from
`commitizen.changelog_formats.markdown.Markdown` with no wrapper indirection.
The `isinstance` fix is achieved via real inheritance, not `abc.ABC.register()`.

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
imported at module top-level in standard order. The staggered import pattern and
`noqa: E402` suppressions from the previous wrapper architecture are removed.
Only `BaseConfig` remains lazy inside `__init__`.

#### Scenario: Module loads cleanly

- **WHEN** Python imports `commitizen_spdx_changelog.formatters.spdx_markdown`
- **THEN** the entry point SHALL load without circular import errors

#### Scenario: Cold import with warm-up succeeds

- **WHEN** Python imports `commitizen.changelog_formats` first, then imports
    `commitizen_spdx_changelog.formatters.spdx_markdown`
- **THEN** the module SHALL load without `AttributeError`

### Requirement: Entry point registration

The `pyproject.toml` entry point SHALL remain
`spdx-markdown = "commitizen_spdx_changelog.formatters.spdx_markdown:SPDXMarkdown"`.

#### Scenario: Entry point loads without circular import

- **WHEN** commitizen scans `commitizen.changelog_format` entry points
- **THEN** the `spdx-markdown` entry point SHALL load without errors
