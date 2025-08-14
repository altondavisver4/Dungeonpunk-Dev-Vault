#!/usr/bin/env python3
from pathlib import Path
import time, re

ROOT = Path(__file__).resolve().parents[1]
SEARCH = ROOT / "search.html"

STAMP = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())

SCAFFOLD = f"""<!doctype html>
<meta charset="utf-8">
<title>Search — PsiOpera</title>
<style>
  :root {{ --bg:#0b0c0f; --fg:#e9eef5; --muted:#9aa6b2; --card:#141821; }}
  body {{ background:var(--bg); color:var(--fg); font:16px/1.6 system-ui,Segoe UI,Roboto,Arial,sans-serif; margin:0; }}
  main {{ max-width: 900px; margin: 40px auto; padding: 20px 28px; }}
  h1 {{ margin:.2rem 0 .8rem }}
  .muted {{ color:var(--muted); }}
  .card {{ background:var(--card); border-radius:16px; padding:22px; }}
</style>
<main>
  <h1>Search</h1>
  <p class="muted">Last updated {STAMP}.</p>
  <div class="card">
    <p>This is a lightweight shell page. The full search UI is built by the scheduled “Build All”.</p>
  </div>
</main>
"""

def main():
    if not SEARCH.exists():
        SEARCH.write_text(SCAFFOLD, encoding="utf-8")
        print("search.html: created")
        return 0

    html = SEARCH.read_text(encoding="utf-8")
    # Replace an existing “Last updated …” line if present; otherwise inject one.
    new = re.sub(
        r'(Last updated )\d{4}-\d{2}-\d{2} \d{2}:\d{2} UTC',
        r'\g<1>' + STAMP,
        html
    )
    if new == html:
        # Try to insert after the first <h1> if no stamp existed
        new = re.sub(r'(<h1[^>]*>.*?</h1>)', r'\1\n  <p class="muted">Last updated ' + STAMP + r'.</p>', html, count=1, flags=re.S)
    if new != html:
        SEARCH.write_text(new, encoding="utf-8")
        print("search.html: timestamp updated")
    else:
        print("search.html: no changes")

if __name__ == "__main__":
    raise SystemExit(main())
