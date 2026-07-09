import type { TokenInfo } from "../types/analysis";

interface TokenTableProps {
  tokens: TokenInfo[];
}

export function TokenTable({ tokens }: TokenTableProps) {
  if (tokens.length === 0) {
    return <p className="text-xs text-muted">No hay tokens para mostrar.</p>;
  }

  return (
    <div className="max-h-64 overflow-auto rounded border border-border bg-panelAlt">
      <table className="w-full border-collapse text-xs font-mono">
        <thead className="sticky top-0 bg-panel">
          <tr className="text-left text-muted">
            <th className="px-3 py-2">Token</th>
            <th className="px-3 py-2">Lexema</th>
            <th className="px-3 py-2">Linea</th>
            <th className="px-3 py-2">Columna</th>
          </tr>
        </thead>
        <tbody>
          {tokens.map((token, index) => (
            <tr key={`${token.type}-${index}`} className="border-t border-border/60">
              <td className="px-3 py-2 text-accent">{token.type}</td>
              <td className="px-3 py-2 text-text">{token.lexeme}</td>
              <td className="px-3 py-2 text-muted">{token.line}</td>
              <td className="px-3 py-2 text-muted">{token.column}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
