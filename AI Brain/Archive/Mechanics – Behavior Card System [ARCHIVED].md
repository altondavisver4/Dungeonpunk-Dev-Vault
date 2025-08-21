---
title: Mechanics – Behavior Card System
type: mechanic
status: draft
tags: [mechanic, draft, ai, behavior]
aliases: [Behavior Cards]
---

# Mechanics – Behavior Card System

**Purpose**  
Drive NPC/monster decisions through weighted "behavior cards" that adapt to state, environment, and faction context.

**Card weighting inputs**
- Actor state: HP/stress, conditions, morale
- Environment: terrain, hazards, LOS, cover
- Faction & memory: loyalties, rivalries, prior outcomes

**Loop**
1. One Machine queries available cards for an actor.  
2. Weights update from current context.  
3. Card is drawn/selected → action generated → progress/stress applied.

**Interfaces**
- Queried by [[Procedural – One Machine Storyteller Engine (draft)]].
- Tightly coupled to [[Mechanics – Encounter Definition – Desire vs. Obstacle (locked)]].

**Open questions**
- Procedural vs. authored archetype decks?
- How much per-actor memory to retain vs. recycle?
