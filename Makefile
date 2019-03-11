ISTIO_VERSION := 1.0.5
SHELL := /bin/bash

all: run

init: istio secrets

istio: istio-${ISTIO_VERSION}
	cd istio-${ISTIO_VERSION} && kubectl apply -f install/kubernetes/helm/istio/templates/crds.yaml
	cd istio-${ISTIO_VERSION} && kubectl apply -f install/kubernetes/istio-demo.yaml
	kubectl rollout status deployment -n istio-system grafana
	kubectl rollout status deployment -n istio-system istio-citadel
	kubectl rollout status deployment -n istio-system istio-egressgateway
	kubectl rollout status deployment -n istio-system istio-galley
	kubectl rollout status deployment -n istio-system istio-ingressgateway
	kubectl rollout status deployment -n istio-system istio-pilot
	kubectl rollout status deployment -n istio-system istio-policy
	kubectl rollout status deployment -n istio-system istio-sidecar-injector
	kubectl rollout status deployment -n istio-system istio-telemetry
	kubectl rollout status deployment -n istio-system istio-tracing
	kubectl rollout status deployment -n istio-system prometheus
	kubectl rollout status deployment -n istio-system servicegraph
	kubectl label namespace default istio-injection=enabled
	kubectl apply -f istio

istio-${ISTIO_VERSION}:
	curl -L https://git.io/getLatestIstio | ISTIO_VERSION=${ISTIO_VERSION} sh -

secrets:
	pip install --quiet --requirement secrets/requirements.txt
	python secrets/create-secrets.py

dev:
	source .env && source .env.local && skaffold dev --default-repo $${DEFAULT_REPO}

run:
	source .env && source .env.local && skaffold run --default-repo $${DEFAULT_REPO}

dashboard:
	kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/master/aio/deploy/recommended/kubernetes-dashboard.yaml
	kubectl rollout status deployment -n kube-system kubernetes-dashboard
	kubectl proxy

.PHONY: \
	all \
	init \
	istio \
	secrets \
	dev \
	run \
	dashboard
