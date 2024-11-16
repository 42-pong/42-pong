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
FROM nginx:${NGINX_TAG} AS production

COPY --from=builder /app/dist /usr/share/nginx/html

# TODO
# COPY nginx.conf /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;"]
