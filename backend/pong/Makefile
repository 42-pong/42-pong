SEPARATOR = @echo "----------------------------------------------"

.PHONY: all
all: check

.PHONY: check
check:
	@make -s lint
	$(SEPARATOR)
	@make -s formatcheck
	$(SEPARATOR)
	@make -s typecheck
	$(SEPARATOR)

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

.PHONY: formatcheck
formatcheck:
	@ruff format --check .
	@ruff check --select I .

# -------------------------------------------------------
# static type checker
# -------------------------------------------------------
.PHONY: typecheck
typecheck:
	@mypy .

# -------------------------------------------------------
# test
# -------------------------------------------------------
.PHONY: unit-test
unit-test:
	@python manage.py test -v2
