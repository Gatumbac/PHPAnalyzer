from .models import AnalysisError
from .symbol_table import SymbolTable


class SemanticAnalyzer:
    def __init__(self, error_list: list[AnalysisError]):
        self.symbol_table = SymbolTable()
        self.errors = error_list
        self.loop_depth = 0

    def declare_variable(self, name, lineno, data_type=None):
        self.symbol_table.put(name, {"type": data_type, "lineno": lineno})

    def check_variable_usage(self, name, lineno):
        if not self.symbol_table.exists(name):
            self.errors.append(
                AnalysisError(
                    phase="semantic",
                    line=lineno,
                    code="SEM_UNINITIALIZED_VARIABLE",
                    message=f"Error Semantico en linea {lineno}: La variable '{name}' no ha sido inicializada.",
                )
            )

    def enter_loop(self):
        self.loop_depth += 1

    def exit_loop(self):
        self.loop_depth -= 1

    def check_break_context(self, lineno):
        if self.loop_depth == 0:
            self.errors.append(
                AnalysisError(
                    phase="semantic",
                    line=lineno,
                    code="SEM_BREAK_OUTSIDE_LOOP",
                    message=f"Error Semantico en linea {lineno}: 'break' no puede usarse fuera de un bucle.",
                )
            )

    def get_variable_type(self, name):
        entry = self.symbol_table.get(name)
        if entry:
            return entry.get("type")
        return None

    def check_arithmetic_types(self, left_type, right_type, operator, lineno):
        if left_type is None or right_type is None:
            return
        numeric_types = {"integer", "float"}
        if left_type not in numeric_types or right_type not in numeric_types:
            self.errors.append(
                AnalysisError(
                    phase="semantic",
                    line=lineno,
                    code="SEM_INCOMPATIBLE_ARITHMETIC_TYPES",
                    message=f'Error Semantico en linea {lineno}: Tipos incompatibles para la operacion "{operator}".',
                )
            )

    def declare_function(self, name, lineno):
        func_key = f"__func_{name}"
        if self.symbol_table.exists(func_key):
            self.errors.append(
                AnalysisError(
                    phase="semantic",
                    line=lineno,
                    code="SEM_FUNCTION_REDECLARATION",
                    message=f"Error Semantico en linea {lineno}: La funcion '{name}' ya ha sido declarada previamente.",
                )
            )
        else:
            self.symbol_table.put(func_key, {"type": "function", "lineno": lineno})
