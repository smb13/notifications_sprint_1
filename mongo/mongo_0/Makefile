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

mongo_first_start: mongo_build mongo_up mongo_config mongo_config_shards mongo_config_routers_shards # Первый запуск

# Build

mongo_build: # Сборка
	docker compose $(DOCKER_COMPOSE) build

# Configuration

mongo_up_config: # Запуск серверов конфигурации
	docker compose $(DOCKER_COMPOSE) up -d mongocfg1

mongo_config: # Конфигурация серверов конфигурации
	docker compose $(DOCKER_COMPOSE) exec -it mongocfg1 bash -c 'echo "rs.initiate({_id: \"mongors1conf\",'\
	' configsvr: true, members: [{_id: 0, host: \"$(MONGO_CFG_1)\"}, {_id: 1, host: \"$(MONGO_CFG_2)\"},'\
	' {_id: 2, host: \"$(MONGO_CFG_3)\"}]})" | mongosh'

# Shards

mongo_up_shards: # Запуск серверов шардов
	docker compose $(DOCKER_COMPOSE) up -d mongors1n1 mongors2n2


mongo_config_shards: mongo_config_shards_1 mongo_config_shards_2 # Конфигурация шардов

mongo_config_shards_1: # Конфигурация первого шарда
	docker exec -it mongors1n1 bash -c 'echo "rs.initiate({_id: \"mongors1\",'\
	' members: [{_id: 0, host: \"${MONGO_SHARD_1N1}\"}, {_id: 1, host: \"${MONGO_SHARD_1N2}\"},'\
	' {_id: 2, host: \"${MONGO_SHARD_1N3}\"}]})" | mongosh'

mongo_config_shards_2: # Конфигурация второго шарда
	docker exec -it mongors2n2 bash -c 'echo "rs.initiate({_id: \"mongors2\",'\
	' members: [{_id: 0, host: \"${MONGO_SHARD_2N1}\"}, {_id: 1, host: \"${MONGO_SHARD_2N2}\"},'\
	' {_id: 2, host: \"${MONGO_SHARD_2N3}\"}]})" | mongosh'

# Routers

mongo_up_mongos: # Запуск роутеров
	docker compose $(DOCKER_COMPOSE) up -d mongos1

mongo_config_routers_shards: mongo_config_routers_shards_1 mongo_config_routers_shards_2 # Конфигурация роутеров

mongo_config_routers_shards_1: # Конфигурация роутеров для первого шарда
	docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors1/${MONGO_SHARD_1N1}\")" | mongosh'

mongo_config_routers_shards_2: # Конфигурация роутеров для второго шарда
	docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors2/${MONGO_SHARD_2N1}\")" | mongosh'

# Logs

mongo_logs: # Журнал
	docker compose $(DOCKER_COMPOSE) logs --tail 100 -f

# Stop & Down

mongo_stop: # Остановка
	docker compose $(DOCKER_COMPOSE) stop

mongo_down: # Удаление
	docker compose $(DOCKER_COMPOSE) down --remove-orphans
