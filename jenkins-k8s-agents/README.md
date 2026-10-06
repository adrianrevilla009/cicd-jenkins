# jenkins-k8s-agents

A Kubernetes cloud definition, a pod template and a `Jenkinsfile` that runs each build in its own short-lived pod.

## Goal

Show ephemeral build agents: every build gets a fresh, resource-limited, non-root pod that disappears afterwards, so the controller needs no permanent workers.

## Run it

```
python3 jenkins-k8s-agents/verify.py
```

Expected: `ok: pod template, Jenkinsfile and cloud config valid`, exit code 0.

Not run end to end: it needs a controller with the Kubernetes plugin, a cluster such as kind, a `jenkins-agents` namespace and a `k8s-sa-token` credential. No pod was started here. A kind cluster is the intended target and costs nothing; `kind delete cluster` removes it.

## What it proves

- `pod-template.yaml` runs a `maven:3.9.9-eclipse-temurin-21` container as user 1000 with `runAsNonRoot`, `allowPrivilegeEscalation: false`, and requests of 500m CPU / 1Gi against limits of 1 CPU / 2Gi.
- `Jenkinsfile` loads that file with `yamlFile` and sets `defaultContainer 'maven'`, so `sh 'mvn -B test'` runs in the Maven container.
- `cloud.yaml` points at namespace `jenkins-agents`, caps concurrency at 5 pods (`containerCapStr`) and uses a credential id rather than a token.
- `verify.py` fails on a root pod, an unpinned or `latest` image, missing requests or limits, a `defaultContainer` that names no container, or a missing cap.

## Trade-offs

- A pod start adds seconds to each build, and Maven dependencies are downloaded again unless a cache volume is added.
- `jenkinsUrl` and `jenkinsTunnel` assume the controller runs in a `jenkins` namespace of the same cluster.
- Only the Maven container is defined; builds that need Docker images require a daemonless builder or an extra container.

## When not to use it

- When there is no Kubernetes cluster; a Docker agent or static nodes are simpler.
- For very short pipelines where pod start-up dominates the run time.
