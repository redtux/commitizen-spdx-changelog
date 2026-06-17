---
# SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
#
# SPDX-License-Identifier: Apache-2.0

description: How to contribute to the commitizen-spdx-changelog plugin
icon: lucide/hand-heart
title: Contributing
---

# Contributing

Hey, thanks for stopping by! Contributions of all kinds are welcome — bug
reports, feature ideas, documentation improvements, or code changes.

## Getting started

This project uses [uv] for dependency management. Python 3.13 or later is
required.

```sh
# Clone the repo
git clone https://github.com/redtux/commitizen-spdx-changelog.git
cd commitizen-spdx-changelog

# Install development dependencies
uv sync --group dev
```

## Development commands

| Action             | Command                                     |
| ------------------ | ------------------------------------------- |
| Run tests          | `uv run pytest -v`                          |
| Run single test    | `uv run python tests/test_spdx_markdown.py` |
| Build docs         | `make docs-build`                           |
| Format markdown    | `make docs-format`                          |
| Lint markdown      | `make docs-lint`                            |
| Serve docs         | `make docs-serve`                           |
| REUSE compliance   | `make reuse`                                |
| Build distribution | `uv build`                                  |

There is no standalone linter or typecheck script — `ruff` runs inside
`mdformat-ruff` (formats code fences in markdown). `pyright` configuration
exists in `pyproject.toml` but is not wired into a command.

### Reproducing the YAML frontmatter bug

This project exists because commitizen's built-in `Markdown` changelog format
has no YAML frontmatter awareness. To see the bug in action:

```sh
uv run python scripts/reproduce_bug.py
```

The script demonstrates the issue in three independent ways: regex analysis, a
`_find_incremental_rev` simulation, and a direct call to commitizen's
`Markdown.get_metadata()` API. Use `--help` for more details.

## Project structure

This is a single-package Python plugin for [commitizen]. It lives at
`src/commitizen_spdx_changelog/`.

### Circular import workaround

The entry point class (`SPDXMarkdown`) is defined before any `commitizen`
import. The real implementation in `_impl.py` is imported lazily inside
`__new__`. This lets commitizen's entry-point scanner find the class without
triggering a circular import.

Only two methods override the parent `Markdown` changelog format:
`get_metadata()` and `get_latest_full_release()`. Both strip `---`-delimited
YAML frontmatter before parsing and adjust line indices accordingly.

For a deeper dive, see the [architecture plan](plans/03-design.md).

## Code conventions

- **SPDX/REUSE header** on every file:
    `SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>`
    `SPDX-License-Identifier: Apache-2.0`
- **EditorConfig**: `indent_size=2` (`.py` and `.toml` use 4),
    `insert_final_newline=false`, `trim_trailing_whitespace=false`
- **Commit style**: conventional commits with `major_version_zero=true` (e.g.
    `feat:`, `fix:`, `docs:`, `chore:`)

## How to contribute

1. Fork the repository and create a branch.
2. Make your changes.
3. Run `uv run pytest -v` to make sure tests pass.
4. Run `make docs-format && make reuse` to format markdown and keep REUSE
    compliance.
5. Open a pull request with a clear description of what you changed and why.

If you're unsure about something, feel free to open an issue first.

## Roadmap

See the [implementation plans](plans/index.md) for the current status and
direction of the project.

[commitizen]: https://commitizen-tools.github.io/commitizen/
[uv]: https://docs.astral.sh/uv/
