DC = docker compose

DEV_ENV = --env-file dev.env

APP_FILE = docker-compose/app.yaml
STORAGES_FILE = docker-compose/storages.yaml

.PHONY: dev-app
dev-app:
	${DC} -f ${APP_FILE} ${DEV_ENV} up --build -d

.PHONY: dev-storages
dev-storages:
	${DC} -f ${STORAGES_FILE} ${DEV_ENV} up --build -d

.PHONY: all
all:
	${MAKE} storages
	${MAKE} app

.PHONY: down-app
down-app:
	${DC} -f ${APP_FILE} ${DEV_ENV} down

.PHONY: down-storages
down-storages:
	${DC} -f ${STORAGES_FILE} ${DEV_ENV} down

.PHONY: down-storages-v
down-storages-v:
	${DC} -f ${STORAGES_FILE} ${DEV_ENV} down -v

.PHONY: down-all
down-all:
	${MAKE} down-storages
	${MAKE} down-app