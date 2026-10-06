#!/usr/bin/env python3
"""Validate the agent pod template and cloud config without a cluster."""
import pathlib, re, sys
import yaml

here = pathlib.Path(__file__).parent
bad = []
pod = yaml.safe_load((here / "pod-template.yaml").read_text())
spec = pod["spec"]
if pod.get("kind") != "Pod":
    bad.append("pod-template is not a Pod")
if not spec.get("securityContext", {}).get("runAsNonRoot"):
    bad.append("pod must run as non-root")
names = [c["name"] for c in spec["containers"]]
for c in spec["containers"]:
    if not re.search(r":[\w.-]+$", c["image"]) or c["image"].endswith(":latest"):
        bad.append(f"{c['name']}: image must have a pinned tag")
    r = c.get("resources", {})
    if "limits" not in r or "requests" not in r:
        bad.append(f"{c['name']}: requests and limits required")
    if c.get("securityContext", {}).get("allowPrivilegeEscalation") is not False:
        bad.append(f"{c['name']}: allowPrivilegeEscalation must be false")
jf = (here / "Jenkinsfile").read_text()
dc = re.search(r"defaultContainer\s+'([\w-]+)'", jf)
if not dc or dc.group(1) not in names:
    bad.append("defaultContainer must name a container in the pod template")
if "pod-template.yaml" not in jf:
    bad.append("Jenkinsfile does not use pod-template.yaml")
cloud = yaml.safe_load((here / "cloud.yaml").read_text())["jenkins"]["clouds"][0]["kubernetes"]
if not cloud.get("containerCapStr"):
    bad.append("cloud needs containerCapStr to bound agents")
print("FAIL: " + "; ".join(bad) if bad else "ok: pod template, Jenkinsfile and cloud config valid")
sys.exit(1 if bad else 0)
