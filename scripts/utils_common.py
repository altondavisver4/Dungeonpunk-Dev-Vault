import hashlib, re
MD_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
WIKI = re.compile(r"\[\[([^\]|#]+)(?:#([^\]|]+))?(?:\|([^\]]+))?\]\]")
FRONT = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
def sha(s: str) -> str: return hashlib.sha1(s.encode("utf-8")).hexdigest()[:12]
def short(text: str, n=360):
    import re
    t = re.sub(r"\s+", " ", text or "").strip()
    return t[:n] + ("…" if len(t) > n else "")
