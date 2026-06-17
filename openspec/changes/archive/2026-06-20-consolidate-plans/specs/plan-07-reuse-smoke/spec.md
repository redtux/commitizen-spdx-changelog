<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>

SPDX-License-Identifier: Apache-2.0
-->

## ADDED Requirements

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
