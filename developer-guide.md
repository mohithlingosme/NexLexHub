# Developer Guide

- Runtime code lives in `src/nexlexhub`.
- Database changes must ship through `alembic/versions`.
- Legacy scraper entrypoints under `Pharse_1/` are compatibility wrappers and should delegate into `src/nexlexhub/scrapers`.
- Use `pytest`, `ruff check .`, and `mypy src` before shipping changes.
