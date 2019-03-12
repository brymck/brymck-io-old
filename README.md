brymck-io
=========

[![Build Status](https://travis-ci.com/brymck/brymck-io.svg?branch=master)](https://travis-ci.com/brymck/brymck-io)

Development
-----------

Prerequisites:

* [Docker](https://www.docker.com/get-started) with Kubernetes enabled
* [Skaffold](https://github.com/GoogleContainerTools/skaffold)

Create an `.env.local` file containing exports for the following environment variables:

* `AUTH_FLASK_SECRET_KEY`
* `AUTH0_CLIENT_ID`
* `AUTH0_CLIENT_SECRET`
* `DEFAULT_REPO`

You need to run the following once:

```bash
make init
```

Going forward, you can then run one of

```bash
make dev  # deploy, watch and push changes, delete on quit
make run  # deploy indefinitely
```
