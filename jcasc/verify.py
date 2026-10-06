#!/usr/bin/env python3
"""Validate the JCasC file: parses, has required roots, no plaintext secrets, plugins pinned."""
import pathlib, re, sys
import yaml

here = pathlib.Path(__file__).parent
cfg = yaml.safe_load((here / "jenkins.yaml").read_text())
bad = []
for root in ("jenkins", "unclassified"):
    if root not in cfg:
        bad.append(f"missing root '{root}'")
j = cfg.get("jenkins", {})
if j.get("numExecutors") != 0:
    bad.append("controller should run 0 executors")
if "authorizationStrategy" not in j:
    bad.append("no authorizationStrategy")
if j.get("authorizationStrategy", {}).get("loggedInUsersCanDoAnything", {}).get("allowAnonymousRead"):
    bad.append("anonymous read enabled")
for u in j.get("securityRealm", {}).get("local", {}).get("users", []):
    if not re.fullmatch(r"\$\{[A-Z_]+\}", str(u.get("password", ""))):
        bad.append(f"user {u.get('id')}: password must be a ${{VAR}} reference")
for line in (here / "plugins.txt").read_text().split():
    if not re.fullmatch(r"[\w-]+:[\w.]+", line):
        bad.append(f"plugin not pinned: {line}")
if "latest" in (here / "Dockerfile").read_text():
    bad.append("Dockerfile uses latest")
compose = yaml.safe_load((here / "compose.yaml").read_text())
if "jenkins" not in compose.get("services", {}):
    bad.append("compose lacks jenkins service")
print("FAIL: " + "; ".join(bad) if bad else "ok: JCasC, plugins and compose valid")
sys.exit(1 if bad else 0)
