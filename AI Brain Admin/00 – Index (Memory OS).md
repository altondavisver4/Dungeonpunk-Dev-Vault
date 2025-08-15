---
title: 00 – Index (Memory OS)
type: ai-process
status: draft
tags: [ai-process, index]
created: 2025-08-15
updated: 2025-08-15
---

# 00 – Index (Memory OS)

## Folders
- [[/Mechanics]]
- [[/Procedural]]
- [[/Presentation]]
- [[/Systems]]
- [[/Special]]
- [[/Lore]]
- [[/Dev]]
- [[/!Staging]]
- [[/AI Brain Admin]]

## Quick Filters (Dataview – optional)
```dataview
TABLE status, type, file.mtime as Updated
FROM ""
WHERE status = "locked"
SORT file.mtime desc
```

```dataview
TABLE type, status, file.mtime as Updated
FROM ""
WHERE status != "locked"
SORT file.mtime desc
```
