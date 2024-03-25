PROJECT ?= 'elk'

PROD = -f docker-compose.yml
DEV = -f docker-compose-dev.yml

help: Makefile
	@echo " Команды для управления проектом "$(PROJECT)":"
	@sed -n 's/^##//p' $< | column -t -s ':' |  sed -e 's/^/ /'


## make start: команда для старта заданного проекта
start:
	docker compose -p ${PROJECT} ${PROD} up --build -d --force-recreate --remove-orphans

## make start_dev: команда для старта заданного проекта
start_dev:
	docker compose -p ${PROJECT} ${DEV} up --build -d --force-recreate --remove-orphans

## make logging: команда для отображения логов заданного приложения
logging:
	docker compose logs -f --tail="100" ${PROJECT}

## make down: команда для удаления контейнера и всех связных данных
down:
	docker compose -p ${PROJECT} down -v --rmi all --remove-orphans

## make clear: команда для очистке всех контейнеров и образов (удалит вообще все)
clear:
	docker system prune -a
	docker volume prune