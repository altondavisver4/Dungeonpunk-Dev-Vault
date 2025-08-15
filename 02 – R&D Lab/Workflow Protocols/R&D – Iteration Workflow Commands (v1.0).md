---
title: R&D – Iteration Workflow Commands
type: workflow
status: locked
tags: [iteration, workflow, protocol]
created: 2025-08-15
updated: 2025-08-15
---

# Iteration-Resistant Development Workflow

A structured workflow designed to prevent process drift and preserve idea integrity during back-and-forth creative sessions.

## Core Commands

**Checkpoint: <name>**  
Freeze current working state into a structured `.md` file with full metadata, links, and version number.  
_Example:_ `Checkpoint: Theme Study – Sanctuaries` → creates `R&D – Theme Study – Sanctuaries (v0.1, draft).md`

**Branch: <name>**  
Fork the current idea into a separate file. Both parent and child get cross-links.  
_Example:_ `Branch: Sanctuaries – Dark Variant`

**Merge: <A> + <B> into <name>**  
Consolidate two or more branches into a new note. Marks old files as deprecated with link to the new merged version.  
_Example:_ `Merge: Sanctuaries + Outposts into Settlements`

**Revert to <checkpoint>**  
Roll back working state to a previous checkpoint, starting a new version from that base.  
_Example:_ `Revert to Sanctuaries v0.1`

**Snapshot transcript**  
Append a short provenance section with the last few chat decisions for context.

---

## Inside Every Checkpoint

1. **Header** – Purpose, scope, status (draft/review/locked), tags, created/updated dates.
2. **Current Canon** – The cleaned, authoritative version of the concept.
3. **Working Deltas** – Bullet list of pending changes, open questions, or experiments.
4. **Variants/Branches** – Links to sibling explorations.
5. **Changelog & Provenance** – Timestamped record of changes, plus link to source conversation.
6. **Cross-links** – To relevant Lore/Mechanics/Procedural notes in your AI Brain.

---

## Versioning Rules

- **Draft in R&D:** `R&D – <Category> – <Topic> (vX.Y, draft).md`
- **Locked to canon:** `Lore – <Topic> (locked).md` (moved out of R&D)
- **Deprecated branches:** Keep links to successors and a banner warning.

---

## Provenance
Source: Generated in live chat during setup of AI Brain iteration workflow guardrails. Purpose: Provide persistent command reference to maintain consistency in creative development.
