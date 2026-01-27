# -*- coding: utf-8 -*-
"""
GitHerd — Resources module.

Contains text resources like help text and constants.
"""

HELP_TEXT = """GitHerd — Real-time Git branch synchronizer

Keeps multiple Git branches aligned in real-time.
Ideal for parallel AI coding sessions or any workflow
with multiple active branches.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HANDLED CASES:

┌─────────────────────────────────────────┬─────────────────────┐
│ Situation                               │ Action              │
├─────────────────────────────────────────┼─────────────────────┤
│ Nothing to do                           │ Idle                │
│ Local main ahead                        │ Auto push           │
│ Branches behind main                    │ Auto push to sync   │
│ 1 branch ahead (not diverged)           │ Fast-forward + push │
│ 1+ diverged branch, disjoint files      │ Merge button        │
│ 1+ diverged branch, common files        │ STOP                │
│ 2+ branches ahead, disjoint files       │ Merge button        │
│ 2+ branches ahead, common files         │ STOP                │
└─────────────────────────────────────────┴─────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MULTI-REPO:

- File menu > Add repository (Ctrl+O)
- Each tab manages a repository independently
- Repositories are saved between sessions

TAB INDICATORS:
- Green background = Polling active
- Gray background = Polling inactive
- Red background = STOP (action required or error)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

KEYBOARD SHORTCUTS:

- Ctrl+O : Add repository
- Ctrl+S : Stop all polling
- Ctrl+R : Restart
- Ctrl+Q : Quit

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ADVANCED MODE (Settings):

When enabled, UI is simplified:
- Single click on tab: select, or toggle polling if selected
- Double click on tab: sync now (any tab)
- Buttons hidden (use menu or tab clicks)
- Log toggle next to status

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

https://github.com/Jacques66/GitHerd
"""
