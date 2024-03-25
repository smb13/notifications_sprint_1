#!make
.PHONY: api core db models schemas services

include ./.env

DOCKER_COMPOSE_ANALYTICS = --env-file ./.env -f ./docker-compose.yml
DOCKER_COMPOSE_DEV = --env-file ./.env -f ./docker-compose-dev.yml

# Default, Help

default: analytics_up

help: # Вывод информации make командах
	@grep -E '^[a-zA-Z0-9 _-]+:.*#' Makefile | while read -r l; \
	do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

# Start, First start

analytics_up:
	docker compose $(DOCKER_COMPOSE_ANALYTICS) up -d

dev_up:
	docker compose $(DOCKER_COMPOSE_DEV) up -d

# Build

analytics_build:
	docker compose $(DOCKER_COMPOSE_ANALYTICS) build

dev_build:
	docker compose $(DOCKER_COMPOSE_DEV) build

# Logs

analytics_logs:
	docker compose $(DOCKER_COMPOSE_ANALYTICS) logs --tail 100 -f analytics

analytics_logs_ui:
	docker compose $(DOCKER_COMPOSE_ANALYTICS) logs --tail 100 -f ui

dev_logs:
	docker compose $(DOCKER_COMPOSE_DEV) logs --tail 100 -f analytics

dev_logs_ui:
	docker compose $(DOCKER_COMPOSE_DEV) logs --tail 100 -f ui

dev_logs_kafka:
	docker compose $(DOCKER_COMPOSE_DEV) logs --tail 100 -f kafka

# Stop & Down

dev_stop:
	docker compose $(DOCKER_COMPOSE_DEV) stop

analytics_stop:
	docker compose $(DOCKER_COMPOSE_ANALYTICS) stop

dev_stop:
	docker compose $(DOCKER_COMPOSE_DEV) stop

analytics_down:
	docker compose $(DOCKER_COMPOSE_ANALYTICS) down --remove-orphans

dev_down:
	docker compose $(DOCKER_COMPOSE_DEV) down --remove-orphans
