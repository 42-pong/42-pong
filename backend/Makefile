# FIXME: ルートのMakefile内からコンテナ名のみ取得したいが、includeすると不要なものも
# 全て読み込まれるため、良くないが一旦再定義
BACKEND_CONTAINER	:=	backend

TOOLS_DIR			:=	tools
REQUIREMENTS_IN		:=	requirements.in
REQUIREMENTS_TXT	:=	requirements.txt

TMP_DIR	:=	tmp

.PHONY: all
all:

# backendコンテナ起動時に使用
# コンテナ内でtools/requirements.inを元にtools/requirements.txtを生成する
.PHONY: gen-dependency
gen-dependency:
	@if ! docker exec $(BACKEND_CONTAINER) which pip-compile > /dev/null 2>&1; then \
		echo "pip-tools is not installed in the container"; \
		exit 1; \
	fi; \
	docker cp $(TOOLS_DIR)/$(REQUIREMENTS_IN) $(BACKEND_CONTAINER):/$(TMP_DIR); \
	docker exec $(BACKEND_CONTAINER) /bin/bash -c "cd /$(TMP_DIR) && pip-compile --strip-extras $(REQUIREMENTS_IN) -o $(REQUIREMENTS_TXT)"; \
	docker cp $(BACKEND_CONTAINER):/$(TMP_DIR)/$(REQUIREMENTS_TXT) $(TOOLS_DIR)/;

# backendコンテナ起動時に使用
# - 新規パッケージ名を入力すると、自動でtools/requirements.inに追記されgen-dependencyを行う
# - パッケージ名の入力に間違えがあった場合も、そのままtools/requirements.inに追記されて
#   gen-dependencyが行われ、tools/requirements.txtの生成を試みる。
#   存在しないパッケージ名の場合はtools/requirements.txtが生成されずにエラー終了する。
.PHONY: add-dependency
add-dependency:
	@read -p "Enter the package to add: " package_name; \
	echo $$package_name >> $(TOOLS_DIR)/$(REQUIREMENTS_IN); \
	make -s gen-dependency
