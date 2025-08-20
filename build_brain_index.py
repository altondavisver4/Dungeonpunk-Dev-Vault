# save as build_brain_index.py
import json, re, os, sys, pathlib, textwrap
from datetime import datetime

# ==== CONFIG ====
# Point this to your Obsidian vault folder (absolute path recommended).
VAULT_ROOT = r"/path/to/Your/Obsidian/Vault"          # <-- edit me
RAW_EXPORT = r"AI Brain/Raw Exports/conversations.json"  # the file you just added
IDEA_DIR   = r"AI Brain/Idea Cards"
INDEX_PATH = r"AI Brain/Brain Index.md"

# ==== HELPERS ====
def safe_slug(s, maxlen=80):
    s = re.sub(r"[^a-zA-Z0-9-_ ]+", "", s).strip().replace(" ", "-")
    return s[:maxlen] if s else "untitled"

def detect_tags(text):
    text_low = text.lower()
    tags = set()
    # quick-and-dirty heuristics; adjust as your Brain grows
    if any(k in text_low for k in ["doctrine", "roll interpreter", "universal narrative rng", "pf2e→fate", "tone band"]):
        tags.add("Doctrine")
    if any(k in text_low for k in ["heat/doom", "graduation", "parallel operator", "behavior card", "progress clock", "tiles", "tracks", "zones"]):
        tags.add("Mechanic")
    if any(k in text_low for k in ["theme", "narrative", "companion", "bioware", "saint's row 2", "conan tone"]):
        tags.add("Theme")
    # stale/experimental hints
    if any(k in text_low for k in ["out of date", "obsolete", "dead end", "superseded"]):
        tags.add("Outdated")
    if "???" in text or "open question" in text_low:
        tags.add("Questionable")
    return sorted(tags) or ["Unsorted"]

def brief_summary(text, limit=280):
    clean = " ".join(text.split())
    return (clean[:limit] + "…") if len(clean) > limit else clean

def ensure_dir(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

# ==== LOAD ====
vault = pathlib.Path(VAULT_ROOT)
export_path = vault / RAW_EXPORT
idea_dir = vault / IDEA_DIR
index_path = vault / INDEX_PATH

ensure_dir(idea_dir)
ensure_dir(index_path.parent)

with open(export_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Exports typically look like: {"conversations": [ {...}, {...} ]}
convos = data.get("conversations", data if isinstance(data, list) else [])

rows = []
for c in convos:
    # fields vary by export version; be defensive
    title = c.get("title") or "Untitled Conversation"
    create_time = c.get("create_time") or c.get("update_time") or c.get("create_time_ts")
    try:
        dt = datetime.fromtimestamp(create_time) if isinstance(create_time, (int, float)) else datetime.fromisoformat(str(create_time).replace("Z",""))
    except Exception:
        dt = None

    date_str = dt.strftime("%Y-%m-%d") if dt else "0000-00-00"
    # Flatten messages for analysis
    msgs = c.get("mapping") or c.get("messages") or {}
    # mapping format: dict of id -> node with "message": {"author":{"role":...}, "content":{...}}
    texts = []
    if isinstance(msgs, dict):
        for node in msgs.values():
            m = node.get("message") if isinstance(node, dict) else None
            if not m: continue
            content = m.get("content") or {}
            parts = content.get("parts") if isinstance(content, dict) else None
            if isinstance(parts, list):
                for p in parts:
                    if isinstance(p, str): texts.append(p)
            elif isinstance(content, str):
                texts.append(content)
    elif isinstance(msgs, list):
        for m in msgs:
            content = m.get("content", "")
            if isinstance(content, str):
                texts.append(content)
            elif isinstance(content, dict) and "parts" in content:
                for p in content["parts"]:
                    if isinstance(p, str): texts.append(p)

    full_text = "\n\n".join(texts).strip()
    summary = brief_summary(full_text or title)
    tags = detect_tags(full_text + " " + title)

    slug = f"{date_str}-{safe_slug(title)}"
    md_path = idea_dir / f"{slug}.md"

    card = f"""---
title: "{title.replace('"','\'')}"
date: {date_str}
tags: {tags}
---

# {title}

**Date:** {date_str}  
**Tags:** {", ".join(tags)}

## 1-Line Summary
{summary}

## Core Topics
- (auto) {", ".join(tags)}

## Notable Mechanics / Ideas
- (skim during curation and replace these bullets)

## Raw Notes (excerpt)
{ textwrap.shorten(full_text, width=2000, placeholder=" …") if full_text else "_(no text parsed)_" }
"""
    with open(md_path, "w", encoding="utf-8") as outf:
        outf.write(card)

    rows.append((date_str, title, tags, os.path.relpath(md_path, vault)))

# Build index
rows.sort(key=lambda r: r[0], reverse=True)
lines = ["# Brain Index\n"]
for date_str, title, tags, rel in rows:
    lines.append(f"- **{date_str}** – [{title}]({rel}) — ({', '.join(tags)})")

with open(index_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ Wrote {len(rows)} Idea Cards to: {idea_dir}")
print(f"✅ Master index at: {index_path}")
