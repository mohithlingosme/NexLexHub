# Deployment Guide

- Use the provided `Dockerfile` and `docker-compose.yml` for local or staging deployments.
- Run Alembic migrations before booting the API.
- Set production-grade API keys and CORS origins through environment variables.
- Place the API behind a reverse proxy and terminate TLS there.
- Run the Celery worker separately for ingestion and compliance jobs.
