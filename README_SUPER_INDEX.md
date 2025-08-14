## Super Index & Snapshots

This repo emits:
- `/_brain/ai_super_index.json` — unified index with tier membership and link graph.
- `/_brain/snapshots/` — rolling JSONL.GZ snapshots of raw markdown (`LATEST` points to current).

Use `ai_super_index.json` for instant cross-tier navigation and related-note jumps.
Use the snapshot when hosting is unavailable to recover raw content quickly.
