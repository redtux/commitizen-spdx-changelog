---
# SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
# SPDX-FileContributor: https://redtux.github.io/commitizen-spdx-changelog/credits/
#
# SPDX-License-Identifier: Apache-2.0

description: Automated doc generation from Google-style docstrings + type hints via mkdocstrings (Zensical-compatible)
icon: lucide/file-text
status: done
title: Plan 09 — Automated Doc Generation
---

Automate the generation of reference documentation from Python source code using
Google-style docstrings, type hints/annotations, and module-level comments via
[`mkdocstrings`][mkdocstrings] with
[`mkdocstrings-python`][mkdocstrings-python].

## Decision

Use **`mkdocstrings`** (not `annotated-doc`). Reason: `mkdocstrings` is
compatible with [Zensical] (the static site generator by the authors of MkDocs
Material, which we use instead of MkDocs), and supports Google-style docstrings
out of the box via the Python handler. Zensical provides preliminary
mkdocstrings support as of version 0.0.11 ([docs][zensical-mkdocstrings]).

## Goal

Eliminate manual authoring of API/CLI reference docs by extracting them directly
from the source. Generated docs should be REUSE-compliant and compatible with
the existing SPDX changelog setup.

## Prerequisite: enrich docstrings

The existing docstrings in the source code are minimal (e.g. one-line module
docstrings, short class descriptions). Before mkdocstrings can render useful API
reference pages, every public symbol must have a proper Google-style docstring:

| Symbol                    | File                          | What to add                                    |
| ------------------------- | ----------------------------- | ---------------------------------------------- |
| `SPDXMarkdown` class      | `formatters/spdx_markdown.py` | Full class docstring (parameters, attributes)  |
| `_strip_frontmatter`      | `formatters/spdx_markdown.py` | Args/returns for the function                  |
| `_SPDXMarkdownImpl` class | `formatters/_impl.py`         | Method docstrings for overrides                |
| Module docstrings         | All `.py` files               | Expand to Google-style (summary + description) |

## `mkdocstrings` integration with Zensical

[`mkdocstrings`][mkdocstrings] renders API reference documentation from source
code docstrings. [`mkdocstrings-python`][mkdocstrings-python] is the Python
handler that supports Google-style docstrings.

### Installation

Added to `[dependency-groups] dev` in `pyproject.toml`:

```text
"mkdocstrings-python>=2.0.5",
```

### Configuration for Zensical

Add to `zensical.toml`:

```toml
[project.plugins.mkdocstrings.handlers.python]
inventories = ["https://docs.python.org/3/objects.inv"]
paths = ["src"]

[project.plugins.mkdocstrings.handlers.python.options]
docstring_style = "google"
heading_level = 3
inherited_members = true
show_root_full_path = false
show_root_heading = true
show_source = false
```

Key options:

- `docstring_style` — `"google"` (we use Google style).
- `heading_level` — heading level for root API entries (3 = `<h3>`).
- `inherited_members` — include inherited methods in the docs.
- `show_root_full_path` — omit the full dotted path prefix on root headings.
- `show_root_heading` — render a visible heading for the documented symbol
    (defaults to `false`, which was the root cause of invisible headings on
    first attempt).
- `show_source` — whether to display the source code link.
- `paths` — directories to search for Python modules (relative to project root).
- `inventories` — intersphinx inventories for cross-referencing (e.g. Python
    stdlib).

> **Note:** Source files outside the `docs/` parent directory are not watched
> for live-reload by Zensical's file agent. The `src/` directory works because
> it is at the project root alongside `docs/`. See the
> [Zensical mkdocstrings page][zensical-mkdocstrings] for details.

### Example usage in a Markdown page

Create `docs/api.md` with a bare `:::` block (no inline YAML options):

```markdown
::: commitizen_spdx_changelog.formatters.spdx_markdown.SPDXMarkdown
```

This renders the full API reference for `SPDXMarkdown` inline in the page. All
handler and option configuration is inherited from `zensical.toml`.

**mdformat caveat**: `:::` blocks with inline YAML (e.g. `handler: python`,
`options:`) get mangled by mdformat because it treats them as regular paragraphs
and collapses multi-line indented options. Use bare identifiers only — any
per-block customisation must go through the global `zensical.toml` config.

**Underscore escape**: mdformat escapes lone underscores in `:::` paths,
breaking references to private symbols (e.g. `::_impl` becomes `:\_impl`). The
workaround is to not document private API entry points via `:::` — instead,
document the public wrapper class whose docstring covers the implementation.

## Implementation steps

1. **Enrich docstrings.** Write Google-style docstrings for every public symbol
    (see prerequisite table above).
