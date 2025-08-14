from pathlib import Path
from urllib.parse import quote
import time

ROOT=Path(".")
IGNORE={'.git','.github','node_modules','dist','build','_brain','scripts','.obsidian'}
urls=[]
for p in ROOT.rglob("*.html"):
    if any(seg in IGNORE for seg in p.parts): continue
    urls.append("/" + "/".join(quote(x) for x in p.parts))

stamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
xml=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in sorted(urls):
    xml.append(f"<url><loc>https://YOUR-SITE.netlify.app{u}</loc><lastmod>{stamp}</lastmod></url>")
xml.append("</urlset>")
Path("sitemap.xml").write_text("\n".join(xml),encoding="utf-8")
print("wrote sitemap.xml with",len(urls),"urls")
