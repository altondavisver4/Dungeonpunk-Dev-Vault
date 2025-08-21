#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]

# Where the search index may live
CANDIDATES = [
    ROOT / "search_index.json",
    ROOT / "site" / "search_index.json",
    ROOT / "_brain" / "search_index.json",
]

def load_index():
    for p in CANDIDATES:
        if p.exists():
            with p.open("r", encoding="utf-8") as f:
                return json.load(f), p
    raise FileNotFoundError("search_index.json not found in expected locations.")

def looks_archived(item: dict) -> bool:
    """Heuristics for your repo:
       - anything inside 'AI Brain/Archive'
       - any path component '/Archive/' under the AI Brain tree
       - title or path contains '[ARCHIVE]'
    """
    # common keys used in your index
    path = (item.get("path") or item.get("p") or "").lower()
    title = (item.get("title") or item.get("t") or "").lower()

    # Normalize slashes
    norm = path.replace("\\", "/")

    if "[archive]" in title or "[archive]" in path:
        return True

    # e.g. "AI Brain/Archive/..." or ".../AI Brain/Archive/..."
    if "ai brain/archive/" in norm:
        return True

    # generic safeguard if an Archive bucket exists under AI Brain
    if "/archive/" in norm and "ai brain/" in norm:
        return True

    return False

def filter_items(items):
    before = len(items)
    kept = [it for it in items if not looks_archived(it if isinstance(it, dict) else {})]
    after = len(kept)
    print(f"filtered archived from search index: kept {after}/{before}")
    return kept

def main():
    data, path = load_index()

    # Preserve original structure (list vs dict)
    if isinstance(data, list):
        data = filter_items(data)
    elif isinstance(data, dict):
        # Try common containers
        key = "items" if "items" in data else ("docs" if "docs" in data else None)
        if key is None:
            raise TypeError("Unexpected search index dict format (no 'items' or 'docs').")
        data[key] = filter_items(data[key])
    else:
        raise TypeError(f"Unexpected search index top-level type: {type(data)}")

    tmp = path.with_suffix(".filtered.tmp.json")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Write back atomically
    tmp.replace(path)
    print(f"wrote filtered search index → {path.relative_to(ROOT)}")

if __name__ == "__main__":
    sys.exit(main())
