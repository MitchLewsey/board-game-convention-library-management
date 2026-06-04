# Architecture

## Tech Stack

| Layer | Technology |
|---|---|
| Web framework | Flask |
| ORM | Flask-SQLAlchemy + Flask-Migrate |
| DB driver | psycopg2-binary |
| Templating | Jinja2 (Flask built-in) |
| CSS | Tailwind CSS Play CDN (no build step) |
| Interactivity | HTMX |
| Database | PostgreSQL |

---

## Project Structure

```
boardgame-convention-library-management/
├── app.py                  # App factory, route registration
├── requirements.txt
├── .env                    # DATABASE_URL, SECRET_KEY (never commit)
├── ARCHITECTURE.md
├── PRD.md
├── TODO.md
├── CLAUDE.md
├── lib/
│   ├── db.py                       # SQLAlchemy instance
│   ├── board_game.py               # BoardGame ORM model
│   ├── game_copy.py                # GameCopy ORM model
│   ├── player.py                   # Player ORM model
│   ├── play.py                     # Play ORM model
│   ├── play_participant.py         # PlayParticipant ORM model
│   ├── board_game_repository.py    # BoardGameRepository
│   ├── game_copy_repository.py     # GameCopyRepository
│   ├── player_repository.py        # PlayerRepository
│   ├── play_repository.py          # PlayRepository
│   └── play_participant_repository.py  # PlayParticipantRepository
├── templates/
│   ├── base.html           # Shared layout (Tailwind CDN, HTMX, nav)
│   ├── dashboard.html      # Inventory overview
│   ├── scan.html           # Barcode scan page
│   ├── games/
│   │   ├── index.html      # Game catalog
│   │   └── detail.html     # Single title with copies
│   ├── plays/
│   │   └── new.html        # Log a play session
│   ├── players/
│   │   ├── index.html      # Player list
│   │   └── detail.html     # Player history
│   └── partials/           # HTMX partial responses (no base layout)
│       ├── scan_result.html
│       ├── player_row.html
│       └── participant_row.html
├── static/                 # Minimal static assets
├── seeds/
│   ├── seeds_board_game.sql
│   ├── seeds_game_copy.sql
│   └── seeds_player.sql
└── tests/
```

---

## Database Schema

### PostgreSQL Types

```sql
CREATE TYPE availability_status AS ENUM ('Available', 'In Play', 'Maintenance');
CREATE TYPE copy_condition AS ENUM ('Excellent', 'Good', 'Fair', 'Poor');
```

### Tables

```sql
CREATE TABLE board_game (
    id              SERIAL          PRIMARY KEY,
    name            VARCHAR(255)    NOT NULL,
    bgg_id          INTEGER,                        -- BoardGameGeek ID
    factory_upc     VARCHAR(20)     UNIQUE,         -- scanned by barcode reader to identify title
    min_players     SMALLINT,
    max_players     SMALLINT,
    min_time        SMALLINT,                       -- minutes
    max_time        SMALLINT,                       -- minutes
    publisher       VARCHAR(255),
    designer        VARCHAR(255),
    artist          VARCHAR(255),
    is_expansion    BOOLEAN         NOT NULL DEFAULT FALSE,
    base_game_id    INTEGER         REFERENCES board_game(id) ON DELETE SET NULL
);

CREATE TABLE game_copy (
    id                  SERIAL              PRIMARY KEY,
    board_game_id       INTEGER             NOT NULL REFERENCES board_game(id) ON DELETE CASCADE,
    availability_status availability_status NOT NULL DEFAULT 'Available',
    condition           copy_condition,
    notes               TEXT,
    shelf_location      VARCHAR(50)
);

CREATE TABLE player (
    id      SERIAL          PRIMARY KEY,
    name    VARCHAR(255)    NOT NULL,
    alias   VARCHAR(100)
);

CREATE TABLE play (
    id                SERIAL      PRIMARY KEY,
    board_game_id     INTEGER     NOT NULL REFERENCES board_game(id) ON DELETE RESTRICT,
    start_time        TIMESTAMP   NOT NULL DEFAULT NOW(),
    end_time          TIMESTAMP,
    duration_minutes  SMALLINT    -- stored on check-in: EXTRACT(EPOCH FROM (end_time - start_time)) / 60
);

CREATE TABLE play_participant (
    play_id     INTEGER         NOT NULL REFERENCES play(id) ON DELETE CASCADE,
    player_id   INTEGER         NOT NULL REFERENCES player(id) ON DELETE RESTRICT,
    is_winner   BOOLEAN         NOT NULL DEFAULT FALSE,
    rating      SMALLINT        CHECK (rating BETWEEN 1 AND 10),
    PRIMARY KEY (play_id, player_id)
);
```

