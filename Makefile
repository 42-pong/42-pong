# docker compose
COMPOSE_FILE			:=	compose.yaml
COMPOSE_FILE_OVERRIDE	:=	compose.override.yaml
COMPOSE_FILE_PROD		:=	compose.prod.yaml

DOCKER_COMPOSE			:=	docker compose -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_PROD)
DOCKER_COMPOSE_DEV		:=	docker compose -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_OVERRIDE)

FRONTEND_SERVICE	:=	frontend
BACKEND_SERVICE		:=	backend
DATABASE_SERVICE	:=	postgres
ADMINER_SERVICE		:=	adminer
REDIS_SERVICE		:=	redis

SERVICES	:=	$(FRONTEND_SERVICE) $(BACKEND_SERVICE) \
				$(DATABASE_SERVICE) $(ADMINER_SERVICE) $(REDIS_SERVICE)

AVATARS_DIR	:=	backend/pong/media/avatars

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

# rm container,volume,network,image,build cache,avatars,ssl_cert
.PHONY: clean
clean: down_v clean_docker rm_avatars rm_ssl_cert
	@echo "All containers, volume, network, images, build cache, avatars, ssl_cert are removed."

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

.PHONY: dev-up
dev-up:
	@$(DOCKER_COMPOSE_DEV) up --build -d

.PHONY: dev-down
dev-down:
	@$(DOCKER_COMPOSE_DEV) down

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
# cleanup
# -------------------------------------------------------
.PHONY: rm_images
rm_images:
	@for service in $(SERVICES); do \
        docker rmi -f $$(docker images -q --filter "reference=$$service") || true; \
    done

.PHONY: rm_builder_cache
rm_builder_cache:
	@-docker builder prune -af

.PHONY: clean_docker
clean_docker: rm_images rm_builder_cache

# デフォルト画像"sample.png"以外のアバター画像を削除
.PHONY: rm_avatars
rm_avatars:
	@find $(AVATARS_DIR) -type f ! -name "sample.png" -delete

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
