#!/usr/bin/env python3
import os, re, urllib.parse
from pathlib import Path

ROOT = Path(os.getcwd())
TEXT_EXTS = {'.md', '.markdown', '.txt'}
IGNORE = {'.git', '.github', '.obsidian', '__pycache__', 'node_modules', 'dist', 'build', 'tags'}

TAG_RE = re.compile(r'(?<!\w)#([A-Za-z0-9][-\w]{0,48})')  # #tag, allow - and _

def list_text_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE]
        for fn in filenames:
            if Path(fn).suffix.lower() in TEXT_EXTS:
                yield Path(dirpath) / fn

def rel(p: Path): return p.relative_to(ROOT).as_posix()
def enc_path(p: str):
    parts = p.split("/")
    return "/" + "/".join(urllib.parse.quote(x, safe="()&-._~ ").replace(" ", "%20") for x in parts)

def scan_tags():
    tagmap = {}
    for p in list_text_files(ROOT):
        try:
            s = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        found = set(m.group(1).lower() for m in TAG_RE.finditer(s))
        if not found: continue
        r = rel(p)
        for t in found:
            tagmap.setdefault(t, []).append(r)
    return {t: sorted(paths) for t, paths in tagmap.items()}

def write_tag_pages(tagmap):
    tags_dir = ROOT / "tags"
    tags_dir.mkdir(exist_ok=True)
    # write index
    idx_lines = ["# TAGS INDEX", ""]
    for t in sorted(tagmap):
        idx_lines.append(f"- [{t}](./tags/{t}.md) ({len(tagmap[t])})")
    (ROOT / "TAGS_INDEX.md").write_text("\n".join(idx_lines) + "\n", encoding="utf-8")

    # each tag page
    for t, paths in tagmap.items():
        lines = [f"# #{t}", ""]
        for r in paths:
            lines.append(f"- [{Path(r).name}]({enc_path(r)})")
        (tags_dir / f"{t}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

def main():
    tagmap = scan_tags()
    write_tag_pages(tagmap)
    print(f"tags: {len(tagmap)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
