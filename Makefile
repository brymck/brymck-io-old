SHELL := /bin/bash

all: run

init: secrets

dev:
	source .env && source .env.local && skaffold dev --default-repo $${DEFAULT_REPO}

run:
	source .env && source .env.local && skaffold run --default-repo $${DEFAULT_REPO}

secrets:
	pip install --quiet --requirement secrets/requirements.txt
	python secrets/create-secrets.py

.PHONY: \
	all \
	init \
	dev \
	run \
	secrets
