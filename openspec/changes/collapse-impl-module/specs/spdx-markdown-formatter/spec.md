<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>

SPDX-License-Identifier: Apache-2.0
-->

# spdx-markdown-formatter Specification

## Purpose

Define the behavior contract for the SPDXMarkdown changelog format plugin.

## Requirements

### Requirement: SPDXMarkdown subclasses Markdown directly

The `SPDXMarkdown` class SHALL inherit from
`commitizen.changelog_formats.markdown.Markdown` directly. There SHALL be no
wrapper class, no `__new__` redirection, and no `_resolve()` lazy-loading
machinery.

#### Scenario: isinstance check passes

- **WHEN** a caller runs `isinstance(formatter, SPDXMarkdown)` on an instance
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

### Requirement: Module imports at top level

Core commitizen types (`Metadata`, `IncrementalMergeInfo`, `Markdown`) SHALL be
imported at module level. Only `BaseConfig` may remain lazy inside `__init__`
(cosmetic — not a workaround).

#### Scenario: Module loads cleanly

- **WHEN** Python imports `commitizen_spdx_changelog.formatters.spdx_markdown`
- **THEN** no `E402` (module-level import not at top) warnings SHALL be raised
    by ruff

### Requirement: Entry point registration

The `pyproject.toml` entry point SHALL remain
`spdx-markdown = "commitizen_spdx_changelog.formatters.spdx_markdown:SPDXMarkdown"`.

#### Scenario: Entry point loads without circular import

- **WHEN** commitizen scans `commitizen.changelog_format` entry points
- **THEN** the `spdx-markdown` entry point SHALL load without errors
