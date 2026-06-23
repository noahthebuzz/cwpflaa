from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import auth, puzzles

app = FastAPI(title="Daily Puzzle API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(puzzles.router, prefix="/api")

@app.get("/health")
async def health_check():
    return {"status": "ok"}
