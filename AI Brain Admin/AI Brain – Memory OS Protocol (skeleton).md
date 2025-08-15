---
title: AI Brain – Memory OS Protocol (skeleton)
type: ai-process
status: draft
tags: [ai-process, protocol, taxonomy, automation]
aliases: [Memory OS Protocol, AI Brain Protocol]
---

# AI Brain – Memory OS Protocol (skeleton)

> Goal: Make every design artifact retrievable, legible, and linkable by both human and AI—without ceremony or guesswork.

## 1) File Naming
**Pattern:** `Category – Title (status).md`  
- **Category:** `Mechanics`, `Procedural`, `Presentation`, `Systems`, `Special`, `Lore`, `Dev`  
- **Title:** Short, unique, descriptive. No version numbers in name.  
- **Status (one):** `sketch`, `draft`, `locked`, `concept`, `deprecated`

**Examples**
- `Mechanics – Behavior Card System (draft).md`
- `Procedural – Unified Action Loop (draft).md`

## 2) YAML Frontmatter (required fields)
```yaml
title: <Category – Title>
type: <mechanic|procedural|presentation|narrative|system-integration|ai-process|lore|dev>
status: <sketch|draft|locked|concept|deprecated>
tags: [<function tags>, <supporting tags>]
aliases: [<optional short names>]
```
**Rules**
- `type` is a single best-fit bucket.
- `tags` are multi; prefer controlled vocabulary (see §3).
- `aliases` optional but helpful for link disambiguation.

## 3) Tag Taxonomy (controlled)
**Function:** `mechanic`, `procedural`, `presentation`, `narrative`, `system-integration`, `ai-process`, `lore`, `dev`  
**Status:** `sketch`, `draft`, `locked`, `concept`, `deprecated`  
**Themes (optional):** `osr`, `fate`, `pf2e`, `narration`, `ai`, `behavior`, `pacing`, `clocks`, `domain`, `grid`, `first-person`

*Add sparingly; prefer reusing existing tags.*

## 4) Cross-Linking Rules
- Link the **first mention** of any other note like `[[Mechanics – Progress Clocks for All Obstacles (draft)]]`.
- If a note doesn’t exist yet, still link it—future files will light up those “stubs”.
- Avoid bare URLs inside content; keep external sources in a `References` section if needed.

## 5) Status Workflow
- **sketch → draft → locked**
- **concept**: high-level pitch not yet integrated.  
- **deprecated**: kept for history; add a header banner and link to the replacement.

**Change control**
- When status changes, update `(status)` in filename and the `status` field in YAML.  
- Add a one-line **Changelog** at the bottom.

## 6) Folder Layout
- `/Mechanics`, `/Procedural`, `/Presentation`, `/Systems`, `/Special`, `/Lore`, `/Dev`, `/!Staging`  
- Staging gets cleared or promoted weekly.

## 7) Automation Hooks (to be scripted later)
- **Commit action:** On command, capture the current chat context that led to the file, append as a `Provenance` block.  
- **Lint pass:** Check naming, required frontmatter, allowed tags, and outbound link validity.  
- **Index build:** Generate an index note per folder listing files by `status` and `type`.

## 8) Provenance Template (optional but recommended)
```
## Provenance
- Source: Chat session YYYY-MM-DD HH:MM (PT)
- Prompt: <short description>
- Decision: <why this was created/changed>
```

## 9) Retrieval Heuristics (for AI queries)
- Prefer notes with `status: locked` for authoritative answers.  
- If multiple notes match, choose the one with the most inbound links.  
- If no locked note exists, prefer `draft` with latest changelog entry.

---

*This is the skeleton. We’ll harden it after Waves 3–4 by adding allowed tag lists and the exact automation triggers you want.*
