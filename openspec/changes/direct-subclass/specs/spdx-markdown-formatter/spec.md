<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>

SPDX-License-Identifier: Apache-2.0
-->

# spdx-markdown-formatter Specification (delta)

This delta spec modifies the existing `spdx-markdown-formatter` capability to
reflect the refactor from ABC wrapper + virtual subclass to direct inheritance.

## MODIFIED Requirements

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
