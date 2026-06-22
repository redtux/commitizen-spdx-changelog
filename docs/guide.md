---
# SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
#
# SPDX-License-Identifier: Apache-2.0

description: Usage guide for the commitizen-spdx-changelog plugin
icon: lucide/book-open
title: Usage Guide
---

This guide covers installing, configuring, and using the
commitizen-spdx-changelog plugin, as well as debugging common issues and
preparing a release.

## Installation

Install the package with [uv]:

```sh
uv add commitizen-spdx-changelog
```

Or with pip:

```sh
pip install commitizen-spdx-changelog
```

## Configuration

Add the following to your `pyproject.toml`:

```toml
[tool.commitizen]
changelog_format = "spdx-markdown"
```

This tells commitizen to use the SPDX-aware formatter instead of the built-in
`Markdown` format.

## Common workflows

### Generate or update a changelog

```sh
cz bump --changelog
```

This parses your conventional commits, bumps the version according to your
commitizen configuration, and prepends a new entry to the changelog.

### Inspect the changelog

Open `docs/changelog.md` (or your configured changelog path) to see the
generated output. The frontmatter block is preserved and version entries are
inserted at the correct position below it.

## Debugging

### Changelog shows wrong version numbers

If your changelog contains a YAML frontmatter block with SPDX license
identifiers (e.g., `Apache-2.0`), commitizen's built-in `Markdown` format may
mistakenly parse the `2.0` as a version number. This plugin solves that by
stripping the frontmatter before parsing.

### Run the reproduction script

To see the bug in action:

```sh
uv run python scripts/reproduce_bug.py
```

This demonstrates the problem in three ways: regex analysis, revision
simulation, and a direct API call. Use `--help` for available options.

### Common issues

- **Unclosed frontmatter**: If your changelog has a `---` opening delimiter but
    no closing `---`, the frontmatter is silently ignored — no stripping occurs.
- **Missing frontmatter detection**: The formatter only strips blocks delimited
    by `---`. Other frontmatter delimiters (e.g., `+++`, `;;;`) are not
    recognised.

## Release procedures

### Tag a release

```sh
git tag v1.0.0
git push origin v1.0.0
```

### Automated publishing

Pushing a tag matching `v*` triggers the [CI/CD pipeline] which:

1. Builds the distribution with `uv build`
2. Publishes to PyPI via [trusted publishing] (OIDC)
3. Creates a GitHub Release with the built artifacts
4. Extracts the changelog section for this tag as release notes

<!-- References -->

[ci/cd pipeline]: https://github.com/redtux/commitizen-spdx-changelog/actions
[trusted publishing]: https://docs.pypi.org/trusted-publishers/
[uv]: https://docs.astral.sh/uv/
