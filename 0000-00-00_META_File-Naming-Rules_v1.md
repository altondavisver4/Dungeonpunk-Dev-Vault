# Dungeonpunk Dev Vault – File Naming Rules

## Pattern
`YYYY-MM-DD_CATEGORY_Short-Slug_vN.md`

---

### Fields
- **YYYY-MM-DD** – Date of creation (date first written, not last edited)
- **CATEGORY** – All caps, one word, main type:
  - `MECHANIC` – Core gameplay mechanics
  - `SYSTEM` – Game systems and subsystems
  - `LORE` – Setting, story, characters, factions
  - `QUEST` – Quest or mission design
  - `META` – Notes about the vault, workflow, naming, organization
  - `ASSET` – Art, sound, or other media files
- **Short-Slug** – Short descriptive phrase, hyphen-separated
- **vN** – Version number, starts at v1

---

### Examples
- `2025-08-14_MECHANIC_Heat-Doom-Matrix_v1.md`
- `2025-08-14_LORE_Eunuch-Guard-Corps_v2.md`
- `2025-08-14_SYSTEM_Bard-Only-Music_v1.md`
- `2025-08-14_META_Development-Workflow_v1.md`

---

### Rules
1. **One major idea per file** – Keep concepts self-contained for easier referencing.  
2. **Start with a summary** – First 1–2 sentences explain the file's purpose.  
3. **Cross-link related notes** – Use `See also: [[Related-Note]]` at the top or bottom.  
4. **Date is the creation date** – Keep it fixed even after edits.  
5. **Version increments on major changes** – Small edits don’t bump the version.  

---

**Purpose:**  
This document ensures consistent file naming for AI indexing, quick search, and easier cross-referencing during development.  
