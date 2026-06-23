<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>

SPDX-License-Identifier: Apache-2.0
-->

## Why

Plan 10 fixed a real circular import by introducing an `abc.ABC` + `__new__` +
`register()` virtual-subclass wrapper. Follow-up reproduction with a captured
traceback established that the circular import only occurs when our own plugin
module is the *first* thing in the process to import
`commitizen.changelog_formats` — a condition that arises in bare/cold `pytest`
collection of our own test module, but never in real `cz` usage, since
commitizen's CLI bootstrap always imports `commitizen.changelog_formats` before
scanning third-party `commitizen.changelog_format` entry points.

The wrapper therefore fixes a problem in production code that production code
never actually triggers. The problem is real, but it belongs at the test
boundary.

## What Changes

- Replace the `abc.ABC` wrapper and `_SPDXMarkdownImpl` pair in
    `spdx_markdown.py` with a single, direct `class SPDXMarkdown(Markdown):`.
- Remove `import abc`, the `_resolve()` classmethod, the `__new__` override, and
    the trailing `SPDXMarkdown.register(_SPDXMarkdownImpl)` call.
- Add a one-line warm-up import to `tests/conftest.py`:
    `import commitizen.changelog_formats  # noqa: F401`
- Update plan 10 to note it is superseded by this change.
- Update `AGENTS.md` architecture section to describe the direct-subclass
    pattern instead of the old `_impl.py` / `__new__` pattern.

## Capabilities

### New Capabilities

None — pure refactor, no behavior change.

### Modified Capabilities

The `spdx-markdown-formatter` capability is modified:

- **Implementation structure**: The `SPDXMarkdown` class now directly inherits
    from `Markdown` instead of using an `abc.ABC` wrapper + `__new__` redirect +
    `register()` virtual subclass. The `isinstance(formatter, SPDXMarkdown)`
    check still returns `True`, but now via real inheritance instead of virtual
    registration.
- **Import structure**: Module-level imports are now standard top-level imports
    (no staggered order, no `noqa: E402`). The warm-up import in
    `tests/conftest.py` handles the cold-import condition at the test boundary.
- **Test-harness behavior**: `tests/conftest.py` gains a warm-up import to
    initialize `commitizen.changelog_formats` before test collection, ensuring
    the entry-point-loading dict comprehension completes before the plugin
    module is imported.

## Impact

- `src/commitizen_spdx_changelog/formatters/spdx_markdown.py` — rewritten,
    single class, no wrapper.
- `tests/conftest.py` — one new line (warm-up import).
- `tests/test_plugin_integration.py` — new file; cold-import and isinstance
    integration tests.
- `tests/test_spdx_markdown.py` — no changes needed; same imports as before
    continue to work, now because conftest warms up the import order rather than
    because the production class redirects.
- `openspec/changes/archive/2026-06-23-collapse-impl-module/` — superseded by
    this change; cross-reference both in `design.md`.
- `AGENTS.md` — architecture section updated.
