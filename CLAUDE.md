# Claude Instructions for This Project

## Always Do This

- Read `TODO.md` at the start of every session before writing any code.
- After completing each TODO item, mark it done (`- [x]`) in `TODO.md` immediately — do not batch updates.
- When a task reveals sub-tasks not already in `TODO.md`, add them to the appropriate phase before starting.
- Complete phases in order. Do not begin Phase 2 work while Phase 1 items are unchecked.

## Reference Documents

- `ARCHITECTURE.md` — canonical tech stack, project structure, SQL schema, and HTMX conventions.
- `PRD.md` — authoritative description of each user flow and its requirements.
- `TODO.md` — the build checklist; source of truth for what is done and what is next.

## Project Context

Board game library management SSR web app built for convention use.

- **Stack:** Flask · PostgreSQL · Flask-SQLAlchemy · Jinja2 · HTMX · Tailwind CSS Play CDN
- **Input device:** USB barcode scanner (keyboard emulator) — UPC → Enter keypress
- **Constraint:** Games never leave the library. No reservation system needed.
- **Operator:** Single librarian on a laptop. No authentication for MVP.
- **Partial responses:** Routes that are called by HTMX should detect the `HX-Request` header and return only the relevant partial template, not the full base layout.
- **One file per model:** each ORM model lives in its own file — `lib/board_game.py`, `lib/game_copy.py`, `lib/player.py`, `lib/play.py`, `lib/play_participant.py`.
- **One file per repository:** each repository lives in its own file — `lib/board_game_repository.py`, `lib/game_copy_repository.py`, `lib/player_repository.py`, `lib/play_repository.py`, `lib/play_participant_repository.py`.
- **Repositories are instance-based:** always instantiate before calling methods — `BoardGameRepository().all()`, not `BoardGameRepository.all()`.

## 📓 Journal System: Learning from the Past

The `docs/journal/` directory contains a historical record of work completed on this project. **This is for understanding past decisions, NOT planning future work.**

### Journal Rules

**When to CREATE a journal entry:**
1. After completing a significant feature or bug fix
2. After making architectural changes (API routes, database schema, state management)
3. After debugging a complex issue and finding the solution
4. After implementing a new Suno API endpoint
5. When you discover important behavior or constraints that aren't obvious from code

**When to REVIEW journal entries:**
1. **Before working on related features** - Check if similar work was done before
2. **When encountering errors** - See if the issue was solved previously
3. **Before modifying existing APIs** - Understand why current implementation exists
4. **User mentions past work** - "Remember when we..." or "Like we did before..."
5. **Working in unfamiliar parts of codebase** - Check if context exists

**NEVER:**
- Edit existing journal entries (they are historical records)
- Use journals for planning future work (use conversations for that)
- Create journal entries for trivial changes (typo fixes, formatting)
- Make assumptions without checking relevant journal entries first

### Journal Structure

**Index File:** `docs/journal/INDEX.md`
- Master catalog of all journal entries
- One-line description per entry
- Organized by date (newest first)
- Updated every time a new entry is created

**Entry Format:** `docs/journal/YYYY-MM-DD-brief-description.md`
- Date-prefixed filename for chronological ordering
- Brief, descriptive name (e.g., `2024-11-24-implement-music-generation.md`)
- Contains: What was done, why, challenges faced, key decisions

**Entry Template:**
```markdown
# [Brief Title]

**Date:** YYYY-MM-DD
**Type:** [Feature/Bugfix/Refactor/Investigation]
**Files Changed:** List main files affected

## What Was Done
Brief description of the work completed.

## Why
The reason this work was necessary or requested.

## Key Decisions
- Decision 1: Reasoning
- Decision 2: Reasoning

## Challenges & Solutions
Problems encountered and how they were solved.

## Testing
How the changes were verified.

## Notes for Future
Any important context that future AI agents should know.
```

### How to Use Journals

**Before starting work:**
```bash
# Check the index to see if related work exists
cat docs/journal/INDEX.md | grep -i "keyword"
```

**After completing work:**
1. Create new journal entry using the template
2. Update `docs/journal/INDEX.md` with new entry at the top
3. Keep entries concise but informative

**Example Review Scenario:**
```
User: "Add the extend music feature"
AI: *First checks docs/journal/INDEX.md for any "extend" or "music generation" entries*
AI: *Reviews relevant entries to understand existing implementation patterns*
AI: *Then reads docs/Suno API/extend-music.md for API spec*
AI: *Implements following established patterns from journal*
```