# shared-library

A Jenkins shared library with a `mavenBuild` pipeline step and a `Version` helper, a consumer `Jenkinsfile.example`, and a layout verifier.

## Goal

Show how a pipeline shape is written once in `vars/` and consumed by one line in each repository. The folder also shows where plain classes live (`src/`) so they can be tested without Jenkins.

## Run it

```
python3 shared-library/verify.py
```

Expected: `ok: 1 step(s), library layout valid`, exit code 0.

Not run end to end: loading the library needs a controller configured with `orders-lib` (the `jcasc` folder declares it, pointing at an address that does not resolve). `Version.groovy` has no unit test here.

## What it proves

- `vars/mavenBuild.groovy` defines `call(Map cfg)` with defaults `goals: 'verify'` and the `maven:3.9.9-eclipse-temurin-21` image, and wraps a whole declarative pipeline with a timeout and JUnit publishing.
- `Jenkinsfile.example` is the full consumer: `@Library('orders-lib@main') _` followed by `mavenBuild(goals: 'verify')`.
- `src/org/orders/Version.groovy` turns a branch and build number into a tag: `main` gives `1.0.<build>`, other branches give a sanitised `<branch>-<build>`.
- `verify.py` checks that every `vars/*.groovy` has `call(`, every `src/` package name matches its directory, and the example only calls steps that exist.

## Trade-offs

- A change to the library affects every consumer at once; pinning `@main` means a bad merge breaks all builds.
- The step fixes the whole pipeline, so teams that need a different stage layout must add options or fork the step.
- The verifier is a layout check, not a compile; Groovy errors only show up in Jenkins.

## When not to use it

- For a single repository, where a plain `Jenkinsfile` is simpler.
- When consumers need very different pipelines; a shared step then hides more than it saves.
