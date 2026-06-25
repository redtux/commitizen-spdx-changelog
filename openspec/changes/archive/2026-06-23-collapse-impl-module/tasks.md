<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
SPDX-FileContributor: https://redtux.github.io/commitizen-spdx-changelog/credits/

SPDX-License-Identifier: Apache-2.0
-->

## 1. Collapse module

- [x] 1.1 Replace `src/commitizen_spdx_changelog/formatters/spdx_markdown.py`
    with single-file wrapper + implementation using abc.ABC virtual subclassing
- [x] 1.2 Delete `src/commitizen_spdx_changelog/formatters/_impl.py`

## 2. Verify and clean

- [x] 2.1 Run `ruff check src/` — zero warnings
- [x] 2.2 Run `uv build && unzip -l dist/*.whl | grep py.typed` — marker present
- [x] 2.3 Run `uv run pytest -v` — existing 19/19 passes unchanged
- [x] 2.4 Run `cz bump --dry-run --changelog` — smoke test succeeds
