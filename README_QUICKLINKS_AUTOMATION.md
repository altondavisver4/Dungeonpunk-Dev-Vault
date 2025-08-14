# Quicklinks Automation Pack

This pack auto-builds:
- AI_QUICKLINKS.md (top active notes)
- Injects a Quicklinks block at the top of AI_INDEX.md (between markers)
- Updates Netlify `_redirects` (/quick, /core, /systems, /lore, /rd)

## Install
1) Unzip into the **root of your repo**.
2) Commit & push:
   git add generate_quicklinks.py .github/workflows/build-quicklinks.yml QUICKLINK_PINS.txt new_note.ps1
   git commit -m "add quicklinks automation"
   git push

## How it ranks notes
Score = pins (10k) + hot frontmatter (500) + 2 * commits in last 14 days + recency bonus
Recency bonus: <=1d +10, <=3d +6, <=7d +4, <=14d +2.

## Shortcuts
- /quick   → AI_QUICKLINKS.md
- /core    → top under "01 – Game Bible/Core Vision"
- /systems → top under "01 – Game Bible/Systems"
- /lore    → top under "01 – Game Bible/World & Lore"
- /rd      → top under "02 – R&D Lab/Daily Dumps"

## Optional
- Add file paths to QUICKLINK_PINS.txt to force-pin.
- Use `new_note.ps1` to create properly named notes quickly.

