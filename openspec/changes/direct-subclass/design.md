<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>

SPDX-License-Identifier: Apache-2.0
-->

## Context

Plan 10 introduced an `abc.ABC` + `__new__` + `register()` wrapper to fix a
circular import reported during entry-point loading. The fix worked, and was
verified with a real traceback at the time. What wasn't yet established was the
*scope* of the problem: under what conditions does the cycle actually occur, and
does it occur in real `cz` usage or only under specific import orderings?

Follow-up reproduction settled this with three controlled tests against the
plain `class SPDXMarkdown(Markdown):` version:

1. `python -c "import commitizen.changelog_formats; from  commitizen_spdx_changelog.formatters.spdx_markdown import SPDXMarkdown"`
    — **succeeds**. Warming up `commitizen.changelog_formats` first avoids the
    cycle entirely.
2. `python -c "from commitizen_spdx_changelog.formatters.spdx_markdown import  SPDXMarkdown"`
    (cold, no warm-up) — **fails** with
    `AttributeError: partially initialized module ... has no attribute  'SPDXMarkdown' (most likely due to a circular import)`.
3. `cz bump --dry-run --changelog` — **succeeds**, unconditionally.

The mechanism, confirmed via full traceback:

```
our module (cold, first import)
  → from commitizen.changelog_formats.markdown import Markdown
  → triggers commitizen.changelog_formats.__init__ to execute
  → its module-level KNOWN_CHANGELOG_FORMATS dict comprehension
  → calls ep.load() on every commitizen.changelog_format entry point,
    including our own
  → re-imports our module, finds it already in sys.modules (partial,
    paused mid-import from the outer frame)
  → AttributeError: SPDXMarkdown not yet defined in the paused module
```

This is a genuine cycle, but it is *triggered by which module imports
`commitizen.changelog_formats` first* — not an inherent property of subclassing
`Markdown`. `cz`'s own CLI bootstrap (`commitizen.cli:main`) imports enough of
commitizen's internals, including `commitizen.changelog_formats`, before it ever
reaches plugin discovery, so production usage never hits the cold path.
`pytest`, collecting `tests/test_spdx_markdown.py` directly, is the one place in
our own toolchain that does hit it — because that test file's first
commitizen-related import is our own module.

## Goals / Non-Goals

**Goals:**

- Restore a direct, honest `class SPDXMarkdown(Markdown):` with no wrapper
    indirection.
- Fix the cold-import problem at test collection, where it actually occurs,
    rather than inside production code.
- Preserve correct `isinstance(formatter, SPDXMarkdown)` behavior via real
    inheritance.
- Document the corrected, narrower understanding of the circular import for
    future maintainers (this design doc, plus a note in plan 10's history).

**Non-Goals:**

- Changing `_strip_frontmatter` logic or any method behavior.
- Changing the `pyproject.toml` entry point registration.
- Re-litigating whether the cycle is "real" — it is; this change narrows *where*
    it occurs and fixes it at that location.

## Decisions

### Direct subclass, no wrapper

**Decision**: `spdx_markdown.py` contains exactly one class,
`SPDXMarkdown(Markdown)`, with the same `__init__`, `get_metadata`, and
`get_latest_full_release` overrides previously on `_SPDXMarkdownImpl`. The
`_resolve()` classmethod, `__new__` override, and `import abc` are removed.

**Rationale**: The wrapper's only job was to dodge a cold-import cycle that
doesn't occur in production. Once the cycle is understood to be a
test-collection-order issue, fixing it in the test harness removes the need for
any production-side workaround.

### Warm-up import in `tests/conftest.py`

**Decision**: Add `import commitizen.changelog_formats  # noqa: F401` as the
first commitizen-related import executed during test collection.

**Rationale**: `conftest.py` is collected by pytest before any test module in
its directory, making it the natural place to establish import order. This
single line guarantees `commitizen.changelog_formats` is fully initialized —
including its entry-point-loading dict comprehension — before
`tests/test_spdx_markdown.py` ever imports our plugin module, eliminating the
cold-import path entirely for the test suite.

**Alternatives considered**:

- Reordering imports inside `test_spdx_markdown.py` itself (e.g. importing
    `commitizen.changelog_formats` before importing `SPDXMarkdown`): works, but
    fragile — any future test file added to the suite would need to remember the
    same ordering. `conftest.py` is collected once and applies to the whole test
    directory, which is more robust.
- Keeping the `abc.ABC` wrapper: rejected, now that it's established the cycle
    never occurs in real usage — keeping it would mean carrying permanent
    production-code complexity to compensate for a test-only condition.

## Risks / Trade-offs

- **Future test files added without awareness of the warm-up requirement**:
    Mitigated by `conftest.py` applying automatically to all tests in the
    directory; no per-file action needed.
- **Someone imports `commitizen_spdx_changelog.formatters.spdx_markdown` cold
    from a script or REPL outside of `cz` or pytest**: Still possible to hit the
    `AttributeError` in that specific scenario. This is judged acceptable — it
    mirrors how commitizen's own built-in formats behave if imported the same
    way, and is not a regression introduced by this package.
