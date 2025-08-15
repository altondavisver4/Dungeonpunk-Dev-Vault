---
title: AI Brain – Memory OS Protocol (v1.0)
type: ai-process
status: locked
tags: [ai-process, protocol, taxonomy, automation]
aliases: [Memory OS Protocol]
created: 2025-08-15
updated: 2025-08-15
---

# AI Brain – Memory OS Protocol (v1.0)

**Goal:** Make every design artifact retrievable, legible, and linkable for both human and AI—without ceremony.

## 1) File Naming
**Pattern:** `Category – Title (status).md`  
- **Category (one of):** Mechanics, Procedural, Presentation, Systems, Special, Lore, Dev  
- **Title:** Short, unique, descriptive. Avoid version numbers in the filename.  
- **Status (one):** sketch, draft, locked, concept, deprecated

**Examples**
- `Mechanics – Behavior Card System (draft).md`
- `Procedural – Unified Action Loop (draft).md`

## 2) Folder Layout
Top-level:
```
/Mechanics
/Procedural
/Presentation
/Systems
/Special
/Lore
/Dev
/!Staging
/AI Brain Admin   # Protocols, checklists, indexes, scripts
```
- Staging is for **M** (hold) items, weekly review then promote or discard.

## 3) YAML Frontmatter (required)
```yaml
title: <Category – Title>
type: <mechanic|procedural|presentation|narrative|system-integration|ai-process|lore|dev>
status: <sketch|draft|locked|concept|deprecated>
tags: [<function tags>, <supporting tags>]
aliases: [<optional short names>]
created: YYYY-MM-DD
updated: YYYY-MM-DD
```
**Rules**
- `type` is exactly one.  
- `status` from the allowed set only.  
- `tags` reuse controlled vocab (see §4).  
- `title` must match the filename’s Category + Title (ignore `(status)` and extension).

## 4) Controlled Tag Taxonomy
**Function (pick 1–2):** mechanic, procedural, presentation, narrative, system-integration, ai-process, lore, dev  
**Themes (optional):** osr, fate, pf2e, narration, ai, behavior, pacing, clocks, domain, grid, first-person, parallax, morale  
**Workflow (optional):** needs-review, example, reference

Keep tags **small and stable**. Prefer editing to add existing tags rather than inventing new ones.

## 5) Status Workflow
```
concept -> sketch -> draft -> locked
                 \-> deprecated
```
- Move forward only when the note has: clear **Purpose**, **Interfaces**, and at least one **Cross-link**.  
- **deprecated** means “kept for history”; add a banner at the top linking to its replacement.

## 6) Cross-Linking Rules
- Link the **first mention** of any other note with `[[Exact File Name (status)]]`.
- If the target doesn’t exist yet, still link it—this is a stub that will light up later.
- Prefer links to **locked** notes for authority. Use `draft` when no locked note exists.

## 7) Provenance & Changelog
At the end of each note:

```
## Changelog
- YYYY-MM-DD: <what changed, why>

## Provenance
- Source: Chat or doc that led to this note
- Decision: 1–2 lines on why it exists
```

## 8) Lint Rules (what the checker enforces)
- Filename matches `Category – Title (status).md`.  
- Frontmatter contains all required keys.  
- `type` and `status` values are from allowed lists.  
- `title` field matches the filename’s Category – Title.  
- At least one outbound `[[link]]`.  
- No orphan notes in core folders (should have ≥1 inbound link within 7 days).  
- A `Changelog` section exists.

## 9) Index & Discovery
Create a top-level **00 – Index** note with:
- Section links to each folder
- Optional Dataview queries by `status` and `type` (see included index note)

## 10) Git & Media Hygiene
- Obsidian Git auto-commit every 5m; auto-push after commit.  
- `.gitignore` filters cache, temp, and plugin noise.  
- Prefer Git for **text**. Use Obsidian Sync for heavy media.

## 11) Protocol Change Control
- Increment **(vX.Y)** in this note when rules change.  
- Add migration steps in **Changelog**.

---

## Changelog
- 2025-08-15: v1.0 initial lock; derived from import rehearsal.
