<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>

SPDX-License-Identifier: Apache-2.0
-->

## ADDED Requirements

### Requirement: CI/CD plan scopes external dependency clearly

The file `docs/plans/06-ci-cd.md` SHALL mark implementation as done while
clearly scoping the PyPI trusted-publisher setup as an external post-release
task.

#### Scenario: Plan has done status for internal implementation

- **WHEN** the file is parsed
- **THEN** `status:` SHALL be `done`

#### Scenario: PyPI setup is documented as external

- **WHEN** the file is read
- **THEN** the PyPI trusted-publisher requirement SHALL appear under `## Tasks`
    as `- [ ]` with a note that it is an external setup step requiring PyPI
    account access
