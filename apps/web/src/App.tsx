import { useEffect, useMemo, useState } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";

import { CodeEditor } from "./components/CodeEditor";
import { InspectorPanel } from "./components/InspectorPanel";
import { StatusConsole } from "./components/StatusConsole";
import { Toolbar } from "./components/Toolbar";
import { checkHealth, analyzeCode } from "./lib/api";
import { exportAnalysisLogs } from "./lib/exportLogs";
import { useUIStore } from "./store/uiStore";

function statusMessageFromResult(status: "success" | "syntax_error" | "semantic_error" | "mixed_error") {
  if (status === "success") {
    return "Análisis completado sin errores.";
  }
  if (status === "syntax_error") {
    return "Se detectaron errores sintácticos.";
  }
  if (status === "semantic_error") {
    return "Se detectaron errores semánticos.";
  }
  return "Se detectaron errores sintácticos y semánticos.";
}

export default function App() {
  const {
    sourceCode,
    includeTokens,
    themeMode,
    sectionsOpen,
    statusMessage,
    healthMessage,
    lastResult,
    setSourceCode,
    setIncludeTokens,
    toggleTheme,
    toggleSection,
    setStatusMessage,
    setHealthMessage,
    setResult,
    hydrateTheme,
    openSectionForStatus,
  } = useUIStore();

  const [requestError, setRequestError] = useState<string>("");

  const healthQuery = useQuery({
    queryKey: ["health"],
    queryFn: checkHealth,
    retry: 1,
    refetchOnWindowFocus: false,
  });

  const analyzeMutation = useMutation({
    mutationFn: analyzeCode,
    onMutate: () => {
      setRequestError("");
      setStatusMessage("Procesando análisis...");
    },
    onSuccess: (result) => {
      setResult(result);
      openSectionForStatus(result.status);
      setStatusMessage(statusMessageFromResult(result.status));
    },
    onError: (error) => {
      const message = error instanceof Error ? error.message : "Error inesperado durante el análisis.";
      setRequestError(message);
      setStatusMessage("No se pudo completar el análisis.");
    },
  });

  useEffect(() => {
    hydrateTheme();
  }, [hydrateTheme]);

  useEffect(() => {
    if (healthQuery.isSuccess) {
      setHealthMessage("API disponible");
      return;
    }
    if (healthQuery.isError) {
      setHealthMessage("API no disponible");
    }
  }, [healthQuery.isSuccess, healthQuery.isError, setHealthMessage]);

  const canAnalyze = useMemo(() => sourceCode.trim().length > 0, [sourceCode]);

  const handleRunAnalysis = () => {
    if (!canAnalyze || analyzeMutation.isPending) {
      return;
    }
    analyzeMutation.mutate({
      source_code: sourceCode,
      include_tokens: includeTokens,
    });
  };

  const handleExport = () => {
    try {
      exportAnalysisLogs(lastResult, includeTokens);
      setStatusMessage("Log exportado correctamente.");
    } catch (error) {
      const message = error instanceof Error ? error.message : "No se pudo exportar el log.";
      setRequestError(message);
    }
  };

  return (
    <main className="mx-auto flex min-h-screen max-w-[1600px] flex-col gap-4 p-4 md:p-6">
      <Toolbar
        includeTokens={includeTokens}
        themeMode={themeMode}
        isAnalyzing={analyzeMutation.isPending}
        onToggleTokens={setIncludeTokens}
        onAnalyze={handleRunAnalysis}
        onExport={handleExport}
        onToggleTheme={toggleTheme}
      />

      <section className="grid min-h-[65vh] grid-cols-1 gap-4 lg:grid-cols-[minmax(0,13fr)_minmax(0,7fr)]">
        <CodeEditor value={sourceCode} onChange={setSourceCode} themeMode={themeMode} />
        <InspectorPanel
          result={lastResult}
          includeTokens={includeTokens}
          sectionsOpen={sectionsOpen}
          onToggleSection={toggleSection}
        />
      </section>

      <StatusConsole
        healthMessage={healthMessage}
        statusMessage={statusMessage}
        errorMessage={requestError}
        lastResult={lastResult}
        isAnalyzing={analyzeMutation.isPending}
      />
    </main>
  );
}
