SHELL:=/bin/bash

export GOOGLE_CLOUD_PROJECT
export MAPBOX_API_KEY

.PHONY: help
help: ##@miscellaneous Show this help message
	@perl ./help.pl $(MAKEFILE_LIST)

.PHONY: build
build: ##@docker Build the docker container
	docker-compose build

.PHONY: start
start: ##@docker Start daemon container with Superset and Postgres
	docker-compose up --detach

.PHONY: shell
shell: ##@docker Calls shell CLI in the Superset container
	docker-compose exec superset /bin/bash

.PHONY: gcloud
gcloud: ##@gcloud Calls gcloud auth login
	docker-compose exec superset \
		gcloud auth login --update-adc --no-launch-browser

.PHONY: stop
stop: ##@docker Stop and remove the container
	docker-compose stop
