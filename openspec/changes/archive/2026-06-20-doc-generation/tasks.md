<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>

SPDX-License-Identifier: Apache-2.0
-->

## 1. Enrich docstrings

- [x] 1.1 Write Google-style module docstrings for all
    `src/commitizen_spdx_changelog/*.py`
- [x] 1.2 Write Google-style class/function docstrings for `SPDXMarkdown`,
    `_strip_frontmatter`, `_SPDXMarkdownImpl`, `hello()`

## 2. Install and configure mkdocstrings

- [x] 2.1 Add `mkdocstrings-python` to dev dependencies with
    `uv add --dev mkdocstrings-python`
- [x] 2.2 Add `[project.plugins.mkdocstrings]` section to `zensical.toml`

## 3. Add `:::` directives

- [x] 3.1 Create `docs/api.md` with mkdocstrings `:::` blocks for public
    modules/classes
- [x] 3.2 Add `api.md` to `zusical.toml` nav

## 4. Update plans and specs

- [x] 4.1 Update `docs/plans/09-doc-generation.md`: mark all tasks done, set
    `status: done`
- [x] 4.2 Archive the change via `openspec archive --yes`
- [x] 4.3 Sync delta specs to main specs via `openspec sync`
- [x] 4.4 Update `openspec/specs/plan-09-doc-generation/spec.md Purpose` if
    placeholder text appears

## 5. Verify and format

- [x] 5.1 Run `make docs-format && make reuse`
- [x] 5.2 Run `make docs-build` to verify end-to-end
