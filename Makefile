SHELL:=/bin/bash

AIRFLOW_HOME=/opt/airflow
USER_ID=$(shell id -u)
GROUP_ID=$(shell id -g)

.PHONY: build
build:
	AIRFLOW_HOME=${AIRFLOW_HOME} \
	USER_ID=${USER_ID} \
	GROUP_ID=${GROUP_ID} \
	GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT} \
		docker-compose build

.PHONY: up
up:
	AIRFLOW_HOME=${AIRFLOW_HOME} \
	USER_ID=${USER_ID} \
	GROUP_ID=${GROUP_ID} \
	GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT} \
		docker-compose up --detach

.PHONY: start
start:
	AIRFLOW_HOME=${AIRFLOW_HOME} \
	USER_ID=${USER_ID} \
	GROUP_ID=${GROUP_ID} \
	GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT} \
		docker-compose exec \
			airflow \
			airflow unpause weather_data_pipeline

.PHONY: gcloud
gcloud:
	AIRFLOW_HOME=${AIRFLOW_HOME} \
	USER_ID=${USER_ID} \
	GROUP_ID=${GROUP_ID} \
	GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT} \
		docker-compose exec \
			airflow \
			gcloud auth login --no-launch-browser --update-adc

.PHONY: stop
stop:
	AIRFLOW_HOME=${AIRFLOW_HOME} \
	USER_ID=${USER_ID} \
	GROUP_ID=${GROUP_ID} \
	GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT} \
		docker-compose stop
