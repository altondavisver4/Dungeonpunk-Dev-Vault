---
title: Dataview – Status & Type dashboards
type: ai-process
status: draft
tags: [ai-process, queries, dataview]
created: 2025-08-15
updated: 2025-08-15
---

# Dataview – Status & Type dashboards

## Locked Lore
```dataview
TABLE file.link as Note, status, type, file.mtime as Updated
FROM ""
WHERE status = "locked" AND type = "lore"
SORT file.mtime desc
```

## Draft Mechanics
```dataview
TABLE file.link as Note, status, tags, file.mtime as Updated
FROM ""
WHERE status = "draft" AND type = "mechanic"
SORT file.mtime desc
```

## Notes Missing Cross-links (heuristic)
> Manually check these for at least one `[[internal link]]`

```dataview
TABLE file.link as Note, status, type
FROM ""
WHERE !contains(file.content, "[[")
SORT file.mtime desc
```

## Recently Updated (any type)
```dataview
TABLE file.link as Note, status, type, file.mtime as Updated
FROM ""
SORT file.mtime desc
LIMIT 20
```