2. **Install `mkdocstrings-python`.** Add to dev dependency group.
3. **Configure in `zensical.toml`.** Add the `[project.plugins.mkdocstrings]`
    section with Python handler settings (Google style, `paths = ["src"]`,
    `inherited_members = true`, `show_source = false`).
4. **Create `docs/api.md`.** Insert a bare `:::` block referencing
    `commitizen_spdx_changelog.formatters.spdx_markdown.SPDXMarkdown`.
5. **Add nav entry.** Add `{ "API Reference" = "api.md" }` to the `nav` list in
    `zensical.toml`.
6. **Discover `show_root_heading`.** Initially documentation appeared to
    produce no output — the root cause was `show_root_heading` defaulting to
    `false`. Without it, mkdocstrings renders the docstring content without
    any visible heading, making the page appear empty. Enable
    `show_root_heading = true` and `show_root_full_path = false`.
7. **Fix mdformat compatibility.** mdformat collapses multi-line options inside
    `:::` blocks and escapes underscores. Switch to bare identifiers and
    remove inline YAML options — all configuration moves to `zensical.toml`.
8. **Expand `SPDXMarkdown` docstring.** Since `_SPDXMarkdownImpl` is private
    and its `:::` path is broken by mdformat's underscore escaping, document
    the implementation architecture (lazy loading, overridden methods) in the
    public `SPDXMarkdown` docstring instead.
9. **Integrate with CI.** Add a `docs` job in `.github/workflows/ci.yaml` that
    builds the Zensical site and fails if docs are out of date.
10. **Verify end-to-end.** Run `make docs-build` and confirm API reference pages
    render correctly and REUSE compliance is maintained.

## Tasks

- [x] **Enrich docstrings.** Write Google-style docstrings for `SPDXMarkdown`,
    `_SPDXMarkdownImpl`, `_strip_frontmatter`, and all module docstrings
    (`hello()` was removed from `__init__.py` instead).
- [x] **Install `mkdocstrings-python`.** Add to `[dependency-groups] dev` in
    `pyproject.toml`.
- [x] **Configure in `zensical.toml`.** Add Python handler with Google docstring
    style, `paths = ["src"]`, `inherited_members = true`, `show_source = false`.
- [x] **Create `docs/api.md`.** Insert bare `:::` block referencing
    `commitizen_spdx_changelog.formatters.spdx_markdown.SPDXMarkdown`.
- [x] **Add nav entry.** Include `{ "API Reference" = "api.md" }` in the `nav`
    list.
- [x] **Fix `show_root_heading`.** Enable `show_root_heading = true` and
    `show_root_full_path = false` to make root symbol headings visible.
- [x] **Fix mdformat compatibility.** Remove inline YAML from `:::` blocks; move
    all configuration to global `zensical.toml`. Note: mdformat escapes
    underscores in paths, so private symbols (`_impl`) cannot use `:::`.
- [x] **Expand `SPDXMarkdown` docstring.** Document lazy-loading architecture,
    `_SPDXMarkdownImpl`, and both overridden methods — covers private
    implementation details that cannot have their own `:::` block.
- [x] **Integrate with CI.** Add a `docs` job that builds with Zensical and runs
    markdown linting.
- [x] **Verify end-to-end.** Run `make docs-build` and confirm API reference
    pages render correctly.

## Dependencies

- Docstring enrichment — standalone, no external dependencies.
- `mkdocstrings-python` available on PyPI.
- `zensical` installed (already in dev dependencies).
- Python 3.13+.

## Acceptance

- [x] Google-style docstrings written for all public symbols.
- [x] `mkdocstrings-python` installed and configured in `zensical.toml`.
- [x] API reference pages render Google-style docstrings correctly.
- [x] docs build succeeds with `make docs-build` — no mkdocstrings errors.
- [x] Generated pages maintain SPDX frontmatter (host pages already have
    headers; mkdocstrings output inherits them).
- [x] CI docs job passes (build succeeds).

## See also

- [Plan 06 — CI/CD](06-ci-cd.md) (CI workflow to extend with docs job)
- [Plan 08 — Release](08-release.md)
- [Zensical mkdocstrings setup][zensical-mkdocstrings]
- [Zensical — static site generator][zensical]
- [`mkdocstrings` — documentation][mkdocstrings]
- [`mkdocstrings-python` — Python handler][mkdocstrings-python]
- [`griffe` — Python struct-doc extraction][griffe]
- [Napoleon — Google/NumPy style docstring support][napoleon]

[griffe]: https://mkdocstrings.github.io/griffe/
[mkdocstrings]: https://mkdocstrings.github.io/
[mkdocstrings-python]: https://mkdocstrings.github.io/python/
[napoleon]: https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
[zensical]: https://zensical.org
[zensical-mkdocstrings]: https://zensical.org/docs/setup/extensions/mkdocstrings/
