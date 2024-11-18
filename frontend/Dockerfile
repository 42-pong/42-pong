# image tags
ARG NODE_TAG=22-alpine3.20
ARG NGINX_TAG=1.26-alpine3.20

# ----- stage: builder -----
FROM node:${NODE_TAG} AS builder

# src directory
ARG SRC_DIR=./pong

WORKDIR /app

COPY ${SRC_DIR} .
RUN npm install && npm run build


# ----- stage: production -----
FROM nginxinc/nginx-unprivileged:${NGINX_TAG} AS production

COPY --from=builder --chown=nginx:nginx /app/dist /usr/share/nginx/html

# TODO
# COPY --chown=nginx:nginx nginx.conf /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;"]
