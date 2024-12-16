# docker compose
COMPOSE_FILE		:=	compose.yaml

BACKEND_SERVICE		:=	backend
DATABASE_SERVICE	:=	db


.PHONY: all
all: up

# -------------------------------------------------------
# docker compose
# -------------------------------------------------------
.PHONY: up
up:
	@docker compose up -d

# rm container,network
.PHONY: down
down:
	@docker compose down

.PHONY: build-up
build-up:
	@docker compose up --build -d

.PHONY: start
start:
	@docker compose start

.PHONY: stop
stop:
	@docker compose stop

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
	@docker compose exec -it $(BACKEND_SERVICE) /bin/bash

.PHONY: exec-db
exec-db:
	@docker compose exec -it $(DATABASE_SERVICE) /bin/bash

# -------------------------------------------------------
# docker compose logs
# -------------------------------------------------------
.PHONY: logs-be
logs-be:
	@docker compose -f $(COMPOSE_FILE) logs $(BACKEND_SERVICE)

.PHONY: logs-db
logs-db:
	@docker compose -f $(COMPOSE_FILE) logs $(DATABASE_SERVICE)
