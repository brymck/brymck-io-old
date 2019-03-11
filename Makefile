all: run

dev:
	skaffold dev --default-repo gcr.io/brymck-io
.PHONY: dev

run:
	skaffold run --default-repo gcr.io/brymck-io
.PHONY: run

secrets:
	pip install --quiet --requirement secrets/requirements.txt
	python secrets/create-secrets.py
.PHONY: secrets
