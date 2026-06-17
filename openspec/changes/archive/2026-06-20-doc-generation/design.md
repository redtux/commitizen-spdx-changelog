<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>

SPDX-License-Identifier: Apache-2.0
-->

## Context

The project has no rendered API reference documentation. Source docstrings are
minimal: one-line module docstrings, short class/function summaries. The
Zensical SSG is already configured and working. mkdocstrings-python is the
standard Python handler for extracting Google-style docstrings into
Zensical/MkDocs pages.

## Goals / Non-Goals

**Goals:**

- All public symbols have Google-style docstrings (Args, Returns, Raises)
- `mkdocstrings-python` installed as a dev dependency
- `zensical.toml` configured with the Python handler
- API reference renders inline on existing docs pages via `:::` directives
- CI runs `make docs-build` to catch doc breakage

**Non-Goals:**

- No `scripts/docgen.py` or separate CLI reference generator (no public CLI)
- No redesign of the documentation site structure
- No docstring coverage in tests or CI enforcement beyond build success

## Decisions

| Decision                  | Choice                        | Rationale                                                                         |
| ------------------------- | ----------------------------- | --------------------------------------------------------------------------------- |
| Docstring style           | Google                        | Already chosen in plan, supported natively by mkdocstrings-python                 |
| `:::` directive placement | New `docs/api.md` page        | Keeps API reference separate from prose pages; nav entry added to `zensical.toml` |
| CI docs step              | `make docs-build` after tests | Fast feedback — docs build is cheap, catches broken `:::` refs                    |
| Spec update               | Delta spec with MODIFIED      | Only changes are removing scripts/docgen.py and updating the verify step          |

## Risks / Trade-offs

- **`show_source = false`** — users can't navigate from docs to source.
    Acceptable for a small plugin; re-enable if users request it.
- **Google-style docstrings are verbose for trivial symbols** — `hello()` only
    needs a one-liner, not full Args/Returns. Accepted: mkdocstrings handles
    short docstrings gracefully.
