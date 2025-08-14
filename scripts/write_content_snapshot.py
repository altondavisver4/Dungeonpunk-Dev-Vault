#!/usr/bin/env python3
import os, json, gzip, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "_brain" / "snapshots"
OUTDIR.mkdir(parents=True, exist_ok=True)

IGNORE_DIRS = {".git", ".github", "node_modules", ".venv", "__pycache__", "_site", "dist", "build", "_brain", "scripts", ".obsidian"}

def iter_md():
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith(".")]
        for f in files:
            if f.lower().endswith(".md"):
                p = Path(root) / f
                rel = p.relative_to(ROOT).as_posix()
                try:
                    txt = p.read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    txt = ""
                yield rel, txt

def main():
    stamp = time.strftime("%Y%m%d-%H%M%S", time.gmtime())
    outpath = OUTDIR / f"snapshot-{stamp}.jsonl.gz"
    n=0
    with gzip.open(outpath, "wt", encoding="utf-8") as gz:
        for rel, txt in iter_md():
            gz.write(json.dumps({"path": rel, "text": txt}, ensure_ascii=False) + "\n")
            n += 1
    (OUTDIR / "LATEST").write_text(outpath.name, encoding="utf-8")
    print(f"Wrote {outpath} with {n} markdown files")
if __name__=="__main__":
    main()
