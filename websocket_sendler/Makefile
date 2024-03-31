.PHONY: build up stop down restart logging pip start

PROJECT ?= websocket-sender
export PYTHONPATH := $(shell pwd):$(PYTHONPATH)
include ./.env


default: help

help: Makefile
	@echo " Choose a command run in "$(PROJECTNAME)":"
	@sed -n 's/^##//p' $< | column -t -s ':' |  sed -e 's/^/ /'

## make start: команда для билда всех контейнеров проекта
start: build up

## make build: команда для создания заданного контейнера проекта
build:
	docker compose -p ${PROJECT} build

## make test: команда для старта тесто
test:
	docker compose -p ${PROJECT} run --rm -e POSTGRES_DB=${PROJECT}_test <НАЗВАНИЕ СЕРВИСА> \
		pytest tests/${FILE} --asyncio-mode=auto -p no:warnings --tb=native -vv --setup-show --cov=src --trace-config -s ${CMD}

## make up: команда для старта заданного проекта (например, PROFILES='--profile websocket')
up:
	docker compose -p ${PROJECT} ${PROFILES} up -d --build --remove-orphans

## make down: команда для остановки заданного контейнера
down:
	docker compose -p ${PROJECT} -v down --rmi all

## make logging: команда для отображения логов заданного приложения
logging:
	docker compose -p ${PROJECT} logs -f --tail="100" ${PROJECT}
