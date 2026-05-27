# TODO — Board Game Library MVP

Work through phases in order. Mark items done as you go.

---

## Phase 0 — Environment Setup

- [ ] Create `requirements.txt` with: Flask, Flask-SQLAlchemy, Flask-Migrate, psycopg2-binary, python-dotenv
- [ ] Create `.env` with `DATABASE_URL` and `SECRET_KEY` (add `.env` to `.gitignore`)
- [ ] Create the PostgreSQL database
- [ ] Set up a Python virtual environment and install requirements

---

## Phase 1 — Database Layer

- [ ] Write `lib/db.py` — create the SQLAlchemy instance (`db = SQLAlchemy()`)
- [ ] Write `lib/models.py` — define ORM models for all 5 tables:
  - `BoardGame`
  - `GameCopy` (with `AvailabilityStatus` enum)
  - `Player`
  - `Play`
  - `PlayParticipant`
- [ ] Wire up Flask app factory in `app.py` (init db, register Flask-Migrate)
- [ ] Run `flask db init`, `flask db migrate`, `flask db upgrade` to create tables
- [ ] Write `seeds/seed.py` with ~10 sample games, ~5 players, and a few game copies with UPCs
- [ ] Run seed script and verify data in psql

---

## Phase 2 — Core Routes & Templates

- [ ] Write `templates/base.html`:
  - Tailwind Play CDN `<script>` tag
  - HTMX `<script>` tag
  - Top navigation bar (Dashboard, Scan, Log Play, Games, Players)
  - Flash message block
- [ ] Dashboard (`GET /`):
  - Route returns all `GameCopy` rows joined to `BoardGame`
  - Template shows status summary counts and filterable copy table
- [ ] Scan page (`GET /scan`):
  - Template with auto-focused UPC input and empty result div
- [ ] Scan lookup (`POST /scan`):
  - Queries `GameCopy` by `factory_upc`
  - Returns `partials/scan_result.html` partial (no base layout)
  - Partial shows game info, status badge, and action buttons
- [ ] Check-out route (`POST /copies/<id>/checkout`):
  - Sets `availability_status = 'In Play'`
  - Returns updated `partials/scan_result.html`
- [ ] Check-in route (`POST /copies/<id>/checkin`):
  - Sets `availability_status = 'Available'`
  - Returns updated `partials/scan_result.html`

---

## Phase 3 — Play Logging

- [ ] Log play page (`GET /plays/new`):
  - Game selector (dropdown or scan input)
  - Date field (default today) and duration field
  - Participant section with Add Player form
- [ ] Player typeahead partial (`GET /players/search?q=`):
  - Returns `partials/player_row.html` with matching players
  - Used by HTMX on keyup in the player name field
- [ ] Add participant partial (`POST /plays/participants/add`):
  - Returns `partials/participant_row.html` appended to the participant list
  - Includes score, winner checkbox, rating (1–10)
- [ ] Save play route (`POST /plays`):
  - Creates `Play` record
  - Creates one `PlayParticipant` per participant
  - Validates at least one participant; only one winner
  - Redirects to `/` with flash success message

---

## Phase 4 — Player & Catalog Management

- [ ] Players list (`GET /players`):
  - Table of all players with total play count and wins
  - Inline "Add Player" form via HTMX
- [ ] Add player route (`POST /players`):
  - Creates player, returns new player row partial
- [ ] Player detail (`GET /players/<id>`):
  - Full play history, win rate, total plays
- [ ] Game catalog (`GET /games`):
  - All titles with expandable copy rows
  - Filter toggle: base games / expansions
- [ ] Game detail (`GET /games/<id>`):
  - Full metadata, copies with status, play history
- [ ] Add game form (`GET /games/new`, `POST /games`):
  - Manual entry form for all `board_game` fields
- [ ] Maintenance flag route (`POST /copies/<id>/maintenance`):
  - Sets status to 'Maintenance', updates condition field with note
  - Returns updated scan result partial

---

## Phase 5 — Polish & Hardening

- [ ] Server-side input validation on all POST routes; flash error messages on failure
- [ ] 404 handler for unknown UPC scans
- [ ] Responsive layout pass for laptop screen (1080p+)
- [ ] Write tests:
  - `tests/test_models.py` — model integrity (FK constraints, enum values)
  - `tests/test_routes.py` — scan route happy path and unknown UPC
- [ ] Review and clean up any N+1 query issues (use `.joinedload()` where needed)
- [ ] Final manual walkthrough of all 8 PRD flows

---

## Stretch Goals (post-MVP)

- [ ] BGG API auto-fill game metadata by BGG ID
- [ ] Export play log to CSV
- [ ] Per-game play stats page (most popular titles, avg duration)
- [ ] Bulk import game copies from a CSV of UPCs
