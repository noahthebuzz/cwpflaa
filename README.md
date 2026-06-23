# Daily Puzzle Platform

A daily puzzle website featuring Wordle, Sudoku, and Schwedenrätsel (Crossword).

## Tech Stack
- **Frontend**: Next.js 14+ (App Router), React, Tailwind CSS
- **Backend**: Python 3.11+, FastAPI
- **Database**: PostgreSQL 15+
- **Auth**: JWT with HttpOnly Cookie refresh tokens
- **Infrastructure**: Docker Compose, Nginx

## Quick Start

1. Clone the repository
2. Copy and configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your values
   ```
3. Start all services:
   ```bash
   docker compose up --build
   ```
4. Access the app at http://localhost:80

## Services
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Nginx**: http://localhost:80

## Development (without Docker)

### Backend
```bash
cd backend
pip install -r requirements.txt
# Set DATABASE_URL to a local PostgreSQL instance
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Database Migrations
```bash
cd backend
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## Seeding Puzzles
```bash
cd backend
python scripts/seed_wordle.py
python scripts/seed_sudoku.py
```
