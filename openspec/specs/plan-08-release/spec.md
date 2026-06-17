<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>

SPDX-License-Identifier: Apache-2.0
-->

# plan-08-release Specification

## Purpose

Define the release plan as a step-by-step checklist for publishing the package
to PyPI via GitHub Actions: create the publish workflow, configure Trusted
Publisher, bump the version, push the tag, and verify the release.

## Requirements

### Requirement: Release plan is a publish-pending checklist

The file `docs/plans/08-release.md` SHALL present the release process as a
step-by-step implementation checklist.

#### Scenario: Plan has pending status

- **WHEN** the file is parsed
- **THEN** `status:` SHALL be `pending`

#### Scenario: All steps are checklisted

- **WHEN** the file is read
- **THEN** `## Tasks` SHALL contain checklist items for: create publish
    workflow, configure PyPI Trusted Publisher, dry-run bump, bump and release,
    push tag, and verify release
