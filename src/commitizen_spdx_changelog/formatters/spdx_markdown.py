# SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
#
# SPDX-License-Identifier: Apache-2.0

# src/commitizen_spdx_changelog/formatters/spdx_markdown.py
#
# This file is part of commitizen-spdx-changelog, a plugin
# for commitizen that generates changelogs in SPDX format.
#
# NOTE: SPDXMarkdown is defined BEFORE any commitizen import to break
# a circular dependency. When commitizen scans changelog_format entry
# points, it imports this module. The entry-point loader (ep.load())
# needs `SPDXMarkdown` to already exist on the partially-loaded module.
# By placing the class definition first (it does not depend on commitizen
# internals), the scanner finds it immediately. The real implementation
# in _impl.py (which imports commitizen.changelog_formats.markdown) is
# imported lazily below.

"""SPDX/REUSE-aware Markdown changelog format for commitizen.

This module defines the ``SPDXMarkdown`` changelog format and the
``_strip_frontmatter`` utility. The entry-point class ``SPDXMarkdown``
is defined before any commitizen imports to avoid circular imports
during commitizen's entry-point scanning phase.
"""

from __future__ import annotations

import sys as _sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

    from commitizen.changelog import IncrementalMergeInfo, Metadata
    from commitizen.config.base_config import BaseConfig


class SPDXMarkdown:
    """Markdown changelog format with YAML frontmatter awareness.

    Compatible with REUSE/SPDX-compliant changelogs that carry an SPDX header
    block before the Markdown body.

    This is a lazy wrapper that delegates to
    ``_SPDXMarkdownImpl(Markdown)`` in the ``_impl`` module. The class is
    defined before any ``commitizen`` import to break a circular dependency
    during entry-point scanning. ``__new__`` resolves the real class lazily
    so commitizen never directly imports the implementation module.

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
        config: BaseConfig instance passed to the real implementation.
    """

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
        return cls._resolve()(config)  # type: ignore[arg-type]

    if TYPE_CHECKING:
        # Type-checking stubs — resolved by __new__ at runtime

        config: BaseConfig

        def get_metadata(self, filepath: str) -> Metadata: ...

        def get_latest_full_release(self, filepath: str) -> IncrementalMergeInfo: ...


# --- Utilities imported below (safe — do not trigger entry-point scanner) ---

import io
from pathlib import Path
from collections.abc import Sequence

from commitizen.changelog import IncrementalMergeInfo, Metadata


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


# --- Real implementation — imported AFTER the wrapper is defined ---

from commitizen_spdx_changelog.formatters._impl import _SPDXMarkdownImpl  # noqa: F401, E402
