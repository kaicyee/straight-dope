# Current Status — Straight Dope Development

**Last Updated:** June 4, 2026  
**Maintained by:** Andrej  
**Current Session Count:** 0 (awaiting first session)

---

## Where We Are

Straight Dope is a conversation management system with a Python/FastAPI backend and modern frontend. The foundation is laid: database storage works, conversation retrieval works, UI is functional.

**Current Phase:** Feature backlog prioritization and iterative development

---

## Tier 1 — Ready to Build (Next Sprint)

### Feature: Selective Conversation Deletion

**Status:** 🔴 Not Started  
**Priority:** HIGH (user-requested, enables safe demos)  
**Effort:** ~15 minutes  
**User Benefit:** Users can delete specific conversations without losing entire history

**What:** Add `DELETE /api/conversations/{conversation_id}` endpoint + backend storage function + frontend delete button

**Why:** Users need to remove sensitive conversations (demos, test data, privacy) without full wipe

**Scope In:**
- Backend delete function in storage.py
- API DELETE endpoint in main.py
- Frontend delete button with confirmation
- Tests for edge cases (non-existent IDs, etc.)

**Scope Out:**
- Trash/restore (permanent delete only)
- Bulk deletion
- Soft deletes

**See:** BACKLOG.md for implementation plan

---

## Tier 2 — Planned (Future Sessions)

- Conversation search/filter
- Export conversations (markdown/PDF)
- Conversation tagging (demo, test, production)
- Bulk operations (delete multiple)

---

## Tier 3 — Strategic (Post-MVP)

- Conversation metadata and versioning
- Sharing (public/private links)
- API rate limiting & usage analytics
- Archival with soft delete

---

## Recent Completions

*None yet; first session approaching*

---

## Open Questions

- What's the deployment target for Straight Dope? (Local dev, cloud, government?)
- Are there compliance/security requirements?
- What's the expected user base? (Internal tool, product, both?)

---

## Technical Decisions Made

| Decision | Reasoning | Date |
|---|---|---|
| FastAPI backend | Fast iteration, modern Python, async support | 2026-05-17 |
| File-based storage | Simple for MVP, no DB dependency | 2026-05-17 |
| React frontend | Modern UX, component reusability | 2026-05-17 |

---

## Known Issues / Technical Debt

- *None documented yet*

---

## Session Handoff

**For next session:**
1. Read BACKLOG.md to refresh on Feature: Selective Conversation Deletion
2. Clarify scope and edge cases with Kai
3. Implement the three components (backend, API, frontend)
4. Test thoroughly
5. Execute END SESSION CEREMONY

---

## Metadata

| Field | Value |
|---|---|
| **Repository** | /Users/kaicyee/Desktop/Straight Dope |
| **Primary AI** | Andrej |
| **Development Phase** | Feature iteration (MVP foundation complete) |
| **Last Context Window** | Fresh (first session starting) |
| **Context Rot Status** | Imminent when reaching ~80-120K tokens in session |

---

**Next Session:** When Kai is ready, read documentation/INDEX.md and begin BEGIN SESSION CEREMONY
