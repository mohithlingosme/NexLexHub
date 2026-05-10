# Setup Guide

## Local backend

1. Copy `.env.example` to `.env`.
2. Install Python dependencies: `pip install -r requirements.txt`
3. Start infrastructure: `docker compose up -d postgres redis`
4. Run migrations: `alembic upgrade head`
5. Start the API: `uvicorn nexlexhub.api.main:app --reload`

The API auto-initializes tables and seeds demo data when `NEXLEXHUB_AUTO_INIT_DB=true` and `NEXLEXHUB_ENABLE_DEMO_SEED=true`.

## Local frontend

1. `cd frontend`
2. `npm install`
3. `npm run dev`

Optional environment variables:

- `NEXT_PUBLIC_API_URL=http://127.0.0.1:8000`
- `NEXT_PUBLIC_API_KEY=dev-api-key`

## Demo login

- Analyst: `analyst@nexlexhub.local` / `analyst123`
- Admin: `admin@nexlexhub.local` / `admin123`

## Validation

- `pytest -q`
- `python -m ruff check .`
- `cd frontend && npm run lint`
- `cd frontend && npm run build`
