# NexLexHub - Full-Stack Legal-Tech Knowledge Platform

NexLexHub is a modular starter platform with:
- **Frontend** (HTML/CSS/Vanilla JS) public website and legal navigation UI.
- **Backend** (PHP REST APIs) for CMS workflows, CRUD, filtering, and secure PDF serving.
- **Database** (MySQL schema) for unified legal content, classification, hierarchy, and applications.
- **Python service** (FastAPI) with `/analyze` endpoint prepared for future AI/RAG.

## Project Structure

```bash
/frontend
/backend-php
/python-service
/uploads
/database
```

## 1) Database Setup

1. Create MySQL database and tables:
   ```bash
   mysql -u root -p < database/schema.sql
   ```
2. Optional env overrides for PHP runtime:
   - `DB_HOST`
   - `DB_NAME`
   - `DB_USER`
   - `DB_PASS`

## 2) Run PHP Backend

From project root:

```bash
php -S localhost:8000 -t backend-php
```

API base URL: `http://localhost:8000/api`

Important endpoints:
- `GET/POST /api/posts.php`
- `GET/POST /api/acts.php`
- `GET /api/sections.php?id={sectionId}`
- `GET /api/news.php?latest=5`
- `POST/GET /api/applications.php`
- `POST/GET /api/files.php`
- `GET /api/admin.php`
- `POST/GET /api/invites.php`
- `POST /api/auth.php?action=login`
- `POST /api/auth.php?action=signup-invite`

### Role-based behavior
Use `X-Role: Admin` or `X-Role: Editor` header for protected write endpoints (placeholder auth).

## 3) Run Frontend

Serve `frontend/` with any static server.

Example:
```bash
cd frontend
python3 -m http.server 5500
```

Then open `http://localhost:5500`.

> If backend is on another port/domain, update `API_BASE` in `frontend/assets/app.js`.

## 4) Run Python AI Service

```bash
cd python-service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8100
```

Endpoints:
- `GET /health`
- `POST /analyze`

Example request:
```bash
curl -X POST http://localhost:8100/analyze \
  -H 'Content-Type: application/json' \
  -d '{"query":"Explain Section 420 IPC"}'
```

## Notes for Production Hardening
- Replace placeholder auth with JWT/session middleware.
- Add CSRF/CORS/rate limits.
- Use richer WYSIWYG editor in admin/editor panel frontend.
- Add file antivirus scanning + signed URL access.
- Add migration tooling and automated tests.
