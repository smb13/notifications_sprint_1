#!make
.PHONY: admin auth etl db_dump tests external

include ./.env

DOCKER_COMPOSE_PROD = --env-file ./.env -f ./docker-compose.yml
DOCKER_COMPOSE_DEV = --env-file ./.env -f ./docker-compose-dev.yml

# Default, Help

default: first_start_dev

help: # Вывод информации make командах
	@grep -E '^[a-zA-Z0-9 _-]+:.*#' Makefile | while read -r l; \
	do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

# Start, First start

first_start: postgres db_create admin_migrate redis redis_auth elastic etl production auth_migrations auth_createsuperuser

first_start_dev: postgres_dev db_create_dev db_restore_dev redis_dev redis_auth_dev flush_redis_dev elastic_dev clear_elastic_index_dev etl_dev dev auth_createsuperuser_dev

start: production auth_migrations

# Tests

first_start_tests: postgres_dev db_create_dev db_restore_dev redis_dev redis_auth_dev flush_redis_dev elastic_dev clear_elastic_index_dev etl_dev tests

tests:
	docker compose $(DOCKER_COMPOSE_DEV) --profile tests up --build --attach tests

# Profiles

production:
	docker compose $(DOCKER_COMPOSE_PROD) up -d

dev:
	docker compose $(DOCKER_COMPOSE_DEV) --profile external_dev --profile admin_dev --profile auth_dev --profile ratings_dev up -d

# Redis

redis:  # Запустить контейнер Redis server
	docker compose $(DOCKER_COMPOSE_PROD) up --wait -d redis

redis_dev:  # Запустить контейнер Redis server
	docker compose $(DOCKER_COMPOSE_DEV) up --wait -d redis

redis_auth:  # Запустить контейнер Redis server Auth
	docker compose $(DOCKER_COMPOSE_PROD) up --wait -d redis_auth

redis_auth_dev:  # Запустить контейнер Redis server Auth
	docker compose $(DOCKER_COMPOSE_DEV) up --wait -d redis_auth

flush_redis_dev:  # Очистить хранилище Redis State
	docker compose $(DOCKER_COMPOSE_DEV) run redis redis-cli -h redis -c "FLUSHALL"

clear_redis_state_dev:  # Очистить хранилище Redis State
	docker compose $(DOCKER_COMPOSE_DEV) run redis redis-cli -h redis -c "DEL" "state_data"

# Elasticsearch

elastic:  # Собрать и запустить контейнер ElasticSearch и должаться статуса healthy
	docker compose $(DOCKER_COMPOSE_PROD) up --build -d elastic --wait

elastic_dev:  # Собрать и запустить контейнер ElasticSearch и должаться статуса healthy
	docker compose $(DOCKER_COMPOSE_DEV) up --build -d elastic --wait

etl:  # Собрать и запустить контейнер приложения ETL из Postgres в ElasticSearch
	docker compose $(DOCKER_COMPOSE_PROD) up --build -d etl

etl_dev:  # Собрать и запустить контейнер приложения ETL из Postgres в ElasticSearch
	docker compose $(DOCKER_COMPOSE_DEV) up --build -d etl

clear_elastic_index_dev:  # Очистить индекс Elasticsearch
	docker compose $(DOCKER_COMPOSE_DEV) run elastic curl -XDELETE http://elastic:9200/movies \
	&& docker compose $(DOCKER_COMPOSE_DEV) run elastic curl -XDELETE http://elastic:9200/persons \
	&& docker compose $(DOCKER_COMPOSE_DEV) run elastic curl -XDELETE http://elastic:9200/genres

# PostgreSQL

postgres:  # Собрать и запустить контейнер Postgres
	docker compose $(DOCKER_COMPOSE_PROD) up --build --force-recreate -d postgres

postgres_dev:  # Собрать и запустить контейнер Postgres
	docker compose $(DOCKER_COMPOSE_DEV) up --build --force-recreate -d postgres

