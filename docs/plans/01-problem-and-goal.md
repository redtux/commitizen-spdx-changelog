---
# SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
# SPDX-FileContributor: https://redtux.github.io/commitizen-spdx-changelog/credits/
#
# SPDX-License-Identifier: Apache-2.0

description: Confirm the bug, document root cause, align on the plugin approach
icon: lucide/flag
status: done
title: Plan 01 — Problem and Goal
---

## Context

Commitizen's built-in `Markdown` changelog format has no YAML frontmatter
awareness. The `RE_TITLE` regex matches `#` lines inside frontmatter as
headings, causing `search_version` to extract false versions (e.g. `2.0` from
`Apache-2.0`). Upstream declined a hardcoded fix
([woile's response][woile-comment]) — the recommended path is a custom
`commitizen.changelog_format` plugin.

See [`docs/changelog.md`](../changelog.md) for the affected file and
[issue #2014][#2014] for the full discussion.

## Tasks

- [x] **Reproduce the bug.** Run `cz bump --dry-run --changelog` against
    `docs/changelog.md` and confirm `NoRevisionError` (exit code 16) or false
    version detection.
    - See `scripts/reproduce_bug.py` for reproduction.
- [x] **Confirm upstream position.** Issue #2014 is closed; woile's comment
    directs users to create a custom plugin — no fix expected upstream.
- [x] **Document root cause.** Added summary of why `RE_TITLE` matches `#`
    inside frontmatter and how `search_version` extracts `2.0` from
    `Apache-2.0`.
    - See `scripts/reproduce_bug.py` docstring and Step 1 output.
- [x] **Sign off on plugin approach.** Confirmed — custom
    `commitizen.changelog_format` entry point is the agreed path forward.
- [x] **Read upstream docs and templates.** Reviewed the
    [changelog template customization][changelog-template],
    [config file customization][config-file],
    [Python class customization][python-class], and
    [cookiecutter template][cookiecutter] — summarized in reproduction script.
- [x] **Read BaseFormat and Markdown sources.** Reviewed ([base-source],
    [markdown-source]) to understand the override points before Plan 02.

## Dependencies

- git repo with a commitizen-managed changelog containing SPDX frontmatter
- `commitizen>=3.0` installed locally (venv or `uv tool`)

## Acceptance

- [x] Bug reproduced and confirmed
- [x] Upstream path is authoritatively closed
- [x] Plugin approach formally agreed by the team

## Next

→ Continue to [Plan 02 — Scaffolding](02-scaffolding.md)

## See also

- [Plan 02 — Scaffolding](02-scaffolding.md)
- [Plan 03 — Design](03-design.md)

## References

- [Issue #2014 — Markdown changelogs with YAML frontmatter][#2014]
- [Changelog Format Protocol source][format-protocol]
- [BaseFormat source][base-source]
- [Markdown format source][markdown-source]

<!-- References -->

[#2014]: https://github.com/commitizen-tools/commitizen/issues/2014
[base-source]: https://github.com/commitizen-tools/commitizen/blob/master/commitizen/changelog_formats/base.py
[changelog-template]: https://commitizen-tools.github.io/commitizen/customization/changelog_template/
[config-file]: https://commitizen-tools.github.io/commitizen/customization/config_file/
[cookiecutter]: https://github.com/commitizen-tools/commitizen_cz_template
[format-protocol]: https://github.com/commitizen-tools/commitizen/blob/master/commitizen/changelog_formats/__init__.py
[markdown-source]: https://github.com/commitizen-tools/commitizen/blob/master/commitizen/changelog_formats/markdown.py
[python-class]: https://commitizen-tools.github.io/commitizen/customization/python_class/
[woile-comment]: https://github.com/commitizen-tools/commitizen/issues/2014#issuecomment-4701012800
