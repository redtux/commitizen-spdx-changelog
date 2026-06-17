<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>

SPDX-License-Identifier: Apache-2.0
-->

## ADDED Requirements

### Requirement: pyproject.toml plan is a completed reference

The file `docs/plans/04-pyproject.md` SHALL present the `pyproject.toml`
configuration as a completed reference document.

#### Scenario: Plan has done status

- **WHEN** the file is parsed
- **THEN** `status:` SHALL be `done`

#### Scenario: Key decisions are documented

- **WHEN** the file is read
- **THEN** notable divergence decisions (e.g., `requires-python >=3.13`,
    `tag_format`, pinned `commitizen`) SHALL be listed in a decisions section
