# Makefile for building and running the Flask app in Docker

APP_TAG?=latest
APP_ORG?=mptrabalho
APP_REPO?=spai-ostools
APP_IMAGE_NAME=$(APP_ORG)/$(APP_REPO):$(APP_TAG)
APP_PORT?=5000

build:
	docker build -t $(APP_IMAGE_NAME) .

run:
	docker run --rm -p $(APP_PORT):$(APP_PORT) $(APP_IMAGE_NAME)

dev:
	docker run --rm -p $(APP_PORT):$(APP_PORT) -v "$(pwd)/app:/app" $(APP_IMAGE_NAME)

test:
	cd app && pytest

push:
	docker push $(APP_IMAGE_NAME)

all: test build run