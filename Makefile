SHELL := /bin/bash

all: run

dev:
	source .env && source .env.local && skaffold dev --default-repo $${DEFAULT_REPO}
.PHONY: dev

run:
	source .env && source .env.local && skaffold run --default-repo $${DEFAULT_REPO}
.PHONY: run

secrets:
	pip install --quiet --requirement secrets/requirements.txt
	python secrets/create-secrets.py
.PHONY: secrets
