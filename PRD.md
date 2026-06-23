# Product Requirements Document

## Overview

A server-side rendered web application for managing a board game lending library at a convention. A librarian operates the app on a laptop. A USB barcode scanner (keyboard emulator) is the primary input device for identifying physical game copies. Games never leave the library building.

All data access goes through repository classes (`lib/repositories.py`). Routes call repository methods — never the database session directly. See `ARCHITECTURE.md` for the full repository reference.

---

## Users

| Role | Description |
|---|---|
| Player | Convention attendee who checks games in/out and logs play sessions |
| Staff | Convention worker who adds and removes game from the library

---

## Core User Flows

### 1. Dashboard — Inventory at a Glance

**Entry point:** `/` (home page)

**What it shows:**
- A table of all game copies grouped or sortable by shelf location, game title, and availability status.
- Status badge per copy: **Available** (green), **In Play** (yellow), **Maintenance** (red).
- Summary counts at the top: total copies, currently in play, available, in maintenance.
- Filter buttons to show only copies with a given status.

**Goal:** Give the librarian an instant read on what's out and what's available without scanning anything.

---

### 2. Scan Page — Identify a Copy

**Entry point:** `/scan` (linked from nav; also the default landing for scanner activity)

**Flow:**
1. Page loads with a text input auto-focused.
2. Librarian scans a UPC barcode (or types one manually and hits Enter).
3. HTMX posts the UPC to `POST /scan`; the server looks up the `board_game` by `factory_upc`, then counts available copies.
4. A result card replaces the placeholder below the input — no full page reload.
5. The result card shows:
   - Game title and cover info (publisher, player count, play time)
   - Number of copies available (e.g. "2 of 3 copies available")
   - Context-appropriate action buttons (see flows 3 and 4 below)
6. The input field is cleared and re-focused for the next scan.

**Error states:**
- UPC not found → "Unknown barcode. Is this game in the catalog?" with a link to add it.
- Game found but no copies available → "All copies are currently in play."
- Scanner inputs a malformed string → "Invalid barcode format."

---

### 3. Check Out — Mark a Game as In Play

**Triggered from:** Scan result card when at least one copy is Available

**Action button:** "Check Out"

**Flow:**
1. Librarian scans game; result card shows copy count (e.g. "2 of 3 available") and "Check Out" button.
2. Player clicks "Check Out" — HTMX swaps in an alias text input within the result card.
3. Player types their alias and submits.
4. Server finds or creates the matching `player` record by alias.
5. Server creates a `play` record (`board_game_id`, `start_time = NOW()`, `checked_out_by_player_id = player.id`).
6. Server sets one `game_copy` WHERE `board_game_id = ? AND availability_status = 'Available'` to `'In Play'`.
7. Result card confirms: "Checked out to [alias]. Good luck!"

**Guard:** If no copies are available, the "Check Out" button is not shown. Instead: "All copies are currently in play."

---

### 4. Check In — Return a Game to the Shelf

**Triggered from:** Scan result card when at least one copy is In Play

**Action button:** "Return to Shelf"

**Flow:**
1. Librarian scans game; result card shows copy counts and "Return to Shelf" button.
2. Player clicks "Return to Shelf" — HTMX swaps in an alias selector listing players with an open play (`end_time IS NULL`) for this game.
3. Player selects their alias and submits.
4. Server sets `play.end_time = NOW()` on the matching open play.
5. Server calculates and stores `duration_minutes` from `end_time - start_time`.
6. Server sets one `game_copy` WHERE `board_game_id = ? AND availability_status = 'In Play'` to `'Available'`.
7. Result card confirms: "Returned. Session was [N] minutes."

---

### 5. Log a Play Session

**Entry point:** `/plays/new` (linked from nav and from the scan result card)

**Flow:**
1. Librarian navigates to Log Play.
2. Selects (or scans) the game being logged.
3. Enters:
   - **Date played** — defaults to today
   - **Duration** — in minutes (optional)
4. Adds participants one at a time:
   - Types an alias; HTMX typeahead suggests matching players.
   - Selects or creates a new player.
   - Enters score (optional), checks "Winner" checkbox, and gives the game a rating out of 10 (optional).
   - Clicks "Add Player" — the participant row appears below via HTMX without a page reload.
5. Clicks "Save Play".
6. Server creates a `play` record and one `play_participant` row per player.
7. Redirect to the dashboard with a success flash message.

**Validation:**
- At least one participant required.
- Only one winner allowed (enforced client-side via JS, validated server-side too).
- Rating must be 1–10 if provided.

---

### 6. Player Management

**Entry point:** `/players`

**List view:**
- Table of all players (alias, total plays, total wins).
- "Add Player" button opens an inline form via HTMX.

**Add player flow:**
1. Librarian fills in alias (required).
2. Submits; new player row appears in the table via HTMX.

**Player detail (`/players/<id>`):**
- Full play history: date, game, score, won?, rating given.
- Win rate and total play count.

---

### 7. Game Catalog

**Entry point:** `/games`

**List view:**
- All board game titles (name, publisher, player count range, play time range, avg rating).
- Expandable rows showing each physical copy (condition, status, shelf location, notes).
- Filter by expansion vs. base game.

**Game detail (`/games/<id>`):**
- Full metadata for the title.
- List of all copies with current status.
- Play history for that title.

**Add game (MVP: manual entry):**
- Form to enter all `board_game` fields manually.
- "Is expansion?" checkbox — when checked, a base game search field appears.
- Librarian types a game name into the search field; HTMX calls `GET /games/search?q=` and shows matching titles as a dropdown.
- Librarian selects a title from the dropdown; its `id` is stored in a hidden `base_game_id` field.
- On submit, `base_game_id` is saved. The librarian never sees or types a raw ID.
- Stretch: auto-fill from BGG API by entering a BGG ID.

---

### 8. Flag for Maintenance

**Triggered from:** Scan result card (any status)

**Action button:** "Flag Maintenance"

**Flow:**
1. Librarian scans game; result card shows "Flag Maintenance" button.
2. Clicking it reveals a short text input for a condition note (e.g., "Missing 3 cards").
3. HTMX posts to `POST /copies/<id>/maintenance`.
4. Server sets `availability_status = 'Maintenance'` and saves the note to the `notes` field.
5. Result card updates — status badge turns red.

---

## Non-Goals (MVP)

- User authentication / login
- Multi-user or multi-device concurrency
- BGG API auto-import (stretch goal)
- Mobile-optimized layout (laptop-only for MVP)
- Email or notification system
- Game reservation / waitlist
