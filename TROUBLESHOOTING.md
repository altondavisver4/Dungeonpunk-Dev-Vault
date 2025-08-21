# TROUBLESHOOTING

## Monitor Health fails ("age too old" or timestamp missing)
- Cause: `health.json` missing numeric `timestamp` or not regenerated.
- Fix:
  1) Ensure `write_health.py` writes `"timestamp": <epoch-seconds>`.
  2) Re-run the workflow that invokes `write_health.py` (Site Index or Quicklinks).
  3) Re-run `Monitor Health` (it fetches `/health.json` from Netlify).

## Netlify shows stale files
- Cause: deployment cache or previous build not triggered.
- Fix: trigger a redeploy on Netlify or push a no-op commit; ensure quick workflows commit regenerated artifacts.

## Old doctrines appear in search
- Cause: Archived files still included in indexes.
- Fix:
  1) Add front-matter flags to archived docs.
  2) Ensure `_brain/policy.json` exists.
  3) Re-run `Build All`.
  4) Run post-filter: `scripts/filter_search_index_archived.py`.

## Search returns nothing for a new doc
- Cause: Quick index build didn’t run or file naming not recognized.
- Fix: Check Actions logs; ensure doc is `.md` inside tracked folders; run `Build All` if needed.
