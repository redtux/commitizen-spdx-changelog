---
# SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
#
# SPDX-License-Identifier: Apache-2.0

description: Class hierarchy, frontmatter detection, SPDXMarkdown class, entry point, package structure
icon: lucide/component
status: done
title: Plan 03 — Design
---

## Class hierarchy

```text
commitizen.changelog_formats.base.BaseFormat
  └─ commitizen.changelog_formats.markdown.Markdown
       └─ commitizen_spdx_changelog.formatters._impl._SPDXMarkdownImpl
              ↑ (resolved at runtime via __new__)
       commitizen_spdx_changelog.formatters.spdx_markdown.SPDXMarkdown (lazy wrapper)
```

The upstream `Markdown` class is intentionally slim — it only provides two
regex-based methods and inherits all file I/O from `BaseFormat`:

```python
# upstream commitizen/changelog_formats/markdown.py (verbatim for reference)
class Markdown(BaseFormat):
    extension = "md"
    alternative_extensions = {"markdown", "mkd"}
    RE_TITLE = re.compile(r"^(?P<level>#+) (?P<title>.*)$")

    def parse_version_from_title(self, line: str) -> VersionTag | None:
        m = self.RE_TITLE.match(line)
        if not m:
            return None
        return self.tag_rules.search_version(m.group("title"))

    def parse_title_level(self, line: str) -> int | None:
        m = self.RE_TITLE.match(line)
        if not m:
            return None
        return len(m.group("level"))
```

`_SPDXMarkdownImpl` does **not** override these parsing methods — it inherits
them unchanged. The only responsibility of `SPDXMarkdown`/`_SPDXMarkdownImpl` is
to strip frontmatter and correct line indices before/after delegating to the
inherited logic.

### Circular import avoidance

When commitizen scans entry points, it calls `ep.load()` on the registered
class. If `spdx_markdown.py` imported `commitizen.changelog_formats.markdown` at
the top level, the partially-loaded commitizen module graph could deadlock. To
break this:

1. `spdx_markdown.py` defines a **lazy wrapper** `SPDXMarkdown` that does not
    import any commitizen internals at module level. Its `__new__` method
    resolves to the real class at instantiation time.
2. The **real implementation** lives in `_impl.py`
    (`_SPDXMarkdownImpl(Markdown)`), which safely imports
    `commitizen.changelog_formats.markdown` because it is loaded lazily, well
    after the entry-point scanner has finished.
3. `_strip_frontmatter` is defined in `spdx_markdown.py` (no commitizen deps)
    and imported by `_impl.py` when it loads.

## Key methods to override

`BaseFormat.get_metadata` and `BaseFormat.get_latest_full_release` each open the
file by path and delegate to a `*_from_file` counterpart:

```python
# upstream commitizen/changelog_formats/base.py (condensed for reference)
def get_metadata(self, filepath: str) -> Metadata:
    with Path(filepath).open(encoding=...) as f:
        return self.get_metadata_from_file(f)


def get_latest_full_release(self, filepath: str) -> IncrementalMergeInfo:
    with Path(filepath).open(encoding=...) as f:
        return self.get_latest_full_release_from_file(f)
```

We override the filepath-level pair (not `*_from_file`):

1. Read the full file content
2. Strip YAML frontmatter (`---` delimited block at file start) and record the
    number of removed lines as `offset`
3. Wrap the clean content in `io.StringIO` (satisfies the `IO[Any]` contract)
4. Call `self.get_metadata_from_file(fake_file)` /
    `self.get_latest_full_release_from_file(fake_file)` — inheriting all
    existing parsing logic without duplication
5. Shift all returned line indices by `+ offset` to restore their positions in
    the original file

This approach preserves correct positioning in the original file and requires no
regex patching or monkey-patching.

## Frontmatter detection

Support only `---` delimited YAML frontmatter at the start of the file.

### Why frontmatter at all? — REUSE and Markdown interaction

