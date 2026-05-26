"""FastAPI application entrypoint."""

from __future__ import annotations

from fastapi import FastAPI

from .routers import admin, auth, puzzles, telemetry

app = FastAPI(title="CWPFlaa", version="0.1.0")
app.include_router(auth.router)
app.include_router(puzzles.router)
app.include_router(telemetry.router)
app.include_router(admin.router)


@app.get("/healthz", tags=["meta"])
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
