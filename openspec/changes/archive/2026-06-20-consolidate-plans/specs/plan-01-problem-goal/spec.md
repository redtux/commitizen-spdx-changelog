<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>

SPDX-License-Identifier: Apache-2.0
-->

## ADDED Requirements

### Requirement: Problem and goal plan is self-contained

The file `docs/plans/01-problem-and-goal.md` SHALL present the root-cause
analysis of the upstream commitizen bug as a standalone implementation plan.

#### Scenario: Plan has SPDX header

- **WHEN** the file is opened
- **THEN** it SHALL start with an SPDX-FileCopyrightText and
    SPDX-License-Identifier header

#### Scenario: Plan has description and status

- **WHEN** the file is parsed
- **THEN** it SHALL contain a `description:` line summarizing the plan
- **THEN** it SHALL contain a `status:` line (one of `done`, `partial`,
    `pending`)

#### Scenario: Pending tasks are checklisted

- **WHEN** the plan contains actionable items
- **THEN** they SHALL appear as `- [ ]` checklist items under a `## Tasks`
    heading
