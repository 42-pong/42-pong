SEPARATOR = @echo "----------------------------------------------"

.PHONY: all
all: check

.PHONY: check
check:
	@make -s lint
	$(SEPARATOR)
	@make -s format
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
