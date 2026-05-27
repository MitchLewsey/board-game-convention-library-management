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
