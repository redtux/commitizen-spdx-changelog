<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
SPDX-FileContributor: https://redtux.github.io/commitizen-spdx-changelog/credits/

SPDX-License-Identifier: Apache-2.0
-->

# docs-landing Specification

## Purpose

Provide a welcoming project landing page with overview, navigation table, and a
reference to Google's Documentation Best Practices.

## Requirements

### Requirement: Landing page provides project overview

The docs landing page SHALL present a clear project overview within the first
paragraph, explaining what the plugin does and why it exists.

#### Scenario: Visitor reads the landing page

- **WHEN** a user navigates to the docs landing page
- **THEN** the first paragraph explains the plugin's purpose and value
- **THEN** the page links to all major documentation sections

### Requirement: Landing page includes navigation table

The docs landing page SHALL include a navigation table with links to each major
documentation page and a brief description of each.

#### Scenario: Navigation table renders correctly

- **WHEN** the docs landing page is rendered
- **THEN** a table lists each docs page with a link and description
- **THEN** the table includes Changelog, Contributing, API Reference, and Usage
    Guide entries

### Requirement: Landing page references Google best practices

The docs landing page SHALL mention that the project follows Google's
Documentation Best Practices.

#### Scenario: User sees best practices reference

- **WHEN** a user reads the docs landing page
- **THEN** they see a reference to Google's Documentation Best Practices
- **THEN** the reference includes a link to the styleguide
