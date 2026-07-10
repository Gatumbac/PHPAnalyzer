import type { AnalyzeResponse, AnalysisError } from "../types/analysis";

function pad(value: number): string {
  return value.toString().padStart(2, "0");
}

function buildTimestamp(date: Date): string {
  return (
    `${date.getFullYear()}${pad(date.getMonth() + 1)}${pad(date.getDate())}` +
    `-${pad(date.getHours())}${pad(date.getMinutes())}${pad(date.getSeconds())}`
  );
}

function formatErrors(errors: AnalysisError[]): string[] {
  if (errors.length === 0) {
    return ["Sin errores."];
  }
  return errors.map(
    (error, index) =>
      `  ${index + 1}. [${error.code}] (linea ${error.line}) ${error.message}`,
  );
}

function formatTokens(result: AnalyzeResponse): string[] {
  if (result.tokens.length === 0) {
    return ["  No hay tokens para mostrar."];
  }
  return result.tokens.map(
    (token) =>
      `  ${token.type}\t${token.lexeme}\t${token.line}\t${token.column}`,
  );
}

function buildLogContent(result: AnalyzeResponse): string {
  const generated = new Date().toLocaleString("es-ES");
  const meta = result.meta;

  const lines: string[] = [
    "PHPAnalyzer - Log de Analisis",
    `Generado: ${generated}`,
    "",
    `Estado: ${result.status}`,
    `Tiempo de ejecucion (ms): ${meta.elapsed_ms}`,
    `Longitud del codigo fuente: ${meta.source_length}`,
    `Version del analizador: ${meta.analyzer_version}`,
    "",
    "== Tokens (Lexico) ==",
    ...formatTokens(result),
    "",
    "== Errores Sintacticos ==",
    ...formatErrors(result.syntactic_errors.filter((error) => error.phase !== "lexical")),
    "",
    "== Errores Semanticos ==",
    ...formatErrors(result.semantic_errors),
    "",
    "== Errores Lexicos ==",
    ...formatErrors(result.syntactic_errors.filter((error) => error.phase === "lexical")),
    "",
    "Fin del log.",
  ];

  return lines.join("\n");
}

export function exportAnalysisLogs(result: AnalyzeResponse | null): void {
  if (!result) {
    throw new Error("No hay resultados para exportar. Ejecute un analisis primero.");
  }

  if (typeof document === "undefined" || typeof window === "undefined") {
    throw new Error("La exportacion de logs solo esta disponible en el navegador.");
  }

  const content = buildLogContent(result);
  const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);

  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = `phpanalyzer-log-${buildTimestamp(new Date())}.txt`;
  document.body.appendChild(anchor);
  anchor.click();
  document.body.removeChild(anchor);

  URL.revokeObjectURL(url);
}