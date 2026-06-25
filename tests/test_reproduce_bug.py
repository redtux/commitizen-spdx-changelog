#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
# SPDX-FileContributor: https://redtux.github.io/commitizen-spdx-changelog/credits/
#
# SPDX-License-Identifier: Apache-2.0

"""Subprocess smoke tests for ``scripts/reproduce_bug.py``.

Every test runs the script in a subprocess and checks for expected
output markers such as ``BUG CONFIRMED`` and the false version ``2.0``.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = Path("scripts", "reproduce_bug.py")


def _run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )


class TestReproduceBug:
    """Verify each step of the bug reproduction script."""

    def test_step3_reproduces_bug(self):
        """Step 3 must detect the false version '2.0' from Apache-2.0."""
        result = _run("--step", "3", "--unattended")
        assert result.returncode == 0, result.stderr
        assert "BUG CONFIRMED" in result.stdout
        assert "2.0" in result.stdout
        # clean up temp files created by step 3
        _run("--clean")

    def test_step3_clean_after_run(self):
        """--clean should succeed even after a prior --clean."""
        _run("--step", "3", "--unattended")
        result = _run("--clean")
        assert result.returncode == 0, result.stderr
        assert "Removed" in result.stdout or "Nothing to clean" in result.stdout

    def test_step1_runs_without_error(self):
        """Step 1 must complete successfully and confirm the bug."""
        result = _run("--step", "1", "--unattended")
        assert result.returncode == 0, result.stderr
        assert "BUG CONFIRMED" in result.stdout

    def test_step2_runs_without_error(self):
        """Step 2 must complete successfully and confirm the bug."""
        result = _run("--step", "2", "--unattended")
        assert result.returncode == 0, result.stderr
        assert "BUG CONFIRMED" in result.stdout

    def test_all_steps_unattended(self):
        """Run all steps in unattended mode."""
        result = _run("--unattended")
        assert result.returncode == 0, result.stderr

    def test_clean_flag_idempotent(self):
        """``--clean`` must succeed even on a clean state."""
        result = _run("--clean")
        assert result.returncode == 0, result.stderr


if __name__ == "__main__":
    import pytest

    raise SystemExit(pytest.main([__file__]))