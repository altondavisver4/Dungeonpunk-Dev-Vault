---
title: Special – Layered 2D Assets for First-Person Depth
type: presentation
status: draft
tags: [presentation, draft, parallax, first-person, 2d-layers]
aliases: [Layered 2D Depth]
---

# Special – Layered 2D Assets for First-Person Depth

**Premise**  
Simulate depth in a 3D first-person view using multiple parallax layers of 2D assets.

**Guidelines**
- Foreground/midground/background atlases; constrain camera to 90° rotations for billboard fidelity.
- Depth cues: scale, blur falloff (optional), speed differential on movement.
- Tile-aware placement: each grid step shifts layers predictably to avoid jitter.

**Interfaces**
- Works with [[Presentation – First-Person Grid-Based Movement (locked)]].
- Complements [[Presentation – Live2D Paper Doll Characters (locked)]].
