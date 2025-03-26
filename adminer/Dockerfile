# syntax=docker/dockerfile:1

FROM adminer:4.8.1

# for healthcheck
USER root
RUN apt-get update && apt-get install -y curl
USER adminer
