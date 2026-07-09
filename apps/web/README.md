# Web App

React + Vite + TypeScript UI for PHPAnalyzer.

## Features (Phase 3)

- Split layout (editor 65% + inspector 35%)
- Monaco editor for PHP input
- Toolbar actions: `Ejecutar Analisis`, `Exportar Logs`
- Inspector sections: Lexico, Sintactico, Semantico
- Contextual status console and API health feedback
- Frontend log export (`.txt`) from analysis response
- Light/Dark mode toggle with persisted preference

## Environment

Create `.env` in `apps/web`:

```bash
cp .env.example .env
```

Set API URL:

```env
VITE_API_URL=http://localhost:8000
```

## Run

From repo root:

```bash
pnpm install
pnpm web:dev
```

Or from `apps/web`:

```bash
pnpm install
pnpm dev
```
