<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>

SPDX-License-Identifier: Apache-2.0
-->

## Why

The two-file architecture (`spdx_markdown.py` + `_impl.py`) with a
`__new__`-based lazy wrapper solves a circular-import problem that does not
exist. In reality, `Markdown` is already in `sys.modules` when commitizen scans
entry points — there is no cycle. Worse, the `__new__` redirection breaks
`isinstance()` because `_SPDXMarkdownImpl` does not subclass `SPDXMarkdown`,
making any type check against the wrapper fail silently.

## What Changes

- Replace `spdx_markdown.py` with a single-file implementation where
    `SPDXMarkdown` directly subclasses `Markdown`.
- Delete `src/commitizen_spdx_changelog/formatters/_impl.py` entirely.
- Remove all lazy-loading machinery (`__new__`, `_resolve()`, `TYPE_CHECKING`
    stubs, `import sys as _sys`).
- Verify `py.typed` (PEP 561 marker) lands in the built wheel.
- Run ruff to confirm E402 violations disappear.

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
