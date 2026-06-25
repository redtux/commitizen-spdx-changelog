<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
SPDX-FileContributor: https://redtux.github.io/commitizen-spdx-changelog/credits/

SPDX-License-Identifier: Apache-2.0
-->

## ADDED Requirements

### Requirement: Test plan separates done from pending

The file `docs/plans/05-tests.md` SHALL clearly separate completed work from the
single remaining optional task.

#### Scenario: Plan has partial status

- **WHEN** the file is parsed
- **THEN** `status:` SHALL be `partial`

#### Scenario: Completed and remaining sections exist

- **WHEN** the file is read
- **THEN** `## Tasks` contains `### Completed` with `- [x]` items and
    `### Remaining` with `- [ ]` items
