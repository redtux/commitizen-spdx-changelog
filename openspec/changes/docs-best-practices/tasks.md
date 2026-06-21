<!--
SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>

SPDX-License-Identifier: Apache-2.0
-->

## 1. Enhance docs landing page

- [ ] 1.1 Rewrite `docs/index.md` with a welcoming project overview and purpose
    statement
- [ ] 1.2 Add navigation table linking to all major docs pages with descriptions
- [ ] 1.3 Add reference to Google's Documentation Best Practices with link to
    styleguide
- [ ] 1.4 Run `make docs-format` and `make reuse` to verify compliance

## 2. Enhance API reference

- [ ] 2.1 Add introductory prose to `docs/api.md` explaining SPDXMarkdown
    purpose and relationship to commitizen's Markdown format
- [ ] 2.2 Add a usage example code block demonstrating configuration or
    invocation
- [ ] 2.3 Ensure mkdocstrings `:::` block documents all overridden methods
- [ ] 2.4 Run `make docs-format` and `make reuse` to verify compliance

## 3. Create usage guide

- [ ] 3.1 Create `docs/guide.md` with YAML frontmatter and a title
- [ ] 3.2 Add installation and setup section with copyable `uv` and `pip`
    commands
- [ ] 3.3 Add common workflows section covering `cz bump --changelog` and output
    inspection
- [ ] 3.4 Add debugging section explaining common issues and the reproduction
    script
- [ ] 3.5 Add release procedures section covering tagging and CI/CD publishing
- [ ] 3.6 Run `make docs-format` and `make reuse` to verify compliance

## 4. Polish changelog

- [ ] 4.1 Review `docs/changelog.md` for alignment with best practices and add
    minor improvements
- [ ] 4.2 Run `make docs-format` and `make reuse` to verify compliance

## 5. Final verification

- [ ] 5.1 Run full test suite: `uv run pytest -v`
- [ ] 5.2 Run `make docs-build` to verify docs render without errors
- [ ] 5.3 Review all changed files for consistency and welcoming tone