db_dump_dev: # Сделать дамп базы данных Postgres в файл ./db_dump/movies_db.backup
	docker compose $(DOCKER_COMPOSE_DEV) exec -i postgres bash -c "pg_dump -U $(POSTGRES_USER) "\
	"-Fc -f /etc/db_dump/movies_db.backup $(POSTGRES_MOVIES_DB)"

db_create: # Создать базы данных для сервисов
	docker compose $(DOCKER_COMPOSE_PROD) exec -i postgres bash -c "/etc/db_dump/wait-for-postgres.sh localhost && "\
	"echo \"SELECT 'CREATE DATABASE $(POSTGRES_MOVIES_DB)' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = "\
	"'$(POSTGRES_MOVIES_DB)')\gexec\" | psql -U $(POSTGRES_USER) && "\
	"echo \"SELECT 'CREATE DATABASE $(POSTGRES_AUTH_DB)' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = "\
	"'$(POSTGRES_AUTH_DB)')\gexec\" | psql -U $(POSTGRES_USER)"

db_create_dev: # Создать базы данных для сервисов
	docker compose $(DOCKER_COMPOSE_DEV) exec -i postgres bash -c "/etc/db_dump/wait-for-postgres.sh localhost && "\
	"echo \"SELECT 'CREATE DATABASE $(POSTGRES_MOVIES_DB)' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = "\
	"'$(POSTGRES_MOVIES_DB)')\gexec\" | psql -U $(POSTGRES_USER) && "\
	"echo \"SELECT 'CREATE DATABASE $(POSTGRES_AUTH_DB)' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = "\
	"'$(POSTGRES_AUTH_DB)')\gexec\" | psql -U $(POSTGRES_USER)"

db_restore_dev: # Восстановить базу данных Postgres из файла ./db_dump/movies_db.backup
	docker compose $(DOCKER_COMPOSE_DEV) exec -i postgres bash -c "/etc/db_dump/wait-for-postgres.sh localhost && "\
	"pg_restore -U $(POSTGRES_USER) -Fc -c --if-exists -O -v --no-acl -d $(POSTGRES_MOVIES_DB) /etc/db_dump/movies_db.backup"

# External API

external:  # Собрать и запустить контейнер External API
	docker compose $(DOCKER_COMPOSE_PROD) up --build -d external

external_dev:  # Собрать и запустить тестовый контейнер External API (с зависимостями для разработки)
	docker compose $(DOCKER_COMPOSE_DEV) --profile external_dev up --build -d

# Auth

auth:  # Собрать и запустить тестовый контейнер Auth (с зависимостями для разработки)
	docker compose $(DOCKER_COMPOSE_PROD) up --build -d auth

auth_dev:  # Собрать и запустить тестовый контейнер Auth (с зависимостями для разработки)
	docker compose $(DOCKER_COMPOSE_DEV) --profile auth_dev up --build -d

auth_createsuperuser:  # Создать суперпользователя по параметрам LOCAL_USER_EMAIL LOCAL_USER_PASSWORD из .env
	@docker compose $(DOCKER_COMPOSE_PROD) run --rm auth bash -c \
    'python /src/commands/create_admin.py --username $(LOCAL_USER_EMAIL) --password $(LOCAL_USER_PASSWORD)'

auth_createsuperuser_dev:  # Создать суперпользователя по параметрам LOCAL_USER_EMAIL LOCAL_USER_PASSWORD из .env
	@docker compose $(DOCKER_COMPOSE_DEV) run --rm auth_dev bash -c \
    'python /src/commands/create_admin.py --username $(LOCAL_USER_EMAIL) --password $(LOCAL_USER_PASSWORD)'

## make auth_upgrade_migration: команда для создания новой ревизии
auth_upgrade_migration:
	docker compose $(DOCKER_COMPOSE_PROD) run --rm --no-deps auth alembic revision --autogenerate -m "${MESSAGE}"

## make auth_migrations: команда для запуска всех миграций бд
auth_migrations:
	docker compose $(DOCKER_COMPOSE_PROD) run --rm auth alembic upgrade head

