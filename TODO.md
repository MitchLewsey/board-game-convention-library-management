# TODO — Board Game Library MVP

Work through phases in order. Write tests before implementation. Mark items done as you go.

---

## Phase 0 — Environment Setup

- [ ] Create `requirements.txt` with: Flask, Flask-SQLAlchemy, Flask-Migrate, psycopg2-binary, python-dotenv, pytest, pytest-flask
- [ ] Create `.env` with `DATABASE_URL`, `TEST_DATABASE_URL`, and `SECRET_KEY`
- [ ] Create the PostgreSQL database and a separate test database
- [ ] Set up a Python virtual environment and install requirements

---

## Phase 1 — Database Layer

- [ ] Write `lib/db.py` — create the SQLAlchemy instance (`db = SQLAlchemy()`)
- [ ] Write `lib/models.py` — define ORM models for all 5 tables:
  - `BoardGame` (with `factory_upc` unique)
  - `GameCopy` (with `AvailabilityStatus` and `CopyCondition` enums)
  - `Player`
  - `Play` (`start_time`, `end_time`, `duration_minutes` — no `date_played`)
  - `PlayParticipant`
- [ ] Wire up Flask app factory in `app.py` (init db, register Flask-Migrate)
- [ ] Run `flask db init`, `flask db migrate`, `flask db upgrade` to create tables
- [ ] Write `tests/conftest.py`:
  - App fixture using `TEST_DATABASE_URL`
  - DB fixture that creates and tears down tables per test
  - Session fixture for inserting test data
- [ ] Write `tests/test_models.py` — one test per constraint:
  - `BoardGame.factory_upc` is unique
  - `BoardGame.base_game_id` self-referential FK (expansion points to base game)
  - `GameCopy.availability_status` rejects values outside the enum
  - `GameCopy.condition` rejects values outside the enum
  - `Play.start_time` defaults to now; `end_time` is nullable
  - `PlayParticipant` composite PK prevents duplicate player per play
  - `PlayParticipant.rating` CHECK rejects values outside 1–10
- [ ] Run tests — all model tests pass
- [ ] Write `seeds/seed.py` with ~10 sample games, ~5 players, and game copies
- [ ] Run seed script and verify data in psql

---

## Phase 2 — Core Routes & Templates

- [ ] Write `templates/base.html`:
  - Tailwind Play CDN `<script>` tag
  - HTMX `<script>` tag
  - Top navigation bar (Dashboard, Scan, Log Play, Games, Players)
  - Flash message block

- [ ] Write tests for dashboard (`tests/test_routes.py`):
  - `GET /` returns 200
  - Response contains copy status summary counts
- [ ] Implement dashboard route + template (`GET /`):
  - Returns all `GameCopy` rows joined to `BoardGame`
  - Shows status summary counts and filterable copy table

- [ ] Write tests for scan page:
  - `GET /scan` returns 200
  - Response contains a UPC input field
- [ ] Implement scan page (`GET /scan`):
  - Template with auto-focused UPC input and empty result div

- [ ] Write tests for scan lookup:
  - `POST /scan` with known UPC returns game title in partial
  - `POST /scan` with unknown UPC returns error message
  - `POST /scan` with no available copies returns "all copies in play" message
- [ ] Implement scan lookup (`POST /scan`):
  - Queries `BoardGame` by `factory_upc`, counts available copies
  - Returns `partials/scan_result.html` (no base layout when `HX-Request` header present)

- [ ] Write tests for check-out:
  - `POST /games/<id>/checkout` with valid alias creates a `Play` and `PlayParticipant`
  - Sets one `GameCopy` to `In Play`
  - Unknown alias creates a new `Player` record
- [ ] Implement check-out alias input partial and route (`POST /games/<id>/checkout`):
  - HTMX swaps in alias text input
  - On submit: find/create player, create `Play` (start_time=NOW()), create `PlayParticipant`, set copy to `In Play`
  - Returns updated `partials/scan_result.html`

- [ ] Write tests for check-in:
  - `POST /games/<id>/checkin` with valid alias sets `play.end_time`, stores `duration_minutes`, sets copy to `Available`
  - Alias selector only shows players with an open play (`end_time IS NULL`) for this game
- [ ] Implement check-in alias selector partial and route (`POST /games/<id>/checkin`):
  - HTMX swaps in alias selector (players with open plays for this game)
  - On submit: set `end_time=NOW()`, calculate and store `duration_minutes`, set copy to `Available`
  - Returns updated `partials/scan_result.html`

- [ ] Run all tests — Phase 2 passes

---

## Phase 3 — Play Logging (Detailed)

- [ ] Write tests for player search:
  - `GET /players/search?q=ali` returns matching players as HTML partial
  - Empty query returns no results
- [ ] Implement player search (`GET /players/search?q=`):
  - Returns `partials/player_row.html` with matching players

- [ ] Write tests for log play page:
  - `GET /plays/new` returns 200
  - `GET /plays/new` with `?game_id=` pre-selects the game
- [ ] Implement log play page (`GET /plays/new`):
  - Game selector (dropdown or scan input), duration field
  - Participant section with Add Player form

- [ ] Write tests for save play:
  - `POST /plays` with valid data creates `Play` and one `PlayParticipant` per participant
  - Rejects submission with zero participants
  - Rejects submission with more than one winner
  - Rejects rating outside 1–10
- [ ] Implement save play route (`POST /plays`):
  - Creates `Play` and `PlayParticipant` records
  - Validates at least one participant; only one winner
  - Redirects to `/` with flash success message

- [ ] Run all tests — Phase 3 passes

---

## Phase 4 — Player & Catalog Management

- [ ] Write tests for player routes:
  - `GET /players` returns 200, lists all players
  - `POST /players` with valid data creates player, returns row partial
  - `GET /players/<id>` returns play history and win count
- [ ] Implement player routes + templates:
  - Players list with inline Add Player form (HTMX)
  - Player detail with play history

- [ ] Write tests for game catalog routes:
  - `GET /games` returns 200, lists all titles
  - `GET /games/<id>` returns game metadata, copies, and play history
  - `POST /games` with valid data creates a `BoardGame` record
- [ ] Implement game catalog routes + templates:
  - Catalog with expandable copy rows, expansion filter
  - Game detail page
  - Add game form (manual entry)

- [ ] Write tests for maintenance flag:
  - `POST /copies/<id>/maintenance` sets `availability_status = Maintenance` and saves `notes`
  - Returns updated scan result partial
- [ ] Implement maintenance flag route (`POST /copies/<id>/maintenance`)

- [ ] Run all tests — Phase 4 passes

---

## Phase 5 — Polish & Hardening

- [ ] Write tests for validation edge cases:
  - POST routes with missing required fields return errors, not 500s
  - Scan with malformed UPC returns "Invalid barcode format"
- [ ] Add server-side input validation and flash error messages to all POST routes
- [ ] Add 404 handler for unknown UPC scans
- [ ] Review and fix any N+1 query issues (use `.joinedload()` where needed)
- [ ] Responsive layout pass for laptop screen (1080p+)
- [ ] Final manual walkthrough of all PRD flows
- [ ] Run full test suite — all tests pass

---

## Stretch Goals (post-MVP)

- [ ] BGG API auto-fill game metadata by BGG ID
- [ ] Export play log to CSV
- [ ] Per-game play stats page (most popular titles, avg duration)
- [ ] Bulk import game copies from a CSV of UPCs
