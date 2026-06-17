<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>

SPDX-License-Identifier: Apache-2.0
-->

# AGENTS.md — commitizen-spdx-changelog

## Commands

| Action                  | Command                                                 |
| ----------------------- | ------------------------------------------------------- |
| Install dev deps        | `uv sync --group dev`                                   |
| Run tests               | `uv run pytest -v`                                      |
| Run single test file    | `uv run python tests/test_spdx_markdown.py -v`          |
| Build docs              | `make docs-build`                                       |
| Format markdown         | `make docs-format`                                      |
| Lint markdown           | `make docs-lint`                                        |
| Serve docs              | `make docs-serve`                                       |
| REUSE annotation        | `make reuse`                                            |
| Bump & changelog        | `cz bump --changelog`                                   |
| Build distribution      | `uv build`                                              |
| Format .opencode/ files | `uv run mdformat .opencode/commands/ .opencode/skills/` |

No standalone linter or typecheck script — `ruff` runs only via `mdformat-ruff`
(markdown code fences). `pyright` config exists in `pyproject.toml` but has no
wired command.

## Architecture

Single-package Python project at `src/commitizen_spdx_changelog/`.

**Circular-import workaround**: The entry point
(`spdx_markdown.py:SPDXMarkdown`) defines the class BEFORE any commitizen
import. The real implementation in `_impl.py` (`_SPDXMarkdownImpl(Markdown)`) is
imported lazily inside `__new__`. This allows commitizen's entry-point scanner
to find the class without triggering a circular import.

Only two methods override the parent `Markdown` changelog format:
`get_metadata()` and `get_latest_full_release()`. Both strip `---`-delimited
YAML frontmatter, delegate to `*_from_file`, then shift returned line indices by
the frontmatter line count.

**Entry point** (in `pyproject.toml`):
`spdx-markdown = "commitizen_spdx_changelog.formatters.spdx_markdown:SPDXMarkdown"`

## Conventions

- **SPDX/REUSE header on every file**

    <!-- REUSE-IgnoreStart -->

    - `SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>`
    - `SPDX-License-Identifier: Apache-2.0`

    <!-- REUSE-IgnoreEnd -->

- **EditorConfig**: `indent_size=2` (except `.py`=4, `.toml`=4),
    `insert_final_newline=false`, `trim_trailing_whitespace=false` (non-default)

- **Commit convention**: `cz_conventional_commits` with
    `major_version_zero=true`

- **mdformat-mkdocs bug**: bare ``` `` ``` (no language label) causes HTML
    validation error → always use \`\`\` `` text`  `` for unlabeled blocks

- **Reference links**: `[label][ref]` in body; orphan refs pruned by mdformat

- **mdformat-gfm**: does not recognize `a.`/`b.`/`c.` as list markers → use
    `- **a.**` / `- **b.**` to keep nesting

## Post-edit checklist

After editing any markdown file or updating OpenSpec changes, run:

```
make docs-format
make reuse
```

**Note**: `make docs-format` does NOT cover `.opencode/` files — format those
separately with `uv run mdformat .opencode/commands/ .opencode/skills/`.

## OpenSpec workflow

1. **Create change** — `/opsx-propose <name>` or manually
2. **Commit** the new artifacts
3. **Implement** — work through each task in the change
4. **Mark tasks done** — update `- [ ]` → `- [x]` in the tasks file after each
5. **Verify** — run tests, docs-build, REUSE check
6. **Ask for approval** — stop and present the result for review
7. **Commit** the implementation changes
8. **Archive** — `openspec archive <name> --yes`
9. **Update specs** — update `openspec/specs/*/spec.md Purpose` if placeholder
    text appears after archive

**IMPORTANT**: Do NOT skip the approval step (step 6). Implementation should
always pause for user confirmation before committing and archiving.

## OpenSpec

- Always use `openspec archive --yes` to archive changes (non-interactive) — do
    NOT `mv` manually, or delta specs will not be synced to `openspec/specs/`.
- 5 slash commands in `.opencode/commands/` and 5 skills in `.opencode/skills/`.
- **After archive/sync**: Check `openspec/specs/*/spec.md` for
    `TBD - created by   archiving change … Update Purpose after archive.`
    placeholders and replace them with a concise purpose paragraph describing
    the capability.

## mkdocstrings `:::` blocks and mdformat

mdformat treats `:::` blocks (mkdocstrings syntax) as regular paragraphs and
collapses multi-line YAML options. **To keep `:::` blocks intact:**

- Put the full identifier on a single line (under 80 chars)
- Omit inline YAML options — rely on global config in
    `[project.plugins.mkdocstrings]` in `zensical.toml`
- Do NOT use `<!-- mdformat off -->` / `<!-- mdformat on -->` — it does not
    protect `:::` content from mdformat paragraph reflow
