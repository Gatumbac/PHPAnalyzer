# Repository Guidelines

## Project Structure & Module Organization
- `packages/analyzer/php_analyzer/`: reusable analyzer core (lexer, parser, semantic analysis, service models).
- `apps/api/`: FastAPI adapter exposing analyzer endpoints (`main.py`, `routes.py`, `schemas.py`).
- `apps/web/`: Vite + React + TypeScript UI (`src/components`, `src/lib`, `src/store`).
- `tests/`: API and unit tests plus sample PHP inputs (`algorithm_*.php`) and generated logs in `tests/logs/`.
- `main.py`: CLI-style entry point for local analysis runs.

## Build, Test, and Development Commands
- Python setup: `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
- Run analyzer locally: `python main.py` (analyzes fixtures and writes logs under `tests/logs/`).
- Run API locally: `uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8000`
- Run tests: `pytest`
- Web dev server (from repo root): `pnpm web:dev`
- Web production build: `pnpm web:build`

## Coding Style & Naming Conventions
- Python: follow PEP 8 (4-space indentation, `snake_case` for functions/variables, `PascalCase` for classes).
- TypeScript/React: keep components in `PascalCase` files (e.g., `InspectorPanel.tsx`), utilities in `camelCase`.
- Keep analyzer logic pure and reusable in `packages/analyzer`; avoid coupling core logic to API or UI layers.
- Prefer small, focused functions and explicit return models (`models.py`, API schemas).

## Testing Guidelines
- Framework: `pytest` with shared fixtures in `tests/conftest.py`.
- Test files: `tests/unit/test_*.py` and `tests/api/test_*.py`.
- Add/adjust tests when changing lexer/parser/semantic rules or API response contracts.
- Validate both success and failure paths (e.g., syntax errors, semantic errors, skipped semantics).

## Commit & Pull Request Guidelines
- Follow Conventional Commits used in history: `feat:`, `fix:`, `test:`, and scoped variants like `feat(api): ...`.
- Keep commits focused by layer (`analyzer`, `api`, or `web`) when possible.
- PRs should include: concise summary, impacted paths, test evidence (`pytest` output), and UI screenshots for `apps/web` changes.
- Reference related issues/tasks and call out any behavior or contract changes explicitly.

## Security & Configuration Tips
- Configure CORS with `ALLOWED_ORIGINS` for API deployments.
- Do not commit secrets or environment-specific credentials.
- Treat `tests/logs/` as generated artifacts; review before relying on them for assertions.
