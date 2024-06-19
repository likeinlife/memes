DC = docker compose

DEV_ENV = --env-file dev.env
PROD_ENV = --env-file prod.env

APP_FILE = docker-compose/app.yaml
STORAGES_FILE = docker-compose/storages.yaml

.PHONY: dev-app
dev-app:
	${DC} -f ${APP_FILE} ${DEV_ENV} up --build -d

.PHONY: app
app:
	${DC} -f ${APP_FILE} ${PROD_ENV} up --build -d

.PHONY: dev-storages
dev-storages:
	${DC} -f ${STORAGES_FILE} ${DEV_ENV} up --build -d

.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} ${PROD_ENV} up --build -d

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

.PHONY: down-storages
down-storages-v:
	${DC} -f ${STORAGES_FILE} ${DEV_ENV} down -v

.PHONY: down-all
down-all:
	${MAKE} down-storages
	${MAKE} down-app