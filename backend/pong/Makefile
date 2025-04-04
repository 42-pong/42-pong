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
		TEST_RESULT=$$?; \
		pytest -v -n auto; \
		PYTEST_RESULT=$$?; \
	else \
		echo "Running tests for: $(ARG)..."; \
		python manage.py test $(ARG) -v2 --parallel; \
		TEST_RESULT=$$?; \
		pytest $(ARG) -v -n auto || (test $$? -eq $(TESTCASE_DOESNOT_EXISTS) && exit 0); \
		PYTEST_RESULT=$$?; \
	fi; \
	if [ $$TEST_RESULT -ne 0 ] || [ $$PYTEST_RESULT -ne 0 ]; then \
		exit 1; \
	fi

# -------------------------------------------------------
# migration
# -------------------------------------------------------
.PHONY: migrate
migrate:
	@python manage.py makemigrations && python manage.py migrate

# -------------------------------------------------------
# django management commands
# -------------------------------------------------------
# NUM:
#	作成するユーザー数。デフォルトは25。
#	email="mock{i}@example.com"で作成されるので、既に存在する場合はエラーになる
# 使用例:
#	make create_mock_players NUM=10
.PHONY: create_mock_players
create_mock_players:
	@python manage.py create_mock_players $(NUM)

.PHONY: create_mock_games
create_mock_games:
	@python manage.py create_mock_tournament
