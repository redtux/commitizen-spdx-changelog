<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>

SPDX-License-Identifier: Apache-2.0
-->

# AGENTS.md — commitizen-spdx-changelog

## Commands

| Action                  | Command                                        |
| ----------------------- | ---------------------------------------------- |
| Install dev deps        | `uv sync --group dev`                          |
| Run tests               | `uv run pytest -v`                             |
| Run single test file    | `uv run python tests/test_spdx_markdown.py -v` |
| Build docs              | `make docs-build`                              |
| Format markdown         | `make docs-format`                             |
| Format Python code      | `make py-format`                               |
| Lint markdown           | `make docs-lint`                               |
| Lint Python code        | `make py-lint`                                 |
| Serve docs              | `make docs-serve`                              |
| REUSE annotation        | `make reuse`                                   |
| Bump & changelog        | `cz bump --changelog`                          |
| Build distribution      | `uv build`                                     |
| Format .opencode/ files | `uv run mdformat .opencode/{commands,skills}`  |

No standalone linter or typecheck script — `ruff` runs only via `mdformat-ruff`
(markdown code fences). `pyright` config exists in `pyproject.toml` but has no
wired command.

## Commit rules

Uses commitizen `cz_conventional_commits` with `major_version_zero=true`.

Format: `<type>(<scope>): <subject>`.

### Subject

Max 52 chars including the `type(scope):` prefix. Run
`cz commit --message-length-limit 52` to enforce it.

### Body

Always include a body, structured in three parts:

1. **Opening paragraph** — what this commit does and why, in plain English.
2. **Bullet details** — all bullets in a single `-m` flag, separated by
    newlines.
3. **Footer** — reference to related issue or PR when applicable.

```sh
git commit <file> \
    -m "type(scope): subject" \
    -m "Paragraph describing what and why." \
-m "- Bullet describing a key change
- Another bullet
- Third bullet if needed, each wrapping naturally" \
    -m "Ref: #X"
```

Use `-F tmp/msg` instead of inline `-m` when the message contains backticks or
dynamic content (see [Shell backticks](#shell-backticks-in-cli-args) below).

### OpenSpec commits

| Action          | Commit message template                     |
| --------------- | ------------------------------------------- |
| Create change   | `docs(openspec): create <change-id> change` |
| Create spec     | `docs(openspec): create '<spec-name>' spec` |
| Mark tasks done | `docs(openspec): mark <change-id> done`     |
| Archive         | `chore(openspec): archive <change-id>`      |

Every file must carry a [SPDX/REUSE header](#conventions). See the Conventions
section above for the exact format.

## Architecture

Single-package Python project at `src/commitizen_spdx_changelog/`.

**Circular-import avoidance**: The `SPDXMarkdown` class directly inherits from
`commitizen.changelog_formats.markdown.Markdown`. A warm-up import in
`tests/conftest.py` initializes `commitizen.changelog_formats` before any test
module imports the plugin, preventing the circular-import cycle that would
otherwise occur if the plugin module is the first to touch commitizen's
entry-point-loading machinery.

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

- **mkdocstrings `:::` blocks**: mdformat treats `:::` blocks (mkdocstrings
    syntax) as regular paragraphs and collapses multi-line YAML options. To keep
    `:::` blocks intact, put the full identifier on a single line (under
    80 chars), omit inline YAML options, and do NOT use `<!-- mdformat off -->`
    / `<!--   mdformat on -->`.

## Constraints

### Shell backticks in CLI args

- **Problem**: Agent uses backticks `` ` `` inside `--body`, `-m`, or similar
    inline string arguments.
- **Consequence**: Bash interprets backticks as command substitution →
    malformed/broken issues, PRs, and commits.
- **Rule**: Always write content to a file first with
    `cat > tmp/<file> <<'EOF'`, then use file-based flags (`--body-file` for
    `gh`, `-F` for `git commit`, etc.).

### Directory permissions

- **Problem**: Agent writes to `/tmp/` or other paths outside the workspace
    without verifying permissions.
- **Consequence**: Security risk; operation is silently denied.
- **Rule**: Use `tmp/` at the project root (`<project-root>/tmp/`). Create with
    `mkdir -p tmp/` before first use. `/tmp/` is always denied — never use it.

### Tool permissions

- **Problem**: Agent attempts bash commands, file operations, or external
    directory access without checking `opencode.jsonc` first.
- **Consequence**: `deny` items are rejected without warning; `ask` items block
    execution until user approves.
- **Rule**: Check `opencode.jsonc` permission block before any operation.

## OpenSpec

### Workflow

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

### Notes

- Always use `openspec archive --yes` to archive changes (non-interactive) — do
    NOT `mv` manually, or delta specs will not be synced to `openspec/specs/`.
- 5 slash commands in `.opencode/commands/` and 5 skills in `.opencode/skills/`.
- **After archive/sync**: Check `openspec/specs/*/spec.md` for
    `TBD - created by   archiving change … Update Purpose after archive.`
    placeholders and replace them with a concise purpose paragraph describing
    the capability.

## Post-edit checklist

After editing any file, run:

```sh
make py-format
make docs-format
make reuse
make py-lint
make docs-lint
```

**Note**: `make docs-format` and `make docs-lint` do NOT cover `.opencode/`
files — format those separately with
`uv run mdformat .opencode/commands/ .opencode/skills/`.
