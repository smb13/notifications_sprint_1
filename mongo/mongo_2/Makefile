#!make
.PHONY: client

include ./.env

DOCKER_COMPOSE = --env-file ./.env -f ./docker-compose.yml

# Default, Help

default: mongo_up

help: # Вывод информации make командах
	@grep -E '^[a-zA-Z0-9 _-]+:.*#' Makefile | while read -r l; \
	do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

# Start, First start

mongo_up: # Запуск всех контейнеров
	docker compose $(DOCKER_COMPOSE) up -d

mongo_first_start: mongo_build mongo_up # Первый запуск

# Build

mongo_build: # Сборка
	docker compose $(DOCKER_COMPOSE) build

# Configuration

mongo_up_config: # Запуск серверов конфигурации
	docker compose $(DOCKER_COMPOSE) up -d mongocfg3

# Shards

mongo_up_shards: # Запуск серверов шардов
	docker compose $(DOCKER_COMPOSE) up -d mongors1n3 mongors2n1

# Routers

mongo_up_mongos: # Запуск роутеров
	docker compose $(DOCKER_COMPOSE) up -d mongos3

# Logs

mongo_logs: # Журнал
	docker compose $(DOCKER_COMPOSE) logs --tail 100 -f

# Stop & Down

mongo_stop: # Остановка
	docker compose $(DOCKER_COMPOSE) stop

mongo_down: # Удаление
	docker compose $(DOCKER_COMPOSE) down --remove-orphans
