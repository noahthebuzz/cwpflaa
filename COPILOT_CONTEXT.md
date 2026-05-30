# cwpflaa – Project Context for GitHub Copilot

**cwpflaa** stands for _Cross-Word-Puzzle-Für-Lara-Und-Ayla_.  
It is a daily puzzle web app where users can solve Schwedenrätsel (Swedish-style crosswords), Wordle, and Sudoku.

---

## Goals

- One new puzzle per game type is available each day (daily system)
- Puzzles are generated automatically (no manual input required)
- Users can create an account to track their statistics
- Logged-in users can also access puzzles from previous days (archive)
- Guest users can only play today's puzzles

---

## Tech Stack

| Layer            | Technology                         |
| ---------------- | ---------------------------------- |
| Backend          | Python 3.12 + FastAPI              |
| Database         | PostgreSQL 16 (via SQLAlchemy ORM) |
| Auth             | JWT (JSON Web Tokens)              |
| Frontend         | React (with Vite)                  |
| Containerization | Docker + Docker Compose            |

---

## Project Structure

```
cwpflaa/
├── backend/
│   ├── app/
│   │   ├── main.py             # FastAPI app entry point
│   │   ├── database.py         # SQLAlchemy engine & session config
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── user.py         # User SQLAlchemy model
│   │   ├── routers/
│   │   │   └── auth_router.py  # Authentication endpoints
│   │   ├── schemas/
│   │   │   └── user.py         # Pydantic request/response schemas
│   │   ├── services/           # Business logic, puzzle generation
│   │   └── auth/
│   │       ├── hashing.py      # Password hashing (bcrypt)
│   │       ├── jwt.py          # JWT token creation & verification
│   │       └── generator/
│   │           ├── username_generator.py     # Username generation logic
│   │           ├── username_prefix.txt       # Prefix word list
│   │           └── username_suffix.txt       # Suffix word list
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   ├── pages/              # One page per game + Home, Stats, Auth
│   │   └── api/                # Axios calls to the backend
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
└── COPILOT_CONTEXT.md
```

---

## Game Types

### Schwedenrätsel (Swedish-style Crossword)

- Grid with black cells; clues are placed directly inside the black cells
- Automatically generated using a word list (German)
- One puzzle per day

### Wordle

- Player guesses a hidden 5- or 6-letter German word in 6 attempts
- Feedback: green (correct position), yellow (wrong position), darkgrey (not in word)
- Word selected daily from a German word list
- Tracking of already used words

### Sudoku

- Classic 9×9 Sudoku
- Generated automatically with a unique solution
- System checks if users result is right (check sudoku rules)
- One puzzle per day, varying difficulty (mostly medium, sometimes hard, never easy)

---

## API Design (Backend)

Base URL: `/api/v1`

Key endpoint groups:

- `POST /auth/register` – create account
- `POST /auth/login` – receive JWT
- `GET /puzzles/today` – fetch all of today's puzzles (guest + user)
  - perhaps broken down into sections for each type of puzzle
- `GET /puzzles/{date}` – fetch puzzles for a specific date (authenticated only)
- `POST /puzzles/{id}/submit` – submit a solution attempt
  - perhaps broken down into sections for each type of puzzle
- `GET /users/me/stats` – fetch stats for the logged-in user
  - wordle
    - fastest completion time
    - how many wordles solved in 1 try
    - how many wordles solved in 2 tries
    - average number of tries to solve
  - kreuzworträtsel / schwedenrätsel
    - fastest completion time
    - average completion time
    - how many words solved in 1 try
  - sudoku
    - fastest completion time

---

## Auth Module Details

### Username Generation (`backend/app/auth/generator/username_generator.py`)

The username generator creates random, memorable usernames from word lists without requiring user input during registration. 

**Key Functions:**

- `generate_unique_username(db: Session, max_attempts: int = 100) -> Optional[str]`
  - Generates a random username and checks the database for uniqueness
  - Returns a unique username string or `None` if unable to find one within max_attempts
  - **Usage**: Call during user registration to auto-assign a unique username
  
- `generate_random_username() -> str`
  - Synchronous version that generates a random username without database checks
  - Used for preview/testing purposes

**Username Format:**
- 1 Prefix word (from `username_prefix.txt`)
- 1–2 Suffix words (from `username_suffix.txt`)
- 3–5 random digits
- Example: `TopDogReptile8907`

