# AI Brain RUNBOOK

Audience: humans and AI assistants maintaining the AI Brain.

---
## Daily (5–10 min)
1. Open Netlify health:
   - `/health.json` should have `timestamp` within 15 minutes of now.
   - `/health.html` should show the latest commit.
2. Check GitHub Actions:
   - `Monitor Health` should be passing.
   - Quick workflows (Search/Quicklinks/Site Index) should be green on your last push.

## Weekly (15–20 min)
1. Run **Build All** (manual or scheduled) to refresh everything.
2. Confirm:
   - `_brain/ai_brain.json` and `_brain/search_index.json` updated.
   - `/search.html` loads and finds new docs.
3. Speed snapshot (optional): run the speed-check workflow if enabled.

## When a build fails
1. Open the failing job → read the first error line.
2. Common fixes:
   - YAML syntax or wrong path → edit `.github/workflows/...` and re-run.
   - Health timestamp missing → re-run job that calls `write_health.py` or fix the script.
   - Search index stale → run quick workflow or `Build All`.

## When old doctrines appear in answers
1. Verify `CANON_POLICY.md` and `_brain/policy.json` exist and list the doctrine as DEPRECATED/ARCHIVED.
2. Ensure archived docs have front-matter:
   ```yaml
   ---
   status: archived
   archived: true
   ---
   ```
3. Re-run `Build All` to recompile indexes.
4. If still visible, run the linter and the post-filter:
   - `scripts/lint_no_archived_in_active.py`
   - `scripts/filter_search_index_archived.py`

## Restore from scratch (disaster)
1. Ensure the repo is intact on GitHub.
2. Re-run `Build All`. If Netlify is stale, trigger a fresh deploy.
3. If health fails, run `write_health.py` locally or via the workflow that calls it.
