# jenkins-multibranch

A Job DSL script that creates a multibranch pipeline for the Orders repository, and the branch-aware `Jenkinsfile` it runs.

## Goal

Show how Jenkins builds every branch of a repository without anyone creating jobs by hand, while keeping deployment limited to `main`.

## Run it

```
python3 jenkins-multibranch/verify.py
```

Expected: `ok: multibranch DSL and Jenkinsfile consistent`, exit code 0.

Not run end to end: `multibranch.groovy` needs a controller with the Job DSL plugin and a reachable repository; its remote is `https://example.invalid/orders.git` and must be replaced. Only the offline consistency check was run.

## What it proves

- `multibranch.groovy` defines `multibranchPipelineJob('orders')` with one Git source, branch discovery, `scriptPath('Jenkinsfile')`, a daily folder re-scan and removal of old branch jobs after 14 days or beyond 10 kept.
- New branches do not build automatically (`noTriggerBranchProperty`), so a scan alone does not start a flood of builds.
- `Jenkinsfile` always runs Test, skips the Integration stage for change requests (`not { changeRequest() }`) and runs Deploy only when `branch 'main'`.
- `verify.py` fails if the DSL lacks those building blocks or the `Jenkinsfile` has no `main` gate, no `changeRequest()` or never reads `BRANCH_NAME`.

## Trade-offs

- Plain Git sources discover branches only; pull request discovery needs an SCM provider such as the GitHub Branch Source plugin.
- A daily scan is cheap but slow to notice new branches unless a webhook triggers it.
- The Deploy stage only echoes the branch and build number; a real deployment is not part of this folder.

## When not to use it

- For a repository with one long-lived branch, where a single pipeline job is enough.
- When all pipelines must live in one central repository rather than next to the code.
