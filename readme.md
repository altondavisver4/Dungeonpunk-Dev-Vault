# AI Brain

The **AI Brain** is a structured knowledge system built to extend ChatGPT’s memory and navigation speed for long-term indie game development.  
It is not a “brain” in the traditional sense, but a **knowledge index + workflow automation system** designed to make it easy for any AI assistant (including future ChatGPT sessions) to load, navigate, and optimize Alton’s project data.

---

## Purpose

- Provide **fast, structured recall** of design docs, rulesets, and notes.  
- Act as a **persistent memory layer** that survives across ChatGPT sessions.  
- Standardize **file naming, indexing, and workflows** so assistants can work without confusion.  
- Support **game design** (Pathfinder d20, FATE hybrid, OSR mechanics, harem/heat systems, One Machine AI storyteller, etc.) with queryable and cross-linked documents.  
- Provide **monitoring & health checks** to ensure the system remains functional.

---

## Structure

### 1. **File Storage**
- The vault stores Markdown (`.md`) files, organized into thematic directories (design notes, systems, companions, encounters, etc.).  
- File naming conventions are documented in a separate reference file so AI can always interpret them consistently.

### 2. **Netlify (Deployed Mirror)**
- The AI Brain is deployed at: **https://psiopera-octopus-ogre-4372.netlify.app/**  
  - Root (`/`) serves the full site.  
  - `/search` enables index-based search.  
  - `/health.html` and `/health.json` confirm system status.
- Netlify provides a **live, browsable copy** of the repo and all generated outputs (brain exports, indexes, health pages).

### 3. **Workflows**
- **Build All** → Full site + index regeneration (heavy, scheduled).  
- **Quick Workflows** → Incremental updates (triggered on file edits).  
- **Monitor Health** → Continuously checks that the AI Brain outputs are up-to-date and operational.

### 4. **Health System**
- Health endpoints (`health.html`, `health.json`) confirm uptime and freshness of outputs.  
- The **Monitor Health** GitHub Action reads these to validate live status.  
- If health checks fail, review the workflow logs and re-run builds as necessary.

---

## Usage Guide (for AI Assistants)

1. **Start here.** Read this README before exploring.  
2. **Check health.** Visit `https://psiopera-octopus-ogre-4372.netlify.app/health.json` to confirm system health.  
3. **Search smartly.** Use `/search` for fast, full-text and semantic queries.  
4. **Navigate with context.** Use file names and directory structure to understand content topics.  
5. **Validate output.** If unsure whether you’re seeing the latest state, compare Netlify to GitHub or re-trigger builds.  
6. **Always ask.** If your context is incomplete, ask for clarification rather than assume.

---

## File Naming & Structure

Files and folders follow structured naming rules for automatic parsing:

| Format                        | Meaning                                |
|-------------------------------|----------------------------------------|
| `2025-08-20_lore_tiles.md`    | Dateed lore note                       |
| `mechanics_progress-clock.md` | System mechanics doc                   |
| `notes_draft_xyz.md`          | Development draft/wip (less reliable)  |

By keeping names explicit and chronological, indexing remains accurate and contextually meaningful.

---

## Troubleshooting & Maintenance

- **Monitor Health failures?**  
  - Re-run the relevant workflow (`Quick` or `Build All`).  
  - Check that `write_health.py` is generating updated content.  
  - Verify that health endpoints are reachable (Netlify site must be up and updated).

- **If search is stale?**  
  - Ensure Quick Workflows have run.  
  - Check that `search_index.json` was generated and committed.

- **Build problems?**  
  - Confirm YAML syntax, triggers, and file paths in `.github/workflows`.  
  - Use manual build triggers if needed.

---

## Improvement Notes

- Future assistants may prefer reading directly from GitHub via connector (after you enable it).  
- To support Pathfinder reference queries, SRD rule data could be imported and indexed into `/pf2e/`.  
- Stay lightweight: text files remain the quickest for search and indexing.  
- Incremental builds vs full builds: Quick workflows keep deployment efficient; heavy rebuilds remain scheduled.

---

## Philosophy

This repo exists so that the AI **never forgets** — because it *is* the AI’s memory.

Principles:
- **Explicit beats implicit.** Every folder and file is discoverable and searchable.
- **Speed over fancy.** JSON and Markdown > image-heavy or binary data.
- **Scalable for years.** Built to grow without fracturing its usefulness.

---

## Status Overview

- ✅ Source docs live in vault  
- ✅ Incremental plus scheduled builds  
- ✅ Netlify live with search and health  
- ⏳ Future: embedding, SRD import, AI-driven summary tools

---

_Authored by Alton — Aspiring Solo Indie Game Dev, co-creating game systems and AI memory workflows with ChatGPT._

