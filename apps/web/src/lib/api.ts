import type {
  AnalyzeRequest,
  AnalyzeResponse,
  HealthResponse,
} from "../types/analysis";

const API_URL =
  import.meta.env.VITE_API_URL ?? "http://localhost:8000";

async function parseError(response: Response): Promise<string> {
  let detail: unknown;
  try {
    detail = await response.json();
  } catch {
    throw new Error(
      `Error de red al contactar la API (HTTP ${response.status}).`,
    );
  }

  if (Array.isArray(detail)) {
    const messages = detail
      .map((item) => (item && typeof item === "object" && "msg" in item ? String((item as { msg: unknown }).msg) : null))
      .filter(Boolean);
    if (messages.length > 0) {
      return messages.join("; ");
    }
  }

  if (
    detail &&
    typeof detail === "object" &&
    "detail" in detail
  ) {
    const inner = (detail as { detail: unknown }).detail;
    if (typeof inner === "string") {
      return inner;
    }
    if (Array.isArray(inner)) {
      return inner
        .map((item) =>
          item && typeof item === "object" && "msg" in item
            ? String((item as { msg: unknown }).msg)
            : null,
        )
        .filter(Boolean)
        .join("; ");
    }
  }

  return `Error inesperado de la API (HTTP ${response.status}).`;
}

export async function checkHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_URL}/health`, {
    method: "GET",
    headers: { Accept: "application/json" },
  });

  if (!response.ok) {
    throw new Error(await parseError(response));
  }

  return (await response.json()) as HealthResponse;
}

export async function analyzeCode(
  request: AnalyzeRequest,
): Promise<AnalyzeResponse> {
  const response = await fetch(`${API_URL}/analyze`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      source_code: request.source_code,
      include_tokens: request.include_tokens ?? true,
    }),
  });

  if (!response.ok) {
    throw new Error(await parseError(response));
  }

  return (await response.json()) as AnalyzeResponse;
}