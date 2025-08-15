---
title: Memory OS Protocol
type: ai-process
status: locked
tags: [protocol, ai-brain, workflow]
created: 2025-08-15
updated: 2025-08-15
---

# Memory OS Protocol v1.1

## §1 – Purpose
The Memory OS is the operational framework for creating, storing, retrieving, and maintaining all AI Brain notes.  
It ensures that every file in the AI Brain follows consistent formatting, metadata standards, and retrieval-friendly practices.

## §2 – Scope
This protocol governs **all** AI-generated content stored in the AI Brain vault. Manual note creation by the user is not part of the workflow.

## §3 – Core Rules

### §3.1 – Naming Conventions
- All files follow: `<Folder> – <Title>.md`
- Folder name is capitalized and matches the vault directory structure exactly.
- Title is written exactly as the user specifies in the "Save" command.

### §3.2 – File Generation Standard
**Trigger:** User command in the form `Save <Title> under <Folder>`.

**Output:**
- **Filename:** `<Folder> – <Title>.md`
- **Location:** `/Folder` directory inside AI Brain vault.
- **Frontmatter:**
```yaml
---
title: <Folder> – <Title>
type: <folder-name-lowercase>   # auto-filled
status: draft                   # unless explicitly set to review/locked
tags: []                         # auto-add topic tags from content context
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**Process:**
1. Content written or compiled per user request.
2. YAML populated automatically — never omitted.
3. Dates always in ISO `YYYY-MM-DD` format.
4. Tags restricted to topic/context, not system metadata.
5. File packaged as `.zip` for vault import.

**Notes:**
- This process applies to **all** AI-generated notes.
- No manual note creation expected in project lifecycle.

### §3.3 – Tag Discipline
- Tags reflect subject matter only.
- System-level metadata (status, type) is never stored in tags.

### §3.4 – Retrieval Readiness
- Every note is created to be immediately searchable via:
    - Obsidian search syntax
    - Dataview queries
    - Backlinks and unlinked mentions

## §4 – Change Management
- Protocol updates are versioned (v1.1, v1.2, etc.).
- Any change to schema, naming, or folder structure must be recorded in this document.

## §5 – Enforcement
- All AI Brain notes are produced under this protocol without exception.
- Deviations require explicit user approval and are recorded in the protocol change log.

---
