---
title: 00 – Retrieval Playbook (v1.0)
type: ai-process
status: locked
tags: [ai-process, retrieval, playbook]
created: 2025-08-15
updated: 2025-08-15
---

# 00 – Retrieval Playbook (v1.0)

**Objective:** Prove you (and the AI) can find the exact note, sentence, or field you need within 10–30 seconds.

## A) Obsidian Retrieval Drill (solo, 5–10 min)
1. **Find by filename**  
   - Search: `file:"Fighter Class Interpretation"`  
   - Open the result. Confirm frontmatter is present and `status: locked`.
2. **Find by tag**  
   - Search: `tag:lore tag:fighter`  
   - Confirm it returns *only* the Fighter note.
3. **Find by cross-link**  
   - Open `Mechanics – “Everything is a Monster” OSR Philosophy (locked)` and navigate to its **backlinks**.  
   - Confirm you see the Fighter note listed.
4. **Find by phrase**  
   - Search this exact sentence fragment: `stack the odds until losing becomes impossible`.  
   - Confirm it jumps to the quote in the Fighter note.
5. **Find by type** *(Dataview)*  
   - Use the dashboard in `AI Brain Admin/Queries/Dataview – Status & Type dashboards.md` to list `type: lore` + `status: locked`.  
   - Confirm Fighter appears.
6. **Broken links check**  
   - Use Obsidian’s **Outgoing Links** on the Fighter note. Confirm all links point to existing notes.

## B) Chat-to-Vault Retrieval Drill (with AI, 5 min)
Copy/paste (or quote) the relevant section of the note into chat as proof for each question below. The AI should **only** answer from the pasted note (no guessing).

- Q1: What is the Fighter’s **Flavor Hook** line, verbatim?  
- Q2: List the three bullets under **Cultural Interpretation**.  
- Q3: Which two notes are listed under **Interfaces / Cross-links**?  
- Q4: What is the **status** and **type** in the Fighter note’s YAML?  
- Q5: What is the **Provenance** purpose line?

*Pass criteria:* All five answers match the note exactly.

## C) Troubleshooting
- If search returns too many hits, tighten with `file:`, `tag:`, or phrase quotes `"..."`.
- If backlinks are empty, open the target notes and add at least one cross-link between them.
- If Dataview shows nothing, ensure frontmatter keys are spelled correctly and `type/status` values match the Protocol.

## D) Optional Speed Run (advanced)
- From the command palette, trigger a saved search (if configured) to filter `type:lore status:locked` and open the top hit.
