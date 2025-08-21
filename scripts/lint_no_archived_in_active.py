#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
bad = []

for p in ROOT.rglob("*.md"):
    rel = p.relative_to(ROOT).as_posix()
    if rel.startswith("AI Brain/Archive/"):
        continue
    try:
        txt = p.read_text(encoding="utf-8", errors="ignore")
    except:
        continue
    head = "\n".join(txt.splitlines()[:25]).lower()
    if "[archive]" in rel.lower() or "status: archived" in head or "archived: true" in head:
        bad.append(rel)

if bad:
    print("Archived docs found outside Archive folder:")
    for b in bad: print(" -", b)
    sys.exit(1)

print("OK: no archived content in active paths.")
