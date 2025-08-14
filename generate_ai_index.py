#!/usr/bin/env python3
import os
import sys
import urllib.parse
from datetime import datetime

# Repo root is current working directory
ROOT = os.getcwd()

# Detect repo/user info for raw links from GitHub Actions env if available
repo = os.environ.get("GITHUB_REPOSITORY", "").strip()  # e.g., "username/repo"
branch = os.environ.get("GITHUB_REF_NAME", "").strip()  # e.g., "main"
if not branch:
    branch = "main"

def is_ignorable(path):
    # Ignore Git internals, workflow files, and common non-content roots
    parts = path.replace("\\", "/").split("/")
    if ".git" in parts or ".github" in parts:
        return True
    # Ignore typical build/deploy artifacts
    basename = os.path.basename(path)
    ignore_names = {"node_modules", "dist", "build", "venv", "__pycache__", ".DS_Store", "Thumbs.db"}
    if basename in ignore_names:
        return True
    return False

def list_markdown_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        # filter ignorable dirs in-place
        dirnames[:] = [d for d in dirnames if not is_ignorable(os.path.join(dirpath, d))]
        for f in filenames:
            # include markdown and simple text files
            if f.lower().endswith((".md", ".markdown", ".txt")):
                full = os.path.join(dirpath, f)
                if not is_ignorable(full):
                    yield full

def rel_url(path):
    rel = os.path.relpath(path, ROOT).replace("\\", "/")
    return rel

def raw_url(rel_path):
    # Encode each segment for a safe URL to raw.githubusercontent.com
    if not repo:
        return None
    encoded = "/".join(urllib.parse.quote(seg, safe="") for seg in rel_path.split("/"))
    return f"https://raw.githubusercontent.com/{repo}/{branch}/{encoded}"

def blob_url(rel_path):
    # Fallback to GitHub HTML view
    if not repo:
        return None
    encoded = "/".join(urllib.parse.quote(seg, safe="") for seg in rel_path.split("/"))
    return f"https://github.com/{repo}/blob/{branch}/{encoded}"

def human_title(rel_path):
    # Use filename without extension as a title; fall back to rel path
    base = os.path.basename(rel_path)
    name = os.path.splitext(base)[0]
    # Replace separators with spaces
    return name.replace("_", " ").replace("-", " ").strip()

def build_index(files):
    lines = []
    lines.append("# AI Index")
    lines.append("")
    lines.append(f"_Auto-generated on {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC_")
    lines.append("")
    lines.append("> Links go to **raw** files when possible (best for AI), with a fallback GitHub view.")
    lines.append("")
    # Group by top-level directory for readability
    groups = {}
    for f in files:
        rel = rel_url(f)
        top = rel.split("/")[0] if "/" in rel else "."
        groups.setdefault(top, []).append(rel)
    for top in sorted(groups.keys(), key=lambda s: s.lower()):
        lines.append(f"## {top}")
        lines.append("")
        for rel in sorted(groups[top], key=lambda s: s.lower()):
            title = human_title(rel)
            rurl = raw_url(rel)
            burl = blob_url(rel)
            if rurl:
                lines.append(f"- [{title}]({rurl})  \n  <sub><sup><a href=\"{burl}\">(view on GitHub)</a></sup></sub>")
            else:
                lines.append(f"- [{title}]({burl})")
        lines.append("")
    return "\n".join(lines)

def main():
    files = list(list_markdown_files(ROOT))
    if not files:
        print("No markdown/text files found; creating minimal AI_INDEX.md")
    content = build_index(files)
    out = os.path.join(ROOT, "AI_INDEX.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Wrote {out} ({len(content.splitlines())} lines)")

if __name__ == "__main__":
    main()
