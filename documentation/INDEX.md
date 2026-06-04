# Documentation Index

### Navigation Map for Straight Dope Development

This index is maintained by Andrej. Use it to navigate all documentation, session summaries, and reference materials.

---

## Quick Navigation

| What You Need | Where to Find It |
|---|---|
| **New to the system?** | [[SESSION-MANAGEMENT.md]] |
| **Where are we?** | [[CURRENT-STATUS.md]] |
| **How to start a session** | [[SESSION-MANAGEMENT.md#begin-session-ceremony-articulate-before-acting]] |
| **How to end a session** | [[SESSION-MANAGEMENT.md#end-session-ceremony-relentless-execution--document--close]] |
| **All past sessions** | [[SESSION-SUMMARIES/]] |
| **Feature backlog** | [[../BACKLOG.md]] |
| **AI role definition** | [[../CLAUDE.md]] |
| **Collaboration protocol** | [[../.cursorrules]] |

---

## Foundation Documents

| Document | Purpose | Last Updated |
|---|---|---|
| [[SESSION-MANAGEMENT.md]] | Session ceremonies, documentation structure, context rot prevention | 2026-06-04 |
| [[CURRENT-STATUS.md]] | Current state, active features, immediate next steps | 2026-06-04 |

---

## Session Summaries

*Every development session is documented here. Most recent first.*

### 2026 (Current)

#### June
- *Awaiting first session summary*

---

## Reference Documents

| Document | Purpose |
|---|---|
| [[SESSION-MANAGEMENT.md]] | Complete guide to session ceremonies and documentation discipline |

---

## Strategic Concepts

See [[../BACKLOG.md]] for feature prioritization and scope.

---

## How to Add to This Index

When a new session completes:

1. Add row to **Session Summaries** section:
   ```markdown
   | [[SESSION-SUMMARIES/2026-06-04-FEATURE-NAME.md]] | Feature: [What was completed] | 2026-06-04 |
   ```

2. Update [[CURRENT-STATUS.md]] with new state and next steps

3. Commit both updates:
   ```bash
   git add documentation/
   git commit -m "Session: [TOPIC]

   Completed: [Summary]
   See documentation/SESSION-SUMMARIES/2026-06-04-[TOPIC].md"
   ```

---

## Organization Principles

- **One session = one document** (SESSION-SUMMARIES/[DATE]-[TOPIC].md)
- **One-line summary in INDEX** (discipline and concision)
- **Documents are permanent** (never move or delete; archive if deprecated)
- **Index points to everything** (if it's important, it's linked here)
- **Chronological order** (most recent first in session summaries)
- **Clear naming** (dates, topics, purposes are obvious from file names)

---

## Integration Points

**From here to Kai's Ecosystem:**
- Session summaries document important technical decisions
- BACKLOG drives prioritization of what gets built next
- Each session builds on previous sessions via CURRENT-STATUS handoff

---

**Maintained by:** Andrej  
**Last updated:** June 4, 2026  
**Next update:** After first development session
