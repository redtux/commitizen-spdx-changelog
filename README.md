<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>

SPDX-License-Identifier: Apache-2.0
-->

# commitizen-spdx-changelog

A [commitizen] changelog format plugin with YAML frontmatter awareness, designed
for REUSE/SPDX-compliant changelogs.

## Overview

Commitizen's built-in `Markdown` changelog format treats `#` lines inside YAML
frontmatter as markdown headings, causing false version detection (e.g. `2.0`
from `Apache-2.0`). This plugin extends the `Markdown` format to strip
`---`-delimited frontmatter before parsing and corrects line indices so new
version entries are inserted at the right position.

## Status

This project is in early development. See the numbered implementation plans
under [`docs/plans/`](docs/plans/index.md) for the current roadmap:

| Plan                                                               | Description                                |
| ------------------------------------------------------------------ | ------------------------------------------ |
| [01 — Problem and Goal](docs/plans/01-problem-and-goal.md)         | Confirm the bug, align on approach         |
| [02 — Scaffolding](docs/plans/02-scaffolding.md)                   | Manual scaffold with uv init + src/ layout |
| [03 — Design](docs/plans/03-design.md)                             | Implement `SPDXMarkdown` class             |
| [04 — pyproject.toml](docs/plans/04-pyproject-toml.md)             | Configure entry points and metadata        |
| [05 — Tests](docs/plans/05-tests.md)                               | Unit and integration tests                 |
| [06 — CI/CD](docs/plans/06-ci-cd.md)                               | GitHub Actions workflows                   |
| [07 — REUSE and Smoke Test](docs/plans/07-reuse-and-smoke-test.md) | REUSE compliance, local verification       |
| [08 — Release](docs/plans/08-release.md)                           | Release process to PyPI                    |
| [09 — Doc Generation](docs/plans/09-doc-generation.md)             | Automated docs from docstrings/argparse    |

## Installation (once published)

```sh
uv add commitizen-spdx-changelog
# or: pip install commitizen-spdx-changelog
```

## Configuration

In `pyproject.toml`:

```toml
[tool.commitizen]
changelog_format = "spdx-markdown"
```

## Usage

```sh
cz bump --changelog
```

The plugin handles changelogs with SPDX frontmatter like:

```markdown
---
# SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
#
# SPDX-License-Identifier: Apache-2.0

icon: lucide/git-commit-vertical
---

# Changelog

## 0.4.0 (2026-06-08)
...
```

## Development

```sh
uv sync --group dev
```

## License

Apache-2.0 — see [LICENSE.md](LICENSE.md).

[commitizen]: https://commitizen-tools.github.io/commitizen/
