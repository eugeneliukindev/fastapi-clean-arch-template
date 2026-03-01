# fastapi-clean-arch-template

Production-ready FastAPI template with async SQLAlchemy, Unit of Work & Repository patterns, Pydantic v2.

## Architecture

```
src/
├── api/
│   ├── exception_handlers.py  # Maps domain exceptions → HTTP responses
│   └── v1/                    # Routers (HTTP layer)
├── core/                      # Database, UoW, enums
├── domain/
│   ├── exceptions.py          # DomainException, NotFoundException, ConflictException
│   ├── repositories/          # BaseRepository + concrete repos
│   └── services/              # Business logic
├── models/                    # SQLAlchemy models
├── schemas/
│   ├── common/                # Shared schemas (ApiResponse, Meta, Pagination, PartialModel)
│   └── users.py               # User request/response schemas
└── config.py                  # Settings via pydantic-settings
```

### Patterns

- **Unit of Work** — wraps session lifecycle, commits/rollbacks in one place
- **Repository** — generic `BaseRepository[T, C, U]` with typed CRUD via `INSERT/UPDATE/DELETE ... RETURNING`
- **Domain exceptions** — services throw `NotFoundException`/`ConflictException`, handlers in the API layer map them to HTTP status codes
- **`ApiResponse[T]`** — consistent response envelope with `data`, `message`, `meta` (pagination)
- **`PartialModel`** — auto-generates PATCH schemas from PUT schemas without field duplication

## Getting started

```bash
git clone https://github.com/your-username/fastapi-clean-arch-template
cd fastapi-clean-arch-template
cp .env.example .env
```

Edit `.env`:

```env
MY_APP__DB__USERNAME=postgres
MY_APP__DB__PASSWORD=postgres
MY_APP__DB__DATABASE=app
```

```bash
just install  # install dependencies
just up       # start PostgreSQL
just migrate  # apply migrations
just dev      # start server
```

API docs: http://localhost:8000/docs

## Commands

```bash
just install              # install dependencies
just dev                  # start development server
just up                   # start Docker services
just down                 # stop Docker services
just logs                 # follow Docker logs
just migrate              # apply all pending migrations
just migration "add ..."  # create a new migration
just lint                 # run linters and formatters
just check                # lint + type checking
```

## Migrations

```bash
just migration "add users table"  # create
just migrate                      # apply
uv run alembic downgrade -1       # rollback one step
```

## API

| Method   | Endpoint             | Description  |
|----------|----------------------|--------------|
| `GET`    | `/api/v1/users`      | List users   |
| `GET`    | `/api/v1/users/{id}` | Get user     |
| `POST`   | `/api/v1/users`      | Create user  |
| `PUT`    | `/api/v1/users/{id}` | Replace user |
| `PATCH`  | `/api/v1/users/{id}` | Update user  |
| `DELETE` | `/api/v1/users/{id}` | Delete user  |

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

[MIT](LICENSE)
