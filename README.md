brymck-io
=========

Development
-----------

Prerequisites:

* [Docker](https://www.docker.com/get-started) with Kubernetes enabled
* [Skaffold](https://github.com/GoogleContainerTools/skaffold)

Create an `.env.local` file containing exports for the following environment variables:

* `AUTH_FLASK_SECRET_KEY`
* `AUTH0_CLIENT_ID`
* `AUTH0_CLIENT_SECRET`
* `KANIKO_SECRET`

Then run

```bash
make dev
```
