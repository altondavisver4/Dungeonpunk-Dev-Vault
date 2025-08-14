#!/usr/bin/env bash
set -euo pipefail

echo "Python version:"
python3 -V

# deps (kept lean)
pip3 install -r requirements.txt

# 1) Generate all pages that Netlify will serve
python3 generate_site_index.py
python3 generate_quicklinks.py || true

# 2) Build ‘AI Brain’ assets (export/index/search)
#    (these live under scripts/ per our repo layout)
python3 scripts/export_brain.py || true
python3 scripts/build_ai_index.py
python3 scripts/build_search_page.py

# 3) Housekeeping: health + ensure search timestamp stays fresh
python3 scripts/write_health.py
python3 scripts/update_search_timestamp.py || true

echo "Build steps finished."
