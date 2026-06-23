---
# SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
#
# SPDX-License-Identifier: Apache-2.0

description: Collapse module into single file and remove lazy import
icon: lucide/combine
status: pending
title: Plan 10 — Collapse _impl.py
---

## Problem

Two issues with the current two-file architecture:

1. **`isinstance` breakage** — `_SPDXMarkdownImpl` does not subclass
    `SPDXMarkdown`, so `isinstance(formatter, SPDXMarkdown)` returns `False`
    even though `SPDXMarkdown(config)` returns that object. This is a latent
    bug for any code (tests, commitizen internals, consumers) that relies on
    type checking.

2. **Unnecessary complexity** — The two-file split (`spdx_markdown.py` +
    `_impl.py`) with lazy `__new__` resolution was motivated by a
    circular-import concern. The concern is real (commitizen's
    `changelog_formats.__init__.py` loads entry points at import time), but the
    same ordering can be preserved in a single file.

## Resolution

### 1. Collapse to single file

Replace `src/commitizen_spdx_changelog/formatters/spdx_markdown.py` with a
single-file implementation. The final form:

- `SPDXMarkdown` wrapper defined first (before any commitizen imports) —
    preserves the entry-point scanning order; inherits from `abc.ABC`
- `_SPDXMarkdownImpl(Markdown)` — inherits from `Markdown` only;
    `SPDXMarkdown.register(_SPDXMarkdownImpl)` creates the virtual subclass
    relationship, fixing the `isinstance` check
- No `__new__` override needed on `_SPDXMarkdownImpl`
- Same `_strip_frontmatter` utility (unchanged logic)
- Same method overrides (`get_metadata`, `get_latest_full_release`)
- Remove `import sys as _sys` (was unused)
- Core commitizen types (`Metadata`, `IncrementalMergeInfo`, `Markdown`) are
    imported at top level; `BaseConfig` stays lazy inside `__init__` (cosmetic —
    not a workaround)
- Staggered imports after class definition are necessary (E402 suppressed via
    `noqa: E402`)

### 2. Delete `_impl.py`

Remove `src/commitizen_spdx_changelog/formatters/_impl.py` entirely.

### 3. `py.typed` verification

Run `uv build && unzip -l dist/*.whl | grep py.typed` to confirm the PEP 561
marker file lands in the wheel.

### 4. ruff cleanup

Run `ruff check src/`. The staggered imports after the class definition are
necessary (circular-import avoidance) and produce E402 warnings. Suppress them
with `noqa: E402` comments. The original code also had these — they are inherent
to the approach.

### 5. Smoke test

Run `cz bump --dry-run --changelog` as a real end-to-end smoke test of the code
path the lazy-loading was nominally protecting.

## Test compatibility

Existing tests (`test_spdx_markdown.py`) import `SPDXMarkdown` and
`_strip_frontmatter` from `spdx_markdown` — zero changes needed. The formatter
instantiation `SPDXMarkdown(config)` now works honestly via virtual subclassing,
matching what the tests already expect.

## Not in scope

Update `03-design.md` & `09-doc-generation.md` to reflect the new architecture.

## Tasks

- [x] **Replace `spdx_markdown.py`** — write single-file implementation:
    `SPDXMarkdown(abc.ABC)` wrapper defined first, `_SPDXMarkdownImpl(Markdown)`
    defined after commitizen imports, `SPDXMarkdown.register()` for virtual
    subclassing.
- [x] **Delete `_impl.py`** — remove
    `src/commitizen_spdx_changelog/formatters/_impl.py`.
- [x] **Verify `py.typed`** — `uv build && unzip -l dist/*.whl | grep py.typed`.
- [x] **Run ruff check** — `ruff check src/` passes cleanly (E402 suppressed).
- [x] **Run tests** — `uv run pytest -v` passes (existing 19/19).
- [x] **Smoke test with cz** — `cz bump --dry-run --changelog` succeeds.

## Files touched

| Action | File                                                        |
| ------ | ----------------------------------------------------------- |
| Modify | `src/commitizen_spdx_changelog/formatters/spdx_markdown.py` |
| Delete | `src/commitizen_spdx_changelog/formatters/_impl.py`         |

## Dependencies

- Current architecture must be stable (plans 01-09 complete).
- `commitizen` with `Markdown` changelog format (built-in).
- Python 3.13+, `ruff`, `uv`.

## Acceptance

- [x] `spdx_markdown.py` is a single file, no imports from `_impl`.
- [x] `_SPDXMarkdownImpl` registered as virtual subclass of `SPDXMarkdown` via
    `abc.ABC` — isinstance checks pass.
- [x] `_impl.py` no longer exists.
- [x] `py.typed` present in the built wheel.
- [x] `ruff check src/` — zero warnings.
- [x] `uv run pytest -v` — 19/19 passes unchanged.
- [x] `cz bump --dry-run --changelog` succeeds.

## See also

- [Plan 01 — Problem and Goal](01-problem-and-goal.md)
- [Plan 03 — Design](03-design.md) (will not be updated)
- [Plan 09 — Doc Generation](09-doc-generation.md) (will not be updated)
- OpenSpec change `collapse-impl-module`
- [GitHub issue #4](https://github.com/redtux/commitizen-spdx-changelog/issues/4)
