# Auto Netlify Index Pack

Generates `index.html` in the root **and every subfolder** with correctly URL-encoded links.
Runs on every push via GitHub Actions; Netlify will deploy browsable indexes automatically.

## Install
1) Unzip into the **root of your repo**.
2) Commit & push:
   git add generate_site_index.py .github/workflows/build-site-index.yml site.css README_AUTO_NETLIFY_INDEX.md
   git commit -m "add auto site index"
   git push

## Notes
- Ignores: `.git`, `.github`, `.obsidian`, etc.
- Links `.md`, `.txt`, `.html`, and common assets.
