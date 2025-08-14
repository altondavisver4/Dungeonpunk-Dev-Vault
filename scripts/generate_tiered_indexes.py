#!/usr/bin/env python3
import os, re, pathlib, sys
from datetime import datetime

REPO = pathlib.Path(".").resolve()

# Folders we never scan
SKIP_DIRS = {".git", ".github", "_brain", "node_modules", "scripts", ".obsidian", "tags", ".venv", "__pycache__"}

# Tiers -> accepted tag synonyms (lowercase)
TIERS = {
    "AI_INDEX_CORE.md":     {"core", "canonical", "pillar"},
    "AI_INDEX_SYSTEMS.md":  {"systems", "mechanics", "rules"},
    "AI_INDEX_LORE.md":     {"lore", "worldbuilding", "story"},
    "AI_INDEX_RND.md":      {"rnd", "r&d", "research", "prototype", "experiment"},
}

MD_LINK_BASE = ""  # use repo-relative links so they render in GitHub

TAG_RE_INLINE = re.compile(r"#([\w&-]+)")  # catches #core #r&d etc
FM_START = re.compile(r"^---\s*$")
FM_TAGS  = re.compile(r"^tags\s*:\s*\[(.*?)\]\s*$", re.IGNORECASE)

def extract_tags(md_text: str):
    tags = set()
    lines = md_text.splitlines()
    # 1) front-matter block (YAML-lite)
    if lines and FM_START.match(lines[0]):
        for i in range(1, min(len(lines), 50)):  # only scan a small header block
            if FM_START.match(lines[i]): break
            m = FM_TAGS.match(lines[i])
            if m:
                vals = [t.strip().strip(",").strip().strip("'\"") for t in m.group(1).split(",")]
                tags.update(v.lower() for v in vals if v)
    # 2) inline hashtags
    for m in TAG_RE_INLINE.finditer(md_text):
        tags.add(m.group(1).lower())
    return tags

def should_skip_dir(dirpath: pathlib.Path) -> bool:
    parts = {p.name for p in dirpath.parts}
    return any(part in SKIP_DIRS for part in parts)

def collect_tagged_files():
    tagged = []  # (relpath, tags)
    for root, dirs, files in os.walk(REPO):
        root_p = pathlib.Path(root)
        # prune directories in-place
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        if should_skip_dir(root_p):
            continue
        for f in files:
            if not f.lower().endswith(".md"): 
                continue
            rel = (root_p / f).relative_to(REPO)
            try:
                text = (root_p / f).read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            tags = extract_tags(text)
            if tags:
                tagged.append((rel.as_posix(), tags))
    return tagged

def build_index(title, pairs):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    out = [f"# {title}\n",
           f"_Auto-generated from tags · Last updated: **{now}**_\n",
           "\n---\n"]
    # Group by top-level folder for neatness
    by_folder = {}
    for path, tags in sorted(pairs, key=lambda x: x[0].lower()):
        top = path.split("/", 1)[0] if "/" in path else "."
        by_folder.setdefault(top, []).append((path, tags))
    for folder in sorted(by_folder):
        out.append(f"\n## {folder}\n")
        for path, tags in by_folder[folder]:
            tag_str = ", ".join(sorted(tags))
            # repo-relative link
            out.append(f"- [{path}]({MD_LINK_BASE}{path})  \n  <sub>tags: {tag_str}</sub>")
    out.append("\n")
    return "\n".join(out)

def main():
    tagged = collect_tagged_files()
    if not tagged:
        print("No tagged files found; generating empty tier indexes.")
    # invert into buckets
    for outfile, accepted in TIERS.items():
        members = [(p, t & accepted) for (p, t) in tagged if (t & accepted)]
        title = outfile.replace("_", " ").replace(".md", "")
        content = build_index(title, members)
        (REPO / outfile).write_text(content, encoding="utf-8")
        print(f"Wrote {outfile} with {len(members)} entries.")
    print("Done.")

if __name__ == "__main__":
    sys.exit(main())
