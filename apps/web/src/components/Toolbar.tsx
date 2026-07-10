interface ToolbarProps {
  includeTokens: boolean;
  themeMode: "light" | "dark";
  isAnalyzing: boolean;
  onToggleTokens: (enabled: boolean) => void;
  onAnalyze: () => void;
  onExport: () => void;
  onToggleTheme: () => void;
}

export function Toolbar({
  includeTokens,
  themeMode,
  isAnalyzing,
  onToggleTokens,
  onAnalyze,
  onExport,
  onToggleTheme,
}: ToolbarProps) {
  return (
    <header className="flex flex-wrap items-center justify-between gap-3 rounded-lg border border-border bg-panel px-4 py-3">
      <div className="flex items-center gap-3">
        <h1 className="font-display text-lg font-semibold text-text">PHPAnalyzer Studio</h1>
        <span className="rounded bg-panelAlt px-2 py-1 text-xs text-muted">Analizador Web</span>
      </div>

      <div className="flex flex-wrap items-center gap-3">
        <label className="flex items-center gap-2 text-xs text-muted" title="Controla la tabla de tokens en la vista y en el archivo de log.">
          <input
            type="checkbox"
            checked={includeTokens}
            onChange={(event) => onToggleTokens(event.target.checked)}
            className="h-4 w-4 accent-accent"
          />
          Incluir tabla de tokens en vista y log
        </label>

        <button
          type="button"
          onClick={onAnalyze}
          disabled={isAnalyzing}
          className="rounded-md border border-accent/60 bg-accent/20 px-3 py-2 text-xs font-semibold text-accent hover:bg-accent/30 disabled:cursor-not-allowed disabled:opacity-60"
        >
          Ejecutar Análisis
        </button>

        <button
          type="button"
          onClick={onExport}
          className="rounded-md border border-border bg-panelAlt px-3 py-2 text-xs font-semibold text-text hover:bg-panel"
        >
          Exportar Logs
        </button>

        <button
          type="button"
          onClick={onToggleTheme}
          aria-label={`Cambiar a tema ${themeMode === "dark" ? "claro" : "oscuro"}`}
          title={`Cambiar a tema ${themeMode === "dark" ? "claro" : "oscuro"}`}
          className="grid h-9 w-9 place-items-center rounded-md border border-border bg-panelAlt text-base text-text hover:bg-panel"
        >
          <span aria-hidden="true">{themeMode === "dark" ? "☀" : "☾"}</span>
        </button>
      </div>
    </header>
  );
}
