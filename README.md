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
=======
# ⚖️ Legal Intelligence Platform

A full-stack **Legal-Tech Knowledge Platform** combining structured legal data, research publishing, and a scalable AI-ready architecture.

This platform enables users to explore **Bare Acts, Case Laws, Articles, Whitepapers, and Legal News**, while providing a **controlled publishing system** for verified contributors and a **future-ready AI (RAG) layer**.

---

## 🚀 Features

### 📚 Core Content Modules

* **Bare Acts**

  * Chapter-wise and section-wise navigation
  * Collapsible sidebar UI
  * Section-level explanations (Law Review)
  * Download full Bare Act PDF

* **Case Laws**

  * Structured summaries (Facts, Issues, Held, Principles)
  * Judgment PDF download
  * Linked to relevant sections and topics

* **Articles / Insights**

  * Short-form legal and business analysis
  * Tagged and categorized

* **Whitepapers**

  * Research-based content
  * Downloadable PDF format

* **Legal News**

  * Latest updates in law and policy
  * Categorized by legal domain

---

### ⚖️ Law Review System (Key Feature)

* Section-wise explanation of laws
* Includes:

  * Bare provision text
  * Simplified explanation
  * Related case laws
  * Related articles

---

### 🔎 Advanced Search & Filtering

* Filter by:

  * Content type (Article, Case Law, Bare Act, Whitepaper, News, Law Review)
  * Legal category (Criminal, Corporate, Tech Law, etc.)
  * Tags

---

### 🔐 Contributor System (Invite-Only)

* Application-based onboarding
* Legal knowledge screening
* Writing skill evaluation
* Admin approval + invite system

---

### 🛠 Admin Panel (CMS)

* Dashboard with platform stats
* Content management (all types)
* Approval workflow (Draft → Pending → Published)
* Application review system
* User management
* File/PDF management

---

### ✍️ Editor Panel

* Rich text editor
* Create and submit content
* Upload PDFs (judgments, whitepapers, bare acts)
* Tagging and categorization

---

### 📂 PDF Upload System

* Upload and manage:

  * Bare Act PDFs
  * Case law judgments
  * Whitepapers
* Secure file storage

---

### 🤖 AI-Ready Architecture (RAG)

* Python microservice prepared for:

  * Embeddings
  * Document retrieval
  * AI-powered legal query system

---

## 🧱 Tech Stack

### Frontend

* HTML
* CSS
* Vanilla JavaScript

### Backend

* PHP (REST API for CRUD operations)
* MySQL (Relational database)

### AI / Processing Layer

* Python (Flask / FastAPI)

---

## 🗂 Project Structure

```
/frontend          # UI (HTML, CSS, JS)
/backend-php       # PHP APIs (CRUD, Auth, Uploads)
/python-service    # AI processing service
/uploads           # PDF storage
/database          # SQL schema
```

## Folder Structure 
NexLexHub
├── assets/                     # Shared static resources (Logos, Icons, Global CSS)
│   ├── css/
│   ├── img/
│   └── fonts/
├── backend-php/                # PHP REST API
│   ├── config/                 # Database & App configurations
│   │   └── database.php
│   ├── src/                    # Core logic
│   │   ├── Auth/               # Login, Register, JWT/Session logic
│   │   ├── Controllers/        # PostController, UserController, ActController
│   │   ├── Models/             # Database queries (Posts, Sections, Cases)
│   │   └── Utils/              # PDF Parsers, Helpers, Response formatters
│   ├── public/                 # API Entry point
│   │   └── index.php           # Slim or custom router
│   └── .htaccess               # URL rewriting for clean APIs
├── database/                   # SQL scripts and migrations
│   ├── schema.sql
│   └── seed_data.sql           # Initial Bare Acts / Categories
├── frontend/                   # Client-side (Vanilla JS)
│   ├── admin/                  # Admin Dashboard UI
│   ├── editor/                 # Editor/Contributor UI
│   ├── public/                 # Public Reader UI (Landing, Acts, Articles)
│   │   ├── assets/             # Page-specific JS/CSS
│   │   └── index.html
│   └── components/             # Reusable UI fragments (Header, Sidebar)
├── python-service/             # AI / RAG Microservice
│   ├── app/
│   │   ├── api/                # FastAPI/Flask routes
│   │   ├── core/               # RAG logic (LangChain/LlamaIndex)
│   │   ├── embeddings/         # Logic to convert text to vectors
│   │   └── scripts/            # Background tasks for PDF OCR/Indexing
│   ├── main.py                 # Entry point
│   └── requirements.txt
├── storage/                    # Centralized File Storage
│   ├── bare_acts/              # Sourced PDF files
│   ├── case_laws/
│   ├── whitepapers/
│   └── uploads/                # Temporary/User-submitted files
├── tests/                      # Unit and Integration tests
├── .env                        # Environment variables (DB_PASS, AI_API_KEY)
├── .gitignore
└── README.md

## 🧠 Database Overview

Key tables include:

* Users, Applications, Invites
* Posts (unified content system)
* Acts, Chapters, Sections
* SectionAnalysis, SectionRelations
* CaseLawMeta, WhitepaperMeta, NewsMeta
* LegalCategories, Tags
* Files

---

## ⚙️ Setup Instructions

### 1. Clone Repository

```
git clone <your-repo-url>
cd legal-intelligence-platform
```

---

### 2. Setup Database

* Import SQL file from `/database`
* Configure MySQL credentials in PHP backend

---

### 3. Run PHP Server

```
php -S localhost:8000 -t backend-php
```

---

### 4. Run Frontend

* Open `/frontend/index.html` in browser
  OR serve via local server

---

### 5. Run Python Service

```
cd python-service
pip install -r requirements.txt
python app.py
```

---

## 🔐 Authentication & Roles

* **Admin**

  * Full access
  * Approve content and users

* **Editor**

  * Create and submit content
  * Cannot publish directly

* **Public User**

  * Read-only access

---

## 🔄 Workflow

1. User applies as contributor
2. Admin reviews application
3. Approved users receive invite link
4. User signs up as Editor
5. Editor submits content
6. Admin approves → content published

---

## 🎯 Roadmap

* [ ] Advanced UI/UX improvements
* [ ] Full-text search optimization
* [ ] RAG-based AI legal assistant
* [ ] Bookmarking & user personalization
* [ ] API integrations (legal databases)

---

## ⚠️ Disclaimer

* Bare Acts and judgments are sourced from public domain materials.
* Always verify legal information before professional use.

---

## 🤝 Contribution

This platform uses a **curated contributor model**.
To contribute, apply through the website.

---

## 📬 Contact

For collaboration, consulting, or inquiries:

* Email: [your-email@example.com](mailto:your-email@example.com)
* LinkedIn: your-linkedin

---

## 🧠 Vision

To build a **modern legal intelligence system** that combines:

* Structured legal knowledge
* Research-driven insights
* AI-powered legal assistance

---

⭐ If you find this project useful, consider starring the repository!
>>>>>>> 6a0c154 (Agent_J)
