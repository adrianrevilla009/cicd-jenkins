#!/usr/bin/env python3
"""Check shared-library layout: vars/*.groovy define call(), src/ packages match paths."""
import pathlib, re, sys

root = pathlib.Path(__file__).parent
bad = []
steps = list(root.glob("vars/*.groovy"))
if not steps:
    bad.append("no vars/*.groovy steps")
for f in steps:
    if not re.search(r"^def call\(", f.read_text(), re.M):
        bad.append(f"{f.name}: no call() method")
for f in root.glob("src/**/*.groovy"):
    m = re.search(r"^package\s+([\w.]+)", f.read_text(), re.M)
    expected = ".".join(f.relative_to(root / "src").parent.parts)
    if not m or m.group(1) != expected:
        bad.append(f"{f.name}: package must be '{expected}'")
ex = (root / "Jenkinsfile.example").read_text()
used = re.search(r"@Library\('([\w-]+)@", ex)
called = re.findall(r"^(\w+)\(", ex, re.M)
for c in called:
    if not (root / "vars" / f"{c}.groovy").exists():
        bad.append(f"example calls unknown step {c}")
if not used:
    bad.append("example lacks @Library")
print("FAIL: " + "; ".join(bad) if bad else f"ok: {len(steps)} step(s), library layout valid")
sys.exit(1 if bad else 0)
