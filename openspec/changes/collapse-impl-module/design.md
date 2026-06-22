<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>

SPDX-License-Identifier: Apache-2.0
-->

## Context

The formatter module (`spdx_markdown.py`) currently defines a lightweight
wrapper class that resolves to `_SPDXMarkdownImpl` via `__new__` at
instantiation time. The real implementation lives in `_impl.py`, which
subclasses `Markdown` directly. This two-file split was motivated by a perceived
circular-import risk during commitizen's entry-point scanning.

In reality, `commitizen.changelog_formats.markdown.Markdown` is already loaded
in `sys.modules` by the time entry points are scanned — commitizen uses it
internally for its built-in `"markdown"` format. There is no cycle to break. The
split also introduces a latent bug: `_SPDXMarkdownImpl` does not subclass
`SPDXMarkdown`, so `isinstance(formatter, SPDXMarkdown)` returns `False`.

## Goals / Non-Goals

**Goals:**

- Fix the `isinstance()` breakage by making `SPDXMarkdown` a direct subclass of
    `Markdown`.
- Remove all unnecessary lazy-loading machinery (`__new__`, `_resolve()`,
    `TYPE_CHECKING` stubs, `import sys as _sys`).
- Eliminate the E402 lint violations caused by staggered imports.
- Verify `py.typed` remains included in the built wheel.

**Non-Goals:**

- Changing any public behavior or API surface.
- Updating downstream documentation plans (`03-design.md`,
    `09-doc-generation.md`).
- Modifying test files (they already work with the new structure).

## Decisions

### Single-file collapse

**Decision**: Merge `_impl.py` into `spdx_markdown.py`. `SPDXMarkdown` becomes a
direct `Markdown` subclass. All commitizen types (`Metadata`,
`IncrementalMergeInfo`, `Markdown`) are imported at module level.

**Rationale**: The two-file split solves a non-existent problem and introduces a
real bug. A single file is simpler, eliminates the E402 warnings, and makes the
class hierarchy honest.

**Alternatives considered**:

- Keeping the split and fixing `isinstance` by having `_SPDXMarkdownImpl`
    inherit from `SPDXMarkdown` — rejected because it preserves unnecessary
    complexity for zero benefit.

### BaseConfig stays lazy

**Decision**: `from commitizen.config.base_config import BaseConfig` remains
inside `__init__` (lazy import).

**Rationale**: This is purely cosmetic — it avoids importing `BaseConfig` at
module level when it is only needed for default config construction. It is not a
circular-import workaround.

### Entry point unchanged

**Decision**: The `pyproject.toml` entry point remains
`spdx_markdown:SPDXMarkdown`. No registration changes needed.

**Rationale**: The public class name and module path are unchanged. The entry
point scanner will find `SPDXMarkdown` directly since it is now defined at
module level without any redirection.

## Risks / Trade-offs

- **py.typed missing from wheel**: Low risk — modern build backends include
    package files by default. Verified with `uv build && unzip -l dist/*.whl`.
- **Tests break**: Very low risk — tests already import `SPDXMarkdown` and
    `_strip_frontmatter` from `spdx_markdown`, which is the same public API. No
    test changes needed.
- **Commitizen entry point scan fails**: Low risk — `Markdown` is already in
    `sys.modules`. The single-file approach removes the only thing that could
    theoretically cause issues.
