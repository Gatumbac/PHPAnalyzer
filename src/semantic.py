from src.utils.symbol_table import SymbolTable 

class SemanticAnalyzer:
    
    def __init__(self, error_list):
        self.symbol_table = SymbolTable()
        self.errors = error_list
        self.loop_depth = 0
    
    # =========================================================================
    # APORTE DE DARWIN DÍAZ
    # =========================================================================
    
    def declare_variable(self, name, lineno, data_type=None):
        self.symbol_table.put(name, {'type': data_type, 'lineno': lineno})
        
    def check_variable_usage(self, name, lineno):
        if not self.symbol_table.exists(name):
            error_msg = f"Error Semántico en línea {lineno}: La variable '{name}' no ha sido inicializada."
            print(error_msg)
            self.errors.append(error_msg)
    
    def enter_loop(self):
        self.loop_depth += 1
    
    def exit_loop(self):
        self.loop_depth -= 1
    
    def check_break_context(self, lineno):
        if self.loop_depth == 0:
            error_msg = f"Error Semántico en línea {lineno}: 'break' no puede usarse fuera de un bucle."
            print(error_msg)
            self.errors.append(error_msg)

    # =========================================================================
    # APORTE DE GABRIEL TUMBACO
    # =========================================================================

    def get_variable_type(self, name):
        entry = self.symbol_table.get(name)
        if entry:
            return entry.get('type')
        return None

    def check_arithmetic_types(self, left_type, right_type, operator, lineno):
        if left_type is None or right_type is None:
            return
        numeric_types = {'integer', 'float'}
        if left_type not in numeric_types or right_type not in numeric_types:
            error_msg = f"Error Semántico en línea {lineno}: Tipos incompatibles para la operación \"{operator}\"."
            print(error_msg)
            self.errors.append(error_msg)

    def declare_function(self, name, lineno):
        func_key = f"__func_{name}"
        if self.symbol_table.exists(func_key):
            error_msg = f"Error Semántico en línea {lineno}: La función '{name}' ya ha sido declarada previamente."
            print(error_msg)
            self.errors.append(error_msg)
        else:
            self.symbol_table.put(func_key, {'type': 'function', 'lineno': lineno})