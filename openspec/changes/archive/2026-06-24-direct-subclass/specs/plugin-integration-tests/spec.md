<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>

SPDX-License-Identifier: Apache-2.0
-->

# plugin-integration-tests Specification (delta)

This delta spec adds integration tests for the `spdx-markdown-formatter`
capability. The tests verify cold-import behavior, circular-import avoidance,
and instanceof checks — concerns that span module-loading infrastructure rather
than individual method behavior.

## ADDED Requirements

### Requirement: Integration test file separate from behavioural tests

The test suite SHALL include `tests/test_plugin_integration.py` as a dedicated
file for plugin-loading and inheritance integration tests, keeping them separate
from the behavioural unit tests in `tests/test_spdx_markdown.py`.

#### Scenario: Cold import test lives in integration file

- **WHEN** pytest collects the test suite
- **THEN** `tests/test_plugin_integration.py` SHALL contain the cold-import and
    instanceof tests
- **THEN** `tests/test_spdx_markdown.py` SHALL contain only behavioural tests
    (`get_metadata`, `get_latest_full_release`, `_strip_frontmatter`)

### Requirement: Cold import with warm-up succeeds

The test suite SHALL succeed in importing `SPDXMarkdown` via a fresh subprocess
when following the warm-up pattern (`import commitizen.changelog_formats`
first), confirming that the circular-import fix at the test boundary is
complete.

#### Scenario: Cold import of SPDXMarkdown succeeds

- **WHEN** a fresh Python subprocess runs
    `import commitizen.changelog_formats; from   commitizen_spdx_changelog.formatters.spdx_markdown import SPDXMarkdown`
- **THEN** the module SHALL load without `AttributeError`

#### Scenario: Cold instantiation and isinstance succeed

- **WHEN** a fresh Python subprocess runs the warm-up import, then instantiates
    `SPDXMarkdown(config)`
- **THEN** `isinstance(formatter, SPDXMarkdown)` SHALL be `True`

### Requirement: In-process isinstance verification

The same-process test suite (warmed up by `tests/conftest.py`) SHALL verify that
`isinstance` returns `True` for both `SPDXMarkdown` and its base class
`Markdown`.

#### Scenario: isinstance SPDXMarkdown passes in-process

- **WHEN** pytest runs `test_isinstance_spdx_markdown`
- **THEN** `isinstance(formatter, SPDXMarkdown)` SHALL be `True`

#### Scenario: isinstance Markdown passes in-process

- **WHEN** pytest runs `test_isinstance_markdown_base`
- **THEN** `isinstance(formatter, Markdown)` SHALL be `True`
