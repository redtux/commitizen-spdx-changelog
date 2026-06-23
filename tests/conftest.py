#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
#
# SPDX-License-Identifier: Apache-2.0

import commitizen.changelog_formats  # noqa: F401  — warm up before plugin import

import pytest


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
