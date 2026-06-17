# SPDX-FileCopyrightText: 2026 Pablo Hörtner <redtux@pm.me>
#
# SPDX-License-Identifier: Apache-2.0

.PHONY: devbox-update devbox-upgrade docs-build docs-format help docs-lint docs-serve reuse test uv-venv uv-sync

help:
	@echo "Available targets:"
	@echo "  devbox-update  	  Update devbox packages"
	@echo "  devbox-upgrade 	  Update devbox version"
	@echo "  docs-build   		  Build documentation site with zensical"
	@echo "  docs-format  		  Format Markdown files with mdformat"
	@echo "  docs-lint    		  Lint Markdown files with mdformat"
	@echo "  docs-serve   		  Serve documentation site locally with zensical"
	@echo "  help         		  Show this help message"
	@echo "  reuse        		  Run REUSE compliance check"
	@echo "  test         		  Run test suite with pytest"
	@echo "  uv-sync      		  Sync dependencies with uv"
	@echo "  uv-venv      		  Create/update uv virtual environment"

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

reuse:
	@uv run reuse annotate \
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

uv-venv:
	@uv venv \
		--allow-existing \
		--quiet

devbox-update:
	@devbox update

devbox-upgrade:
	@devbox version update

docs-build:
	@uv run zensical build

docs-serve:
	@uv run zensical serve

uv-sync:
	@uv sync \
		--active \
		--all-extras \
		--all-groups \
		--all-packages \
		--system-certs \
		--upgrade
