# SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
#
# SPDX-License-Identifier: Apache-2.0

# src/commitizen_spdx_changelog/formatters/spdx_markdown.py
#
# SPDXMarkdown is defined BEFORE any commitizen import to break
# a circular dependency. When commitizen scans changelog_format entry
# points, it imports this module. The entry-point loader (ep.load())
# needs `SPDXMarkdown` to already exist on the partially-loaded module.
# By placing the class definition first (it does not depend on commitizen
# internals), the scanner finds it immediately. The real implementation
# in _SPDXMarkdownImpl (which imports commitizen.changelog_formats.markdown)
# is defined AFTER the wrapper and all commitizen imports.

"""SPDX/REUSE-aware Markdown changelog format for commitizen.

This module defines the ``SPDXMarkdown`` wrapper and the real
``_SPDXMarkdownImpl`` implementation. ``SPDXMarkdown`` is defined before
any commitizen imports to avoid circular imports during commitizen's
entry-point scanning phase.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

    from commitizen.changelog import IncrementalMergeInfo, Metadata
    from commitizen.config.base_config import BaseConfig


class SPDXMarkdown:
    """Markdown changelog format with YAML frontmatter awareness.

    Compatible with REUSE/SPDX-compliant changelogs that carry an SPDX header
    block before the Markdown body.

    This is a lazy wrapper that delegates to ``_SPDXMarkdownImpl(Markdown)``
    in the same module. The class is defined before any ``commitizen`` import
    to break a circular dependency during entry-point scanning.
    ``__new__`` resolves the real class lazily so commitizen never triggers
    the import chain while its own modules are still loading.

    The real implementation overrides two methods from the parent ``Markdown``
    changelog format:

    - ``get_metadata()`` — strips ``---``-delimited YAML frontmatter via
      :func:`_strip_frontmatter`, delegates to
      ``get_metadata_from_file()``, then shifts returned line indices by the
      frontmatter line count.
    - ``get_latest_full_release()`` — same frontmatter stripping and index
      shift applied to ``get_latest_full_release_from_file()``.

    Attributes:
        extension: Default file extension for changelog files.
        alternative_extensions: Additional recognised file extensions.
    """

    extension = "md"
    alternative_extensions = {"markdown", "mkd"}

    _real_cls = None

    @classmethod
    def _resolve(cls):
        if cls._real_cls is None:
            cls._real_cls = _SPDXMarkdownImpl
        return cls._real_cls

    def __new__(cls, config=None):
        return cls._resolve()(config)  # type: ignore[arg-type]

    if TYPE_CHECKING:
        config: BaseConfig

        def get_metadata(self, filepath: str) -> Metadata: ...

        def get_latest_full_release(self, filepath: str) -> IncrementalMergeInfo: ...


# --- Safe to import commitizen internals — SPDXMarkdown is already defined ---

import io  # noqa: E402
from pathlib import Path  # noqa: E402
from collections.abc import Sequence  # noqa: E402

from commitizen.changelog import IncrementalMergeInfo, Metadata  # noqa: E402
from commitizen.changelog_formats.markdown import Markdown  # noqa: E402


def _strip_frontmatter(lines: Sequence[str]) -> tuple[list[str], int]:
    """Strip ``---``-delimited YAML frontmatter.

    Args:
        lines: The input lines, which may start with ``---`` frontmatter.

    Returns:
        A tuple of ``(clean_lines, offset)`` where ``clean_lines`` is the
        content after the closing ``---`` and ``offset`` is the number of
        frontmatter lines (0 if no frontmatter is detected).
    """
    if not lines or lines[0].rstrip() != "---":
        return list(lines), 0

    in_fm = False
    offset = 0
    for i, line in enumerate(lines):
        stripped = line.rstrip()
        if stripped == "---":
            offset += 1
            if not in_fm:
                in_fm = True
            else:
                return list(lines[i + 1 :]), offset
        elif in_fm:
            offset += 1

    return list(lines), 0  # unclosed frontmatter — treat as no-op


class _SPDXMarkdownImpl(SPDXMarkdown, Markdown):
    """Actual implementation — subclasses Markdown for work, SPDXMarkdown for isinstance.

    Wraps :class:`commitizen.changelog_formats.markdown.Markdown` with
    YAML frontmatter stripping via :func:`_strip_frontmatter`.

    Attributes:
        config: The commitizen configuration object.
    """

    def __new__(cls, config=None):  # noqa: D102
        return Markdown.__new__(cls)

    def __init__(self, config=None):
        if config is None:
            from commitizen.config.base_config import BaseConfig

            config = BaseConfig()
        if "encoding" not in config.settings:
            config.update({"encoding": "utf-8"})
        super().__init__(config)

    def get_metadata(self, filepath: str) -> Metadata:
        """Extract changelog metadata with frontmatter offset correction.

        Args:
            filepath: Path to the changelog file.

        Returns:
            A :class:`commitizen.changelog.Metadata` instance with line
            indices adjusted for stripped YAML frontmatter.
        """
        file = Path(filepath)
        if not file.is_file():
            return Metadata()

        encoding = self.config.settings.get("encoding", "utf-8")
        raw = file.read_text(encoding=encoding)
        clean_lines, offset = _strip_frontmatter(raw.splitlines(keepends=True))

        meta = self.get_metadata_from_file(io.StringIO("".join(clean_lines)))

        if meta.unreleased_start is not None:
            meta.unreleased_start += offset
        if meta.unreleased_end is not None:
            meta.unreleased_end += offset
        if meta.latest_version_position is not None:
            meta.latest_version_position += offset

        return meta

    def get_latest_full_release(self, filepath: str) -> IncrementalMergeInfo:
        """Retrieve the latest full release info with frontmatter offset correction.

        Args:
            filepath: Path to the changelog file.

        Returns:
            An :class:`commitizen.changelog.IncrementalMergeInfo` with the
            release index adjusted for stripped YAML frontmatter.
        """
        file = Path(filepath)
        if not file.is_file():
            return IncrementalMergeInfo()

        encoding = self.config.settings.get("encoding", "utf-8")
        raw = file.read_text(encoding=encoding)
        clean_lines, offset = _strip_frontmatter(raw.splitlines(keepends=True))

        result = self.get_latest_full_release_from_file(
            io.StringIO("".join(clean_lines))
        )

        return IncrementalMergeInfo(
            name=result.name,
            index=(result.index + offset) if result.index is not None else None,
        )
