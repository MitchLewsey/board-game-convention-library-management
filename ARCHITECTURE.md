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
│   ├── db.py               # SQLAlchemy instance
│   └── models.py           # ORM models for all 5 tables
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
│   └── seed.py             # Sample games and players
└── tests/
```

---

## Database Schema

### PostgreSQL Types

```sql
CREATE TYPE availability_status AS ENUM ('Available', 'In Play', 'Maintenance');
```

### Tables

```sql
CREATE TABLE board_game (
    id              SERIAL          PRIMARY KEY,
    name            VARCHAR(255)    NOT NULL,
    bgg_id          INTEGER,                        -- BoardGameGeek ID
    min_players     SMALLINT,
    max_players     SMALLINT,
    min_time        SMALLINT,                       -- minutes
    max_time        SMALLINT,                       -- minutes
    publisher       VARCHAR(255),
    designer        VARCHAR(255),
    artist          VARCHAR(255),
    is_expansion    BOOLEAN         NOT NULL DEFAULT FALSE,
    base_game_id    INTEGER         REFERENCES board_game(id) ON DELETE SET NULL,
    avg_rating      NUMERIC(4, 2)   CHECK (avg_rating BETWEEN 0 AND 10)
);

CREATE TABLE game_copy (
    id                  SERIAL              PRIMARY KEY,
    board_game_id       INTEGER             NOT NULL REFERENCES board_game(id) ON DELETE CASCADE,
    factory_upc         VARCHAR(20)         UNIQUE,         -- scanned by barcode reader
    availability_status availability_status NOT NULL DEFAULT 'Available',
    condition           VARCHAR(50),                        -- 'Excellent', 'Good', 'Fair', 'Poor'
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
    date_played       DATE        NOT NULL DEFAULT CURRENT_DATE,
    duration_minutes  SMALLINT
);

CREATE TABLE play_participant (
    play_id     INTEGER         NOT NULL REFERENCES play(id) ON DELETE CASCADE,
    player_id   INTEGER         NOT NULL REFERENCES player(id) ON DELETE RESTRICT,
    score       NUMERIC(8, 2),
    is_winner   BOOLEAN         NOT NULL DEFAULT FALSE,
    rating      SMALLINT        CHECK (rating BETWEEN 1 AND 10),
    PRIMARY KEY (play_id, player_id)
);
```

### Relationship Notes

- `board_game.base_game_id` is a self-referential FK — expansions point to their base game.
- `game_copy.factory_upc` is the value the barcode scanner reads. It must be `UNIQUE` so a scan unambiguously identifies one physical copy.
- `play_participant` uses a composite PK — a player can appear at most once per play session.
- `play` references `board_game` (not `game_copy`) because we track what was played, not which physical box.

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

The `POST /scan` route queries `game_copy` by UPC and returns only the `partials/scan_result.html` fragment — no full page reload. Action buttons (Check Out / Return / Flag Maintenance) are rendered inside this partial and each POST to their own routes, which also return partials to update the result area.

---

## Key Conventions

- All routes return full pages **or** HTMX partials. Partials omit the base layout and are identified by the `HX-Request` header (Flask: `request.headers.get('HX-Request')`).
- Status badges use Tailwind utility classes: green for Available, yellow for In Play, red for Maintenance.
- No JavaScript build step — Tailwind Play CDN and HTMX are loaded from CDN `<script>` tags in `base.html`.
- Database migrations managed via Flask-Migrate (`flask db init / migrate / upgrade`).
