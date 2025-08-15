---
title: Presentation – First-Person Grid-Based Movement
type: presentation
status: locked
tags: [presentation, locked, grid, first-person, 90deg]
aliases: [First-Person Grid, 90° Grid Movement]
---

# Presentation – First-Person Grid-Based Movement

**Premise**  
Player moves in discrete tiles with 90° rotations. Tile width ≈ screen width to keep the "you are here" feeling with visible hands/weapons.

**Implications**
- Reliable Live2D billboard angles (no odd oblique views).
- Camera snap reduces motion sickness and animation burden.
- Encounter density assumptions: monsters-per-tile constraints tie into encounter math.

**Interfaces**
- Coordinates with [[Presentation – Live2D Paper Doll Characters (locked)]] for billboard expectations.
- Feeds encounter math used by [[Procedural – Unified Action Loop (draft)]].
