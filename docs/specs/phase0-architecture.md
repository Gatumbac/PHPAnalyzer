# PHPAnalyzer Web Architecture (Phase 0)

## Goal
Define a monorepo architecture that separates analyzer core logic from delivery layers (CLI, API, Web UI) while preserving current functionality.

## Boundaries
- `packages/analyzer/php_analyzer`: Pure analysis core. No file writes. Public entrypoint is `analyze_php(source_code, include_tokens=True)`.
- `main.py`: CLI adapter. Reads files, calls analyzer package, writes logs.
- `apps/web`: Frontend workspace scaffold for React + Vite + TypeScript.
- Future `apps/api`: FastAPI service adapter that will expose analyzer package through HTTP.

## Analyzer I/O Contract (v1)
- Input:
  - `source_code: str` (UTF-8 PHP source)
  - `include_tokens: bool = True`
- Output (`AnalysisResult`):
  - `status: success | syntax_error | semantic_error | mixed_error`
  - `tokens: TokenInfo[]`
  - `syntactic_errors: AnalysisError[]`
  - `semantic_errors: AnalysisError[]`
  - `meta: AnalysisMeta`

## Non-Functional Constraints
- State must reset between runs.
- Reusable from CLI and future API without behavior drift.
- Error messages remain Spanish-first.
- Keep current CLI flow with `python main.py`.
