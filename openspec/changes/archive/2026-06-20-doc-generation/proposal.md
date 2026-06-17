<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>

SPDX-License-Identifier: Apache-2.0
-->

## Why

The project's API reference documentation exists only as implied by the source
code — there is no rendered API doc page. Docstrings are minimal (one-line
module/class summaries). Every change to the source requires manual doc updates.
mkdocstrings extracts docs directly from Google-style docstrings, eliminating
drift between code and documentation.

## What Changes

- Add `mkdocstrings-python` to dev dependencies
- Configure `[project.plugins.mkdocstrings]` in `zensical.toml`
- Enrich docstrings in all source `*.py` files (Google style)
- Add `:::` directives to docs pages
- Add `make docs-build` step to `ci.yaml`
- Update `docs/plans/09-doc-generation.md` status to `done` and complete all
    tasks
- Update `openspec/specs/plan-09-doc-generation/spec.md` — remove
    `scripts/docgen.py` and `uv run docgen` from requirements

## Capabilities

### New Capabilities

*(None — all work falls under the existing plan-09-doc-generation scope.)*

### Modified Capabilities

- `plan-09-doc-generation`: Requirement "tasks SHALL contain ... create
    scripts/docgen.py, add uv run docgen entry point" replaced with docstring
    enrichment prerequisite. Requirement "tasks SHALL contain ... verify
    end-to-end" updated to use `make docs-build` instead of `zensical build`.

## Impact

- `pyproject.toml`: dev dependency added
- `zensical.toml`: mkdocstrings plugin section added
- `src/commitizen_spdx_changelog/*.py`: docstrings enriched
- `docs/`: `:::` mkdocstrings directives added to doc pages
- `.github/workflows/ci.yaml`: docs-build step added
- `openspec/specs/plan-09-doc-generation/spec.md`: requirements updated
- `docs/plans/09-doc-generation.md`: status updated, tasks marked complete
