# cwpflaa

**cwpflaa** stands for _Cross-Word-Puzzle-Für-Lara-Und-Ayla_.

A daily puzzle web app where users can solve **Schwedenrätsel** (Swedish-style crosswords), **Wordle**, and **Sudoku**—one new puzzle per game type every day.

---

## 1. Project Overview

### What We're Building

A web application with three daily puzzle games:

- **Schwedenrätsel** – Swedish-style crossword with clues in the grid
- **Wordle** – Guess a German 5–6 letter word in 6 attempts
- **Sudoku** – Classic 9×9 puzzle with varying difficulty

### Features

- **Daily Puzzles** – One fresh puzzle per game type each day
- **User Accounts** – Create accounts to track statistics
- **Statistics** – Completion times, success rates, streaks
- **Guest Access** – Play today's puzzles without logging in
- **Archive** – Logged-in users can access and replay previous days' puzzles
- **Auto-Generation** – All puzzles are generated automatically (no manual input)

### Technology Stack

| Layer              | Technology                                                |
| ------------------ | --------------------------------------------------------- |
| **Backend**        | Python 3.12 + FastAPI                                     |
| **Database**       | PostgreSQL 16 + SQLAlchemy ORM                            |
| **Authentication** | JWT (JSON Web Tokens) + Argon2 hashing                    |
| **Frontend**       | React + Vite                                              |
| **Deployment**     | Docker + Docker Compose (local), Nginx + VPS (production) |

---

## 2. Backend

The backend is a FastAPI application that handles user authentication, puzzle generation, and game logic.

### Quick Start

1. **Prerequisites**: Docker & Docker Compose
2. **Start the backend**:
   ```bash
   docker compose up
   ```
3. **API is running at**: `http://localhost:8000`
4. **Interactive docs**: `http://localhost:8000/docs`

### What's Running

- FastAPI server on port `8000`
- PostgreSQL database on port `5432`
- Auto-generates database tables on startup

### Key Features

- ✅ User registration & login (JWT tokens)
- ✅ Protected API endpoints with authentication
- ✅ Argon2 password hashing (OWASP recommended)
- ✅ Database models for users, puzzles, and attempts

### Stack

- **Framework**: FastAPI (async, auto-documentation)
- **Database**: PostgreSQL 16 + SQLAlchemy ORM
- **Auth**: JWT + HTTPBearer tokens
- **Password Hashing**: Argon2

**→ For detailed setup, configuration, and API documentation, see [docs/backend.md](docs/backend.md)**

---

## 3. Frontend

The frontend is a React application (built with Vite) where users can solve puzzles, create accounts, and view their statistics.

### Quick Start

1. **Prerequisites**: Node.js 18+
2. **Start the frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
3. **App is running at**: `http://localhost:5173`

### What's Included

- React 18 + Vite (fast dev server)
- Routing with React Router
- API communication with Axios
- Responsive UI components

### Stack

- **Framework**: React 18
- **Build Tool**: Vite
- **Routing**: React Router
- **HTTP Client**: Axios
- **Styling**: CSS Modules / Tailwind (configurable)

**→ For detailed setup, configuration, and component structure, see [docs/frontend.md](docs/frontend.md)**

---

## Development

### Running Everything Locally

```bash
# Start backend + database
docker compose up

# In another terminal, start frontend
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173` and the backend API will be accessible at `http://localhost:8000`.

### Project Structure

```
cwpflaa/
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── main.py
│   │   ├── models/       # SQLAlchemy models
│   │   ├── routers/      # API endpoints
│   │   ├── schemas/      # Pydantic validation
│   │   ├── services/     # Business logic & puzzle generation
│   │   └── auth/         # Authentication & JWT
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/             # React application
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── api/          # Backend API calls
│   ├── package.json
│   └── vite.config.js
├── docs/                 # Setup & development guides
│   ├── backend.md
│   └── frontend.md
├── docker-compose.yml
├── COPILOT_CONTEXT.md    # Detailed project context for Copilot
└── README.md
```

---

## Development Phases

### Phase 1: Foundation ✅ Complete

- Docker setup with local dev environment
- FastAPI backend scaffold
- PostgreSQL connection & ORM
- User authentication (register, login, JWT)

### Phase 2: Daily Puzzle System (Next)

- Word vocabulary system (300+ German words with difficulty ratings)
- Puzzle generation (Sudoku, Wordle, Schwedenrätsel)
- DailyPuzzle model for storing generated puzzles
- API endpoints for fetching and submitting puzzles
- Daily puzzle scheduling with APScheduler (4 AM generation, 6 days advance)

### Phase 3: Frontend

- React UI for all game types
- Login / register pages
- Puzzle game views
- Statistics dashboard

### Phase 4: Stats & Archive

- Store solution attempts
- User statistics & streaks
- Puzzle archive access

### Phase 5: Deployment

- VPS hosting (e.g., Hetzner)
- Nginx reverse proxy
- HTTPS / Let's Encrypt
- Production Docker setup

---

## Contributing

- Backend changes? See [docs/backend.md](docs/backend.md)
- Frontend changes? See [docs/frontend.md](docs/frontend.md)
- Full project context? See [COPILOT_CONTEXT.md](COPILOT_CONTEXT.md)

---

## License

[Add your license here]
