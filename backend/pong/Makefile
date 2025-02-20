SEPARATOR = @echo "----------------------------------------------"

# 定数
TESTCASE_DOESNOT_EXISTS = 5

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

# ARG:
#   アプリ名・ファイル名・クラス名・関数名などのテスト対象モジュールへのパス
# 形式:
#   make test ARG=<APP_NAME>.<TEST_DIRECTORY>.<TEST_FILE_NAME>.<TEST_CLASS_NAME>.<TEST_FUNCTION_NAME>
# 使用例:
#   make test ARG="accounts"
#   make test ARG="accounts.tests.serializers"
#   make test ARG="accounts.tests.serializers.test_user_serializer"
.PHONY: test
test:
	@if [ -z "$(ARG)" ]; then \
		echo "Running all tests..."; \
		python manage.py test -v2 --parallel; \
		pytest -v -n auto; \
	else \
		echo "Running tests for: $(ARG)..."; \
		python manage.py test $(ARG) -v2 --parallel; \
		pytest $(ARG) -v -n auto || (test $$? -eq $(TESTCASE_DOESNOT_EXISTS) && exit 0); \
	fi

# -------------------------------------------------------
# migration
# -------------------------------------------------------
.PHONY: migrate
migrate:
	@python manage.py makemigrations && python manage.py migrate
