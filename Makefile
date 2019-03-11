ISTIO_VERSION := 1.0.5
SHELL := /bin/bash

all: run

init: istio secrets

istio: istio-${ISTIO_VERSION}
	cd istio-${ISTIO_VERSION} && kubectl apply -f install/kubernetes/helm/istio/templates/crds.yaml
	sleep 10s
	cd istio-${ISTIO_VERSION} && kubectl apply -f install/kubernetes/istio-demo.yaml

istio-${ISTIO_VERSION}:
	curl -L https://git.io/getLatestIstio | ISTIO_VERSION=${ISTIO_VERSION} sh -

secrets:
	pip install --quiet --requirement secrets/requirements.txt
	python secrets/create-secrets.py

dev:
	source .env && source .env.local && skaffold dev --default-repo $${DEFAULT_REPO}

run:
	source .env && source .env.local && skaffold run --default-repo $${DEFAULT_REPO}

ambassador:
	kubectl apply -f blah/ambassador/ambassador-rbac.yaml
	kubectl rollout status deployment ambassador

dashboard:
	# kubectl create -f https://raw.githubusercontent.com/kubernetes/dashboard/master/aio/deploy/recommended/kubernetes-dashboard.yaml
	kubectl proxy

.PHONY: \
	all \
	init \
	istio \
	secrets \
	dev \
	run \
	dashboard