The [REUSE specification][reuse-spec] requires SPDX license/copyright headers on
every file. For Markdown files there are two conventions:

<!-- REUSE-IgnoreStart -->

- **HTML comment** (`<!-- -->`): default, valid Markdown, invisible when
    rendered. `<!-- SPDX-License-Identifier: Apache-2.0 -->`
- **YAML comment inside frontmatter** (`---` / `---`): valid, standard SPDX
    block, visible in source. `---` / `# SPDX-License-Identifier: Apache-2.0` /
    `---`

<!-- REUSE-IgnoreEnd -->

This project uses the **YAML frontmatter** convention. Because we already use
frontmatter for documentation metadata (`icon`, `description`, etc.), REUSE
detects the `---` delimiters and formats the SPDX header as YAML comments
(`#`-prefixed) inside the block instead of wrapping them in HTML comments.

The problem is that **upstream commitizen's `Markdown` changelog format is not
frontmatter-aware**. Its `RE_TITLE` regex (`^(?P<level>#+) (?P<title>.*)$`)
matches `#` prefixes inside the frontmatter block. When it encounters

<!-- REUSE-IgnoreStart -->

`# SPDX-License-Identifier: Apache-2.0`, it parses that as a level-1 heading
with title `SPDX-License-Identifier: Apache-2.0`.

<!-- REUSE-IgnoreEnd -->

It then feeds the title to `search_version`, which extracts `2.0` from
`Apache-2.0` — a false positive. This causes `cz bump` to either pick the wrong
version or raise `NoRevisionError`.

The `SPDXMarkdown` plugin solves this by stripping the frontmatter block before
delegating to the inherited parsing, then shifting line indices back to the
original file coordinates (see below).

### Plugin is path-agnostic

The plugin itself does **not** enforce a specific changelog file path or name.
It works with any path the user configures via `changelog_file` in
`[tool.commitizen]`. Consumer projects can use the conventional `CHANGELOG.md`,
while this project overrides it to `docs/changelog.md` to embed the changelog in
the documentation site. This is a project-level choice, not a plugin concern.

### Algorithm

```python
def _strip_frontmatter(lines: list[str]) -> tuple[list[str], int]:
    """
    Strip ``---``-delimited YAML frontmatter from the start of *lines*.

    Returns ``(clean_lines, offset)`` where *offset* is the number of
    removed lines (including both ``---`` delimiters).

    Edge cases:
    - File does not start with ``---``  -> (lines, 0), no-op.
    - Unclosed frontmatter (no second ``---``) -> (lines, 0), no-op.
    - Empty file -> ([], 0).
    """
    if not lines or lines[0].rstrip() != "---":
        return lines, 0  # no frontmatter

    in_fm = False
    offset = 0
    for i, line in enumerate(lines):
        stripped = line.rstrip()
        if stripped == "---":
            offset += 1
            if not in_fm:
                in_fm = True  # opening delimiter consumed
            else:
                # Closing delimiter consumed; return everything after it.
                return lines[i + 1 :], offset
        elif in_fm:
            offset += 1

    # Reached EOF without a closing ``---`` — treat whole file as body.
    return lines, 0
```

<!-- REUSE-IgnoreStart -->

**Trace for our 7-line frontmatter block (used in `docs/changelog.md`):**

```text
i=0  "---"                                                    → in_fm=True,  offset=1
i=1  "# SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>"  → in_fm,  offset=2
i=2  "#"                                                       → in_fm,       offset=3
i=3  "# SPDX-License-Identifier: Apache-2.0"                   → in_fm,       offset=4
i=4  ""                                                         → in_fm,       offset=5
i=5  "icon: lucide/git-commit-vertical"                        → in_fm,       offset=6
i=6  "---"                                                     → in_fm=False, offset=7  → return lines[7:], 7
```

<!-- REUSE-IgnoreEnd -->

Result: 7 lines stripped, `offset = 7`. The body starts at line 7 (blank line
after the closing `---`). The first version heading `## 0.4.0 (2026-06-08)` is
at clean line 3 → position 10 in the original file. ✓

