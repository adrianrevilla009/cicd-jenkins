# jcasc

A Jenkins controller image with pinned plugins, configured entirely by a Configuration as Code file and started with Docker Compose.

## Goal

Make the controller reproducible: no setup wizard and no UI clicks, just a Dockerfile, a plugin list and `jenkins.yaml`. The admin password comes from the environment, never from the file.

## Run it

```
python3 jcasc/verify.py
cp jcasc/.env.example jcasc/.env      # then change the password
docker compose -f jcasc/compose.yaml up --build
```

Expected from the verifier: `ok: JCasC, plugins and compose valid`. After `up`, the controller should listen on http://localhost:8080 and ask for the `admin` login.

Not run end to end: the image build and the container start were not run here, only the offline verifier. Cleanup: `docker compose -f jcasc/compose.yaml down -v` removes the container and the `jenkins_home` volume. Compose refuses to start if `JENKINS_ADMIN_PASSWORD` is unset.

## What it proves

- `Dockerfile` uses `jenkins/jenkins:2.492.1-lts-jdk21`, disables the setup wizard and installs the five plugins in `plugins.txt`, each pinned to a version.
- `jenkins.yaml` sets zero executors, a local `admin` user whose password is `${JENKINS_ADMIN_PASSWORD}`, no signup, no anonymous read and a CSRF crumb issuer.
- It declares the global library `orders-lib` (remote `https://example.invalid/orders-lib.git`, which must be replaced with a real repository) and a Job DSL `orders-ci` job.
- `verify.py` fails on a user password that is not a `${VAR}` reference, an unpinned plugin, `latest` in the Dockerfile, anonymous read, or a non-zero executor count.

## Trade-offs

- With zero executors on the controller, no build runs until an agent exists; see `jenkins-k8s-agents`.
- The `orders-ci` job uses `agent any` in its inline script, which the sample job tolerates but real pipelines should avoid.
- Plugin versions need regular bumps; pinned versions go stale and the verifier only checks the format.

## When not to use it

- For a throwaway local Jenkins where a UI-configured container is enough.
- When the controller is managed by a Helm chart that already carries its own JCasC values.
