# docker compose
COMPOSE_FILE		:=	compose.yaml
DOCKER_COMPOSE		:=	docker compose -f $(COMPOSE_FILE)

BACKEND_SERVICE		:=	backend
DATABASE_SERVICE	:=	db


.PHONY: all
all: up

# -------------------------------------------------------
# docker compose
# -------------------------------------------------------
.PHONY: up
up:
	@$(DOCKER_COMPOSE) up -d

# rm container,network
.PHONY: down
down:
	@$(DOCKER_COMPOSE) down

.PHONY: build-up
build-up:
	@$(DOCKER_COMPOSE) up --build -d

.PHONY: start
start:
	@$(DOCKER_COMPOSE) start

.PHONY: stop
stop:
	@$(DOCKER_COMPOSE) stop

# -------------------------------------------------------
# docker ps
# -------------------------------------------------------
.PHONY: ps
ps:
	@docker ps

.PHONY: psa
psa:
	@docker ps -a

# -------------------------------------------------------
# docker compose exec
# -------------------------------------------------------
.PHONY: exec-be
exec-be:
	@$(DOCKER_COMPOSE) exec -it $(BACKEND_SERVICE) /bin/bash

.PHONY: exec-db
exec-db:
	@$(DOCKER_COMPOSE) exec -it $(DATABASE_SERVICE) /bin/bash

# -------------------------------------------------------
# docker compose logs
# -------------------------------------------------------
.PHONY: logs-be
logs-be:
	@$(DOCKER_COMPOSE) logs $(BACKEND_SERVICE)

.PHONY: logs-db
logs-db:
	@$(DOCKER_COMPOSE) logs $(DATABASE_SERVICE)
