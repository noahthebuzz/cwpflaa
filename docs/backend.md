# Backend Setup & Development Guide

## Overview

The backend is a **FastAPI** application that provides REST API endpoints for user authentication, puzzle generation, and game submission. It uses **PostgreSQL** for data persistence and **SQLAlchemy** for ORM.

---

## Prerequisites

- Docker & Docker Compose (for containerized development)
- Python 3.12+ (for local development without Docker)
- PostgreSQL 16 (if running locally)

---

## Quick Start (Docker)

### 1. Start the Backend

From the project root:

```bash
docker compose up
```

This will start:

- **Backend** on `http://localhost:8000`
- **PostgreSQL** on `localhost:5432`

### 2. Test the Backend

Check if it's running:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{ "status": "ok" }
```

### 3. Access API Documentation

Open your browser:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## Local Development (Without Docker)

### 1. Setup Python Environment

```bash
cd backend

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Setup PostgreSQL

#### Option A: Using Docker (recommended)

```bash
docker run --name cwpflaa-postgres \
  -e POSTGRES_USER=cwpflaa \
  -e POSTGRES_PASSWORD=cwpflaa_dev \
  -e POSTGRES_DB=cwpflaa_db \
  -p 5432:5432 \
  -d postgres:16
```

#### Option B: Using Local PostgreSQL

Install PostgreSQL 16 and create the database:

```bash
createdb -U postgres cwpflaa_db
```

### 3. Configure Environment

Create a `.env` file in the `backend/` directory:

```env
DATABASE_URL=postgresql://cwpflaa:cwpflaa_dev@localhost:5432/cwpflaa_db
JWT_SECRET_KEY=your_secret_key_here_minimum_32_chars
```

Generate a secure JWT secret:

```bash
openssl rand -hex 32
```

### 4. Run the Backend

```bash
cd backend
uvicorn app.main:app --reload
```

The API is now at `http://localhost:8000`

---

## Project Structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI app entry point
│   ├── database.py             # SQLAlchemy setup & session
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py             # User database model
│   ├── routers/
│   │   └── auth_router.py      # Authentication endpoints
│   ├── schemas/
│   │   └── user.py             # Pydantic request/response models
│   ├── services/               # Business logic (puzzle generation, etc.)
│   └── auth/
│       ├── hashing.py          # Password hashing (Argon2)
│       ├── jwt.py              # JWT token creation & verification
│       └── generator/
│           ├── username_generator.py
│           ├── username_prefix.txt
│           └── username_suffix.txt
├── Dockerfile
├── requirements.txt
└── .env                        # (Create locally, not in git)
```

---

## API Endpoints

### Authentication

#### Generate Username

```
POST /api/auth/generate-username
Response: { "username": "TopDogReptile8907" }
```

#### Register

```
POST /api/auth/register
Body: {
  "username": "optional_username",
  "email": "user@example.com",
  "password": "secure_password"
}
Response: { "id": 1, "username": "...", "email": "..." }
```

#### Login

```
POST /api/auth/login
Body: {
  "email": "user@example.com",
  "password": "secure_password"
}
Response: { "access_token": "eyJhbGc...", "token_type": "bearer" }
```

#### Get Current User

```
GET /api/auth/me
Headers: Authorization: Bearer <token>
Response: { "id": 1, "username": "...", "email": "..." }
```

---

## Database Models

### User

```python
id: int (primary key)
username: str (unique, max 50 chars)
email: str (unique, max 255 chars)
hashed_password: str
created_at: datetime
```

### DailyPuzzle (Phase 2)

```python
id: int (primary key)
date: date
game_type: str (enum: wordle, sudoku, schwedenrätsel)
puzzle_data: JSON
solution_data: JSON
```

### Attempt (Phase 2)

```python
id: int (primary key)
user_id: int (foreign key)
puzzle_id: int (foreign key)
submitted_at: datetime
solved: bool
attempt_data: JSON
```

---

## Authentication Flow

### How JWT Works

1. **User registers** → Account created, password hashed with Argon2
2. **User logs in** → Email/password validated, JWT token generated
3. **Client stores token** → Usually in localStorage or secure cookie
4. **API requests** → Include token in `Authorization: Bearer <token>` header
5. **Backend validates** → Token decoded, user retrieved from database
6. **Protected endpoints** → Return 401 if token is invalid/missing

### Token Details

- **Algorithm**: HS256 (symmetric)
- **Expiration**: 24 hours
- **Payload**: `{ "sub": "<user_id>", "exp": <timestamp> }`
- **Secret**: Loaded from `JWT_SECRET_KEY` environment variable

---

## Dependencies

### Core

- **fastapi** – Web framework
- **uvicorn[standard]** – ASGI server
- **sqlalchemy** – ORM
- **psycopg2-binary** – PostgreSQL driver
- **python-dotenv** – Environment variable management

### Authentication

- **passlib[argon2]** – Password hashing (Argon2)
- **python-jose[cryptography]** – JWT handling

### Validation

- **pydantic[email]** – Request/response validation

---

## Development Tips

### Hot Reload

When running locally with `uvicorn app.main:app --reload`, code changes automatically restart the server.

### Database Migrations (Future)

Currently, tables are auto-created on startup. For production, use **Alembic**:

```bash
pip install alembic
alembic init migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### Debugging

Enable verbose logging:

```bash
# In .env
LOG_LEVEL=DEBUG

# Or via uvicorn
uvicorn app.main:app --reload --log-level debug
```

### Testing

Add test files in `backend/tests/`:

```bash
pip install pytest pytest-asyncio
pytest tests/
```

---

## Troubleshooting

### 1. "database connection refused"

**Solution**: Ensure PostgreSQL is running:

```bash
docker ps  # Should show cwpflaa-db-1 container
```

### 2. "cannot import name 'HTTPAuthorizationCredentials'"

**Solution**: Ensure fastapi version is compatible. Check `requirements.txt`.

### 3. "JWT secret is not set"

**Solution**: Check that `JWT_SECRET_KEY` is in `.env` or docker-compose.yml environment:

```bash
docker compose logs backend | grep JWT_SECRET_KEY
```

### 4. "Argon2 hashing fails"

**Solution**: Ensure `passlib[argon2]` is installed:

```bash
pip install --upgrade passlib argon2-cffi
```

---

## Next Steps

- **Phase 2**: Add puzzle generation services and endpoints
- **Phase 3**: Build frontend to consume these endpoints
- **Phase 4**: Add statistics tracking and attempt storage
- **Phase 5**: Deploy to production with Nginx and HTTPS

---

## Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Python-Jose Docs](https://python-jose.readthedocs.io/)
- [Pydantic Docs](https://docs.pydantic.dev/)

---

## Questions?

Check [../COPILOT_CONTEXT.md](../COPILOT_CONTEXT.md) for detailed project architecture and planned features.
