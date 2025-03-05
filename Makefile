# docker compose
COMPOSE_FILE		:=	compose.yaml
DOCKER_COMPOSE		:=	docker compose -f $(COMPOSE_FILE)

BACKEND_SERVICE		:=	backend
DATABASE_SERVICE	:=	db

# ssl
DOMAIN_NAME		:=	localhost
SSL_DIR			:=	frontend/ssl
SSL_CERT_DIR	:=	$(SSL_DIR)/certs
SSL_KEY_DIR		:=	$(SSL_DIR)/private
SSL_CA_CERT		:=	$(SSL_CERT_DIR)/${DOMAIN_NAME}.crt
SSL_CA_KEY		:=	$(SSL_KEY_DIR)/${DOMAIN_NAME}.key
# SSL_DIR外に配置する
SSL_CNF_PATH	:=	frontend/openssl.cnf

.PHONY: all
all: gen_ssl_cert up

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

# rm container,volume,network
.PHONY: down_v
down_v:
	@$(DOCKER_COMPOSE) down -v

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

# -------------------------------------------------------
# ssl
# -------------------------------------------------------
.PHONY: gen_ssl_cert
gen_ssl_cert:
	@mkdir -p ${SSL_DIR}
	@mkdir -p ${SSL_CERT_DIR}
	@mkdir -p ${SSL_KEY_DIR}

	@openssl genrsa -out ${SSL_CA_KEY} 2048
	@openssl req -new -x509 \
		-key ${SSL_CA_KEY} \
		-out ${SSL_CA_CERT} \
       -subj "/C=JP/ST=Tokyo/L=Shinjuku/O=42Tokyo/OU=42Pong/CN=${DOMAIN_NAME}/" \
       -extensions v3_req \
       -config $(SSL_CNF_PATH)

.PHONY: rm_ssl_cert
rm_ssl_cert:
	@rm -rf ${SSL_CERT_DIR} ${SSL_KEY_DIR}
