<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>

SPDX-License-Identifier: Apache-2.0
-->

# 𝗰𝗼𝗺𝗺𝗶𝘁𝗶𝘇𝗲𝗻-𝚜𝚙𝚍𝚡-𝓬𝓱𝓪𝓷𝓰𝓮𝓵𝓸𝓰

[![Typing SVG][typing-svg-badge]][typing-svg-link]

[![License][license-badge]][license-link] [![PyPI][pypi-badge]][pypi-link]
[![Python][python-badge]][pypi-link] [![CI][ci-badge]][ci-link]
[![Release][release-badge]][release-link]

A [commitizen] changelog format plugin with YAML frontmatter awareness —
designed for REUSE/SPDX-compliant changelogs. No more false version detection
from license headers like `Apache-2.0`.

> [!WARNING]
> _This project is in early development._

## Features

- [x] **SPDX-aware** — strips `---`-delimited YAML frontmatter before parsing
- [x] **Correct version detection** — no false positives from `Apache-2.0` style
    headers
- [x] **Drop-in replacement** — extends commitizen's built-in `Markdown` format
- [x] **Zero extra config** — just set `changelog_format = "spdx-markdown"`

## Why do I need this?

If you keep your changelog in `docs/changelog.md` instead of the project root,
placing it alongside your documentation lets readers of your published site who
might not directly browse the git repository stay informed about recent changes.

Documentation generators like [Zensical], [Docusaurus], and tools using Google's
[Open Knowledge Format (OKF)][okf] require a YAML front matter for `meta` data.

When you apply a [REUSE/SPDX][reuse] license header with `reuse annotate`, the
header lands as a YAML comment inside the front matter, not as an HTML comment:

<!-- REUSE-IgnoreStart -->

- `# SPDX-License-Identifier: Apache-2.0`

<!-- REUSE-IgnoreEnd -->

**The catch:** commitizen's built-in `Markdown` format does not understand YAML
front matter. It reads `Apache-2.0` as a version number, causing
`cz bump --changelog` to fail silently or produce wrong results.

> [!NOTE]
> This plugin strips the front matter before parsing, so your changelog stays
> compliant, doc-generator-friendly, and commitizen-compatible — all at once.

## Getting started

### Installation

```sh
uv add commitizen-spdx-changelog
# or: pip install commitizen-spdx-changelog
```

> [!TIP]
> See the [docs landing page](docs/index.md) for a full overview, and the
> [usage guide](docs/guide.md) for furher setup and workflow instructions.

### Configuration

In `pyproject.toml`:

```toml
[tool.commitizen]
changelog_format = "spdx-markdown"
```

### Usage

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

### Development

```sh
direnv allow
uv sync --group dev
```

> [!TIP]
> Running `direnv allow` will activate the [devbox] environment automatically.
> See the [Devbox guide](docs/devbox.md) for all available commands and tools.

## Contributing

> [!NOTE]
> Bug reports, feature requests, and pull requests are welcome.

- See [docs/contributing.md](docs/contributing.md) for guidelines.

For documentation contributions, please follow these principles:

Write for humans, keep it minimal, update docs with code, delete dead content.
Every page in `docs/` and the project `README.md` are held to these standards.

## License

Distributed under the terms of the [Apache License 2.0](LICENSE.md).

- Copyright © 2026 Pablo Hörtner

<!-- References -->

[ci-badge]: https://badgen.net/github/checks/redtux/commitizen-spdx-changelog
[ci-link]: https://github.com/redtux/commitizen-spdx-changelog/actions
[commitizen]: https://commitizen-tools.github.io/commitizen/
[devbox]: https://github.com/jetify-com/devbox
[docusaurus]: https://docusaurus.io/
[license-badge]: https://badgen.net/github/license/redtux/commitizen-spdx-changelog
[license-link]: LICENSE.md
[okf]: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
[pypi-badge]: https://badgen.net/pypi/v/commitizen-spdx-changelog
[pypi-link]: https://pypi.org/project/commitizen-spdx-changelog/
[python-badge]: https://badgen.net/pypi/python/commitizen-spdx-changelog
[release-badge]: https://badgen.net/github/release/redtux/commitizen-spdx-changelog
[release-link]: https://github.com/redtux/commitizen-spdx-changelog/releases
[reuse]: https://reuse.software/
[typing-svg-badge]: https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&width=435&lines=SPDX-compliant+Commitizen+Changelogs
[typing-svg-link]: https://git.io/typing-svg
[zensical]: https://zensical.org/
