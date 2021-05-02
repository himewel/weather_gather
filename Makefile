SHELL:=/bin/bash

AIRFLOW_HOME=/opt/airflow
USER_ID=$(shell id -u)
GROUP_ID=$(shell id -g)

export AIRFLOW_HOME
export BQ_DATASET
export GOOGLE_CLOUD_PROJECT
export GCS_BUCKET
export GROUP_ID
export USER_ID

.PHONY: help
help: ##@miscellaneous Show this help message.
	@perl ./help.pl $(MAKEFILE_LIST)

.PHONY: build
build:
	docker-compose build

.PHONY: up
up:
	docker-compose up --detach

.PHONY: start
start:
	docker-compose exec \
		airflow \
		airflow unpause weather_data_pipeline

.PHONY: gcloud
gcloud:
	docker-compose exec \
		airflow \
		gcloud auth login --no-launch-browser --update-adc

.PHONY: stop
stop:
	docker-compose stop
