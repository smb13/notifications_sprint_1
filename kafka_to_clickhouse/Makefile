PROJECT ?= 'kafka_etl'

PROD = -f docker-compose.yml
DEV = -f docker-compose-dev.yml

help: Makefile
	@echo " Choose a command run in "$(PROJECTNAME)":"
	@sed -n 's/^##//p' $< | column -t -s ':' |  sed -e 's/^/ /'


## make start: команда для старта заданного проекта
start:
	docker-compose -p ${PROJECT} ${PROD} up --build -d --force-recreate --remove-orphans

## make start_dev: команда для старта заданного проекта
start_dev:
	docker-compose -p ${PROJECT} ${DEV} up --build -d --force-recreate --remove-orphans

## make logging: команда для отображения логов заданного приложения
logging:
	docker-compose logs -f --tail="100" ${PROJECT}
