# PHPAnalyzer UI Wireframe and Behavior Spec (Phase 0)

## Layout
- Top toolbar (thin):
  - App title
  - Primary action: `Ejecutar Analisis`
  - Secondary action: `Exportar Logs`
- Split view:
  - Left panel (65%): code editor
  - Right panel (35%): analysis inspector
- Bottom status console:
  - Contextual result messages and errors

## Inspector Sections
- Global status: `Esperando codigo...` or `Analisis completado`.
- Collapsible sections:
  - Lexico
  - Sintactico
  - Semantico
- Error behavior:
  - If syntax or semantic error occurs, the failing section auto-expands.

## Feedback Semantics
- Red: syntax/semantic errors.
- Yellow: lexical warnings.
- Token table (`Token`, `Lexema`, `Linea`, `Columna`) visible only after successful analysis.

## UX Rules
- Minimal visual noise; code editor is the primary focus.
- Immediate feedback after `Ejecutar Analisis`.
- Consistent monospaced typography for code.
