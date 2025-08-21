# AI Brain ARCHITECTURE

## Purpose
A private, tiered semantic knowledge base with continuous indexing and a live mirror so assistants can answer with full context—without relying on chat memory.

## Components
- **Source of truth (GitHub)**: Markdown notes, scripts, workflows.
- **Generated artifacts (Netlify)**: `_brain/ai_brain.json`, `_brain/search_index.json`, `search.html`, `health.html/json`.
- **Workflows (GitHub Actions)**:
  - Quick workflows on push (regen search/quicklinks/site index/health).
  - Build All (heavy) on schedule/manual.
  - Monitor Health (fetches `/health.json` and fails if stale).
- **Policy**:
  - `_brain/policy.json` + `CANON_POLICY.md` define what is ACTIVE vs ARCHIVED/DEPRECATED.

## Data Flow (high level)
1. You edit Markdown → push to GitHub.
2. Quick workflows regenerate indexes and health → commit outputs.
3. Netlify serves the updated artifacts immediately.
4. Assistant reads raw files from GitHub for source and uses Netlify for compiled indexes and health.

## Canon Enforcement
- Archived/Deprecated docs flagged via **front-matter** and/or **path** (`AI Brain/Archive`) and/or **title markers** (`[ARCHIVE]`, `[DEPRECATED]`).
- Builders and post-filters **skip** archived content using `_brain/policy.json`.
- A linter fails CI if archived docs leak into active areas.
