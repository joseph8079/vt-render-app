# Vision Therapy Ops (Render-ready) — Monorepo

A turnkey **Django + DRF** backend + **React (Vite)** frontend for a Vision Therapy department.

## Included
- Pipeline (no-drop statuses) + communication log
- Clinical review + program goals
- Slot templates (recurring pair) + slot assignment
- Program auto-generates **22 sessions** (2/week, **30 min** each)
- Therapist notes (stored internally) + basic outcome signals
- Dashboards (executive / ops / therapist)

Defaults:
- **2 sessions per week**
- **30 minutes** each
- **22 sessions total** (~11 weeks)

---

## Local Quickstart

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo
python manage.py runserver 0.0.0.0:8000
```

### Frontend
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Frontend: http://localhost:5173  
Backend: http://localhost:8000  
API: http://localhost:8000/api/

Demo users after seeding (password: `password`):
- `vt_manager`, `intake`, `reviewer`, `therapist_m1`, `therapist_f1`

---

## Render Deploy

Push this repo to GitHub, then in Render use **Blueprint** with `render.yaml`.

