#!/usr/bin/env python3
"""Check the Job DSL seed and the branch-aware Jenkinsfile."""
import pathlib, re, sys

here = pathlib.Path(__file__).parent
dsl = (here / "multibranch.groovy").read_text()
jf = (here / "Jenkinsfile").read_text()
bad = []
if dsl.count("{") != dsl.count("}"):
    bad.append("multibranch.groovy: unbalanced braces")
for key in ("multibranchPipelineJob", "branchSources", "orphanedItemStrategy", "periodicFolderTrigger", "gitBranchDiscovery"):
    if key not in dsl:
        bad.append(f"DSL lacks {key}")
if not re.search(r"scriptPath\('Jenkinsfile'\)", dsl):
    bad.append("scriptPath must point at Jenkinsfile")
if not re.search(r"when\s*\{\s*branch 'main'", jf):
    bad.append("deploy must be gated on main")
if "changeRequest()" not in jf:
    bad.append("no PR fast path (changeRequest)")
if "BRANCH_NAME" not in jf:
    bad.append("Jenkinsfile never reads BRANCH_NAME")
print("FAIL: " + "; ".join(bad) if bad else "ok: multibranch DSL and Jenkinsfile consistent")
sys.exit(1 if bad else 0)
