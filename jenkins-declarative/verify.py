#!/usr/bin/env python3
"""Structural lint of a declarative Jenkinsfile (no Jenkins needed)."""
import re, sys

t = open(sys.argv[1] if len(sys.argv) > 1 else "Jenkinsfile").read()
need = {
    "pipeline block": r"^pipeline\s*\{",
    "agent": r"^\s*agent\s",
    "stages": r"^\s*stages\s*\{",
    "timeout option": r"timeout\(",
    "post section": r"^\s*post\s*\{",
    "at least 2 stages": r"(?s)stage\(.*stage\(",
}
bad = [k for k, rx in need.items() if not re.search(rx, t, re.M)]
if t.count("{") != t.count("}"):
    bad.append("unbalanced braces")
if re.search(r"agent\s+any\b", t):
    bad.append("agent any is too broad")
if re.search(r"(password|token)\s*=\s*['\"]", t, re.I):
    bad.append("hard-coded secret")
print("FAIL: " + ", ".join(bad) if bad else "ok: Jenkinsfile structure valid")
sys.exit(1 if bad else 0)
