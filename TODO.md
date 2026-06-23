# TODO — Board Game Library MVP

Work through phases in order. Write tests before implementation. Mark items done as you go.

---

## Phase 0 — Environment Setup

- [x] Create `requirements.txt` with: Flask, Flask-SQLAlchemy, Flask-Migrate, psycopg2-binary, python-dotenv, pytest, pytest-flask
- [x] Create `.env` with `DATABASE_URL`, `TEST_DATABASE_URL`, and `SECRET_KEY`
- [x] Create the PostgreSQL database and a separate test database
- [x] Set up a Python virtual environment and install requirements

---

## Phase 1 — Database Layer

- [x] Write `lib/db.py` — create the SQLAlchemy instance (`db = SQLAlchemy()`)
- [ ] Write one ORM model file per table in `lib/`:
  - `lib/board_game.py` — `BoardGame` (with `factory_upc` unique)
  - `lib/game_copy.py` — `GameCopy` (with `AvailabilityStatus` and `CopyCondition` enums)
  - `lib/player.py` — `Player`
  - `lib/play.py` — `Play` (`start_time`, `end_time`, `duration_minutes` — no `date_played`)
  - `lib/play_participant.py` — `PlayParticipant`
- [ ] Wire up Flask app factory in `app.py` (init db, register Flask-Migrate)
- [ ] Run `flask db init`, `flask db migrate`, `flask db upgrade` to create tables
- [x] Write `tests/conftest.py`:
  - App fixture using `TEST_DATABASE_URL`
  - DB fixture that creates and tears down tables per test
  - Session fixture for inserting test data
- [x] Write one model test file per model in `tests/`:
  - `tests/test_board_game_model.py` — constructs correctly, `factory_upc` is unique, self-referential FK (expansion → base game)
  - `tests/test_game_copy_model.py` — `availability_status` rejects values outside enum, `condition` rejects values outside enum
  - `tests/test_play_model.py` — `start_time` defaults to now, `end_time` is nullable
  - `tests/test_play_participant_model.py` — composite PK prevents duplicate player per play, `rating` CHECK rejects values outside 1–10
- [ ] Run tests — all model tests pass
- [ ] Write one repository test file per repository in `tests/`:
  - `tests/test_board_game_repository.py` — `all` returns all games, `find_by_upc` returns correct game; returns `None` for unknown UPC, `find_by_name` returns partial name matches ordered by name
  - `tests/test_game_copy_repository.py` — `count_available`, `find_available` returns copies or an empty list, `find_in_play`, `flag_maintenance` sets status and notes
  - `tests/test_player_repository.py` — `find_by_alias` returns player or `None`, `find_or_create` returns existing or creates new, `find_with_open_plays`
  - `tests/test_play_repository.py` — `create` sets `start_time` to the current time and leaves `end_time` as `None`, `find_open`, `close` sets `end_time` and `duration_minutes`
  - `tests/test_play_participant_repository.py` — `create` creates participant row, `add_detail` updates score, winner flag, and rating
- [ ] Write one repository file per model in `lib/` — implement all classes to pass the tests:
  - `lib/board_game_repository.py` — `BoardGameRepository`
  - `lib/game_copy_repository.py` — `GameCopyRepository`
  - `lib/player_repository.py` — `PlayerRepository`
  - `lib/play_repository.py` — `PlayRepository`
  - `lib/play_participant_repository.py` — `PlayParticipantRepository`
- [ ] Run tests — all repository tests pass
- [ ] Run seed files and verify data in psql:
  ```
  psql -h 127.0.0.1 boardgame_library < seeds/seeds_board_game.sql
  psql -h 127.0.0.1 boardgame_library < seeds/seeds_game_copy.sql
  psql -h 127.0.0.1 boardgame_library < seeds/seeds_player.sql
  ```

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
  - Uses `GameCopyRepository.get_all_for_game` and `BoardGameRepository.get_all`
  - Shows status summary counts and filterable copy table

- [ ] Write tests for scan page:
  - `GET /scan` returns 200
  - Response contains a UPC input field
- [ ] Implement scan page (`GET /scan`):
  - Template with auto-focused UPC input and empty result div

- [ ] Write tests for scan lookup (mock repositories):
  - `POST /scan` with known UPC returns game title in partial
  - `POST /scan` with unknown UPC returns error message
  - `POST /scan` with no available copies returns "all copies in play" message
