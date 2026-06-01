import logging
import sys
from fastapi import FastAPI
from app.database import Base, engine, SessionLocal
from app.models import user, Word
from app.routers.auth_router import router as auth_router
from app.seeds.seed_words import seed_words

# Configure logging to output to stdout (so Docker can capture it)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)

logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)   # creates tables at the start of the application, 
                                        # TODO in production consider using Alembic for migrations

# Run seed operation on startup
logger.info("Running seed operation...")
db = SessionLocal()
try:
    seed_words(db)
finally:
    db.close()

app = FastAPI(
    title="CWPFLaa Backend",
    description="API for the cwpflaa puzzle application – Schwedenrätsel, Wordle, and Sudoku",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.include_router(auth_router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok"}