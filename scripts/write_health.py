#!/usr/bin/env python3
import subprocess, time
from pathlib import Path
from datetime import datetime, timezone
import json

ROOT = Path(__file__).resolve().parents[1]
stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
try:
    sha = subprocess.check_output(["git","rev-parse","--short","HEAD"], cwd=ROOT, text=True).strip()
except Exception:
    sha = "unknown"

payload = {
    "status": "ok",
    "generated_at_utc": stamp,
    "commit": sha,
    "repo": ROOT.name,
}

# health.json
(ROOT / "health.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

# health.html
(ROOT / "health.html").write_text(f"""<!doctype html>
<meta charset="utf-8">
<title>Health — {ROOT.name}</title>
<style>body{{font:14px/1.5 system-ui,Segoe UI,Roboto,Arial,sans-serif;padding:24px}}</style>
<h1>Health</h1>
<p><b>Status:</b> ok</p>
<p><b>Generated at (UTC):</b> {stamp}</p>
<p><b>Commit:</b> {sha}</p>
""", encoding="utf-8")
print("Wrote health.json and health.html")
