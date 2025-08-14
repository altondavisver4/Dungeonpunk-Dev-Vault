#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate four tiered index files (sorted by last git-modified time):
  - AI_INDEX_CORE.md
  - AI_INDEX_SYSTEMS.md
  - AI_INDEX_LORE.md
  - AI_INDEX_RND.md
"""

from __future__ import annotations
import os
import subprocess
from pathlib import Path
from datetime import datetime
import re
from typing import List, Dict, Tuple

ROOT = Path(__file__).resolve().parents[1]  # repo root
REPO_SLUG = os.environ.get("GITHUB_REPOSITORY", "altondavisver4/Dungeonpunk-Dev-Vault")
GH_BLOB_BASE = f"https://github.com/{REPO_SLUG}/blob/main"

# Category definitions: (friendly name, output filename, include folders)
CATEGORIES: List[Tuple[str, str, List[str]]] = [
    ("Core Vision", "AI_INDEX_CORE.md", ["01 – Game Bible/Core Vision"]),
    ("Systems",     "AI_INDEX_SYSTEMS.md", ["01 – Game Bible/Systems"]),
    ("World & Lore","AI_INDEX_LORE.md", ["01 – Game Bible/World & Lore"]),
    ("R&D Lab",     "AI_INDEX_RND.md", ["02 – R&D Lab"]),
]

# Filters (filenames to skip anywhere)
SKIP_BASENAMES = {
    "README.md",
    "AI_INDEX.md",
    "AI_INDEX_CORE.md",
    "AI_INDEX_SYSTEMS.md",
    "AI_INDEX_LORE.md",
    "AI_INDEX_RND.md",
    "AI_QUICKLINKS.md",
    "TAGS_INDEX.md",
    "README_AUTO_INDEX.md",
    "README_AUTO_NETLIFY_INDEX.md",
}
# Skip hidden / utility files
def should_skip(p: Path) -> bool:
    if p.name in SKIP_BASENAMES: return True
    if p.name.startswith("_"): return True
    # Only markdown notes
    if p.suffix.lower() != ".md": return True
    return False

H1_RE = re.compile(r"^#\s+(.*)")

def first_title_from_markdown(md: str) -> str | None:
    for line in md.splitlines():
        m = H1_RE.match(line.strip())
        if m:
            t = m.group(1).strip()
            # strip trailing markdown link markers etc
            t = re.sub(r"\s*\[*\]?\(.*\)\s*$", "", t).strip()
            return t
    return None

def get_git_mtime(path: Path) -> int:
    """Return unix timestamp of last commit touching this file (0 if unknown)."""
    try:
        out = subprocess.check_output(
            ["git", "log", "-1", "--format=%ct", "--", str(path)],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        return int(out) if out else 0
    except Exception:
        return 0

def rel_url(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    return f"{GH_BLOB_BASE}/{rel}"

def collect_notes(includes: List[str]) -> List[Dict]:
    results: List[Dict] = []
    for inc in includes:
        base = ROOT / inc
        if not base.exists():
            continue
        for p in base.rglob("*.md"):
            if should_skip(p):
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                text = ""
            title = first_title_from_markdown(text) or p.stem.replace("_", " ").strip()
            ts = get_git_mtime(p)
            results.append({
                "path": p,
                "title": title,
                "ts": ts,
                "url": rel_url(p),
            })
    # newest first
    results.sort(key=lambda d: d["ts"], reverse=True)
    return results

def write_index(out_name: str, label: str, items: List[Dict]) -> None:
    out_path = ROOT / out_name
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"# {label} — Recent Notes",
        "",
        f"_Auto-generated • Updated {now}_",
        "",
    ]
    for d in items:
        date = datetime.utcfromtimestamp(d["ts"]).strftime("%Y-%m-%d") if d["ts"] else "—"
        lines.append(f"- **{date}** — [{d['title']}]({d['url']})")
    lines.append("")  # final newline
    out_path.write_text("\n".join(lines), encoding="utf-8")

def main():
    for label, out_file, includes in CATEGORIES:
        notes = collect_notes(includes)
        write_index(out_file, label, notes)

if __name__ == "__main__":
    main()
