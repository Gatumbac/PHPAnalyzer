export type AnalysisStatus = "success" | "syntax_error" | "semantic_error" | "mixed_error";

export interface TokenInfo {
  type: string;
  lexeme: string;
  line: number;
  column: number;
}

export type ErrorPhase = "lexical" | "syntactic" | "semantic";

export interface AnalysisError {
  phase: ErrorPhase;
  message: string;
  line: number;
  code: string;
}

export interface AnalysisMeta {
  elapsed_ms: number;
  source_length: number;
  analyzer_version: string;
}

export interface AnalyzeResponse {
  status: AnalysisStatus;
  tokens: TokenInfo[];
  syntactic_errors: AnalysisError[];
  semantic_errors: AnalysisError[];
  semantic_skipped: boolean;
  meta: AnalysisMeta;
}

export interface AnalyzeRequest {
  source_code: string;
  include_tokens?: boolean;
}

export interface HealthResponse {
  status: "ok";
}
