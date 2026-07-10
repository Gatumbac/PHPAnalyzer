import type { AnalyzeResponse, AnalysisError } from "../types/analysis";

function pad(value: number): string {
  return value.toString().padStart(2, "0");
}

function buildTimestamp(date: Date): string {
  return (
    `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}` +
    `_${pad(date.getHours())}-${pad(date.getMinutes())}-${pad(date.getSeconds())}`
  );
}

function formatErrors(errors: AnalysisError[], emptyMessage = "Sin errores."): string[] {
  if (errors.length === 0) {
    return [emptyMessage];
  }
  return errors.map(
    (error, index) =>
      `  ${index + 1}. [${error.code}] (línea ${error.line}) ${error.message}`,
  );
}

function formatTokens(result: AnalyzeResponse): string[] {
  if (result.tokens.length === 0) {
    return ["No hay tokens para mostrar."];
  }

  const headers = ["Token", "Lexema", "Línea", "Columna"];
  const rows = result.tokens.map((token) => [
    token.type,
    String(token.lexeme),
    String(token.line),
    String(token.column),
  ]);
  const widths = headers.map((header, index) =>
    Math.max(header.length, ...rows.map((row) => row[index].length)),
  );
  const separator = `+-${widths.map((width) => "-".repeat(width)).join("-+-")}-+`;
  const formatRow = (row: string[]) =>
    `| ${row.map((cell, index) => cell.padEnd(widths[index])).join(" | ")} |`;

  return [separator, formatRow(headers), separator, ...rows.map(formatRow), separator];
}

function buildLogContent(result: AnalyzeResponse, includeTokens: boolean): string {
  const generated = new Date().toLocaleString("es-ES");
  const meta = result.meta;

  const lines: string[] = [
    "PHPAnalyzer - Log de Análisis",
    `Generado: ${generated}`,
    "",
    `Estado: ${result.status}`,
    `Tiempo de ejecución (ms): ${meta.elapsed_ms}`,
    `Longitud del código fuente: ${meta.source_length}`,
    `Versión del analizador: ${meta.analyzer_version}`,
    "",
    "== Tokens (Léxico) ==",
    ...(includeTokens ? formatTokens(result) : ["Tabla de tokens no incluida."]),
    "",
    "== Errores Léxicos ==",
    ...formatErrors(result.syntactic_errors.filter((error) => error.phase === "lexical")),
    "",
    "== Errores Sintácticos ==",
    ...formatErrors(result.syntactic_errors.filter((error) => error.phase !== "lexical")),
    "",
    "== Errores Semánticos ==",
    ...formatErrors(
      result.semantic_errors,
      result.semantic_skipped ? "No ejecutado debido a errores sintácticos." : undefined,
    ),
    "",
    "Fin del log.",
  ];

  return lines.join("\n");
}

export function exportAnalysisLogs(result: AnalyzeResponse | null, includeTokens: boolean): void {
  if (!result) {
    throw new Error("No hay resultados para exportar. Ejecute un análisis primero.");
  }

  if (typeof document === "undefined" || typeof window === "undefined") {
    throw new Error("La exportación de logs solo está disponible en el navegador.");
  }

  const content = buildLogContent(result, includeTokens);
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