### Relationship Notes

- `board_game.base_game_id` is a self-referential FK — expansions point to their base game.
- `board_game.factory_upc` is the value the barcode scanner reads. It identifies the game *title*, not an individual copy. `UNIQUE` here is correct — one UPC per edition.
- `game_copy` has no barcode; copies are distinguished only by their `id` and status. Scanning resolves to a title, then the system picks any available copy.
- `play_participant` uses a composite PK — a player can appear at most once per play session.
- `play` references `board_game` (not `game_copy`) because we track what was played, not which physical box.
- `play.end_time IS NULL` indicates an active session. Check-in finds the open play by matching `board_game_id` and the player's alias via `play_participant`.

---

## Barcode Scanner Strategy

The USB scanner is a keyboard emulator: it rapidly sends the UPC digits followed by an Enter keypress.

**Implementation with HTMX:**

```html
<!-- scan.html -->
<input
  id="upc-input"
  name="upc"
  type="text"
  autofocus
  hx-post="/scan"
  hx-trigger="keyup[keyCode==13]"
  hx-target="#scan-result"
  hx-swap="innerHTML"
/>
<div id="scan-result"></div>
```

The `POST /scan` route queries `board_game` by `factory_upc`, then counts available `game_copy` rows for that title. It returns only the `partials/scan_result.html` fragment — no full page reload. The partial shows the game title, available copy count, and context-appropriate action buttons. If no copies are available, it shows a "No copies available" message instead. Action buttons POST to their own routes, which also return partials to update the result area.

---

## Repository Layer

Each model has its own repository file in `lib/`. Routes never call `db.session` directly — they instantiate a repository and call its methods instead. This keeps routes thin and makes queries mockable in tests.

| File | Repository | Responsibility |
|---|---|---|
| `lib/board_game_repository.py` | `BoardGameRepository` | Look up games by UPC or ID, list all, create |
| `lib/game_copy_repository.py` | `GameCopyRepository` | Count/find available or in-play copies, flag maintenance, create |
| `lib/player_repository.py` | `PlayerRepository` | Find by alias, find-or-create on check-out, list players with open plays |
| `lib/play_repository.py` | `PlayRepository` | Create on check-out, find open session, close on check-in |
| `lib/play_participant_repository.py` | `PlayParticipantRepository` | Add participant on check-out, add score/winner/rating detail |

Repositories are **instance-based** — instantiate before calling methods:

```python
repo = BoardGameRepository()
game = repo.find_by_upc(upc)
```

**Example — scan route using repositories:**

```python
from lib.board_game_repository import BoardGameRepository
from lib.game_copy_repository import GameCopyRepository

@app.route("/scan", methods=["POST"])
def scan():
    upc = request.form["upc"]
    game = BoardGameRepository().find_by_upc(upc)
    if not game:
        return render_template("partials/scan_result.html", error="Unknown barcode.")
    available = GameCopyRepository().count_available(game.id)
    total = GameCopyRepository().count_total(game.id)
    return render_template("partials/scan_result.html", game=game, available=available, total=total)
```

**Testing with mocked repositories:**

```python
from unittest.mock import patch
from lib.board_game import BoardGame

def test_scan_unknown_upc(client):
    with patch.object(BoardGameRepository, "find_by_upc", return_value=None):
        response = client.post("/scan", data={"upc": "000000000000"})
        assert b"Unknown barcode" in response.data
```

---

## Key Conventions

- All routes return full pages **or** HTMX partials. Partials omit the base layout and are identified by the `HX-Request` header (Flask: `request.headers.get('HX-Request')`).
- Routes instantiate repository classes and call their methods — never `db.session` directly.
- Each model lives in its own file (`lib/board_game.py`, `lib/player.py`, etc.).
- Each repository lives in its own file (`lib/board_game_repository.py`, `lib/player_repository.py`, etc.).
- Repositories are instance-based: `BoardGameRepository().all()`, not `BoardGameRepository.all()`.
- Status badges use Tailwind utility classes: green for Available, yellow for In Play, red for Maintenance.
- No JavaScript build step — Tailwind Play CDN and HTMX are loaded from CDN `<script>` tags in `base.html`.
- Database migrations managed via Flask-Migrate (`flask db init / migrate / upgrade`).
