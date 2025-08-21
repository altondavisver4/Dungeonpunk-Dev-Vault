---
title: Special – Group Entities with Morale-Based Disbanding
type: system-integration
status: draft
tags: [system-integration, draft, morale, groups]
aliases: [Group Entities, Morale Disband]
---

# Special – Group Entities with Morale-Based Disbanding

**Premise**  
Multi-unit enemy groups are represented as a single entity that can split or disband dynamically when leadership breaks or morale fails.

**Behaviors**
- **Leader down:** all sub-groups test morale; on fail, disband to individuals or flee.
- **Rout threshold:** stress/HP crossing triggers morale checks.
- **Regroup clock:** surviving units can reform after a timer if conditions allow.

**Interfaces**
- Hooks into [[Mechanics – Progress Clocks for All Obstacles (draft)]].
- Informed by [[Systems – OSR Engagement Checks (locked)]].
