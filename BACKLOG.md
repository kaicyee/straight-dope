# Straight Dope Development Backlog

## Prioritized Features & Enhancements

---

## TIER 1 - User Experience (High Priority)

### Feature: Selective Conversation Deletion
**Status:** Documented, not yet implemented  
**Date Identified:** June 3, 2026  
**Reason:** Users may want to remove specific conversations (e.g., sensitive topics, demos) without deleting the entire history

**Implementation Plan:**

1. **Backend (storage.py)** — Add delete function:
```python
def delete_conversation(conversation_id: str):
    """Delete a single conversation by ID."""
    path = get_conversation_path(conversation_id)
    if not os.path.exists(path):
        raise ValueError(f"Conversation {conversation_id} not found")
    os.remove(path)
```

2. **API (main.py)** — Add DELETE endpoint:
```python
@app.delete("/api/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a specific conversation."""
    try:
        storage.delete_conversation(conversation_id)
        return {"status": "deleted", "conversation_id": conversation_id}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
```

3. **Frontend** — Add delete button (optional UI enhancement):
   - Small delete icon next to each conversation in sidebar
   - Confirmation modal before deletion
   - Instant removal from list on success

**Effort:** ~15 minutes total (2 min backend, 2 min API, 5 min frontend, 6 min testing)

**Use Cases:**
- Remove sensitive demo conversations before sharing
- Clean up test conversations
- Maintain demo environment for proposals/presentations
- User privacy (delete specific conversations retroactively)

**Note:** Deletion is permanent (no trash/restore). Consider this when designing UI.

---

## TIER 2 - Future Enhancements (Nice-to-Have)

- [ ] Conversation search/filter
- [ ] Export conversations to markdown/PDF
- [ ] Conversation tagging (demo, test, production, etc.)
- [ ] Bulk operations (delete multiple, export multiple)
- [ ] Conversation archival (soft delete with restore option)

---

## TIER 3 - Strategic Improvements (Post-MVP)

- [ ] Conversation metadata (tags, access level, archival status)
- [ ] Version history (track edits to questions)
- [ ] Sharing (public/private conversation links)
- [ ] API rate limiting & usage analytics

---

**Last Updated:** June 3, 2026  
**Maintained By:** Andrej
