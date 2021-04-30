SHELL:=/bin/bash

AIRFLOW_HOME=/opt/airflow
USER_ID=$(shell id -u)
GROUP_ID=$(shell id -g)

.PHONY: build
build:
	AIRFLOW_HOME=${AIRFLOW_HOME} \
	USER_ID=${USER_ID} \
	GROUP_ID=${GROUP_ID} \
		docker-compose build

.PHONY: up
up:
	AIRFLOW_HOME=${AIRFLOW_HOME} \
	USER_ID=${USER_ID} \
	GROUP_ID=${GROUP_ID} \
		docker-compose up --detach

.PHONY: stop
stop:
	docker-compose stop
