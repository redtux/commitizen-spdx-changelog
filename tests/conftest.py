#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
# SPDX-FileContributor: https://redtux.github.io/commitizen-spdx-changelog/credits/
#
# SPDX-License-Identifier: Apache-2.0

"""Shared fixtures for the commitizen-spdx-changelog test suite.

The warm-up import of ``commitizen.changelog_formats`` must happen at
module level to break the circular-import cycle described in
:mod:`commitizen_spdx_changelog.formatters.spdx_markdown`.
"""

import pytest

import commitizen.changelog_formats  # noqa: F401  — warm up before plugin import


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
    """Changelog with no YAML frontmatter."""
    return """\
# Changelog

## 0.4.0 (2026-06-08)

### Feat

- Add something
"""


@pytest.fixture
def changelog_unclosed_frontmatter() -> str:
    """Changelog with a ``---`` that is never closed — treated as regular content."""
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
    """Empty string fixture for edge-case testing."""
    return ""
