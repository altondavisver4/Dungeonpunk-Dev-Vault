#!/usr/bin/env python3
"""
generate_quicklinks.py (updated)
- Stronger git scoring (robust --since handling)
- Better last-commit timestamp handling
- Optional DEBUG output of top-N scores to Action logs
- Same outputs: AI_QUICKLINKS.md, AI_INDEX.md quicklinks block, _redirects
"""

import os, re, subprocess, shlex, time, urllib.parse, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(os.getcwd())

# ====== CONFIG ======
TOP_N = int(os.environ.get("QL_TOP_N", "8"))
DAYS_WINDOW = int(os.environ.get("QL_DAYS_WINDOW", "14"))
DEBUG = os.environ.get("QL_DEBUG", "1") == "1"  # set to "0" to silence debug
MARKER_START = "<!-- QUICKLINKS:START -->"
MARKER_END   = "<!-- QUICKLINKS:END -->"

IGNORE_DIRS = {".git", ".github", ".obsidian", "node_modules", "dist", "build", "__pycache__"}
EXTS = {".md", ".markdown", ".txt"}

PINS_FILE = ROOT / "QUICKLINK_PINS.txt"

def list_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        for name in filenames:
            if Path(name).suffix.lower() in EXTS:
                p = Path(dirpath) / name
                yield p.relative_to(root)

def git(*args, check=True):
    cmd = "git " + " ".join(shlex.quote(a) for a in args)
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and res.returncode != 0:
        raise RuntimeError(f"git failed: {cmd}\n{res.stderr}")
    return res.stdout

def last_commit_ts(relpath: Path):
    """UTC epoch seconds of the last commit touching this file; 0 if none."""
    try:
        out = git("log", "-1", "--format=%ct", "--", str(relpath), check=False).strip()
        return int(out) if out.isdigit() else 0
    except Exception:
        return 0

def commits_in_window(relpath: Path, days=DAYS_WINDOW):
    """
    Count commits touching this file in the last N days.
    Use a portable --since format and count commit hashes.
    """
    try:
        since_arg = f"--since={days} days ago"
        out = git("log", since_arg, "--pretty=%H", "--", str(relpath), check=False)
        return len([ln for ln in out.splitlines() if ln.strip()])
    except Exception:
        return 0

_fr_re = re.compile(r"^---\s*(.*?)\s*---", re.S)
def has_hot_frontmatter(abspath: Path):
    try:
        with open(abspath, "r", encoding="utf-8", errors="ignore") as f:
            head = f.read(8192)  # read small header chunk
        m = _fr_re.match(head)
        if not m:
            return False
        block = m.group(1)
        for line in block.splitlines():
            if line.strip().lower().startswith("hot:"):
                val = line.split(":",1)[1].strip().lower()
                return val in {"true","yes","1","on"}
        return False
    except Exception:
        return False

def load_pins():
    pins = set()
    if PINS_FILE.exists():
        for line in PINS_FILE.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            pins.add(line.replace("\\","/"))
    return pins

def score_file(relpath: Path, pins_cache):
    abspath = ROOT / relpath
    s = 0.0
    # pin bonus
    if str(relpath).replace("\\","/") in pins_cache:
        s += 10000
    # hot frontmatter
    if has_hot_frontmatter(abspath):
        s += 500
    # commits in window
    c = commits_in_window(relpath, DAYS_WINDOW)
    s += c * 2
    # recency bonus
    ts = last_commit_ts(relpath)
    if ts:
        delta_days = (time.time() - ts) / 86400.0
        if delta_days <= 1: s += 10
        elif delta_days <= 3: s += 6
        elif delta_days <= 7: s += 4
        elif delta_days <= 14: s += 2
    return s, c, ts

def encode_url_path(relpath: Path):
    parts = str(relpath).replace("\\","/").split("/")
    enc = "/".join(urllib.parse.quote(p, safe="()&-._~ " ).replace(" ","%20") for p in parts)
    return "/" + enc

