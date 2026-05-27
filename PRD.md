# Product Requirements Document

## Overview

A server-side rendered web application for managing a board game lending library at a convention. A librarian operates the app on a laptop. A USB barcode scanner (keyboard emulator) is the primary input device for identifying physical game copies. Games never leave the library building.

---

## Users

| Role | Description |
|---|---|
| Librarian | Convention staff who checks games in/out and logs play sessions |
| (No login required) | Single-operator tool; no authentication for MVP |

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
3. HTMX posts the UPC to `POST /scan`; the server looks up the `game_copy` by `factory_upc`.
4. A result card replaces the placeholder below the input — no full page reload.
5. The result card shows:
   - Game title and cover info (publisher, player count, play time)
   - Current status badge
   - Copy condition and shelf location
   - Context-appropriate action buttons (see flows 3 and 4 below)
6. The input field is cleared and re-focused for the next scan.

**Error states:**
- UPC not found → "Unknown barcode. Is this game in the catalog?" with a link to add it.
- Scanner inputs a malformed string → "Invalid barcode format."

---

### 3. Check Out — Mark a Game as In Play

**Triggered from:** Scan result card when status is **Available**

**Action button:** "Mark In Play"

**Flow:**
1. Librarian scans game; result card shows Available status and "Mark In Play" button.
2. Librarian clicks button (or it could be a second scan confirm — keep it simple for MVP).
3. HTMX posts to `POST /copies/<id>/checkout`.
4. Server sets `availability_status = 'In Play'`.
5. Result card updates in place — status badge changes to yellow, button changes to "Return to Shelf".

**Guard:** If status is already In Play or Maintenance, the "Mark In Play" button is not shown. Instead, a warning message is displayed ("Already checked out" or "In maintenance — see librarian").

---

### 4. Check In — Return a Game to the Shelf

**Triggered from:** Scan result card when status is **In Play**

**Action button:** "Return to Shelf"

**Flow:**
1. Librarian scans game; result card shows In Play status and "Return to Shelf" button.
2. Librarian clicks button.
3. HTMX posts to `POST /copies/<id>/checkin`.
4. Server sets `availability_status = 'Available'`.
5. Result card updates — status badge changes to green.

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
   - Types a player name or alias; HTMX typeahead suggests matching players.
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
- Table of all players (name, alias, total plays, total wins).
- "Add Player" button opens an inline form via HTMX.

**Add player flow:**
1. Librarian fills in name (required) and alias (optional).
2. Submits; new player row appears in the table via HTMX.

**Player detail (`/players/<id>`):**
- Full play history: date, game, score, won?, rating given.
- Win rate and total play count.

---

### 7. Game Catalog

**Entry point:** `/games`

**List view:**
- All board game titles (name, publisher, player count range, play time range, avg rating).
- Expandable rows showing each physical copy (UPC, condition, status, shelf location).
- Filter by expansion vs. base game.

**Game detail (`/games/<id>`):**
- Full metadata for the title.
- List of all copies with current status.
- Play history for that title.

**Add game (MVP: manual entry):**
- Form to enter all `board_game` fields manually.
- Stretch: auto-fill from BGG API by entering a BGG ID.

---

### 8. Flag for Maintenance

**Triggered from:** Scan result card (any status)

**Action button:** "Flag Maintenance"

**Flow:**
1. Librarian scans game; result card shows "Flag Maintenance" button.
2. Clicking it reveals a short text input for a condition note (e.g., "Missing 3 cards").
3. HTMX posts to `POST /copies/<id>/maintenance`.
4. Server sets `availability_status = 'Maintenance'` and updates `condition` with the note.
5. Result card updates — status badge turns red.

---

## Non-Goals (MVP)

- User authentication / login
- Multi-user or multi-device concurrency
- BGG API auto-import (stretch goal)
- Mobile-optimized layout (laptop-only for MVP)
- Email or notification system
- Game reservation / waitlist
