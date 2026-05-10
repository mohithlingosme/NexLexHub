# Deployment Guide

## Containers

- `postgres`: `pgvector/pgvector:pg16`
- `redis`: `redis:7`
- `api`: Python 3.11 image from `Dockerfile`
- `worker`: Celery worker using the same image

## Boot sequence

1. Provision Postgres and Redis.
2. Run `alembic upgrade head`.
3. Start the API container.
4. Start Celery workers.
5. Deploy the Next.js frontend separately or behind the same reverse proxy.

## Required configuration

- `NEXLEXHUB_DATABASE_URL`
- `NEXLEXHUB_SYNC_DATABASE_URL`
- `NEXLEXHUB_REDIS_URL`
- `NEXLEXHUB_ALLOWED_KEYS`
- `NEXLEXHUB_JWT_SECRET`
- `NEXLEXHUB_CORS_ORIGINS`

## Production notes

- Replace demo secrets and API keys.
- Put the API behind TLS termination.
- Run the frontend with `NEXT_PUBLIC_API_URL` pointing to the API origin.
- Disable demo seeding outside non-production environments.
- Use Postgres for all deployed environments; the SQLite path exists only to support automated tests.
