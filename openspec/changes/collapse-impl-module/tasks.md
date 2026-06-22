<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>

SPDX-License-Identifier: Apache-2.0
-->

## 1. Collapse module

- [ ] 1.1 Replace `src/commitizen_spdx_changelog/formatters/spdx_markdown.py`
    with single-file `SPDXMarkdown(Markdown)` implementation
- [ ] 1.2 Delete `src/commitizen_spdx_changelog/formatters/_impl.py`

## 2. Verify and clean

- [ ] 2.1 Run `ruff check src/` — zero warnings
- [ ] 2.2 Run `uv build && unzip -l dist/*.whl | grep py.typed` — marker present
- [ ] 2.3 Run `uv run pytest -v` — existing 19/19 passes unchanged
- [ ] 2.4 Run `cz bump --dry-run --changelog` — smoke test succeeds
