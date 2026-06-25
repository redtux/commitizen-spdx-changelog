<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
SPDX-FileContributor: https://redtux.github.io/commitizen-spdx-changelog/credits/

SPDX-License-Identifier: Apache-2.0
-->

## Why

The project's `docs/` directory currently has minimal content — a sparse landing
page, a bare API reference, and a standard changelog. Following Google's
Documentation Best Practices will make the project more welcoming and accessible
for potential contributors, especially first-time users.

## What Changes

- **docs/index.md** — rewrite from sparse placeholder into a proper landing page
    with a project overview, navigation guidance, and links to key resources
- **docs/api.md** — add usage context, examples, and explanatory prose around
    the existing mkdocstrings block
- **docs/guide.md** — create a new usage guide covering installation,
    configuration, common workflows, debugging, and release procedures
- **docs/changelog.md** — minor polish to align with best practices
- **docs/contributing.md** — already strong; ensure it references Google's best
    practices as a standard (covered by prior commits)

## Capabilities

### New Capabilities

- `docs-landing`: Improved docs landing page with project overview, navigation
    structure, and links to all documentation resources
- `docs-api-enhancement`: Enhanced API reference with usage examples and
    contextual documentation alongside the mkdocstrings-generated content
- `docs-guide`: Comprehensive usage guide covering setup, configuration,
    workflows, debugging, and release procedures

### Modified Capabilities

<!-- No existing spec-level behavior is changing — only documentation content
     is being added or improved. -->

## Impact

- **docs/**: Three files modified (index.md, api.md, changelog.md), one created
    (guide.md)
- **docs/plans/**: Unchanged
- **README.md**: Unchanged (already aligned in prior work)
- No code, dependencies, or API changes
