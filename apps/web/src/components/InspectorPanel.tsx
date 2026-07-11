import type { ReactNode } from "react";
import type { AnalyzeResponse, AnalysisError } from "../types/analysis";
import { TokenTable } from "./TokenTable";

type SectionKey = "lexico" | "sintactico" | "semantico";

interface InspectorPanelProps {
  result: AnalyzeResponse | null;
  includeTokens: boolean;
  sectionsOpen: Record<SectionKey, boolean>;
  onToggleSection: (section: SectionKey) => void;
}

function ErrorList({ errors, emptyMessage = "Sin errores." }: { errors: AnalysisError[]; emptyMessage?: string }) {
  if (errors.length === 0) {
    return <p className="text-xs text-ok">{emptyMessage}</p>;
  }

  return (
    <ul className="space-y-2 text-xs font-mono">
      {errors.map((error, idx) => (
        <li key={`${error.code}-${idx}`} className="rounded border border-error/40 bg-error/10 p-2 text-error">
          <p>{error.message}</p>
          <p className="mt-1 text-[11px] text-muted">Código: {error.code}</p>
        </li>
      ))}
    </ul>
  );
}

function SectionCard({
  title,
  section,
  isOpen,
  onToggle,
  children,
}: {
  title: string;
  section: SectionKey;
  isOpen: boolean;
  onToggle: (section: SectionKey) => void;
  children: ReactNode;
}) {
  return (
    <article className="rounded-lg border border-border bg-panelAlt">
      <button
        type="button"
        onClick={() => onToggle(section)}
        className="flex w-full items-center justify-between px-3 py-2 text-left"
      >
        <span className="text-sm font-semibold text-text">{title}</span>
        <span className="text-xs text-muted">{isOpen ? "Ocultar" : "Mostrar"}</span>
      </button>
      {isOpen ? <div className="border-t border-border px-3 py-3">{children}</div> : null}
    </article>
  );
}

export function InspectorPanel({ result, includeTokens, sectionsOpen, onToggleSection }: InspectorPanelProps) {
  const syntacticErrors = result?.syntactic_errors ?? [];
  const semanticErrors = result?.semantic_errors ?? [];
  const lexicalErrors = syntacticErrors.filter((error) => error.phase === "lexical");

  const shouldShowTokens = !!result && result.tokens.length > 0;

  return (
    <aside className="flex h-full flex-col gap-3 rounded-lg border border-border bg-panel p-3">
      <div className="rounded border border-border bg-panelAlt px-3 py-2">
        <p className="text-xs text-muted">Estado</p>
        <p className="text-sm font-semibold text-text">
          {result ? "Análisis completado" : "Esperando código..."}
        </p>
      </div>

      <SectionCard
        title="Léxico"
        section="lexico"
        isOpen={sectionsOpen.lexico}
        onToggle={onToggleSection}
      >
        <div className="space-y-3">
          {lexicalErrors.length > 0 ? <ErrorList errors={lexicalErrors} /> : null}
          {includeTokens ? (
            shouldShowTokens ? <TokenTable tokens={result.tokens} /> : <p className="text-xs text-muted">No hay tokens para mostrar.</p>
          ) : null}
          {lexicalErrors.length === 0 && !includeTokens ? <p className="text-xs text-ok">Sin errores.</p> : null}
        </div>
      </SectionCard>

      <SectionCard
        title="Sintáctico"
        section="sintactico"
        isOpen={sectionsOpen.sintactico}
        onToggle={onToggleSection}
      >
        <ErrorList errors={syntacticErrors.filter((error) => error.phase === "syntactic")} />
      </SectionCard>

      <SectionCard
        title="Semántico"
        section="semantico"
        isOpen={sectionsOpen.semantico}
        onToggle={onToggleSection}
      >
        <ErrorList
          errors={semanticErrors}
          emptyMessage={result?.semantic_skipped ? "No ejecutado debido a errores sintácticos." : undefined}
        />
      </SectionCard>
    </aside>
  );
}
