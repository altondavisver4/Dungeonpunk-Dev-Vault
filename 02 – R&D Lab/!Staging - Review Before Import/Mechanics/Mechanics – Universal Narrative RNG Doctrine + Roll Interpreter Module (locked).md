---
title: Mechanics – Universal Narrative RNG Doctrine + Roll Interpreter Module
type: mechanic
status: locked
tags: [mechanic, locked, narration, d20]
aliases: [UNRNG Doctrine, Roll Interpreter Module]
---

# Mechanics – Universal Narrative RNG Doctrine + Roll Interpreter Module

**Purpose**  
Narration-first d20 resolution that turns *every roll* into consistent story beats the One Machine can use.

**Core classifications**
- **Outcome:** success or failure
- **Competence tone:** natural competence vs. circumstantial interference
- **Origin point:** which bonus crossed the DC first; that source earns narrative credit/blame
- **Tone band:** nat 1 = rare mishap; 2–9 = circumstance interference; 11–19 = competent under pressure; nat 20 = extraordinary
- **DC label:** difficulty as seen by the world (ties into pacing/telegraphing)

**Flow**
1. Roll → determine success/failure vs DC.  
2. Identify *origin point* (the modifier that crosses the DC).  
3. Map to **tone band**.  
4. Emit narration packet: `{result, origin, tone, dc_label}`.

**Interfaces**
- Feeds [[Procedural – Target-Number Narration Across All Rolls (locked)]] packets.
- Pairs with [[Mechanics – Progress Clocks for All Obstacles (draft)]].

**Notes**
- Probability truth: DC 11 is the true 50% point for +0.  
- Take 10/Take 20 semantics provide calm vs. persistence expressions of competence.
