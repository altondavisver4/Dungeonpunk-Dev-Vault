#!/usr/bin/env python3
import json, re, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRAIN = ROOT / "_brain" / "ai_brain.json"
OUT = ROOT / "_brain" / "ai_super_index.json"

TIER_FILES = {
    "core":      "AI_INDEX_CORE.md",
    "systems":   "AI_INDEX_SYSTEMS.md",
    "lore":      "AI_INDEX_LORE.md",
    "rnd":       "AI_INDEX_RND.md",
}

def load_tier_members():
    members = {k:set() for k in TIER_FILES}
    for tier, fn in TIER_FILES.items():
        p = ROOT / fn
        if not p.exists():
            continue
        txt = p.read_text(encoding="utf-8", errors="ignore")
        for line in txt.splitlines():
            line=line.strip()
            if not line.startswith("- "): 
                continue
            m = re.search(r"\]\(([^)]+)\)", line)
            if m:
                path = m.group(1).split("#",1)[0]
                members[tier].add(path)
    return members

def make_graph(files):
    by_path = {f["path"]: f for f in files}
    graph = {p: set() for p in by_path}
    for f in files:
        p = f["path"]
        # md links
        for L in f.get("links", []):
            if L.get("kind")=="md":
                tgt = (L.get("target","").split("#",1)[0]).strip()
                if tgt in by_path:
                    graph[p].add(tgt)
        # wiki links (resolved)
        for res in f.get("wiki_resolved", []):
            for rp in res.get("resolved_paths", []):
                if rp in by_path:
                    graph[p].add(rp)
    # make undirected for robustness
    for a in list(graph.keys()):
        for b in list(graph[a]):
            if b in graph:
                graph[b].add(a)
    return {k: sorted(v) for k,v in graph.items()}

def main():
    if not BRAIN.exists():
        raise SystemExit("ai_brain.json not found. Run scripts/export_brain.py first.")
    data = json.loads(BRAIN.read_text(encoding="utf-8"))
    files = data.get("files", [])
    tiers = load_tier_members()
    graph = make_graph(files)

    docs = []
    for f in files:
        path = f["path"]
        fm = f.get("front_matter", {}) or {}
        tags = fm.get("tags") or fm.get("tag") or []
        if isinstance(tags, str):
            tags = [tags]
        tiers_member = [t for t, ps in tiers.items() if path in ps]
        docs.append({
            "id": f.get("id"),
            "path": path,
            "title": f.get("title"),
            "tags": tags,
            "blocks": f.get("blocks", []),
            "neighbors": graph.get(path, []),
            "tiers": tiers_member,
        })
    super_index = {
        "schema": "psiopera.ai_super_index.v1",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "files_count": len(files),
        "docs": docs,
    }
    OUT.write_text(json.dumps(super_index, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUT} with {len(docs)} docs.")
if __name__=="__main__":
    main()
