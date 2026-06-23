<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>

SPDX-License-Identifier: Apache-2.0
-->

## Why

The two-file architecture (`spdx_markdown.py` + `_impl.py`) with a
`__new__`-based lazy wrapper solves a real circular-import problem (commitizen's
`changelog_formats.__init__.py` loads entry points at import time). However, the
split also introduces a latent bug: `_SPDXMarkdownImpl` does not subclass
`SPDXMarkdown`, so `isinstance(formatter, SPDXMarkdown)` returns `False`.

## What Changes

- Collapse `_impl.py` into `spdx_markdown.py`. The wrapper `SPDXMarkdown` is
    defined first (before any commitizen imports), then `_SPDXMarkdownImpl` is
    defined after commitizen imports, inheriting only from `Markdown`. The
    `isinstance` fix is achieved via `abc.ABCMeta` virtual subclassing
    (`SPDXMarkdown.register()`).
- Delete `src/commitizen_spdx_changelog/formatters/_impl.py` entirely.
- Remove unused `import sys as _sys`.
- Verify `py.typed` (PEP 561 marker) lands in the built wheel.

## Capabilities

### New Capabilities

None — this is a pure refactor with no behavior change.

### Modified Capabilities

None — the public API and behavior remain identical.

## Impact

- `src/commitizen_spdx_changelog/formatters/spdx_markdown.py` — rewritten
- `src/commitizen_spdx_changelog/formatters/_impl.py` — deleted
- Entry point registration in `pyproject.toml` — unchanged (still points to
    `spdx_markdown:SPDXMarkdown`)
- Tests — no changes needed (they already import from `spdx_markdown`)
