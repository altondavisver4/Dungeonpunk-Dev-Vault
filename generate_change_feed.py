#!/usr/bin/env python3
import os, subprocess, shlex, datetime
from pathlib import Path

ROOT = Path(os.getcwd())
DAYS = int(os.environ.get("CHANGE_DAYS", "14"))

def git(*args):
    cmd = "git " + " ".join(shlex.quote(a) for a in args)
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if p.returncode != 0:
        return ""
    return p.stdout

def changes_since(days):
    since = f"--since={days} days ago"
    out = git("log", since, "--name-only", "--pretty=format:%ct|%h|%an|%s")
    entries = {}
    current = None
    for line in out.splitlines():
        if not line: 
            continue
        if "|" in line and line.split("|",1)[0].isdigit():
            ts, h, an, s = line.split("|",3)
            current = (int(ts), h, an, s)
        else:
            path = line.strip()
            if not path or current is None: 
                continue
            entries.setdefault(path, []).append(current)
    return entries

def write_feed(entries):
    items = sorted(entries.items(), key=lambda kv: max(ts for ts,_,_,_ in kv[1]), reverse=True)
    lines = ["# CHANGE FEED (last {} days)".format(DAYS), ""]
    for path, commits in items:
        latest = max(commits)[0]
        dt = datetime.datetime.utcfromtimestamp(latest).strftime("%Y-%m-%d %H:%M UTC")
        lines.append(f"## {path}  _(last: {dt}, {len(commits)} commits)_")
        for ts, h, an, s in sorted(commits, reverse=True):
            dt2 = datetime.datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
            lines.append(f"- {dt2} — `{h}` by {an}: {s}")
        lines.append("")
    (ROOT / "CHANGE_FEED.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

def main():
    entries = changes_since(DAYS)
    write_feed(entries)
    print(f"files changed: {len(entries)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
