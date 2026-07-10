import type { ReactNode } from "react";
import type { AnalyzeResponse, AnalysisError } from "../types/analysis";
import { TokenTable } from "./TokenTable";

type SectionKey = "lexico" | "sintactico" | "semantico";

interface InspectorPanelProps {
  result: AnalyzeResponse | null;
  sectionsOpen: Record<SectionKey, boolean>;
  activeSection: SectionKey | null;
  onToggleSection: (section: SectionKey) => void;
}

function ErrorList({ errors }: { errors: AnalysisError[] }) {
  if (errors.length === 0) {
    return <p className="text-xs text-ok">Sin errores.</p>;
  }

  return (
    <ul className="space-y-2 text-xs font-mono">
      {errors.map((error, idx) => (
        <li key={`${error.code}-${idx}`} className="rounded border border-error/40 bg-error/10 p-2 text-error">
          <p>{error.message}</p>
          <p className="mt-1 text-[11px] text-muted">Codigo: {error.code}</p>
        </li>
      ))}
    </ul>
  );
}

function SectionCard({
  title,
  section,
  isOpen,
  isActive,
  onToggle,
  children,
}: {
  title: string;
  section: SectionKey;
  isOpen: boolean;
  isActive: boolean;
  onToggle: (section: SectionKey) => void;
  children: ReactNode;
}) {
  return (
    <article className={`rounded-lg border ${isActive ? "border-accent" : "border-border"} bg-panelAlt`}>
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

export function InspectorPanel({ result, sectionsOpen, activeSection, onToggleSection }: InspectorPanelProps) {
  const syntacticErrors = result?.syntactic_errors ?? [];
  const semanticErrors = result?.semantic_errors ?? [];
  const lexicalErrors = syntacticErrors.filter((error) => error.phase === "lexical");

  const shouldShowTokens = !!result && result.tokens.length > 0;

  return (
    <aside className="flex h-full flex-col gap-3 rounded-lg border border-border bg-panel p-3">
      <div className="rounded border border-border bg-panelAlt px-3 py-2">
        <p className="text-xs text-muted">Estado</p>
        <p className="text-sm font-semibold text-text">
          {result ? "Analisis completado" : "Esperando codigo..."}
        </p>
      </div>

      <SectionCard
        title="Lexico"
        section="lexico"
        isOpen={sectionsOpen.lexico}
        isActive={activeSection === "lexico"}
        onToggle={onToggleSection}
      >
        {lexicalErrors.length > 0 ? <ErrorList errors={lexicalErrors} /> : null}
        {shouldShowTokens ? <TokenTable tokens={result.tokens} /> : <p className="text-xs text-muted">No hay tokens para mostrar.</p>}
      </SectionCard>

      <SectionCard
        title="Sintactico"
        section="sintactico"
        isOpen={sectionsOpen.sintactico}
        isActive={activeSection === "sintactico"}
        onToggle={onToggleSection}
      >
        <ErrorList errors={syntacticErrors.filter((error) => error.phase === "syntactic")} />
      </SectionCard>

      <SectionCard
        title="Semantico"
        section="semantico"
        isOpen={sectionsOpen.semantico}
        isActive={activeSection === "semantico"}
        onToggle={onToggleSection}
      >
        <ErrorList errors={semanticErrors} />
      </SectionCard>
    </aside>
  );
}
