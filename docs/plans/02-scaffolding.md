---
# SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
#
# SPDX-License-Identifier: Apache-2.0

description: Scaffold the project manually with uv init, set up src/ layout, verify directory structure
icon: lucide/wrench
status: done
title: Plan 02 — Scaffolding
---

## Context

The project was scaffolded manually with `uv init` using the `src/` layout from
the start, avoiding the overhead of a template-based approach. The upstream
[`commitizen_cz_template`][cookiecutter] was initially considered — it targets
**commit-style plugins** (`commitizen.plugin` entry point), not changelog format
plugins (`commitizen.changelog_format` entry point, subclassing `BaseFormat`) —
so it was **not used**.

## Tasks

### Completed

- [x] **Scaffold project manually.** Created with `uv init` using `src/` layout.
    See actual `pyproject.toml` in [Plan 04](04-pyproject.md).
- [x] **Set up `src/` package structure.** Created
    `src/commitizen_spdx_changelog/formatters/` with `__init__.py` files.
- [x] **Verify scaffold.** Directory tree matches the expected structure from
    [Plan 03](03-design.md#package-structure).

## Dependencies

- **Plan 01 must be complete** — bug confirmed, upstream path closed, plugin
    approach agreed.
- Python 3.13+ available locally (project uses 3.14 in `.python-version`).
- curl/wget available (for fetching `LICENSES/Apache-2.0.txt` in Plan 07).

## Acceptance

- [x] Project directory exists with `src/` layout
- [x] `pyproject.toml` created with uv/uv_build config
- [x] Package lives under `src/commitizen_spdx_changelog/`
- [x] Directory structure matches the expected layout

## Next

→ Continue to [Plan 03 — Design](03-design.md)

## See also

- [Plan 01 — Problem and Goal](01-problem-and-goal.md)
- [Plan 03 — Design](03-design.md)
- [Plan 04 — pyproject.toml](04-pyproject.md)

<!-- References -->

[cookiecutter]: https://github.com/commitizen-tools/commitizen_cz_template
