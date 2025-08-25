# BCM Maturity Assessment Portal (BCM-MAP)

Monorepo scaffold for a React (Vite) frontend and Django REST backend implementing ISO 22301-aligned BCM maturity assessments.

## Stack
- Frontend: Vite + React + TypeScript, React Router, React Query, Chart.js
- Backend: Django 5 + DRF + SimpleJWT + drf-spectacular, SQLite (dev)
- Auth: JWT (access/refresh)

## Requirements
- Node.js 18+ (we use 22)
- Python 3.11+ (we use 3.13)

## Backend setup
```bash
cd backend
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt  # optional if you create one; otherwise skip
python manage.py migrate
python manage.py seed_roles  # creates superuser admin/admin123 once
python manage.py runserver 0.0.0.0:8000
```

API base: `http://localhost:8000/api`
- Health: `GET /api/auth/health/`
- Obtain JWT: `POST /api/auth/token/` { username, password }
- Refresh JWT: `POST /api/auth/token/refresh/` { refresh }
- Resources: `/api/domains/`, `/api/questions/`, `/api/assessments/`, `/api/responses/`, `/api/evidence/`
- Exports: `/api/auth/export/csv/`, `/api/auth/export/pdf/`
- OpenAPI: `/api/schema/`, Swagger UI `/api/docs/`

Environment variables:
- `ALLOWED_HOSTS` comma-separated
- `FRONTEND_ORIGIN` frontend origin for CORS (default http://localhost:5173)

## Frontend setup
```bash
cd frontend
npm install
npm run dev
```

Configure environment in `frontend/.env` (optional):
```
VITE_API_BASE=http://localhost:8000/api
```

## Notes
- File upload limit 10 MB; PDF/DOCX/XLSX accepted.
- Ratings are 0–5 integers; averages are computed per domain and overall.
- Roles: Admin, BCM Coordinator, Business Unit Champion, Steering Committee.