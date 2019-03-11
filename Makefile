secrets:
	pip install --quiet --requirement secrets/requirements.txt
	python secrets/create-secrets.py

.PHONY: secrets