- [ ] Implement scan lookup (`POST /scan`):
  - Uses `BoardGameRepository.find_by_upc`, `GameCopyRepository.count_available`, `GameCopyRepository.count_total`
  - Returns `partials/scan_result.html` (no base layout when `HX-Request` header present)

- [ ] Write tests for check-out (mock repositories):
  - `POST /games/<id>/checkout` with valid alias creates a `Play` and `PlayParticipant`
  - Sets one `GameCopy` to `In Play`
  - Unknown alias creates a new `Player` record via `PlayerRepository.find_or_create`
- [ ] Implement check-out alias input partial and route (`POST /games/<id>/checkout`):
  - HTMX swaps in alias text input
  - On submit: `PlayerRepository.find_or_create`, `PlayRepository.create`, `PlayParticipantRepository.create`, `GameCopyRepository.find_available` → set to `In Play`
  - Returns updated `partials/scan_result.html`

- [ ] Write tests for check-in (mock repositories):
  - `POST /games/<id>/checkin` with valid alias sets `play.end_time`, stores `duration_minutes`, sets copy to `Available`
  - Alias selector only shows players returned by `PlayerRepository.find_with_open_plays`
- [ ] Implement check-in alias selector partial and route (`POST /games/<id>/checkin`):
  - HTMX swaps in alias selector via `PlayerRepository.find_with_open_plays`
  - On submit: `PlayRepository.find_open` → `PlayRepository.close`, `GameCopyRepository.find_in_play` → set to `Available`
  - Returns updated `partials/scan_result.html`

- [ ] Run all tests — Phase 2 passes

---

## Phase 3 — Play Logging (Detailed)

- [ ] Write tests for player search:
  - `GET /players/search?q=ali` returns matching players as HTML partial
  - Empty query returns no results
- [ ] Implement player search (`GET /players/search?q=`):
  - Uses `PlayerRepository.find_by_alias` (or name search)
  - Returns `partials/player_row.html` with matching players

- [ ] Write tests for log play page:
  - `GET /plays/new` returns 200
  - `GET /plays/new` with `?game_id=` pre-selects the game
- [ ] Implement log play page (`GET /plays/new`):
  - Uses `BoardGameRepository.get_all` for game selector
  - Game selector (dropdown or scan input), duration field
  - Participant section with Add Player form

- [ ] Write tests for save play (mock repositories):
  - `POST /plays` with valid data calls `PlayRepository.create` and `PlayParticipantRepository.create` per participant
  - Rejects submission with zero participants
  - Rejects submission with more than one winner
  - Rejects rating outside 1–10
- [ ] Implement save play route (`POST /plays`):
  - Uses `PlayRepository.create`, `PlayParticipantRepository.create`, `PlayParticipantRepository.add_detail`
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
  - Uses `PlayerRepository.get_all`, `PlayerRepository.create`, `PlayerRepository.get_by_id`
  - Uses `PlayRepository.get_all_for_player` for player detail history
  - Players list with inline Add Player form (HTMX)
  - Player detail with play history

- [ ] Write tests for game catalog routes (mock repositories):
  - `GET /games` returns 200, lists all titles
  - `GET /games/<id>` returns game metadata, copies, and play history
  - `GET /games/search?q=` returns matching titles as HTML partial
  - `POST /games` with valid data creates a `BoardGame` record
- [ ] Implement game catalog routes + templates:
  - Uses `BoardGameRepository.get_all`, `BoardGameRepository.get_by_id`, `BoardGameRepository.create`
  - Uses `GameCopyRepository.get_all_for_game`, `PlayRepository.get_all_for_game`
  - Catalog with expandable copy rows, expansion filter
  - Game detail page
  - Add game form with "Is expansion?" checkbox and base game typeahead (`BoardGameRepository.find_by_name` → `GET /games/search?q=` partial)
  - `GET /games/search?q=` route returns `partials/game_search_result.html` for HTMX typeahead

- [ ] Write tests for maintenance flag (mock repositories):
  - `POST /copies/<id>/maintenance` calls `GameCopyRepository.flag_maintenance` with status and notes
  - Returns updated scan result partial
- [ ] Implement maintenance flag route (`POST /copies/<id>/maintenance`):
  - Uses `GameCopyRepository.flag_maintenance`

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
