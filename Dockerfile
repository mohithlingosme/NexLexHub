FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml requirements.txt README.md ./
COPY src ./src
COPY alembic.ini ./
COPY alembic ./alembic
RUN pip install --no-cache-dir -r requirements.txt
CMD ["sh", "-c", "alembic upgrade head && uvicorn nexlexhub.api.main:app --host 0.0.0.0 --port 8000"]
