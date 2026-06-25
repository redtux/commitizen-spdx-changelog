---
# SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
# SPDX-FileContributor: https://redtux.github.io/commitizen-spdx-changelog/credits/
#
# SPDX-License-Identifier: Apache-2.0

description: Release process — publish to PyPI via GitHub Actions and commitizen
icon: lucide/rocket
status: pending
title: Plan 08 — Release
---

Once the package passes REUSE compliance and smoke tests, release it to PyPI.

## Release process

1. **Bump version and generate changelog** via `cz bump --changelog`. This
    creates a `v*` git tag, updates `[project] version` and
    `[tool.commitizen] version` in `pyproject.toml`, and writes the release to
    `docs/changelog.md`.
2. **Push the tag** — the `v*` tag triggers the `publish.yaml` workflow.
3. **Workflow builds and publishes** to PyPI via OIDC trusted publishing
    (`pypa/gh-action-pypi-publish`).

## Prerequisites

### `.github/workflows/publish.yaml`

Plan 06 describes this workflow but the file was never written to disk. Create
it before the first release:

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

### PyPI Trusted Publisher

Register `.github/workflows/publish.yaml` with environment `pypi` in PyPI
account settings for the `commitizen-spdx-changelog` project. This must be done
before the first triggered release.

## Dry-run verification

Before the real release, confirm the bump works:

```sh
cz bump --dry-run --changelog --yes
```

Expected: version `0.0.1 → 0.1.0`, increment MINOR, changelog entry for the
initial `feat:` commit.

## Tasks

- [ ] **Create `.github/workflows/publish.yaml`.** Write the Publish workflow
    (see code block above).
- [ ] **Configure PyPI Trusted Publisher.** Register the workflow at
    `https://pypi.org/manage/account/publishing/` with environment `pypi`.
- [ ] **Dry-run bump.** Run `cz bump --dry-run --changelog --yes` one final time
    to confirm the release state.
- [ ] **Bump and release.** Run `cz bump --changelog` to create the `v0.1.0`
    tag, update `pyproject.toml`, and generate the changelog.
- [ ] **Push tag.** `git push --follow-tags` to trigger the publish workflow.
- [ ] **Verify release.** Confirm the package appears on PyPI and
    `pip install   commitizen-spdx-changelog` works.

## Dependencies

- **Plan 07 must be complete** — REUSE compliance passes, smoke test successful.
- PyPI account with trusted publishing configured.
- GitHub Actions enabled for the repository.
- `cz bump` succeeds (confirmed in Plan 07).

## Acceptance

- [ ] `.github/workflows/publish.yaml` exists and is correct.
- [ ] PyPI Trusted Publisher registered for the workflow.
- [ ] `cz bump` creates tag `v0.1.0` and updates version in `pyproject.toml`.
- [ ] `git push --follow-tags` triggers the publish workflow.
- [ ] Package is installable from PyPI via
    `pip install commitizen-spdx-changelog`.

## See also

- [Plan 06 — CI/CD](06-ci-cd.md) (CI workflow, publish workflow definition)
- [Plan 07 — REUSE and Smoke Test](07-reuse-and-smoke-test.md)
- [Plan 09 — Doc Generation](09-doc-generation.md)
- [PyPI Trusted Publishing docs](https://docs.pypi.org/trusted-publishers/)
- [`pypa/gh-action-pypi-publish`](https://github.com/marketplace/actions/pypi-publish)
