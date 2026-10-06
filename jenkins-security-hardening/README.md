# jenkins-security-hardening

A hardened Configuration as Code file for a Jenkins controller and a script that audits it against an 11-item checklist.

## Goal

Turn common Jenkins hardening advice into settings you can read in one file and check automatically, so a regression shows up as a failed check.

## Run it

```
python3 jenkins-security-hardening/verify.py
```

Expected: eleven lines starting with `ok`, one per check, and exit code 0. Any `FAIL` line makes the exit code 1.

Not run end to end: `hardened.yaml` was never loaded into a controller. The `roleBased` strategy needs the Role-based Authorization Strategy plugin, which is not in the `jcasc` plugin list, so add it before using this file there.

## What it proves

- `hardened.yaml` sets zero controller executors, no signup, no remember-me, role-based authorization (an `admin` role and a read/build-only `dev` role) and a crumb issuer.
- It turns on agent-to-controller protection, disables legacy API tokens, closes the SSHD port (`-1`) and runs queued builds as the triggering user.
- Job DSL script security is on and the approved-signature list is empty.
- `verify.py` prints one line per check and also fails if the word `password` appears anywhere in the file.

## Trade-offs

- The audit reads the YAML only; it cannot tell whether the running controller matches it.
- Strict roles break pipelines that relied on open permissions; the `developers` group must exist in the identity source.
- `securityRealm` stays local with no users defined, so a real realm such as LDAP or OIDC has to be added.

## When not to use it

- As a complete security programme: it ignores plugin updates, network exposure, credentials handling and agent hardening.
- On a controller that already enforces these settings through a managed platform.
