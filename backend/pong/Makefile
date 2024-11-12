.PHONY: all
all: check

.PHONY: check
check: lint format typecheck

# -------------------------------------------------------
# linter
# -------------------------------------------------------
.PHONY: lint
lint:
	@ruff check .

# -------------------------------------------------------
# formatter
# -------------------------------------------------------
.PHONY: format
format:
	@ruff format . # black
	@ruff check --select I --fix . # isort

# -------------------------------------------------------
# static type checker
# -------------------------------------------------------
.PHONY: typecheck
typecheck:
	@mypy .
