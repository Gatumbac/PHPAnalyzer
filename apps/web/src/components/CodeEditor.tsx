import Editor from "@monaco-editor/react";
import type { ThemeMode } from "../store/uiStore";

interface CodeEditorProps {
  value: string;
  onChange: (value: string) => void;
  themeMode: ThemeMode;
}

export function CodeEditor({ value, onChange, themeMode }: CodeEditorProps) {
  return (
    <div className="h-full rounded-lg border border-border bg-panel shadow-glow">
      <Editor
        height="100%"
        defaultLanguage="php"
        language="php"
        value={value}
        onChange={(nextValue) => onChange(nextValue ?? "")}
        options={{
          minimap: { enabled: false },
          fontFamily: "JetBrains Mono, Fira Code, monospace",
          fontSize: 14,
          lineNumbersMinChars: 3,
          scrollBeyondLastLine: false,
          wordWrap: "on",
          automaticLayout: true,
          tabSize: 2,
          padding: { top: 12, bottom: 12 },
        }}
        theme={themeMode === "dark" ? "vs-dark" : "vs"}
      />
    </div>
  );
}
