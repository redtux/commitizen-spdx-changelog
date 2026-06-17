# SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
#
# SPDX-License-Identifier: Apache-2.0

# src/commitizen_spdx_changelog/formatters/_impl.py
#
# This file is part of commitizen-spdx-changelog, a plugin
# for commitizen that generates changelogs in SPDX format.
#
# NOTE: This module is NOT the entry point. It is imported lazily
# by the SPDXMarkdown wrapper in spdx_markdown.py to avoid a
# circular import during commitizen's entry-point scanner.

"""Real implementation of SPDXMarkdown — safe to import commitizen internals.

This module is NOT the entry point. It is imported lazily by the
``SPDXMarkdown`` wrapper in :mod:`spdx_markdown` to avoid a circular
import during commitizen's entry-point scanner.
"""

from __future__ import annotations

import io
from pathlib import Path

from commitizen.changelog import IncrementalMergeInfo, Metadata
from commitizen.changelog_formats.markdown import Markdown

from commitizen_spdx_changelog.formatters.spdx_markdown import _strip_frontmatter


class _SPDXMarkdownImpl(Markdown):
    """Actual implementation — not imported during entry-point scanning.

    Wraps :class:`commitizen.changelog_formats.markdown.Markdown` with
    YAML frontmatter stripping via :func:`_strip_frontmatter`.

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
