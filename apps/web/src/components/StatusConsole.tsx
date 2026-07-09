import type { AnalyzeResponse } from "../types/analysis";

interface StatusConsoleProps {
  healthMessage: string;
  statusMessage: string;
  errorMessage?: string;
  lastResult: AnalyzeResponse | null;
  isAnalyzing: boolean;
}

export function StatusConsole({
  healthMessage,
  statusMessage,
  errorMessage,
  lastResult,
  isAnalyzing,
}: StatusConsoleProps) {
  const statusColor = errorMessage
    ? "text-error"
    : lastResult?.status === "success"
      ? "text-ok"
      : "text-warn";

  return (
    <section className="rounded-lg border border-border bg-panel px-4 py-3">
      <div className="flex flex-wrap items-center gap-3 text-xs font-mono">
        <span className="rounded bg-panelAlt px-2 py-1 text-muted">{healthMessage}</span>
        <span className={`rounded bg-panelAlt px-2 py-1 ${statusColor}`}>{statusMessage}</span>
        {isAnalyzing ? <span className="rounded bg-panelAlt px-2 py-1 text-accent">Analizando...</span> : null}
        {errorMessage ? <span className="rounded bg-panelAlt px-2 py-1 text-error">{errorMessage}</span> : null}
      </div>
    </section>
  );
}
