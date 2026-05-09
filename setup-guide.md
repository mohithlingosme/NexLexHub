# Setup Guide

1. Copy `.env.example` to `.env`.
2. Install Python dependencies with `pip install -r requirements.txt`.
3. Start infrastructure with `docker compose up -d postgres redis`.
4. Run `alembic upgrade head`.
5. Seed demo data with `nexlexhub-seed`.
6. Start the API with `uvicorn nexlexhub.api.main:app --reload`.
7. Start the frontend with `cd frontend && npm install && npm run dev`.
