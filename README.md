# cwpflaa

Cross-word puzzles for lara and ayla.

## Suggested lightweight monolith structure

```text
backend/
  app/
    db.py
    main.py
    models.py
    schemas.py
    routers/
      auth.py
      puzzles.py
      telemetry.py
      admin.py
    services/
      text_normalization.py
frontend/
  src/
    utils/
      crosswordInputController.ts
tests/
  backend/
    test_text_normalization.py
```

## Start the backend

```bash
# from repository root
pip install -r requirements.txt
uvicorn backend.app.main:app --reload
```

Backend will be available at `http://127.0.0.1:8000` (health check: `/healthz`).

## Start the frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend dev server will typically run at `http://127.0.0.1:5173`.