## `SPDXMarkdown` lazy wrapper (`spdx_markdown.py`)

The public entry point defines a lightweight wrapper that resolves to
`_SPDXMarkdownImpl` at call time. See the actual source for the full code (too
long to reproduce here in full). Key structure:

```python
# SPDX header ...

"""SPDX/REUSE-aware Markdown changelog format for commitizen."""

from __future__ import annotations

import sys as _sys
from collections.abc import Sequence
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from commitizen.changelog import IncrementalMergeInfo, Metadata
    from commitizen.config.base_config import BaseConfig


class SPDXMarkdown:
    """Lazy wrapper — resolved to _SPDXMarkdownImpl via __new__."""

    extension = "md"
    alternative_extensions = {"markdown", "mkd"}
    _real_cls = None

    @classmethod
    def _resolve(cls):
        if cls._real_cls is None:
            from commitizen_spdx_changelog.formatters._impl import _SPDXMarkdownImpl

            cls._real_cls = _SPDXMarkdownImpl
        return cls._real_cls

    def __new__(cls, config=None):
        return cls._resolve()(config)

    # TYPE_CHECKING stubs for IDE support ...


# --- Utilities imported below (safe — no entry-point scanner trigger) ---


def _strip_frontmatter(lines: Sequence[str]) -> tuple[list[str], int]: ...


# --- Real implementation (lazy) ---
from commitizen_spdx_changelog.formatters._impl import _SPDXMarkdownImpl
```

## `_SPDXMarkdownImpl` real implementation (`_impl.py`)

Holds the actual `Markdown` subclass with the frontmatter-aware overrides:

```python
"""Real implementation — safe to import commitizen internals."""

from __future__ import annotations

import io
from pathlib import Path

from commitizen.changelog import IncrementalMergeInfo, Metadata
from commitizen.changelog_formats.markdown import Markdown
from commitizen_spdx_changelog.formatters.spdx_markdown import _strip_frontmatter


class _SPDXMarkdownImpl(Markdown):
    def __init__(self, config=None):
        if config is None:
            from commitizen.config.base_config import BaseConfig

            config = BaseConfig()
        if "encoding" not in config.settings:
            config.update({"encoding": "utf-8"})
        super().__init__(config)

    def get_metadata(self, filepath: str) -> Metadata:
        file = Path(filepath)
        if not file.is_file():
            return Metadata()
        raw = file.read_text(encoding=self.config.settings["encoding"])
        clean_lines, offset = _strip_frontmatter(raw.splitlines(keepends=True))
        meta = self.get_metadata_from_file(io.StringIO("".join(clean_lines)))
        if meta.latest_version_position is not None:
            meta.latest_version_position += offset
        return meta

    def get_latest_full_release(self, filepath: str) -> IncrementalMergeInfo:
        file = Path(filepath)
        if not file.is_file():
            return IncrementalMergeInfo()
        raw = file.read_text(encoding=self.config.settings["encoding"])
        clean_lines, offset = _strip_frontmatter(raw.splitlines(keepends=True))
        result = self.get_latest_full_release_from_file(
            io.StringIO("".join(clean_lines)),
        )
        return IncrementalMergeInfo(
            name=result.name,
            index=(result.index + offset) if result.index is not None else None,
        )
```

> **Note on mutability:** `Metadata` is a mutable dataclass (fields are set
> in-place in `get_metadata_from_file`). `IncrementalMergeInfo` may be a
> `NamedTuple` depending on the commitizen version — reconstructing it is safe
> in both cases.

## Entry point registration

```toml
[project.entry-points."commitizen.changelog_format"]
spdx-markdown = "commitizen_spdx_changelog.formatters.spdx_markdown:SPDXMarkdown"
```

