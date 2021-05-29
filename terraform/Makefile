SHELL:=/bin/bash

IMAGE_NAME=weather_gather_terraform
CONTAINER_NAME=weather_gather_terraform_1

.PHONY: help
help: ##@miscellaneous Show this help message
	@perl ./help.pl $(MAKEFILE_LIST)

.PHONY: build
build: ##@docker Build the docker container
	docker build . --tag $(IMAGE_NAME)

.PHONY: start
start: ##@docker Start daemon container with Terraform
	docker run \
		--rm \
		--detach \
		--volume ${PWD}/gcp:/root/gcp \
		--name $(CONTAINER_NAME) \
		--env GOOGLE_CLOUD_PROJECT=$(GOOGLE_CLOUD_PROJECT) \
		--env TF_VAR_BQ_DATASET=$(BQ_DATASET) \
		--env TF_VAR_GCS_BUCKET=$(GCS_BUCKET) \
		$(IMAGE_NAME)

.PHONY: shell
shell: ##@docker Calls shell CLI in the terraform container
	docker exec \
		--interactive \
		--tty \
		$(CONTAINER_NAME) \
		/bin/sh

.PHONY: gcloud
gcloud: ##@docker Calls gcloud auth login
	docker exec \
		--interactive \
		--tty \
		$(CONTAINER_NAME) \
		gcloud auth login --no-launch-browser --update-adc

.PHONY: stop
stop: ##@docker Stop and remove the container
	docker stop $(CONTAINER_NAME)
