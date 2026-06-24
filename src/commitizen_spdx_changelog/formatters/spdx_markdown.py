# SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
#
# SPDX-License-Identifier: Apache-2.0

"""SPDX/REUSE-aware Markdown changelog format for commitizen.

Compatible with REUSE/SPDX-compliant changelogs that carry a ``---``
delimited YAML frontmatter block (e.g. SPDX headers) before the Markdown
body. Registered under the ``commitizen.changelog_format`` entry point
as ``spdx-markdown``.

Note: importing this module directly, before anything else in the
process has imported ``commitizen.changelog_formats``, will raise an
``AttributeError`` due to a circular import inside commitizen's own
entry-point-loading machinery (it loads all registered
``commitizen.changelog_format`` plugins, including this one, from a
module-level dict comprehension). This never occurs during real ``cz``
usage, since commitizen's CLI bootstrap imports
``commitizen.changelog_formats`` before scanning plugins. It can occur
if a test imports this module cold — see ``tests/conftest.py`` for the
one-line warm-up import that avoids it for the test suite.
"""

from __future__ import annotations

import io
from collections.abc import Sequence
from pathlib import Path

from commitizen.changelog import IncrementalMergeInfo, Metadata
from commitizen.changelog_formats.markdown import Markdown


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


class SPDXMarkdown(Markdown):
    """Markdown changelog format with YAML frontmatter awareness.

    Overrides two methods from :class:`commitizen.changelog_formats.markdown.Markdown`:

    - ``get_metadata()`` — strips frontmatter via :func:`_strip_frontmatter`,
      delegates to ``get_metadata_from_file()``, then shifts the returned
      line indices by the frontmatter line count.
    - ``get_latest_full_release()`` — same stripping and index shift applied
      to ``get_latest_full_release_from_file()``.

    Attributes:
        config: The commitizen configuration object.
    """

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