def build_quicklinks(files):
    pins_cache = load_pins()
    scored = []
    for rp in files:
        try:
            s, c, ts = score_file(rp, pins_cache)
            scored.append((s, rp, c, ts))
        except Exception as e:
            if DEBUG:
                print(f"[WARN] scoring failed for {rp}: {e}")
            continue
    # Sort by score desc, then path
    scored.sort(key=lambda x: (-(x[0]), str(x[1]).lower()))
    return scored

def write_ai_quicklinks(scored):
    top = scored[:TOP_N]
    lines = []
    lines.append("# AI Quicklinks")
    lines.append("")
    lines.append("_Auto-generated; top active notes based on pins, hot frontmatter, recency, and recent edits._")
    lines.append("")
    for s, rp, c, ts in top:
        url = encode_url_path(rp)
        title = rp.name
        lines.append(f"- [{title}]({url})")
    lines.append("")
    out = ROOT / "AI_QUICKLINKS.md"
    old = out.read_text(encoding="utf-8", errors="ignore") if out.exists() else ""
    new = "\n".join(lines)
    changed = new.strip() != old.strip()
    if changed:
        out.write_text(new, encoding="utf-8")
    return changed

def update_ai_index_quicklinks(scored):
    idx = ROOT / "AI_INDEX.md"
    if not idx.exists():
        return False
    top = scored[:TOP_N]
    block_lines = ["## Quicklinks", "", MARKER_START]
    for s, rp, c, ts in top:
        url = encode_url_path(rp)
        block_lines.append(f"- [{rp.name}]({url})")
    block_lines.append(MARKER_END)
    block_lines.append("")
    block = "\n".join(block_lines)

    content = idx.read_text(encoding="utf-8", errors="ignore")
    if MARKER_START in content and MARKER_END in content:
        pre, rest = content.split(MARKER_START, 1)
        inside, post = rest.split(MARKER_END, 1)
        new_content = pre + block + post
    else:
        new_content = block + "\n" + content

    changed = new_content.strip() != content.strip()
    if changed:
        idx.write_text(new_content, encoding="utf-8")
    return changed

def pick_top_under(prefix, scored):
    pref = prefix.replace("\\","/")
    best = None
    best_s = -1e18
    for s, rp, c, ts in scored:
        if str(rp).replace("\\","/").startswith(pref):
            if s > best_s:
                best_s, best = s, rp
    return best

def update_redirects(scored):
    mapping = {}
    if (ROOT/"AI_QUICKLINKS.md").exists():
        mapping["/quick"] = "/AI_QUICKLINKS.md"
    m = {
        "/core":   "01 – Game Bible/Core Vision",
        "/systems":"01 – Game Bible/Systems",
        "/lore":   "01 – Game Bible/World & Lore",
        "/rd":     "02 – R&D Lab/Daily Dumps",
    }
    for short, pref in m.items():
        top = pick_top_under(pref, scored)
        if top:
            mapping[short] = encode_url_path(top)

    lines = [f"{k}    {v}" for k, v in mapping.items()]
    out = ROOT / "_redirects"
    old = out.read_text(encoding="utf-8", errors="ignore") if out.exists() else ""
    new = "\n".join(lines) + ("\n" if lines else "")
    changed = new.strip() != old.strip()
    if changed:
        out.write_text(new, encoding="utf-8")
    return changed

def debug_dump(scored):
    if not DEBUG:
        return
    print("---- QUICKLINKS DEBUG (Top 12 by score) ----")
    for i, (s, rp, c, ts) in enumerate(scored[:12], 1):
        age = "n/a"
        if ts:
            age_days = (time.time() - ts)/86400.0
            age = f"{age_days:.1f}d ago"
        print(f"{i:2d}. score={s:.1f}  commits14d={c:2d}  last={age:>8}  {rp}")

def main():
    files = list(list_files(ROOT))
    if not files:
        print("No markdown/text files found.")
        return 0
    scored = build_quicklinks(files)
    debug_dump(scored)
    ch1 = write_ai_quicklinks(scored)
    ch2 = update_ai_index_quicklinks(scored)
    ch3 = update_redirects(scored)
    print(f"Updated: quicklinks={ch1}, index={ch2}, redirects={ch3}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
