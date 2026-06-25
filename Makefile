# SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
# SPDX-FileContributor: https://redtux.github.io/commitizen-spdx-changelog/credits/
#
# SPDX-License-Identifier: Apache-2.0

# Makefile
#
# This file is part of commitizen-spdx-changelog, a plugin
# for commitizen that generates changelogs in SPDX format.
#
# Run `make <target>` to execute a target. Run `make help` to list all targets.

.PHONY: devbox-update devbox-upgrade docs-build docs-format docs-lint \
  docs-serve py-format py-lint help reuse test uv-lock uv-sync uv-venv

help:
	@echo "Available targets:"
	@echo "  devbox-update  	  Update devbox packages"
	@echo "  devbox-upgrade 	  Update devbox version"
	@echo "  docs-build   		  Build documentation site with zensical"
	@echo "  docs-format  		  Format Markdown files with mdformat"
	@echo "  docs-lint    		  Lint Markdown files with mdformat"
	@echo "  docs-serve   		  Serve documentation site locally with zensical"
	@echo "  py-format    		  Format Python source files with ruff & ty"
	@echo "  py-lint      		  Lint Python source files with ruff & ty"
	@echo "  help         		  Show this help message"
	@echo "  reuse        		  Run REUSE compliance check"
	@echo "  test         		  Run test suite with pytest"
	@echo "  uv-lock      		  Update and commit uv.lock lockfile"
	@echo "  uv-sync      		  Sync dependencies with uv"
	@echo "  uv-venv      		  Create/update uv virtual environment"

devbox-update:
	@devbox update

devbox-upgrade:
	@devbox version update

docs-format:
	@uv run mdformat \
		AGENTS.md \
		README.md \
		docs/ \
		openspec/

docs-lint:
	@uv run mdformat --check \
		AGENTS.md \
		README.md \
		docs/ \
		openspec/

docs-build:
	@uv run zensical build

docs-serve:
	@uv run zensical serve

py-format:
	# Formatting src/ files with ruff
	@uv run ruff check src/ --fix --unsafe-fixes
	# Formatting src/ files with ty
	@uv run ty check src/ --fix
	# Formatting tests/ files with ruff
	@uv run ruff check tests/ --fix --unsafe-fixes
	# Formatting tests/ files with ty
	@uv run ty check tests/ --fix

py-lint:
	# Linting src/ files with ruff
	@uv run ruff check src/
	# Linting src/ files with ty
	@uv run ty check src/
	# Linting tests/ files with ruff
	@uv run ruff check tests/
	# Linting tests/ files with ty
	@uv run ty check tests/

reuse:
	@uv run reuse annotate \
		--contributor "https://redtux.github.io/commitizen-spdx-changelog/credits/" \
		--copyright "Pablo Hörtner <redtux@pm.me>" \
		--fallback-dot-license \
		--license Apache-2.0 \
		--merge-copyrights \
		--recursive \
		--skip-existing \
		--year 2026 . > /dev/null || \
		{ echo "reuse annotate failed (exit $$?)" >&2; exit 1; }
	@uv run reuse lint | glow

test:
	@uv run pytest -v

uv-lock:
	@uv lock
	git add uv.lock
	git commit -m "build(deps): update uv.lock"

uv-sync:
	@uv sync \
		--active \
		--all-extras \
		--all-groups \
		--all-packages \
		--system-certs \
		--upgrade

uv-venv:
	@uv venv \
		--allow-existing \
		--quiet