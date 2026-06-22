<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>

SPDX-License-Identifier: Apache-2.0
-->

## Context

The formatter module (`spdx_markdown.py`) currently defines a lightweight
wrapper class that resolves to `_SPDXMarkdownImpl` via `__new__` at
instantization time. The real implementation lives in `_impl.py`, which
subclasses `Markdown` directly. This two-file split was motivated by a
circular-import risk during commitizen's entry-point scanning — and the risk is
real. When commitizen's `changelog_formats.__init__.py` loads, it scans entry
points at import time, which triggers our module to load. The wrapper
`SPDXMarkdown` must exist on the partially-loaded module before any commitizen
imports run.

The split also introduces a latent bug: `_SPDXMarkdownImpl` does not subclass
`SPDXMarkdown`, so `isinstance(formatter, SPDXMarkdown)` returns `False`.

## Goals / Non-Goals

**Goals:**

- Fix the `isinstance()` breakage via multiple inheritance.
- Collapse the two-file architecture into a single module.
- Preserve the entry-point scanning order (wrapper defined before commitizen
    imports).
- Remove the unused `import sys as _sys`.
- Verify `py.typed` remains included in the built wheel.

**Non-Goals:**

- Changing any public behavior or API surface.
- Updating downstream documentation plans (`03-design.md`,
    `09-doc-generation.md`).
- Modifying test files (they already work with the new structure).
- Eliminating E402 warnings (they are inherent to the staggered-import approach
    and were present in the original code too).

## Decisions

### Single-file collapse with multiple inheritance

**Decision**: Merge `_impl.py` into `spdx_markdown.py`. The wrapper
`SPDXMarkdown` is defined first (before any commitizen imports). The
`_SPDXMarkdownImpl` class inherits from both `SPDXMarkdown` and `Markdown`,
fixing the `isinstance` check. A `__new__` override on `_SPDXMarkdownImpl`
prevents infinite recursion.

**Rationale**: The two-file split is unnecessary complexity. A single file is
simpler and makes the class hierarchy honest. The `__new__` pattern is still
necessary because `commitizen.changelog_formats.__init__.py` loads entry points
at import time — the wrapper must exist before `Markdown` is imported.

**Alternatives considered**:

- Making `SPDXMarkdown` a direct `Markdown` subclass: rejected because importing
    `Markdown` triggers entry point scanning before `SPDXMarkdown` is defined →
    `AttributeError`.
- Removing the `__new__` pattern entirely: rejected for the same reason as
    above.

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
point scanner will find `SPDXMarkdown` directly since it is defined before
commitizen imports run.

## Risks / Trade-offs

- **py.typed missing from wheel**: Low risk — modern build backends include
    package files by default. Verified with `uv build && unzip -l dist/*.whl`.
- **Tests break**: Very low risk — tests already import `SPDXMarkdown` and
    `_strip_frontmatter` from `spdx_markdown`, which is the same public API. No
    test changes needed.
- **E402 warnings**: Inherent to the staggered-import approach. Suppressed with
    `noqa: E402`. The original code also had these.
