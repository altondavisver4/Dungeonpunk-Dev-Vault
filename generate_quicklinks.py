#!/usr/bin/env python3
import os, re, subprocess, shlex, time, urllib.parse, sys
from pathlib import Path

ROOT = Path(os.getcwd())

TOP_N = int(os.environ.get("QL_TOP_N", "8"))
DAYS_WINDOW = int(os.environ.get("QL_DAYS_WINDOW", "14"))
DEBUG = os.environ.get("QL_DEBUG", "0") == "1"
MARKER_START = "<!-- QUICKLINKS:START -->"
MARKER_END   = "<!-- QUICKLINKS:END -->"

PINS_FILE = ROOT / "QUICKLINK_PINS.txt"
EXTS = (".md", ".markdown", ".txt")
IGNORE = {".git", ".github", ".obsidian", "node_modules", "dist", "build", "__pycache__"}

def git(*args, check=True):
    cmd = "git " + " ".join(shlex.quote(a) for a in args)
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and p.returncode != 0:
        raise RuntimeError(f"git failed: {cmd}\n{p.stderr}")
    return p.stdout

def tracked_text_files():
    out = git("ls-files", check=True)
    files = []
    for line in out.splitlines():
        if not line: continue
        lp = line.strip()
        if any(part in IGNORE for part in Path(lp).parts):
            continue
        if Path(lp).suffix.lower() in EXTS:
            files.append(Path(lp))
    return files

def last_commit_ts(path: Path):
    out = git("log", "-1", "--format=%ct", "--", str(path), check=False).strip()
    return int(out) if out.isdigit() else 0

def commits_in_window(path: Path, days=DAYS_WINDOW):
    out = git("log", f"--since={days} days ago", "--pretty=%H", "--", str(path), check=False)
    return len([ln for ln in out.splitlines() if ln.strip()])

def load_pins():
    pins = set()
    if PINS_FILE.exists():
        for line in PINS_FILE.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if not line or line.startswith("#"): continue
            pins.add(line.replace("\\","/"))
    return pins

_fm = re.compile(r"^---\s*(.*?)\s*---", re.S)
def has_hot_frontmatter(path: Path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            head = f.read(8192)
        m = _fm.match(head)
        if not m: return False
        block = m.group(1)
        for line in block.splitlines():
            k = line.split(":",1)[0].strip().lower()
            if k == "hot":
                val = line.split(":",1)[1].strip().lower()
                return val in {"1","true","yes","on"}
        return False
    except Exception:
        return False

def score(path: Path, pins):
    s = 0.0
    if str(path).replace("\\","/") in pins: s += 10000
    if has_hot_frontmatter(path): s += 500
    c = commits_in_window(path)
    s += c * 2
    ts = last_commit_ts(path)
    if ts:
        age_days = (time.time() - ts)/86400.0
        if age_days <= 1: s += 10
        elif age_days <= 3: s += 6
        elif age_days <= 7: s += 4
        elif age_days <= 14: s += 2
    return s, c, ts

def enc(rel: Path):
    parts = str(rel).replace("\\","/").split("/")
    return "/" + "/".join(urllib.parse.quote(p, safe="()&-._~ ").replace(" ", "%20") for p in parts)

def write_quicklinks(scored):
    top = scored[:TOP_N]
    lines = ["# AI Quicklinks", "", "_Auto-generated; top active notes._", ""]
    for s, rp, c, ts in top:
        lines.append(f"- [{rp.name}]({enc(rp)})")
    body = "\n".join(lines) + "\n"
    out = ROOT / "AI_QUICKLINKS.md"
    old = out.read_text("utf-8") if out.exists() else ""
    if old.strip() != body.strip():
        out.write_text(body, "utf-8")
        return True
    return False

def update_index_block(scored):
    idx = ROOT / "AI_INDEX.md"
    if not idx.exists(): return False
    top = scored[:TOP_N]
    block = ["## Quicklinks", "", MARKER_START]
    for s, rp, c, ts in top:
        block.append(f"- [{rp.name}]({enc(rp)})")
    block.append(MARKER_END)
    block.append("")
    block_text = "\n".join(block)
    content = idx.read_text("utf-8")
    if MARKER_START in content and MARKER_END in content:
        pre, rest = content.split(MARKER_START, 1)
        inside, post = rest.split(MARKER_END, 1)
        new = pre + block_text + post
    else:
        new = block_text + "\n" + content
    if new.strip() != content.strip():
        idx.write_text(new, "utf-8")
        return True
    return False

def pick_top_under(prefix, scored):
    pref = prefix.replace("\\","/")
    best = None; bests = -1e18
    for s, rp, c, ts in scored:
        if str(rp).replace("\\","/").startswith(pref):
            if s > bests:
                bests = s; best = rp
    return best

def write_redirects(scored):
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
        hit = pick_top_under(pref, scored)
        if hit:
            mapping[short] = enc(hit)
    lines = [f"{k}    {v}" for k,v in mapping.items()]
    out = ROOT / "_redirects"
    old = out.read_text("utf-8") if out.exists() else ""
    new = "\n".join(lines) + ("\n" if lines else "")
    if new.strip() != old.strip():
        out.write_text(new, "utf-8")
        return True
    return False

def main():
    pins = load_pins()
    files = tracked_text_files()
    scored = []
    for rp in files:
        try:
            s, c, ts = score(rp, pins)
            scored.append((s, rp, c, ts))
        except Exception as e:
            if DEBUG: print("[WARN] scoring failed:", rp, e)
    scored.sort(key=lambda x: (-(x[0]), str(x[1]).lower()))
    if DEBUG:
        print("---- QUICKLINKS DEBUG (Top 12) ----")
        for i, (s, rp, c, ts) in enumerate(scored[:12], 1):
            print(f"{i:2d}. {s:6.2f}  c14={c:2d}  {rp}")
    ch1 = write_quicklinks(scored)
    ch2 = update_index_block(scored)
    ch3 = write_redirects(scored)
    print(f"Updated: quicklinks={ch1}, index={ch2}, redirects={ch3}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
