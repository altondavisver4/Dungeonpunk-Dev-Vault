#!/usr/bin/env python3
import os, html, urllib.parse
from pathlib import Path

ROOT = Path(os.getcwd())
TOP_N = int(os.environ.get("CACHE_TOP_N", "20"))
SOURCE = ROOT / "AI_QUICKLINKS.md"

def parse_quicklinks(md_path: Path):
    paths = []
    if not md_path.exists():
        return paths
    for line in md_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line.startswith("- ["): 
            continue
        try:
            start = line.index("](") + 2
            end = line.index(")", start)
            url = line[start:end]
            if url.startswith("/"):
                url = url[1:]
            p = urllib.parse.unquote(url)
            paths.append(p)
        except Exception:
            continue
    return paths[:TOP_N]

def read_file_text(rel_path: str):
    p = ROOT / rel_path
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""

def build_cache_html(paths):
    sections = []
    for rel in paths:
        name = html.escape(Path(rel).name)
        content = html.escape(read_file_text(rel))
        sections.append(f"<section><h2>{name}</h2><pre>{content}</pre></section>")
    doc = f"""<!doctype html>
<meta charset="utf-8">
<title>Cache Snapshot</title>
<h1>Cache Snapshot (Top {len(paths)})</h1>
{''.join(sections)}
"""
    (ROOT / "cache.html").write_text(doc, encoding="utf-8")

def main():
    paths = parse_quicklinks(SOURCE)
    build_cache_html(paths)
    print(f"cache sections: {len(paths)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
