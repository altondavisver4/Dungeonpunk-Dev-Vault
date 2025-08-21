---
title: Procedural – One Machine Storyteller Engine
type: procedural
status: draft
tags: [procedural, draft, ai, storyteller, generation]
aliases: [One Machine, Storyteller Engine]
---

# Procedural – One Machine Storyteller Engine

**Purpose**  
Central director that selects and renders the next encounter/scene by querying mechanics, world state, and behavior cards.

**Core Inputs**
- World state (time, location, factions, hazards)
- Actor state (PC + NPC stats, stress, aspects, memory)
- [[Mechanics – Behavior Card System (draft)]]
- [[Mechanics – Encounter Definition – Desire vs. Obstacle (locked)]]

**Decision Loop**
1. Identify player's current **desire** and the relevant **obstacle** candidates.
2. Score candidates using OSR engagement checks and novelty weighting.
3. Select encounter → instantiate progress clocks/stress.
4. Render narration via [[Presentation – Dynamic Text Narration Layer (locked)]].

**Outputs**
- Encounter definition packet
- Action economy hooks for [[Procedural – Unified Action Loop (draft)]]
