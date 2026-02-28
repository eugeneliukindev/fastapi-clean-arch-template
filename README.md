# fastapi-clean-arch-template

Production-ready FastAPI template with async SQLAlchemy, Unit of Work & Repository patterns, Pydantic v2.

## Architecture

```
src/
├── api/v1/          # Routers (HTTP layer)
├── core/            # Database, UoW, enums
├── domain/
│   ├── repositories/  # BaseRepository + concrete repos
│   └── services/      # Business logic
├── models/          # SQLAlchemy models
├── schemas/
│   ├── common/      # Shared schemas (ApiResponse, Meta, Pagination, PartialModel)
│   └── users.py     # User request/response schemas
└── config.py        # Settings via pydantic-settings
```

### Patterns

- **Unit of Work** — wraps session lifecycle, commits/rollbacks in one place
- **Repository** — generic `BaseRepository[T, C, U]` with typed CRUD via `INSERT/UPDATE/DELETE ... RETURNING`
- **`ApiResponse[T]`** — consistent response envelope with `data`, `message`, `meta` (pagination)
- **`PartialModel`** — auto-generates PATCH schemas from PUT schemas without field duplication

## Getting started

### 1. Clone & install dependencies

```bash
git clone https://github.com/your-username/fastapi-clean-arch-template
cd fastapi-clean-arch-template
uv sync
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env`:

```env
MY_APP__DB__USERNAME=postgres
MY_APP__DB__PASSWORD=postgres
MY_APP__DB__DATABASE=app
```

### 3. Start database

```bash
docker compose up -d
```

### 4. Run migrations

```bash
uv run alembic upgrade head
```

### 5. Start server

```bash
uv run src/main.py
```

API docs: http://localhost:8000/docs

## Migrations

```bash
# Create migration
uv run alembic revision --autogenerate -m "description"

# Apply
uv run alembic upgrade head

# Rollback one step
uv run alembic downgrade -1
```

## API

| Method   | Endpoint             | Description    |
|----------|----------------------|----------------|
| `GET`    | `/api/v1/users`      | List users     |
| `GET`    | `/api/v1/users/{id}` | Get user       |
| `POST`   | `/api/v1/users`      | Create user    |
| `PUT`    | `/api/v1/users/{id}` | Replace user   |
| `PATCH`  | `/api/v1/users/{id}` | Update user    |
| `DELETE` | `/api/v1/users/{id}` | Delete user    |

All responses follow the `ApiResponse[T]` envelope:

```json
{
  "data": { "id": "...", "first_name": "John", "last_name": "Doe", "status": "active", "created_at": "...", "updated_at": "..." }
}
```

List with pagination (`?page=1&per_page=20`):

```json
{
  "data": [...],
  "meta": { "total": 100, "page": 1, "per_page": 20, "total_pages": 5 }
}
```

## License

MIT
