---
# SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
# SPDX-FileContributor: https://redtux.github.io/commitizen-spdx-changelog/credits/
#
# SPDX-License-Identifier: Apache-2.0

description: Complete pyproject.toml with build config, entry points, and tool settings
icon: lucide/file-cog
status: done
title: Plan 04 — pyproject.toml
---

The project uses `uv`/`uv_build`. The `pyproject.toml` registers the
`commitizen.changelog_format` entry point and fills in the project metadata.

## Current `pyproject.toml` (as implemented)

```toml
# SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
#
# SPDX-License-Identifier: Apache-2.0

# pyproject.toml
#
# This file is part of commitizen-spdx-changelog, a plugin
# for commitizen that generates changelogs in SPDX format.

[build-system]
build-backend = "uv_build"
requires = ["uv_build>=0.11.21,<0.12.0"]

[project]
authors = [
  { name = "Pablo Hörtner", email = "redtux@pm.me" },
]
dependencies = [
  "commitizen>=4.16.3",
]
description = "Commitizen changelog format plugin with YAML frontmatter awareness for REUSE/SPDX-compliant changelogs"
keywords = ["commitizen", "changelog", "spdx", "reuse", "yaml", "frontmatter"]
license = "Apache-2.0"
classifiers = [
  "Development Status :: 3 - Alpha",
  "Intended Audience :: Developers",
  "Programming Language :: Python :: 3",
  "Programming Language :: Python :: 3.13",
  "Programming Language :: Python :: 3.14",
]
name = "commitizen-spdx-changelog"
readme = "README.md"
requires-python = ">=3.13"
version = "0.0.1"

[project.urls]
Homepage = "https://github.com/redtux/commitizen-spdx-changelog"
Issues = "https://github.com/redtux/commitizen-spdx-changelog/issues"
Source = "https://github.com/redtux/commitizen-spdx-changelog"

[project.entry-points."commitizen.changelog_format"]
spdx-markdown = "commitizen_spdx_changelog.formatters.spdx_markdown:SPDXMarkdown"

[dependency-groups]
dev = [
  "basedpyright>=1.39.8",
  "mdformat-gfm-alerts>=2.0.0",
  "mdformat-mkdocs[recommended]>=5.1.4",
  "mdformat-pyproject>=0.1.1",
  "pytest>=9.1.1",
  "rich>=15.0.0",
  "ruff>=0.15.18",
  "ty>=0.0.51",
  "uv>=0.11.22",
  "zensical>=0.0.45",
]

[tool.commitizen]
changelog_file = "docs/changelog.md"
changelog_format = "spdx-markdown"
changelog_incremental = true
major_version_zero = true
name = "cz_conventional_commits"
post_bump_hooks = ["uv lock", "git push --follow-tags"]
tag_format = "v$version"
update_changelog_on_bump = true
version = "0.0.1"
version_files = [
  "pyproject.toml:version",
]
version_scheme = "semver2"

[tool.pyright]
venvPath = "."
venv = ".venv"

[tool.mdformat]
exclude = [
  "**/*.env",
  "**/*.json",
  "**/*.jsonc",
  "**/*.lock",
  "**/*.sh",
  "**/*.toml",
  "**/*.yaml",
  "**/*.yml",
  "**/.venv/**",
  "**/LICENSE.md",
  "**/LICENSES/**",
  "**/Makefile",
  "**/node_modules/**",
  "**/out/**",
  "**/tmp/**",
]
number = true
wrap = 80
```

## Key decisions (updates from plan)

- **`requires-python`**: `>=3.14` → `>=3.13` (to match CI matrix)
- **`tag_format`**: `"$version"` → `"v$version"` (with `v` prefix)
- **`dependencies`**: `"commitizen>=3.0"` → `"commitizen>=4.16.3"` (pinned to
    tested version)
- **`license`**: via classifier → via PEP 639 `license = "Apache-2.0"`
- **Dev deps**: `commitizen` moved to runtime dep; dev has `basedpyright`,
    `ruff`, `rich`, `zensical`, etc.
- **`[tool.pyright]`**: Not mentioned → present for IDE type-checking
- **`changelog_format`**: Not set → `"spdx-markdown"` (dogfooding)

## Tasks

- [x] **Create `pyproject.toml`** from scratch (no cookiecutter).
- [x] **Set `[project]` metadata.** Description, keywords, classifiers, license,
    `[project.urls]`.
- [x] **Add runtime dependency.** `"commitizen>=4.16.3"` in
    `[project] dependencies`.
- [x] **Register the entry point.** Under `commitizen.changelog_format`.
- [x] **Set `changelog_format = "spdx-markdown"`** for dogfooding.
- [x] **Verify.** `uv sync` completes. Entry point visible via
    `importlib.metadata.entry_points(group='commitizen.changelog_format')`.

## Dependencies

- **Plan 03 must be complete** — `SPDXMarkdown` class exists and is importable.
- `uv` installed (the project uses `uv` for package management).

## Acceptance

- [x] `pyproject.toml` has the correct description, keywords, classifiers.
- [x] `commitizen>=4.16.3` listed as a runtime dependency.
- [x] Entry point registered under `commitizen.changelog_format`.
- [x] `uv sync` completes without errors.
- [x] Entry point is visible via `importlib.metadata.entry_points`.

## Next

→ Continue to [Plan 05 — Tests](05-tests.md)

## See also

- [Plan 02 — Scaffolding](02-scaffolding.md)
- [Plan 03 — Design](03-design.md)
