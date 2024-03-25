#!make
.PHONY: client

DOCKER_COMPOSE = -f ./docker-compose.yml

# Default, Help

default: mongo_up

help: # Вывод информации make командах
	@grep -E '^[a-zA-Z0-9 _-]+:.*#' Makefile | while read -r l; \
	do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

# Start, First start

mongo_up: # Запуск всех контейнеров
	docker compose $(DOCKER_COMPOSE) up -d

mongo_first_start: mongo_build mongo_up mongo_config mongo_config_shards mongo_config_routers_shards # Первый запуск

# Configuration

mongo_config: # Конфигурация серверов конфигурации
	docker compose $(DOCKER_COMPOSE) exec -it mongocfg1 bash -c 'echo "rs.initiate({_id: \"mongors1conf\", configsvr: true, members: [{_id: 0, host: \"mongocfg1\"}]})" | mongosh'

# Shards

mongo_config_shards: # Конфигурация шардов
	docker exec -it mongors1n1 bash -c 'echo "rs.initiate({_id: \"mongors1\", members: [{_id: 0, host: \"mongors1n1\"}]})" | mongosh'

# Routers

mongo_config_routers_shards: # Конфигурация роутеров
	docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors1/mongors1n1\")" | mongosh'

# Logs

mongo_logs: # Журнал
	docker compose $(DOCKER_COMPOSE) logs --tail 100 -f

# Stop & Down

mongo_stop: # Остановка
	docker compose $(DOCKER_COMPOSE) stop

mongo_down: # Удаление
	docker compose $(DOCKER_COMPOSE) down --remove-orphans
