<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>

SPDX-License-Identifier: Apache-2.0
-->

# plan-05-tests Specification

## Purpose

Define the test plan as a partially completed document separating done items
from the single remaining optional task, documenting fixture differences and
pytest configuration.

## Requirements

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
