---
# SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
# SPDX-FileContributor: https://redtux.github.io/commitizen-spdx-changelog/credits/
#
# SPDX-License-Identifier: Apache-2.0

description: Use direct Markdown subclass; fix cold import in conftest instead of production code
icon: lucide/undo-2
status: complete
title: Plan 11 — Use direct subclass
---

## Problem

Plan 10 fixed a circular import by wrapping `SPDXMarkdown` in an `abc.ABC` +
`__new__` + `register()` indirection. Reproduction with a full traceback
established that the cycle only occurs when our plugin module is the *first*
thing in the process to import `commitizen.changelog_formats` — a condition met
by cold `pytest` collection of our own test file, but never met by real `cz`
usage (`cz bump --dry-run --changelog` succeeds unconditionally, with or without
the wrapper).

The traceback:

```
tests/test_spdx_markdown.py:12
  → src/spdx_markdown.py:20  from commitizen.changelog_formats.markdown import Markdown
  → .venv/.../changelog_formats/__init__.py:59  ep.name: ep.load()
  → importlib/metadata/__init__.py:181  functools.reduce(getattr, attrs, module)
  → AttributeError: partially initialized module has no attribute 'SPDXMarkdown'
```

Carrying the wrapper in production code is therefore unnecessary complexity for
a problem that only manifests at test collection time.

## Resolution

### 1. Use direct subclass

Replace `spdx_markdown.py` with a single class:

- `class SPDXMarkdown(Markdown):` — direct inheritance, no wrapper, no
    `abc.ABC`, no `__new__`, no `register()`.
- Same `__init__`, `get_metadata`, `get_latest_full_release` overrides as the
    previous `_SPDXMarkdownImpl`.
- Same `_strip_frontmatter` utility, unchanged.
- Normal top-level imports — no staggered ordering, no `noqa: E402` needed.

### 2. Fix the cold import in `tests/conftest.py`

Add one line, before any other commitizen-related import in the test suite:

```python
import commitizen.changelog_formats  # noqa: F401  — warm up before plugin import
```

This guarantees `commitizen.changelog_formats`'s entry-point-loading dict
comprehension has already completed before `tests/test_spdx_markdown.py` imports
`SPDXMarkdown`, eliminating the cold-import path for the whole test directory.

### 3. Update docs

- Mark plan 10 (`10-collapse-impl.md`) as superseded by this plan, with a
    one-line note linking here.
- Update `AGENTS.md` architecture section — it still describes the old
    `_impl.py` / `__new__` pattern.

## Test compatibility

`tests/test_spdx_markdown.py` needs **no changes** — it already imports
`SPDXMarkdown` and `_strip_frontmatter` from `spdx_markdown`, and that import
now succeeds because `conftest.py` establishes the correct order, not because
the class itself redirects.

## Tasks

- [ ] **Replace `spdx_markdown.py`** — single direct
    `class SPDXMarkdown(Markdown):`, no wrapper.
- [ ] **Add warm-up import to `tests/conftest.py`**.
- [ ] **Run `ruff check src/`** — should pass cleanly with no `noqa` needed.
- [ ] **Run `uv run pytest -v`** — confirm all tests still pass with the
    conftest fix in place.
- [ ] **Run cold `python -c` reproduction** — confirm it now succeeds with the
    warm-up import (sanity check, not required for tests).
- [ ] **Run `cz bump --dry-run --changelog`** — confirm unchanged success.
- [ ] **Mark plan 10 as superseded** — add a note at the top of
    `10-collapse-impl.md` linking to this plan.
- [ ] **Update `AGENTS.md`** — replace `_impl.py` / `__new__` architecture
    description with the current direct-subclass pattern.

## Files touched

| Action | File                                                        |
| ------ | ----------------------------------------------------------- |
| Modify | `src/commitizen_spdx_changelog/formatters/spdx_markdown.py` |
| Modify | `tests/conftest.py`                                         |
| Create | `tests/test_plugin_integration.py`                          |
| Modify | `10-collapse-impl.md` (supersession note)                   |
| Modify | `AGENTS.md` (architecture section)                          |

## Dependencies

- `commitizen` with `Markdown` changelog format (built-in), same version pinned
    as before (`>=4.16.3`, tested against `4.16.4`).

## Acceptance

- [ ] `spdx_markdown.py` contains one class, no wrapper, no `register()`.
- [ ] `isinstance(formatter, SPDXMarkdown)` is `True` via real inheritance.
- [ ] `tests/conftest.py` contains the warm-up import.
- [ ] `ruff check src/` — zero warnings, no `noqa: E402` needed anywhere.
- [ ] `uv run pytest -v` — all tests pass unchanged.
- [ ] `cz bump --dry-run --changelog` succeeds.
- [ ] Plan 10 marked superseded.
- [ ] AGENTS.md architecture section updated.

## See also

- [Plan 10 — Collapse `_impl.py`](10-collapse-impl.md) (superseded by this plan)
- GitHub issue: [#6 — refactor: use direct Markdown subclass][issue-6]

[issue-6]: https://github.com/redtux/commitizen-spdx-changelog/issues/6
