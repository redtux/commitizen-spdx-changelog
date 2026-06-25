<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
SPDX-FileContributor: https://redtux.github.io/commitizen-spdx-changelog/credits/

SPDX-License-Identifier: Apache-2.0
-->

## MODIFIED Requirements

### Requirement: Doc-generation plan is a prioritized backlog

The file `docs/plans/09-doc-generation.md` SHALL list all doc-generation tasks
in priority order with dependencies noted.

#### Scenario: Plan has pending status

- **WHEN** the file is parsed
- **THEN** `status:` SHALL be `pending`

#### Scenario: Tasks are ordered and dependency-aware

- **WHEN** the file is read
- **THEN** `## Tasks` SHALL contain `- [ ]` checklist items for: enrich
    docstrings, install mkdocstrings-python, configure in zensical.toml, add
    `:::` directives, integrate with CI, and verify end-to-end with
    `make docs-build`
- **THEN** tasks that have prerequisites (e.g., configuration before directives)
    SHALL note the dependency inline