**Word Lists:**
- `username_prefix.txt` – Capitalized prefix words (one per line)
- `username_suffix.txt` – Capitalized suffix words (one per line)

---

## Database Models (planned)

- `User` – id, username, email, hashed_password, created_at
- `DailyPuzzle` – id, date, game_type (enum: wordle/sudoku/schweden), puzzle_data (JSON), solution_data (JSON)
- `Attempt` – id, user_id, puzzle_id, submitted_at, solved (bool), attempt_data (JSON)

---

## Key Rules & Conventions

- Backend uses **async** FastAPI route handlers where possible
- All DB access goes through **SQLAlchemy** (no raw SQL)
- Auth middleware protects all routes that require a logged-in user
- Puzzle generation logic lives in `backend/app/services/`
- Check puzzle result logic lives in `backend/app/services/`
- Frontend communicates with the backend exclusively via REST API (no direct DB access)
- Docker Compose is used for local development; all services start with `docker compose up`
- Environment variables (DB URL, JWT secret) are passed via Docker Compose and never hardcoded

---

## Current Implementation Status – Phase 1

### ✅ Completed

- **Docker Compose Setup** – Backend + Frontend + PostgreSQL running locally
- **FastAPI Scaffold** – Basic app structure with auto-migration (SQLAlchemy creates tables)
- **PostgreSQL + SQLAlchemy** – Database connection and ORM models
- **User Model** – Database schema with `id`, `username`, `email`, `hashed_password`, `created_at`
- **Authentication Endpoints:**
  - `POST /api/auth/generate-username` – Generate a unique, random username
  - `POST /api/auth/register` – Register a new user (auto-generate username if not provided)
  - `POST /api/auth/login` – Login with email/password, receive JWT token
  - `GET /api/auth/me` – Retrieve authenticated user info (protected route)
- **Password Hashing** – Argon2 via passlib (OWASP recommended, no length limitations)
- **JWT Token Creation & Verification** – HS256 tokens with 1-day expiration
- **JWT Middleware** – `get_current_user()` dependency protects authenticated routes
- **End-to-End Testing** – Verified: register → login → access protected routes → 401 on unauthorized

---

## Next Steps

### Phase 1 Complete ✅

All core authentication features are implemented and tested:
- User registration with unique username generation
- Login with JWT token issuance
- Protected `/me` endpoint with JWT middleware
- Proper error handling (401 for unauthorized access)
- Argon2 password hashing (OWASP recommended)

### Upcoming: Phase 2 – Daily Puzzle System

Build the core puzzle infrastructure:

1. **Create Database Models**
   - `DailyPuzzle` – date, game_type (enum), puzzle_data (JSON), solution_data (JSON)
   - `Attempt` – user_id, puzzle_id, submitted_at, solved (bool), attempt_data (JSON)
   - `GameType` – enum (wordle, sudoku, schwedenrätsel)

2. **Build Puzzle Generation Service** (`backend/app/services/`)
   - Sudoku generator with unique solution
   - Wordle daily word selection
   - Schwedenrätsel generator

3. **Create Puzzle API Endpoints**
   - `GET /api/puzzles/today` – Fetch all today's puzzles (guest + authenticated)
   - `POST /api/puzzles/{id}/submit` – Submit and check solution
   - `GET /api/puzzles/{date}` – Fetch archived puzzles (authenticated only)

---

## Phases Overview

### Phase 1 — Foundation ✅ Complete

- Docker Compose setup (Backend + Frontend + DB running locally) ✅
- FastAPI scaffold + PostgreSQL connection via SQLAlchemy ✅
- User authentication (Register, Login, JWT, Protected routes) ✅

### Phase 2 — Daily Puzzle System

- DB schema for daily puzzles (one puzzle per game type per day)
- Automatic puzzle generation (Sudoku → Wordle → Schwedenrätsel)
- API endpoints: fetch today's puzzle, submit a solution

### Phase 3 — Frontend

- React scaffold with routing (React Router)
- Login / Register UI
- Sudoku game view
- Wordle game view
- Schwedenrätsel game view (most complex)

### Phase 4 — Stats & Archive

- Store solution attempts in DB
- Statistics page (streak, success rate, etc.)
- Puzzle archive accessible to logged-in users only

### Phase 5 — Deployment

- Domain + VPS (e.g. Hetzner, ~€4/month)
- Nginx as reverse proxy
- HTTPS via Let's Encrypt
