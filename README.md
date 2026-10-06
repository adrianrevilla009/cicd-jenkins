# cicd-jenkins

Six small Jenkins setups for a build-and-test pipeline of a Java 21 Orders service: declarative pipelines, a shared library, a reproducible controller with Configuration as Code, Kubernetes agents, multibranch and a security checklist.

## What is inside

| Folder | What it shows | Run |
| --- | --- | --- |
| [`jenkins-declarative`](./jenkins-declarative) | Declarative `Jenkinsfile` with Docker agent, timeout, stages, a gated deploy and post actions | `python3 jenkins-declarative/verify.py jenkins-declarative/Jenkinsfile` |
| [`shared-library`](./shared-library) | Shared library with a `mavenBuild` step, a `Version` helper and a consumer `Jenkinsfile` | `python3 shared-library/verify.py` |
| [`jcasc`](./jcasc) | Controller image with pinned plugins and a JCasC file, run through Docker Compose | `python3 jcasc/verify.py` |
| [`jenkins-k8s-agents`](./jenkins-k8s-agents) | One-pod-per-build Kubernetes agents from a pod template and a cloud definition | `python3 jenkins-k8s-agents/verify.py` |
| [`jenkins-multibranch`](./jenkins-multibranch) | Job DSL seed for a multibranch job and a branch-aware `Jenkinsfile` | `python3 jenkins-multibranch/verify.py` |
| [`jenkins-security-hardening`](./jenkins-security-hardening) | A hardened JCasC file audited against an 11-item checklist | `python3 jenkins-security-hardening/verify.py` |

## Prerequisites

- Python 3 with PyYAML (`jcasc`, `jenkins-k8s-agents` and `jenkins-security-hardening` verifiers)
- Docker with Compose, only to build and start the controller in `jcasc`
- A Kubernetes cluster such as kind, only to run the pipeline in `jenkins-k8s-agents`

## How to read it

Start with `jenkins-declarative`, then `shared-library`, which reuses the same build. Every folder has a `verify.py` that checks the files offline; none of them needs a running Jenkins. The shared Orders domain only appears as the service being built.
