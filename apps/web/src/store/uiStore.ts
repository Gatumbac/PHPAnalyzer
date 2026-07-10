import { create } from "zustand";

import type { AnalyzeResponse } from "../types/analysis";

export type SectionKey = "lexico" | "sintactico" | "semantico";
export type ThemeMode = "light" | "dark";

const DEFAULT_SOURCE = `<?php\n$nombre = "Ana";\n$edad = 20;\nif ($edad >= 18) {\n    echo "Mayor de edad";\n} else {\n    echo "Menor de edad";\n}\n?>`;
const THEME_STORAGE_KEY = "phpanalyzer_theme_mode";

interface UIState {
  sourceCode: string;
  includeTokens: boolean;
  themeMode: ThemeMode;
  activeSection: SectionKey | null;
  sectionsOpen: Record<SectionKey, boolean>;
  statusMessage: string;
  healthMessage: string;
  lastResult: AnalyzeResponse | null;
  setSourceCode: (value: string) => void;
  setIncludeTokens: (value: boolean) => void;
  setThemeMode: (mode: ThemeMode) => void;
  toggleTheme: () => void;
  hydrateTheme: () => void;
  setActiveSection: (section: SectionKey | null) => void;
  toggleSection: (section: SectionKey) => void;
  setStatusMessage: (value: string) => void;
  setHealthMessage: (value: string) => void;
  setResult: (result: AnalyzeResponse | null) => void;
  openSectionForStatus: (status: AnalyzeResponse["status"]) => void;
}

function resolveInitialTheme(): ThemeMode {
  if (typeof window === "undefined") {
    return "light";
  }

  const savedTheme = window.localStorage.getItem(THEME_STORAGE_KEY);
  if (savedTheme === "light" || savedTheme === "dark") {
    return savedTheme;
  }

  if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
    return "dark";
  }
  return "light";
}

function applyThemeToDocument(mode: ThemeMode): void {
  if (typeof document === "undefined") {
    return;
  }
  document.documentElement.setAttribute("data-theme", mode);
}

export const useUIStore = create<UIState>((set) => ({
  sourceCode: DEFAULT_SOURCE,
  includeTokens: true,
  themeMode: "light",
  activeSection: null,
  sectionsOpen: {
    lexico: false,
    sintactico: false,
    semantico: false,
  },
  statusMessage: "Esperando código...",
  healthMessage: "Verificando API...",
  lastResult: null,
  setSourceCode: (value) => set({ sourceCode: value }),
  setIncludeTokens: (value) => set({ includeTokens: value }),
  setThemeMode: (mode) => {
    applyThemeToDocument(mode);
    if (typeof window !== "undefined") {
      window.localStorage.setItem(THEME_STORAGE_KEY, mode);
    }
    set({ themeMode: mode });
  },
  toggleTheme: () =>
    set((state) => {
      const nextTheme = state.themeMode === "light" ? "dark" : "light";
      applyThemeToDocument(nextTheme);
      if (typeof window !== "undefined") {
        window.localStorage.setItem(THEME_STORAGE_KEY, nextTheme);
      }
      return { themeMode: nextTheme };
    }),
  hydrateTheme: () => {
    const initialMode = resolveInitialTheme();
    applyThemeToDocument(initialMode);
    if (typeof window !== "undefined") {
      window.localStorage.setItem(THEME_STORAGE_KEY, initialMode);
    }
    set({ themeMode: initialMode });
  },
  setActiveSection: (section) => set({ activeSection: section }),
  toggleSection: (section) =>
    set((state) => ({
      sectionsOpen: {
        ...state.sectionsOpen,
        [section]: !state.sectionsOpen[section],
      },
    })),
  setStatusMessage: (value) => set({ statusMessage: value }),
  setHealthMessage: (value) => set({ healthMessage: value }),
  setResult: (result) => set({ lastResult: result }),
  openSectionForStatus: (status) =>
    set((state) => {
      const base = {
        ...state.sectionsOpen,
        lexico: true,
      };
      if (status === "success") {
        return {
          sectionsOpen: base,
          activeSection: "lexico",
        };
      }
      if (status === "syntax_error") {
        return {
          sectionsOpen: {
            ...base,
            sintactico: true,
          },
          activeSection: "sintactico",
        };
      }
      if (status === "semantic_error") {
        return {
          sectionsOpen: {
            ...base,
            semantico: true,
          },
          activeSection: "semantico",
        };
      }
      return {
        sectionsOpen: {
          ...base,
          sintactico: true,
          semantico: true,
        },
        activeSection: "sintactico",
      };
    }),
}));
