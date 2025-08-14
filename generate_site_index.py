#!/usr/bin/env python3
import os, html, urllib.parse
from pathlib import Path

ROOT = Path(os.getcwd())
IGNORE = {'.git', '.github', '.obsidian', '__pycache__', 'node_modules', 'dist', 'build'}
TEXT_EXTS = {'.md', '.markdown', '.txt'}

def list_dirs_with_text(root: Path):
    keep = set()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE]
        if any(Path(fn).suffix.lower() in TEXT_EXTS for fn in filenames):
            keep.add(Path(dirpath))
    return sorted(keep)

def enc_path(p: Path):
    parts = str(p).replace("\\","/").split("/")
    return "/"+"/".join(urllib.parse.quote(x, safe="()&-._~ ").replace(" ","%20") for x in parts)

def file_link(p: Path):
    name = html.escape(p.name)
    return f'<li><a href="{enc_path(p)}">{name}</a></li>'

def write_index_for_dir(d: Path):
    files = sorted([x for x in d.iterdir() if x.is_file() and x.suffix.lower() in TEXT_EXTS])
    if not files and d != ROOT:
        return False
    rel = d.relative_to(ROOT) if d != ROOT else Path(".")
    title = " / ".join(rel.parts) if rel != Path(".") else "Root"
    items = "\n".join(file_link(f) for f in files)
    up = enc_path(rel.parent) + "/index.html" if rel not in {Path("."), Path("")} else None
    html_doc = f"""<!doctype html>
<meta charset="utf-8">
<title>{html.escape(title)}</title>
<h1>{html.escape(title)}</h1>
{('<p><a href="'+up+'">⬆ up</a></p>' if up else '')}
<ul>
{items}
</ul>
"""
    out = d / "index.html"
    old = out.read_text("utf-8") if out.exists() else ""
    if old.strip() != html_doc.strip():
        out.write_text(html_doc, "utf-8")
        return True
    return False

def main():
    changed = False
    for d in list_dirs_with_text(ROOT):
        if write_index_for_dir(d):
            changed = True
    write_index_for_dir(ROOT)
    print("site-index changed:", changed)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
