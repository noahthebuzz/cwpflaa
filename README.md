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

## Run backend locally

```bash
pip install -r requirements.txt
uvicorn backend.app.main:app --reload
```
