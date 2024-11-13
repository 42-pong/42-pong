# FIXME: ルートのMakefile内からコンテナ名のみ取得したいが、includeすると不要なものも
# 全て読み込まれるため、良くないが一旦再定義
BACKEND_CONTAINER	:=	backend

TOOLS_DIR			:=	tools
REQUIREMENTS_IN		:=	requirements.in
REQUIREMENTS_TXT	:=	requirements.txt

PROJECT_DIR	:=	pong

.PHONY: all
all:

# backendコンテナ起動時に使用
# コンテナ内でtools/requirements.inを元にtools/requirements.txtを生成する
.PHONY: gen-dependency
gen-dependency:
	@cp $(TOOLS_DIR)/$(REQUIREMENTS_IN) $(PROJECT_DIR)/; \
	docker exec $(BACKEND_CONTAINER) pip-compile --strip-extras $(REQUIREMENTS_IN) -o $(REQUIREMENTS_TXT); \
	mv $(PROJECT_DIR)/$(REQUIREMENTS_TXT) $(TOOLS_DIR)/; \
	rm $(PROJECT_DIR)/$(REQUIREMENTS_IN)
