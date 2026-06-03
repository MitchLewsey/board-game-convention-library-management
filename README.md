# Board Game Convention Library

A server-side rendered web app for managing a board game lending library at a convention. A librarian operates it on a laptop with a USB barcode scanner. Games never leave the library.

## Stack

- **Flask** — web framework
- **Flask-SQLAlchemy + Flask-Migrate** — ORM and migrations
- **PostgreSQL** — database
- **Jinja2** — templating
- **HTMX** — partial page updates (barcode scanner flow)
- **Tailwind CSS Play CDN** — styling (no build step)

## Architecture

Each model and repository has its own file in `lib/`:
- Models: `board_game.py`, `game_copy.py`, `player.py`, `play.py`, `play_participant.py`
- Repositories: `board_game_repository.py`, `game_copy_repository.py`, `player_repository.py`, `play_repository.py`, `play_participant_repository.py`

Routes instantiate repository classes and call their methods — never `db.session` directly. Repositories are instance-based: `BoardGameRepository().all()`. This keeps routes thin and makes queries mockable in tests.

See `ARCHITECTURE.md` for the full schema, project structure, and conventions.
See `PRD.md` for user flows and requirements.
See `TODO.md` for the build checklist.

## Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file at the project root:
   ```
   DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/boardgame_library
   TEST_DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/boardgame_library_test
   SECRET_KEY=your-secret-key
   ```

4. Create the databases:
   ```bash
   psql -U postgres -c "CREATE DATABASE boardgame_library;"
   psql -U postgres -c "CREATE DATABASE boardgame_library_test;"
   ```

5. Run migrations:
   ```bash
   flask db upgrade
   ```

6. Seed sample data:
   ```bash
   psql -h 127.0.0.1 boardgame_library < seeds/seeds_board_game.sql
   psql -h 127.0.0.1 boardgame_library < seeds/seeds_game_copy.sql
   psql -h 127.0.0.1 boardgame_library < seeds/seeds_player.sql
   ```

7. Start the development server:
   ```bash
   flask run
   ```

## Testing

```bash
pytest tests/ -v
```

Tests use a separate test database (`TEST_DATABASE_URL`). Route tests mock repository methods so they don't require database access.
