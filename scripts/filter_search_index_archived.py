#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = json.loads((ROOT/"_brain/policy.json").read_text(encoding="utf-8"))
SINDEX = ROOT/"_brain"/"search_index.json"
if not SINDEX.exists():
    raise SystemExit("search_index.json not found")

data = json.loads(SINDEX.read_text(encoding="utf-8"))
items = data.get("items") or data.get("docs") or []

def is_archived(item):
    path = (item.get("path") or item.get("file") or "")
    title = (item.get("title") or "")
    fm = item.get("front_matter") or {}
    rules = POLICY.get("archive_rules", {})
    if any(p in path for p in rules.get("path_prefixes", [])): return True
    if any(m in path or m in title for m in rules.get("title_markers", [])): return True
    if str(fm.get("status","")).lower() in rules.get("front_matter_values", []): return True
    if fm.get("archived") is True or fm.get("deprecated") is True: return True
    return False

filtered = [it for it in items if not is_archived(it)]
for k in ("items","docs"):
    if k in data: data[k] = filtered

SINDEX.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Filtered {len(items)-len(filtered)} archived entries from search index.")
