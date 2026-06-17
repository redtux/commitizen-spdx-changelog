<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>

SPDX-License-Identifier: Apache-2.0
-->

# plan-07-reuse-smoke Specification

## Purpose

Define the REUSE and smoke-test plan enumerating remaining verification tasks as
actionable checklists with exact commands for REUSE lint, editable install,
entry-point check, and dry-run bump.

## Requirements

### Requirement: REUSE and smoke-test plan enumerates remaining tasks

The file `docs/plans/07-reuse-and-smoke-test.md` SHALL list all remaining
verification tasks as actionable checklists.

#### Scenario: Plan has partial status

- **WHEN** the file is parsed
- **THEN** `status:` SHALL be `partial`

#### Scenario: Remaining tasks are actionable

- **WHEN** the file is read
- **THEN** `## Tasks` SHALL contain `- [ ]` checklist items for: REUSE lint
    verification, editable install, entry-point registration check, and dry-run
    bump test
- **THEN** each task SHALL include the exact command to run