## make auth_downgrade_migration: команда для отката последней ревизии
auth_downgrade_migration:
	docker compose $(DOCKER_COMPOSE_PROD) run --rm auth alembic downgrade -1


# Django Admin

admin:  # Собрать и запустить контейнер Django Admin
	docker compose $(DOCKER_COMPOSE_PROD) up --build -d admin

admin_dev:  # Собрать и запустить тестовый контейнер Django Admin (с зависимостями для разработки и запуска автотестов)
	docker compose $(DOCKER_COMPOSE_DEV) --profile admin_dev up --build -d

admin_migrate:  # Запустить миграции Django для создания структуры базы данных
	@docker compose $(DOCKER_COMPOSE_PROD) run --rm admin bash -c "python ./manage.py migrate"

admin_createsuperuser:  # Создать суперпользователя по параметрам LOCAL_USER LOCAL_USER_EMAIL LOCAL_USER_PASSWORD из .env
	@docker compose $(DOCKER_COMPOSE_PROD) run --rm admin bash -c 'echo "from django.contrib.auth import get_user_model;'\
	'User = get_user_model(); User.objects.create_superuser(\"$(LOCAL_USER)\", \"$(LOCAL_USER_EMAIL)\", '\
	'\"$(LOCAL_USER_PASSWORD)\") if not User.objects.filter(username=\"$(LOCAL_USER)\").exists() '\
	'else print(\"Имя суперпользователя занято\")" | python manage.py shell'

admin_createsuperuser_dev:  # Создать суперпользователя по параметрам LOCAL_USER LOCAL_USER_EMAIL LOCAL_USER_PASSWORD из .env
	@docker compose $(DOCKER_COMPOSE_DEV) run --rm admin_dev bash -c 'echo "from django.contrib.auth import get_user_model;'\
	'User = get_user_model(); User.objects.create_superuser(\"$(LOCAL_USER)\", \"$(LOCAL_USER_EMAIL)\", '\
	'\"$(LOCAL_USER_PASSWORD)\") if not User.objects.filter(username=\"$(LOCAL_USER)\").exists() '\
	'else print(\"Имя суперпользователя занято\")" | python manage.py shell'

admin_generate_secret_key:
	@docker compose $(DOCKER_COMPOSE_PROD) run --rm admin bash -c \
	'python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"'

admin_generate_secret_key_dev:
	@docker compose $(DOCKER_COMPOSE_DEV) run --rm admin_dev bash -c \
	'python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"'

# Mongo DB

mongo_dev: # Запуск всех контейнеров
	docker compose $(DOCKER_COMPOSE_DEV) up -d mongocfg1 mongors1n1 mongos1

mongo_dev_first_start: mongo_dev mongo_config mongo_config_shards mongo_config_routers_shards # Первый запуск

mongo_config: # Конфигурация серверов конфигурации
	docker compose $(DOCKER_COMPOSE_DEV) exec -it mongocfg1 bash -c 'echo "rs.initiate({_id: \"mongors1conf\", configsvr: true, members: [{_id: 0, host: \"mongocfg1\"}]})" | mongosh'

mongo_config_shards: # Конфигурация шардов
	docker exec -it mongors1n1 bash -c 'echo "rs.initiate({_id: \"mongors1\", members: [{_id: 0, host: \"mongors1n1\"}]})" | mongosh'

mongo_config_routers_shards: # Конфигурация роутеров
	docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors1/mongors1n1\")" | mongosh'

mongo_logs: # Журнал
	docker compose $(DOCKER_COMPOSE_DEV) logs --tail 100 -f


# Stop & Down

stop:
	docker compose $(DOCKER_COMPOSE_PROD) stop

stop_dev:
	docker compose $(DOCKER_COMPOSE_DEV) --profile production --profile external_dev \
	--profile admin_dev --profile tests --profile auth_dev --profile ratings_dev  stop

down:
	docker compose $(DOCKER_COMPOSE_PROD) down --remove-orphans

down_dev:
	docker compose $(DOCKER_COMPOSE_DEV) --profile production --profile external_dev \
	--profile admin_dev --profile tests down --remove-orphans
