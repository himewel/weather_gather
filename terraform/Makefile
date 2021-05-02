SHELL:=/bin/bash

IMAGE_NAME=weather_gather_terraform
CONTAINER_NAME=weather_gather_terraform_1

.PHONY: build
build:
	docker build . --tag $(IMAGE_NAME)

.PHONY: start
start:
	docker run \
		--rm \
		--detach \
		--volume ${PWD}/gcp:/root/gcp \
		--name $(CONTAINER_NAME)
		$(IMAGE_NAME)

.PHONY: shell
shell:
	docker exec \
		--interactive \
		--tty \
		$(CONTAINER_NAME) \
		/bin/sh
