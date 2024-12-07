# image/container
BACKEND		:=	backend
DATABASE	:=	postgres

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
# docker exec
# -------------------------------------------------------
.PHONY: exec-be
exec-be:
	@docker exec -it $(BACKEND) /bin/bash

.PHONY: exec-db
exec-db:
	@docker exec -it $(DATABASE) /bin/bash

# -------------------------------------------------------
# docker logs
# -------------------------------------------------------
.PHONY: logs-be
logs-be:
	@docker logs $(BACKEND)

.PHONY: logs-db
logs-db:
	@docker logs $(DATABASE)
