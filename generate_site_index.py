#!/usr/bin/env python3
import os, html, urllib.parse, time
from pathlib import Path

ROOT = Path(os.getcwd())
IGNORE = {'.git', '.github', '.obsidian', '__pycache__', 'node_modules', 'dist', 'build'}
TEXT_EXTS = {'.md', '.markdown', '.txt', '.html'}

def enc_path(p: Path):
    parts = str(p).replace("\\","/").split("/")
    return "/"+"/".join(urllib.parse.quote(x, safe="()&-._~ ").replace(" ","%20") for x in parts)

def list_dirs_with_text(root: Path):
    keep = set()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE]
        if any(Path(fn).suffix.lower() in TEXT_EXTS for fn in filenames):
            keep.add(Path(dirpath))
    return sorted(keep)

def file_link(p: Path):
    name = html.escape(p.name)
    return f'<li><a href="{enc_path(p)}">{name}</a></li>'

def write_index_for_dir(d: Path):
    files = sorted([x for x in d.iterdir() if x.is_file() and x.suffix.lower() in TEXT_EXTS])
    # For non-root folders, skip if no files
    if not files and d != ROOT:
        return False
    rel = d.relative_to(ROOT) if d != ROOT else Path(".")
    title = " / ".join(rel.parts) if rel != Path(".") else "Home"
    items = "\n".join(file_link(f) for f in files)
    up = enc_path(rel.parent) + "/index.html" if rel not in {Path("."), Path("")} else None

    # Simple, clean HTML (dark-friendly)
    html_doc = f"""<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} — PsiOpera</title>
<style>
  :root {{ --bg:#0b0c0f; --fg:#e9eef5; --muted:#9aa6b2; --card:#141821; }}
  body {{ background:var(--bg); color:var(--fg); font:16px/1.6 system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif; margin:0; }}
  main {{ max-width: 900px; margin: 40px auto; padding: 0 20px 80px; }}
  h1 {{ margin:.2rem 0 1rem; }}
  .crumbs {{ color:var(--muted); font-size:14px; margin-bottom:10px; }}
  .card {{ background:var(--card); border-radius:16px; padding:22px; }}
  ul {{ margin:0; padding-left:1.2rem; }}
  a {{ color:#8ad; text-decoration:none; }} a:hover {{ text-decoration:underline; }}
  .meta {{ color:var(--muted); font-size:13px; margin-top:14px; }}
</style>
<main>
  <div class="crumbs">{breadcrumb(rel)}</div>
  <h1>{html.escape(title)}</h1>
  <div class="card">
    {"<p><em>(Empty)</em></p>" if not items else f"<ul>{items}</ul>"}
  </div>
  {f'<p class="meta"><a href="{up}">⬆ up</a></p>' if up else ""}
</main>
"""
    out = d / "index.html"
    old = out.read_text("utf-8") if out.exists() else ""
    if old.strip() != html_doc.strip():
        out.write_text(html_doc, "utf-8")
        return True
    return False

def breadcrumb(rel: Path):
    if rel in {Path("."), Path("")}: return "Home"
    parts = []
    run = []
    parts.append('<a href="/index.html">Home</a>')
    for p in rel.parts:
        run.append(p)
        href = "/" + "/".join(urllib.parse.quote(x) for x in run) + "/index.html"
        parts.append(f'<a href="{href}">{html.escape(p)}</a>')
    return " / ".join(parts)

def build_root_index():
    # Build a compact overview page with top folders and quick links to folder indexes
    folders = [d for d in ROOT.iterdir() if d.is_dir() and d.name not in IGNORE]
    folder_links = "\n".join(
        f'<li><a href="{enc_path(d)}/index.html">{html.escape(d.name)}</a></li>'
        for d in sorted(folders, key=lambda p: p.name.lower())
    )
    stamp = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())
    doc = f"""<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>PsiOpera — AI Brain</title>
<style>
  :root {{ --bg:#0b0c0f; --fg:#e9eef5; --muted:#9aa6b2; --card:#141821; }}
  body {{ background:var(--bg); color:var(--fg); font:16px/1.6 system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif; margin:0; }}
  main {{ max-width: 900px; margin: 40px auto; padding: 0 20px 80px; }}
  h1 {{ margin:.2rem 0 .3rem; }}
  .muted {{ color:var(--muted); }}
  .card {{ background:var(--card); border-radius:16px; padding:22px; }}
  ul.cols {{ columns:2; gap:2rem; padding-left:1.2rem; }}
  a {{ color:#8ad; text-decoration:none; }} a:hover {{ text-decoration:underline; }}
</style>
<main>
  <h1>PsiOpera / Dungeonpunk — AI Brain</h1>
  <p class="muted">Auto-generated folder index. Last updated {stamp}.</p>
  <div class="card">
    <h2>Folders</h2>
    <ul class="cols">
      {folder_links or "<li><em>(No folders)</em></li>"}
    </ul>
  </div>
  <p class="muted">Shortcuts: <a href="/AI_QUICKLINKS.md">AI_QUICKLINKS</a> · <a href="/TAGS_INDEX.md">TAGS_INDEX</a> · <a href="/CHANGE_FEED.md">CHANGE_FEED</a> · <a href="/cache.html">cache</a></p>
</main>
"""
    out = ROOT / "index.html"
    old = out.read_text("utf-8") if out.exists() else ""
    if old.strip() != doc.strip():
        out.write_text(doc, "utf-8")
        return True
    return False

def main():
    changed = False
    for d in list_dirs_with_text(ROOT):
        if write_index_for_dir(d):
            changed = True
    # Always (re)write a smart root
    if build_root_index():
        changed = True
    print("site-index changed:", changed)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
