<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>

SPDX-License-Identifier: Apache-2.0
-->

## ADDED Requirements

### Requirement: Guide covers installation and setup

The usage guide SHALL include installation instructions using both `uv` and
`pip`, and configuration steps for `pyproject.toml`.

#### Scenario: User follows installation steps

- **WHEN** a user reads the installation section
- **THEN** they see copyable commands for `uv add` and `pip install`
- **THEN** they see the `pyproject.toml` configuration block

### Requirement: Guide covers common workflows

The usage guide SHALL explain common workflows: generating a changelog, bumping
a version, and verifying the output.

#### Scenario: User follows a workflow

- **WHEN** a user reads the workflows section
- **THEN** they see step-by-step instructions for `cz bump --changelog`
- **THEN** they see how to inspect the generated changelog

### Requirement: Guide covers debugging

The usage guide SHALL include a debugging section that explains how to identify
and resolve common issues, such as incorrect frontmatter formatting or version
detection problems.

#### Scenario: User debugs an issue

- **WHEN** a user encounters a changelog parsing issue
- **THEN** the debugging section helps them identify common problems
- **THEN** they see how to run the reproduction script

### Requirement: Guide covers release procedures

The usage guide SHALL document the release process, including how the CI/CD
pipeline publishes to PyPI and how the changelog section is extracted.

#### Scenario: Maintainer prepares a release

- **WHEN** a maintainer reads the release section
- **THEN** they see how to tag a release with `git tag v*`
- **THEN** they understand that the CI pipeline handles PyPI publishing
- **THEN** they understand how changelog sections are extracted for release
    notes
