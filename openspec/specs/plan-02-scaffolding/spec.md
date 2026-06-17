<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>

SPDX-License-Identifier: Apache-2.0
-->

# plan-02-scaffolding Specification

## Purpose

Define the scaffolding plan as a completed reference plan documenting key
decisions (cookiecutter rejection, `uv init` + `src/` layout) with done status
and no remaining tasks.

## Requirements

### Requirement: Scaffolding plan is marked complete

The file `docs/plans/02-scaffolding.md` SHALL be formatted as a completed
reference plan with no remaining tasks.

#### Scenario: Plan has done status

- **WHEN** the file is parsed
- **THEN** `status:` SHALL be `done`

#### Scenario: Implementation summary present

- **WHEN** the file is read
- **THEN** it SHALL include a summary of key decisions made during scaffolding
    (e.g., cookiecutter rejection, `uv init` + `src/` layout)
