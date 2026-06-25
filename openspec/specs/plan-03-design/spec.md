<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
SPDX-FileContributor: https://redtux.github.io/commitizen-spdx-changelog/credits/

SPDX-License-Identifier: Apache-2.0
-->

# plan-03-design Specification

## Purpose

Define the design plan as a completed architecture reference with cross-links to
other plans, documenting the lazy import pattern and SPDXMarkdown wrapper
approach.

## Requirements

### Requirement: Design plan is marked complete with reference links

The file `docs/plans/03-design.md` SHALL be formatted as a completed
architecture reference.

#### Scenario: Plan has done status

- **WHEN** the file is parsed
- **THEN** `status:` SHALL be `done`

#### Scenario: Cross-references to other plans

- **WHEN** the file references other plans (e.g., problem-and-goal, scaffolding)
- **THEN** those references use `[label]` reference-style links with definitions
    at file bottom
