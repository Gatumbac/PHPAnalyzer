# API App

FastAPI adapter for `packages/analyzer/php_analyzer`.

## Run locally

```bash
uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8000
```

## Environment variables

- `ALLOWED_ORIGINS`: comma-separated frontend origins.
  - Example: `ALLOWED_ORIGINS=http://localhost:5173,https://web-production.up.railway.app`

## Railway start command

```bash
uvicorn apps.api.main:app --host 0.0.0.0 --port $PORT
```
