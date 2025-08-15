---
title: Search Macros – Fast Retrieval
type: ai-process
status: draft
tags: [ai-process, queries, search]
created: 2025-08-15
updated: 2025-08-15
---

# Search Macros – Fast Retrieval

Use these in Obsidian’s search bar.

- **By filename (exact):**
  - `file:"Fighter Class Interpretation"`
- **By tag combo:**
  - `tag:lore tag:fighter`
- **By type + status (Dataview required for full dashboard):**
  - `type: lore status: locked` (as frontmatter keys in filters if using plugins)
- **By phrase (exact):**
  - `"stack the odds until losing becomes impossible"`
- **Find notes with no outbound links:**
  - `-"[["` (negative search for page links), or use the Dataview query in the dashboards note
- **Find notes touched today:**
  - `modified:day`
