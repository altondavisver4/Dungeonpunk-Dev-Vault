#!/usr/bin/env python3
"""
generate_quicklinks.py
Auto-builds:
- AI_QUICKLINKS.md (top N most "active/important" notes)
- Injects a Quicklinks block into AI_INDEX.md (between markers)
- Updates Netlify `_redirects` with short paths (/quick, /core, /systems, /lore, /rd)

Scoring heuristic (privacy-friendly):
- pin bonus: +10_000 if path listed in QUICKLINK_PINS.txt
- hot frontmatter in YAML: +500
- commits in last 14 days: +2 each
- recency bonus for last commit:
    <=1 day: +10
    <=3 days: +6
    <=7 days: +4
    <=14 days: +2
    else: +0
"""

import os, re, subprocess, shlex, time, urllib.parse
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(os.getcwd())

# configuration
TOP_N = 8
DAYS_WINDOW = 14
MARKER_START = "<!-- QUICKLINKS:START -->"
MARKER_END   = "<!-- QUICKLINKS:END -->"

IGNORE_DIRS = {".git", ".github", ".obsidian", "node_modules", "dist", "build", "__pycache__"}
EXTS = {".md", ".markdown", ".txt"}

PINS_FILE = ROOT / "QUICKLINK_PINS.txt"

def list_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        # prune ignored dirs
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
    try:
        out = git("log", "-1", "--format=%ct", "--", str(relpath))
        out = out.strip()
        return int(out) if out else 0
    except RuntimeError:
        return 0

def commits_in_window(relpath: Path, days=14):
    since = f"--since={days}.days"
    try:
        out = git("log", since, "--name-only", "--pretty=", "--", str(relpath), check=False)
        # Count appearances of exactly this relpath line
        cnt = 0
        for line in out.splitlines():
            if line.strip() == str(relpath).replace("\\","/"):
                cnt += 1
        return cnt
    except RuntimeError:
        return 0

_fr_re = re.compile(r"^---\s*(.*?)\s*---", re.S)
def has_hot_frontmatter(abspath: Path):
    try:
        # Only read first ~8KB for speed
        with open(abspath, "r", encoding="utf-8", errors="ignore") as f:
            head = f.read(8192)
        m = _fr_re.match(head)
        if not m:
            return False
        block = m.group(1)
        # naive parse for "hot: true"
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

def score_file(relpath: Path):
    # Base on activity + recency + frontmatter + pins
    abspath = ROOT / relpath
    s = 0.0
    # pins
    if str(relpath).replace("\\","/") in load_pins():
        s += 10000
    # hot frontmatter
    if has_hot_frontmatter(abspath):
        s += 500
    # commits in window
    c = commits_in_window(relpath, DAYS_WINDOW)
    s += c * 2
    # recency bonus by age
    ts = last_commit_ts(relpath)
    if ts:
        delta_days = (time.time() - ts) / 86400.0
        if delta_days <= 1: s += 10
        elif delta_days <= 3: s += 6
        elif delta_days <= 7: s += 4
        elif delta_days <= 14: s += 2
    return s

def encode_url_path(relpath: Path):
    parts = str(relpath).replace("\\","/").split("/")
    enc = "/".join(urllib.parse.quote(p, safe="()&-._~ " ).replace(" ","%20") for p in parts)
    return "/" + enc

def build_quicklinks(files):
    # Score & sort
    scored = []
    for rp in files:
        try:
            s = score_file(rp)
            scored.append((s, rp))
        except Exception as e:
            # ignore problematic files
            continue
    scored.sort(key=lambda x: (-(x[0]), str(x[1]).lower()))
    return [rp for _, rp in scored[:TOP_N]]

def write_ai_quicklinks(paths):
    lines = []
    lines.append("# AI Quicklinks")
    lines.append("")
    lines.append("_Auto-generated; top active notes based on pins, hot frontmatter, recency, and recent edits._")
    lines.append("")
    for rp in paths:
        url = encode_url_path(rp)
        title = rp.name
        lines.append(f"- [{title}]({url})")
    lines.append("")
    out = ROOT / "AI_QUICKLINKS.md"
    old = out.read_text(encoding="utf-8", errors="ignore") if out.exists() else ""
    new = "\n".join(lines)
    if new.strip() != old.strip():
        out.write_text(new, encoding="utf-8")
        return True
    return False

def update_ai_index_quicklinks(paths):
    idx = ROOT / "AI_INDEX.md"
    if not idx.exists():
        return False
    content = idx.read_text(encoding="utf-8", errors="ignore")
    block_lines = ["## Quicklinks", "", MARKER_START]
    for rp in paths:
        url = encode_url_path(rp)
        block_lines.append(f"- [{rp.name}]({url})")
    block_lines.append(MARKER_END)
    block_lines.append("")
    block = "\n".join(block_lines)

    if MARKER_START in content and MARKER_END in content:
        # replace existing
        pre, rest = content.split(MARKER_START, 1)
        inside, post = rest.split(MARKER_END, 1)
        new_content = pre + block + post
    else:
        # prepend at top
        new_content = block + "\n" + content

    if new_content.strip() != content.strip():
        idx.write_text(new_content, encoding="utf-8")
        return True
    return False

def pick_top_under(prefix):
    # pick the highest-scored file under a path prefix
    prefix = prefix.replace("\\","/")
    candidates = [p for p in list_files(ROOT) if str(p).replace("\\","/").startswith(prefix)]
    if not candidates:
        return None
    best = None
    best_s = -1e9
    for p in candidates:
        s = score_file(p)
        if s > best_s:
            best_s, best = s, p
    return best

def update_redirects(quick_paths):
    mapping = {}
    # Always map /quick to AI_QUICKLINKS.md
    if (ROOT/"AI_QUICKLINKS.md").exists():
        mapping["/quick"] = "/AI_QUICKLINKS.md"
    # Core/Systems/Lore/R&D shortcuts
    m = {
        "/core":   "01 – Game Bible/Core Vision",
        "/systems":"01 – Game Bible/Systems",
        "/lore":   "01 – Game Bible/World & Lore",
        "/rd":     "02 – R&D Lab/Daily Dumps",
    }
    for short, pref in m.items():
        top = pick_top_under(pref)
        if top:
            mapping[short] = encode_url_path(top)

    # write _redirects
    lines = []
    for k, v in mapping.items():
        lines.append(f"{k}    {v}")
    out = ROOT / "_redirects"
    old = out.read_text(encoding="utf-8", errors="ignore") if out.exists() else ""
    new = "\n".join(lines) + ("\n" if lines else "")
    if new.strip() != old.strip():
        out.write_text(new, encoding="utf-8")
        return True
    return False

def main():
    files = list(list_files(ROOT))
    if not files:
        print("No markdown/text files found.")
        return 0
    quick = build_quicklinks(files)
    ch1 = write_ai_quicklinks(quick)
    ch2 = update_ai_index_quicklinks(quick)
    ch3 = update_redirects(quick)
    changed = ch1 or ch2 or ch3
    print(f"Updated: quicklinks={ch1}, index={ch2}, redirects={ch3}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
