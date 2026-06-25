#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
# SPDX-FileContributor: https://redtux.github.io/commitizen-spdx-changelog/credits/
#
# SPDX-License-Identifier: Apache-2.0

"""Integration tests for the commitizen SPDX-Markdown plugin.

Tests cold import (no circular imports), entry-point resolution,
and instanceof checks via real inheritance.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest
from commitizen.config.base_config import BaseConfig

from commitizen_spdx_changelog.formatters.spdx_markdown import (
    SPDXMarkdown,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


class TestColdImport:
    """Run imports in a fresh subprocess to verify no circular imports."""

    def _run(self, code: str) -> subprocess.CompletedProcess:
        env = os.environ.copy()
        src_dir = str(REPO_ROOT / "src")
        env["PYTHONPATH"] = (
            f"{src_dir}{os.pathsep}{env['PYTHONPATH']}"
            if "PYTHONPATH" in env
            else src_dir
        )
        return subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            env=env,
            timeout=10,
        )

    def test_cold_import_spdx_markdown(self):
        """Import must succeed in a cold process."""
        code = (
            "import commitizen.changelog_formats; "
            "from commitizen_spdx_changelog.formatters.spdx_markdown "
            "import SPDXMarkdown"
        )
        result = self._run(code)
        assert result.returncode == 0, (
            f"Cold import failed:\n{result.stderr}"
        )

    def test_cold_instantiate_and_isinstance(self):
        """Instantiate SPDXMarkdown and verify isinstance in a cold process.

        The warm-up import (commitizen.changelog_formats) is required to
        avoid a circular import when our plugin module is the first thing
        to touch commitizen's changelog formats registry. See
        ``docs/plans/11-direct-subclass.md`` for details.
        """
        code = (
            "import commitizen.changelog_formats; "
            "from commitizen.config.base_config import BaseConfig; "
            "from commitizen_spdx_changelog.formatters.spdx_markdown "
            "import SPDXMarkdown; "
            "config = BaseConfig(); "
            "config.update({'encoding': 'utf-8'}); "
            "f = SPDXMarkdown(config); "
            "assert isinstance(f, SPDXMarkdown), 'isinstance(SPDXMarkdown) is False'; "
            "print('isinstance:', isinstance(f, SPDXMarkdown))"
        )
        result = self._run(code)
        assert result.returncode == 0, (
            f"Cold instantiation failed:\n{result.stderr}"
        )
        assert "isinstance: True" in result.stdout


class TestSPDXMarkdownIsInstance:
    """Verify isinstance checks in the same process (after warm-up)."""

    @pytest.fixture
    def formatter(self):
        config = BaseConfig()
        config.update({"encoding": "utf-8"})
        return SPDXMarkdown(config)

    def test_isinstance_spdx_markdown(self, formatter: SPDXMarkdown):
        assert isinstance(formatter, SPDXMarkdown)

    def test_isinstance_markdown_base(self, formatter: SPDXMarkdown):
        from commitizen.changelog_formats.markdown import Markdown

        assert isinstance(formatter, Markdown)


if __name__ == "__main__":
    sys.exit(pytest.main([__file__]))
