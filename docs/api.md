---
# SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
#
# SPDX-License-Identifier: Apache-2.0

description: API reference for the commitizen-spdx-changelog plugin
icon: lucide/file-code
title: API Reference
---

## Formatters

The `SPDXMarkdown` formatter extends commitizen's built-in `Markdown` changelog
format with YAML frontmatter awareness. It strips `---`-delimited SPDX headers
before parsing, so license identifiers like `Apache-2.0` are never mistaken for
version numbers.

Use this formatter when your changelog includes an SPDX/REUSE header block — set
`changelog_format = "spdx-markdown"` in your project configuration.

## Usage example

Configure [commitizen] in `pyproject.toml`:

```toml
[tool.commitizen]
changelog_format = "spdx-markdown"
```

Then generate your changelog:

```sh
cz bump --changelog
```

---

::: commitizen_spdx_changelog.formatters.spdx_markdown.SPDXMarkdown

<!-- References -->

[commitizen]: https://commitizen-tools.github.io/commitizen/
