<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
SPDX-FileContributor: https://redtux.github.io/commitizen-spdx-changelog/credits/

SPDX-License-Identifier: Apache-2.0
-->

## ADDED Requirements

### Requirement: Consolidated plan index

The system SHALL maintain a `docs/plans/index.md` file that serves as the
navigation hub for all implementation plans.

#### Scenario: Index lists all plans

- **WHEN** a user opens `docs/plans/index.md`
- **THEN** all 9 plan files (`01-*.md` through `09-*.md`) are listed with their
    titles and descriptions
- **THEN** each plan entry links to its file via a reference-style link
- **THEN** the index includes a `status:` column showing `done`, `partial`, or
    `pending`

#### Scenario: Status column reflects plan metadata

- **WHEN** a plan's `status:` field is updated
- **THEN** the index status column MUST match that value