> Changelog format plugins use the `"commitizen.changelog_format"` entry point
> group, as defined in `commitizen/changelog_formats/__init__.py`:
> `CHANGELOG_FORMAT_ENTRYPOINT = "commitizen.changelog_format"`. This differs
> from commit-style plugins (`"commitizen.plugin"` group).

## Package structure

```text
commitizen-spdx-changelog/
├── .editorconfig
├── .github/
│   └── workflows/
│       ├── ci.yaml          # test matrix on push/PR
│       └── publish.yaml     # PyPI publish on tag
├── .gitignore
├── .python-version
├── AGENTS.md
├── docs/
│   ├── changelog.md         # own changelog — with SPDX frontmatter (under docs/ for docs integration)
│   └── plans/
│       └── ...
├── LICENSES/
│   └── Apache-2.0.txt       # full Apache 2.0 license text (required for REUSE)
├── LICENSE.md
├── README.md
├── opencode.jsonc
├── pyproject.toml
├── src/
│   └── commitizen_spdx_changelog/
│       ├── __init__.py
│       └── formatters/
│           ├── __init__.py
│           ├── _impl.py              # real _SPDXMarkdownImpl(Markdown)
│           └── spdx_markdown.py      # lazy wrapper (entry point)
└── tests/
    ├── conftest.py
    └── test_spdx_markdown.py
```

> **Note:** `CHANGELOG.md` is the de facto standard name and is fully supported.
> This project places the file at `docs/changelog.md` (and configures
> `changelog_file = "docs/changelog.md"` in `pyproject.toml`) so it integrates
> with the documentation site. The plugin is path-agnostic — consumers can use
> any path they prefer.

## Tasks

- [x] **Create package directory structure.** Create
    `src/commitizen_spdx_changelog/formatters/` with `__init__.py` files.
- [x] **Implement `_strip_frontmatter`.** Write the standalone function in
    `spdx_markdown.py` that strips `---`-delimited YAML frontmatter and returns
    `(clean_lines, offset)`. Handle all edge cases: no frontmatter, unclosed,
    empty file.
- [x] **Implement lazy wrapper `SPDXMarkdown`.** Define a class in
    `spdx_markdown.py` with no commitizen imports at module level, using
    `__new__` to resolve to `_SPDXMarkdownImpl` at call time.
- [x] **Implement `_SPDXMarkdownImpl._get_metadata` and
    `_get_latest_full_release`** in `_impl.py`. Override to strip frontmatter,
    delegate to `*_from_file`, and shift line indices by offset.
- [x] **Register the entry point.** Add
    `[project.entry-points."commitizen.changelog_format"]` with
    `spdx-markdown = "commitizen_spdx_changelog.formatters.spdx_markdown:SPDXMarkdown"`
    in `pyproject.toml`.
- [x] **Verify the module imports.** Run
    `python -c "from commitizen_spdx_changelog.formatters.spdx_markdown import SPDXMarkdown"`
    to confirm it loads without errors.

## Dependencies

- **Plan 02 must be complete** — scaffold exists, `pyproject.toml` is in place.
- Python 3.13+ with `commitizen>=4.16` installed.
- `uv_build` available (build backend).

## Acceptance

- [x] `src/commitizen_spdx_changelog/formatters/spdx_markdown.py` exists.
- [x] `src/commitizen_spdx_changelog/formatters/_impl.py` exists.
- [x] `_strip_frontmatter` handles all edge cases (no frontmatter, unclosed,
    empty).
- [x] `SPDXMarkdown` class compiles and imports cleanly without triggering
    circular imports.
- [x] Entry point registered in `pyproject.toml`.
- [x] Package structure matches the tree above (with `docs/changelog.md`).

## Next

→ Continue to [Plan 04 — pyproject.toml](04-pyproject.md)

## See also

- [Plan 01 — Problem and Goal](01-problem-and-goal.md)
- [Plan 02 — Scaffolding](02-scaffolding.md)
- [Plan 04 — pyproject.toml](04-pyproject.md)

[reuse-spec]: https://reuse.software/spec/ "REUSE Specification — FSFE"
