#!/usr/bin/env python3
import os, json, re, time
from pathlib import Path
from utils_common import MD_LINK, WIKI, FRONT, sha

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "_brain"
OUTDIR.mkdir(exist_ok=True)

IGNORE_DIRS = {".git", ".github", ".obsidian", "node_modules", ".venv", "__pycache__", "_site", "dist", "build", ".next", ".vite"}
ATTACH_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".mp3", ".wav", ".ogg", ".flac", ".mp4", ".mov", ".pdf"}

def parse_front(text: str):
    m = FRONT.match(text)
    if not m:
        return {}, text
    try:
        import yaml
        fm = yaml.safe_load(m.group(1)) or {}
    except Exception:
        fm = {}
    return fm, text[m.end():]

def headings_blocks(body: str):
    lines = body.splitlines()
    blocks = []
    cur = {"heading": None, "content": []}
    for line in lines:
        if line.startswith("#"):
            if cur["heading"] or cur["content"]:
                blocks.append(cur)
            cur = {"heading": line.strip(), "content": []}
        else:
            cur["content"].append(line)
    if cur["heading"] or cur["content"]:
        blocks.append(cur)
    return blocks

def extract_links(text: str):
    links = []
    for m in MD_LINK.finditer(text):
        links.append({"kind": "md", "text": m.group(1), "target": m.group(2)})
    for m in WIKI.finditer(text):
        links.append({"kind": "wiki", "page": m.group(1), "section": m.group(2), "alias": m.group(3)})
    return links

def file_manifest():
    man = {}
    for root, dirs, files in os.walk(ROOT):
        rel = Path(root).relative_to(ROOT)
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith(".")]
        for f in files:
            p = Path(root) / f
            relp = p.relative_to(ROOT).as_posix()
            if p.suffix.lower() in ATTACH_EXT:
                man[relp] = {"type": "asset", "size": p.stat().st_size, "mtime": int(p.stat().st_mtime)}
            elif p.suffix.lower() == ".md":
                try: txt = p.read_text(encoding="utf-8", errors="ignore")
                except Exception: txt = ""
                man[relp] = {"type": "note", "sha": sha(txt), "size": len(txt), "mtime": int(p.stat().st_mtime)}
    return man

def collect():
    manifest = file_manifest()
    files = []; attachments = []
    by_name = {}
    for path, meta in manifest.items():
        if meta["type"] == "asset":
            attachments.append(path); continue
        p = ROOT / path
        txt = p.read_text(encoding="utf-8", errors="ignore")
        fm, body = parse_front(txt)
        blocks = headings_blocks(body)
        links = extract_links(body)
        title = fm.get("title") or (blocks[0]["heading"][1:].strip() if blocks and blocks[0]["heading"] else Path(path).stem)
        obj = {"id": sha(path), "path": path, "title": title, "sha": meta["sha"],
               "front_matter": fm, "links": links,
               "blocks": [{"anchor": (b["heading"][1:].strip() if b["heading"] else None),
                           "content": "\n".join(b["content"]).strip()} for b in blocks]}
        files.append(obj)
        by_name.setdefault(Path(path).stem.lower(), []).append(path)
    # resolve wiki refs
    for f in files:
        resolves = []
        for L in f.get("links", []):
            if L["kind"] == "wiki":
                target = (L.get("page") or "").strip()
                if not target: continue
                cands = by_name.get(Path(target).stem.lower(), [])
                if cands: resolves.append({"page": target, "resolved_paths": cands, "section": L.get("section"), "alias": L.get("alias")})
        if resolves: f["wiki_resolved"] = resolves
    brain = {"schema": "psiopera.ai_brain.v2", "source_repo": Path('.').resolve().name,
             "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
             "files_count": len(files), "attachments_count": len(attachments),
             "files": sorted(files, key=lambda x: x["path"].lower()), "attachments": sorted(attachments),
             "manifest": manifest}
    (OUTDIR / "ai_brain.json").write_text(json.dumps(brain, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Wrote _brain/ai_brain.json with", len(files), "notes")
if __name__ == "__main__":
    collect()
