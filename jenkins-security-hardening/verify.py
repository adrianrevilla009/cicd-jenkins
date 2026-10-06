#!/usr/bin/env python3
"""Audit hardened.yaml against a short checklist; exits non-zero on any miss."""
import pathlib, sys
import yaml

cfg = yaml.safe_load((pathlib.Path(__file__).parent / "hardened.yaml").read_text())
j, s = cfg["jenkins"], cfg["security"]
checks = {
    "controller builds nothing (numExecutors 0)": j.get("numExecutors") == 0,
    "signup disabled": j["securityRealm"]["local"]["allowsSignup"] is False,
    "role-based authorization": "roleBased" in j["authorizationStrategy"],
    "no anonymous/loggedIn-can-do-anything": "loggedInUsersCanDoAnything" not in j["authorizationStrategy"],
    "CSRF crumb issuer on": "crumbIssuer" in j,
    "agent-to-controller security on": j.get("remotingSecurity", {}).get("enabled") is True,
    "legacy API tokens off": s["apiToken"]["creationOfLegacyTokenEnabled"] is False,
    "SSHD disabled": s["sSHD"]["port"] == -1,
    "builds run as triggering user": "queueItemAuthenticator" in s,
    "Job DSL script security on": cfg["unclassified"]["globalJobDslSecurityConfiguration"]["useScriptSecurity"] is True,
    "no inline passwords": "password" not in yaml.dump(cfg).lower(),
}
failed = [k for k, ok in checks.items() if not ok]
for k, ok in checks.items():
    print(("ok   " if ok else "FAIL ") + k)
sys.exit(1 if failed else 0)
