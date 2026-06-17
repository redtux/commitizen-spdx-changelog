---
# SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
#
# SPDX-License-Identifier: Apache-2.0

description: REUSE compliance, license files, local smoke test, editable install verification
icon: lucide/shield
status: done
title: Plan 07 — REUSE Compliance and Local Smoke Test
---

## REUSE compliance

The package itself must be REUSE-compliant. Every source file needs an SPDX
header (as shown in all snippets). Provide the full license text:

```sh
mkdir -p LICENSES
curl -sL https://www.apache.org/licenses/LICENSE-2.0.txt \
    -o LICENSES/Apache-2.0.txt
```

Verify compliance locally:

```sh
uv run reuse lint
```

The package's own changelog (`docs/changelog.md`) carries the same YAML
frontmatter with SPDX headers — a nice self-hosting dogfood loop. (We use
`docs/changelog.md` instead of the conventional `CHANGELOG.md` so it embeds in
the documentation site; the path is configurable via `changelog_file` in
`pyproject.toml`.)

## Local smoke test

After installing in editable mode, verify the entry point is visible to
commitizen and that a dry-run bump works end-to-end:

```sh
# Editable install into the project venv
uv pip install -e .

# Confirm the entry point is registered
python -c "
from importlib.metadata import entry_points
eps = {ep.name: ep.value for ep in entry_points(group='commitizen.changelog_format')}
print(eps)
# Expected: {'markdown': '...', 'spdx-markdown': 'commitizen_spdx_changelog...'}
"

# Dry-run bump against the project's own changelog (docs/changelog.md)
cz bump --dry-run --changelog --yes
# Confirm: no false version detection, insertion point is after the frontmatter.
# --yes is required for the first tag confirmation prompt (no git tags yet).
```

## Tasks

### Completed

- [x] **Download the Apache 2.0 license text.** `LICENSES/Apache-2.0.txt`
    exists.
- [x] **Add SPDX headers to all source files.** Every `.py`, `.md`, `.toml`,
    `.yml`, `.yaml`, `.sh`, `.cfg`, `.editorconfig`, `.gitignore`, and
    `.python-version` file has SPDX headers.
- [x] **Verify REUSE compliance.** `uv run reuse lint` passes with 77/77 files.
- [x] **Editable install.** `uv pip install -e .` succeeds.
- [x] **Verify entry point registration.** `spdx-markdown` is visible in
    `commitizen.changelog_format` entry points.
- [x] **Dry-run bump.** `cz bump --dry-run --changelog --yes` succeeds and
    increments `0.0.1 → 0.1.0` (MINOR, `feat:` commit).

### Remaining

(All tasks complete.)

## Dependencies

- **Plan 06 must be complete** — CI workflows are in place.
- `reuse` tool installed (in dev dependencies).
- `commitizen>=4.16.3` installed (in runtime dependencies).
- `curl` or `wget` available.

## Acceptance

- [x] `LICENSES/Apache-2.0.txt` exists.
- [x] `uv run reuse lint` passes with zero errors.
- [x] `uv pip install -e .` succeeds.
- [x] Entry point `spdx-markdown` is visible via
    `importlib.metadata.entry_points`.
- [x] `cz bump --dry-run --changelog --yes` completes without `NoRevisionError`
    and bumps `0.0.1 → 0.1.0`.

## Next

→ Continue to [Plan 08 — Release](08-release.md)

## See also

- [Plan 06 — CI/CD](06-ci-cd.md)
- [Plan 08 — Release](08-release.md)
