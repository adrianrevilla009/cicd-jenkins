# jenkins-declarative

A declarative `Jenkinsfile` that builds and tests the Orders service, plus a verifier that lints its structure without Jenkins.

## Goal

Show the parts of a production-minded declarative pipeline: a pinned build container, run limits, stage ordering, a gated deploy and cleanup. The verifier catches common structural mistakes before the file reaches a controller.

## Run it

```
python3 jenkins-declarative/verify.py jenkins-declarative/Jenkinsfile
```

Expected: `ok: Jenkinsfile structure valid`, exit code 0. Inside the folder the file argument can be omitted.

Not run end to end: the pipeline itself needs a Jenkins controller with Docker available to its agents. Only the structural lint was run here.

## What it proves

- `Jenkinsfile` runs in `maven:3.9.9-eclipse-temurin-21`, with a 15 minute timeout, 20 kept builds, no concurrent builds and timestamps.
- Stages are Build (`mvn -B -q -DskipTests package`), Test (`mvn -B test`, JUnit reports published in `post { always }`) and Deploy.
- Deploy only runs on `main`, asks for manual approval through `input`, and is an `echo` step, not a real deployment.
- `verify.py` fails on a missing `pipeline`, `agent`, `stages`, `timeout(` or `post` block, fewer than two stages, unbalanced braces, `agent any`, or a hard-coded `password`/`token` assignment.

## Trade-offs

- The check is regex and brace counting, not a Groovy parse; it will not catch a syntax error that keeps braces balanced.
- The Docker agent needs a Docker socket or Docker-capable node, which is a privilege many teams avoid on shared controllers.
- `cleanWs()` keeps agents tidy but throws away the workspace; Maven caches in `.m2` are lost between builds.

## When not to use it

- When many services share the same pipeline shape; move the stages into a shared library (see `shared-library`).
- When agents run in Kubernetes; use a pod template instead of a Docker agent (see `jenkins-k8s-agents`).
