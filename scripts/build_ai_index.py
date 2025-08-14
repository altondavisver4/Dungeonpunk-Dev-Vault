#!/usr/bin/env python3
import json, os, re, gzip
from pathlib import Path
from utils_common import short

ROOT = Path(__file__).resolve().parents[1]
BRAIN = ROOT / "_brain" / "ai_brain.json"
OUT_INDEX = ROOT / "_brain" / "ai_index.json"
OUT_SEARCH = ROOT / "_brain" / "search_index.json"

TARGET_CHARS = int(os.environ.get("INDEX_TARGET_CHARS", "1200"))
MAX_CHARS = int(os.environ.get("INDEX_MAX_CHARS", "1800"))

def folder_tags(path_str: str):
    parts = Path(path_str).parts
    tags = []
    for p in parts[:-1]:
        clean = re.sub(r"\s+", "-", p.strip())
        if clean and clean[0].isalnum(): tags.append(clean)
    return tags

def chunk_blocks(blocks):
    chunks=[]; buf=[]; size=0
    def flush():
        nonlocal buf, size
        if not buf: return None
        text="\n\n".join(buf).strip(); buf=[]; size=0; return text
    for b in blocks or [{"anchor":None,"content":""}]:
        content=(b.get("content") or "").strip()
        paras=[p.strip() for p in content.split("\n\n") if p.strip()]
        for para in paras:
            if size+len(para)>MAX_CHARS:
                ch=flush()
                if ch: chunks.append(ch)
            buf.append(para); size+=len(para)+2
            if size>=TARGET_CHARS:
                ch=flush()
                if ch: chunks.append(ch)
    ch=flush()
    if ch: chunks.append(ch)
    return chunks or [""]

def build():
    data=json.loads(BRAIN.read_text(encoding="utf-8"))
    chunks=[]; search_docs=[]
    for f in data["files"]:
        tags=set(folder_tags(f["path"]))
        fm=f.get("front_matter",{}).get("tags") or f.get("front_matter",{}).get("tag") or []
        if isinstance(fm,str): fm=[fm]
        tags.update([str(t).strip() for t in fm if str(t).strip()])
        text_chunks=chunk_blocks(f.get("blocks"))
        for i, txt in enumerate(text_chunks,1):
            cid=f'{f["id"]}:{i:03d}'
            entry={"id":cid,"file_id":f["id"],"path":f["path"],"title":f["title"],
                   "anchor":None,"tags":sorted(tags),"summary":short(txt,300)}
            chunks.append(entry)
            search_docs.append({"id":cid,"t":f["title"],"p":f["path"],"g":sorted(tags),"s":short(txt,700)})
    index={"schema":"psiopera.ai_index.v2","generated_from":"ai_brain.json","chunks":chunks}
    OUT_INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_SEARCH.write_text(json.dumps(search_docs, ensure_ascii=False, indent=2), encoding="utf-8")
    # gz
    for src, gzname in [(OUT_INDEX, ROOT/'_brain/ai_index.json.gz'),
                        (BRAIN, ROOT/'_brain/ai_brain.json.gz'),
                        (OUT_SEARCH, ROOT/'_brain/search_index.json.gz')]:
        with gzip.open(gzname,'wb') as gz: gz.write(src.read_bytes())
    print("Chunks:", len(chunks), "Search docs:", len(search_docs))
if __name__=="__main__":
    build()
