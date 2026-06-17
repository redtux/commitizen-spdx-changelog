#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
#
# SPDX-License-Identifier: Apache-2.0

from pathlib import Path

import pytest
from commitizen.config.base_config import BaseConfig

from commitizen_spdx_changelog.formatters.spdx_markdown import (
    SPDXMarkdown,
    _strip_frontmatter,
)


class TestStripFrontmatter:
    def test_no_frontmatter(self):
        lines = ["# Changelog\n", "## 0.1.0\n"]
        clean, offset = _strip_frontmatter(lines)
        assert clean == lines
        assert offset == 0

    def test_empty_file(self):
        clean, offset = _strip_frontmatter([])
        assert clean == []
        assert offset == 0

    def test_with_frontmatter(self, spdx_frontmatter_changelog):
        lines = spdx_frontmatter_changelog.splitlines(keepends=True)
        clean, offset = _strip_frontmatter(lines)
        assert offset == 7
        assert clean[0] == "\n"
        assert clean[1] == "# Changelog\n"

    def test_unclosed_frontmatter(self, changelog_unclosed_frontmatter):
        lines = changelog_unclosed_frontmatter.splitlines(keepends=True)
        clean, offset = _strip_frontmatter(lines)
        # unclosed frontmatter should be treated as no frontmatter
        assert clean == lines
        assert offset == 0

    def test_leading_newline_before_frontmatter(self, tmp_path: Path):
        content = "\n---\nkey: val\n---\n# Changelog\n"
        lines = content.splitlines(keepends=True)
        clean, offset = _strip_frontmatter(lines)
        assert offset == 0  # doesn't start with ---

    def test_frontmatter_with_only_delimiters(self):
        lines = ["---\n", "---\n", "# Changelog\n"]
        clean, offset = _strip_frontmatter(lines)
        assert offset == 2
        assert clean == ["# Changelog\n"]


def _make_config(tmp_path: Path, content: str) -> str:
    path = tmp_path / "CHANGELOG.md"
    path.write_text(content, encoding="utf-8")
    return str(path)


class TestSPDXMarkdown:
    @pytest.fixture
    def formatter(self):
        config = BaseConfig()
        config.update({"encoding": "utf-8"})
        return SPDXMarkdown(config)

    def test_get_metadata_no_file(self, formatter: SPDXMarkdown, tmp_path: Path):
        meta = formatter.get_metadata(str(tmp_path / "nonexistent.md"))
        assert meta.unreleased_start is None
        assert meta.latest_version_position is None

    def test_get_metadata_plain(self, formatter: SPDXMarkdown, tmp_path: Path):
        filepath = _make_config(tmp_path, "# Changelog\n\n## 0.4.0 (2026-06-08)\n")
        meta = formatter.get_metadata(filepath)
        assert meta.latest_version == "0.4.0"
        assert meta.latest_version_position == 2

    def test_get_metadata_with_frontmatter(
        self, formatter: SPDXMarkdown, tmp_path: Path, spdx_frontmatter_changelog
    ):
        filepath = _make_config(tmp_path, spdx_frontmatter_changelog)
        meta = formatter.get_metadata(filepath)
        assert meta.latest_version == "0.4.0"
        # offset=7, "## 0.4.0" is at clean line 3 → 3 + 7 = 10
        assert meta.latest_version_position == 10

    def test_get_metadata_frontmatter_does_not_leak_spdx_version(
        self, formatter: SPDXMarkdown, tmp_path: Path, spdx_frontmatter_changelog
    ):
        """Apache-2.0 in the frontmatter must NOT be parsed as a version."""
        filepath = _make_config(tmp_path, spdx_frontmatter_changelog)
        meta = formatter.get_metadata(filepath)
        assert meta.latest_version == "0.4.0"
        assert "Apache" not in (meta.latest_version or "")

    def test_get_latest_full_release_no_file(
        self, formatter: SPDXMarkdown, tmp_path: Path
    ):
        result = formatter.get_latest_full_release(
            str(tmp_path / "nonexistent.md")
        )
        assert result.name is None
        assert result.index is None

    def test_get_latest_full_release_plain(
        self, formatter: SPDXMarkdown, tmp_path: Path
    ):
        filepath = _make_config(tmp_path, "# Changelog\n\n## 0.4.0 (2026-06-08)\n")
        result = formatter.get_latest_full_release(filepath)
        assert result.name == "0.4.0"
        assert result.index == 2

    def test_get_latest_full_release_with_frontmatter(
        self, formatter: SPDXMarkdown, tmp_path: Path, spdx_frontmatter_changelog
    ):
        filepath = _make_config(tmp_path, spdx_frontmatter_changelog)
        result = formatter.get_latest_full_release(filepath)
        assert result.name is not None
        # offset=7, title at clean line 3 → 3 + 7 = 10
        assert result.index is not None and result.index > 7


if __name__ == "__main__":
    import pytest

    raise SystemExit(pytest.main([__file__]))
