---
# SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
# SPDX-FileContributor: https://redtux.github.io/commitizen-spdx-changelog/credits/
#
# SPDX-License-Identifier: Apache-2.0

description: GitHub Actions CI and publish workflows
icon: lucide/refresh-cw
status: done
title: Plan 06 — GitHub Actions
---

## `.github/workflows/ci.yaml`

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.13', '3.14']
    steps:
      - uses: actions/checkout@v4

      - uses: astral-sh/setup-uv@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dev dependencies
        run: uv sync --group dev

      - name: Run tests
        run: uv run pytest -v

      - name: REUSE compliance check
        run: uv run reuse lint
```

## `.github/workflows/publish.yaml`

```yaml
name: Publish

on:
  push:
    tags: [v*]

jobs:
  publish:
    runs-on: ubuntu-latest
    environment: pypi
    permissions:
      id-token: write
    steps:
      - uses: actions/checkout@v4

      - uses: astral-sh/setup-uv@v5

      - name: Build distribution
        run: uv build

      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
```

> Configure a PyPI Trusted Publisher for `commitizen-spdx-changelog` under your
> PyPI account settings before the first release. The workflow file path to
> register is `.github/workflows/publish.yaml`, environment `pypi`.

## Tasks

- [x] **Create `.github/workflows/` directory.**
- [x] **Create `.github/workflows/ci.yaml`.** Test matrix (Python 3.13, 3.14),
    uv setup, test run, REUSE compliance check.
- [x] **Create `.github/workflows/publish.yaml`.** Tag-triggered (`v*`) publish
    with OIDC trusted publishing.

## Dependencies

- **Plan 05 must be complete** — tests pass and the package is functional.
- GitHub repository with `uv` support (astral-sh/setup-uv action).
- PyPI account with trusted publishing configured.

## Acceptance

- [x] `.github/workflows/ci.yaml` exists with the test matrix.
- [x] `.github/workflows/publish.yaml` exists with tag-triggered publish.
- [x] Workflow files pass YAML validation (no syntax errors).

## Next

→ Continue to [Plan 07 — REUSE and Smoke Test](07-reuse-and-smoke-test.md)

## See also

- [Plan 05 — Tests](05-tests.md)
- [Plan 07 — REUSE and Smoke Test](07-reuse-and-smoke-test.md)
