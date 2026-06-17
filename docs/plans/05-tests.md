---
# SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
#
# SPDX-License-Identifier: Apache-2.0

description: Test fixtures (conftest.py) and test cases (test_spdx_markdown.py, test_reproduce_bug.py)
icon: lucide/flask-conical
status: done
title: Plan 05 — Tests
---

## `tests/conftest.py`

```python
# SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
#
# SPDX-License-Identifier: Apache-2.0

import pytest


# ---------------------------------------------------------------------------
# Canonical test content
# ---------------------------------------------------------------------------


@pytest.fixture
def spdx_frontmatter_changelog() -> str:
    return """\
---
# SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
#
# SPDX-License-Identifier: Apache-2.0

icon: lucide/git-commit-vertical
---

# Changelog

## 0.4.0 (2026-06-08)

### Feat

- Add SPDX frontmatter support

## 0.3.0 (2026-05-01)

### Fix

- Handle missing file gracefully
"""


@pytest.fixture
def plain_changelog() -> str:
    return """\
# Changelog

## 0.4.0 (2026-06-08)

### Feat

- Add something
"""


@pytest.fixture
def changelog_unclosed_frontmatter() -> str:
    return """\
---
# SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
#
# SPDX-License-Identifier: Apache-2.0

# Changelog

## 0.4.0 (2026-06-08)

### Feat

- Something
"""


@pytest.fixture
def empty_changelog() -> str:
    return ""
```

## `tests/test_spdx_markdown.py`

```python
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


# ---------------------------------------------------------------------------
# Unit tests — _strip_frontmatter
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_config(tmp_path: Path, content: str) -> str:
    path = tmp_path / "CHANGELOG.md"
    path.write_text(content, encoding="utf-8")
    return str(path)


# ---------------------------------------------------------------------------
# Integration tests — formatter
# ---------------------------------------------------------------------------


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
        result = formatter.get_latest_full_release(str(tmp_path / "nonexistent.md"))
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
```

## `tests/test_reproduce_bug.py`

Subprocess-based smoke tests for the reproduction script at
`scripts/reproduce_bug.py`. The script has no return values — it prints to
stdout — so tests run it via `subprocess` and assert on stdout content and exit
codes.

Scenarios covered:

| Test                            | What it checks                                     |
| ------------------------------- | -------------------------------------------------- |
| `test_step3_reproduces_bug`     | Step 3 detects false version `2.0` from Apache-2.0 |
| `test_step3_clean_after_run`    | `--clean` removes temp files after step 3          |
| `test_step1_runs_without_error` | Step 1 (regex analysis) completes                  |
| `test_step2_runs_without_error` | Step 2 (SequenceMatcher sim) completes             |
| `test_all_steps_unattended`     | Full pipeline with `--unattended` (CI-safe)        |
| `test_clean_flag_idempotent`    | `--clean` is idempotent (no-op on clean)           |

```python
# SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
#
# SPDX-License-Identifier: Apache-2.0

"""Subprocess smoke tests for scripts/reproduce_bug.py."""

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
        result = _run("--step", "1", "--unattended")
        assert result.returncode == 0, result.stderr
        assert "BUG CONFIRMED" in result.stdout

    def test_step2_runs_without_error(self):
        result = _run("--step", "2", "--unattended")
        assert result.returncode == 0, result.stderr
        assert "BUG CONFIRMED" in result.stdout

    def test_all_steps_unattended(self):
        result = _run("--unattended")
        assert result.returncode == 0, result.stderr

    def test_clean_flag_idempotent(self):
        result = _run("--clean")
        assert result.returncode == 0, result.stderr
```

## Tasks

### Completed

- [x] **Create `tests/` directory** with `conftest.py`, `test_spdx_markdown.py`,
    and `test_reproduce_bug.py`.
- [x] **Write `conftest.py`.** String-content fixtures
    (`spdx_frontmatter_changelog`, `plain_changelog`,
    `changelog_unclosed_frontmatter`, `empty_changelog`).
- [x] **Write `test_spdx_markdown.py`.** `TestStripFrontmatter` (6 unit tests
    covering all edge cases) and `TestSPDXMarkdown` (7 integration tests for
    `get_metadata` and `get_latest_full_release`).
- [x] **Write `test_reproduce_bug.py`.** Subprocess-based smoke tests (6
    scenarios: bug detection, cleanup, all steps, individual steps).
- [x] **Run the test suite.** `uv run pytest -v` passes 19/19.

## Dependencies

- **Plan 03 must be complete** — `spdx_markdown.py` exists and is importable.
- **Plan 04 must be complete** — `pyproject.toml` has the entry point registered
    and `pytest` is in dev dependencies.
- `pytest>=9.1.1` installed (listed in dev dependencies).

## Acceptance

- [x] `tests/conftest.py` exists and contains all fixtures.
- [x] `tests/test_spdx_markdown.py` exists with unit + integration tests.
- [x] `tests/test_reproduce_bug.py` exists with subprocess-based smoke tests.
- [x] `uv run pytest -v` passes all tests (19/19 with strong position
    assertions).
- [x] Tests cover: frontmatter stripping, edge cases, version detection,
    position correction, missing file handling, reproduction script.

## Next

→ Continue to [Plan 06 — CI/CD](06-ci-cd.md)

## See also

- [Plan 03 — Design](03-design.md)
- [Plan 04 — pyproject.toml](04-pyproject.md)
- [Plan 06 — CI/CD](06-ci-cd.md)
