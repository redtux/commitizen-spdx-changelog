<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>

SPDX-License-Identifier: Apache-2.0
-->

# direct-subclass — Implementation Tasks

## 1. Production code refactor

- [ ] 1.1 Replace `spdx_markdown.py` with direct `class SPDXMarkdown(Markdown):`
    — remove `abc.ABC`, `_resolve()`, `__new__`, `register()`, and
    `_SPDXMarkdownImpl` class.
- [ ] 1.2 Verify `isinstance(formatter, SPDXMarkdown)` returns `True` via real
    inheritance.
- [ ] 1.3 Verify `isinstance(formatter, Markdown)` returns `True`.
- [ ] 1.4 Run `ruff check src/` — confirm zero warnings, no `noqa: E402` needed.

## 2. Test harness fix

- [ ] 2.1 Add warm-up import to `tests/conftest.py`:
    `import commitizen.changelog_formats  # noqa: F401`
- [ ] 2.2 Run `uv run pytest -v` — confirm all 13 tests pass.
- [ ] 2.3 Create `tests/test_plugin_integration.py` with cold-import and
    isinstance tests (separates integration concerns from behavioural unit
    tests).
- [ ] 2.4 Run `uv run pytest tests/test_plugin_integration.py -v -k cold` —
    confirm all cold-import tests pass (verifies warm-up pattern in a fresh
    subprocess).

## 3. Production validation

- [ ] 3.1 Run `cz bump --dry-run --changelog` — confirm success.
- [ ] 3.2 Run `uv run pytest tests/test_plugin_integration.py -v -k isinstance`
    — confirm isinstance checks pass (both in-process and cold-subprocess).

## 4. Documentation

- [ ] 4.1 Update plan 11 (`11-direct-subclass.md`) with new implementation (if
    needed).
- [ ] 4.2 Mark plan 10 (`10-collapse-impl.md`) as superseded with link to Plan
    11\.
- [ ] 4.3 Update `AGENTS.md` architecture section — replace `_impl.py` /
    `__new__` description with direct-subclass pattern.
