import ply.lex as lex

class PhpLexer:
    
    tokens = (
        # --- TOKENS DE DARWIN DÍAZ ---
        'VARIABLE',
        'INTEGER',
        'FLOAT',
        'STRING',
        'BOOLEAN',
        'COMMENT',
        # --- TOKEN DE CONTROL DE ERRORES ---
        'ERROR'
    )

    # Caracteres a ignorar (espacios y tabulaciones)
    t_ignore = ' \t'

    def __init__(self):
        # Construye el lexer a partir de lo definido dentro de esta clase
        self.lexer = lex.lex(module=self)

    # =========================================================================
    # APORTE DE DARWIN DÍAZ (Variables, Datos Primitivos y Comentarios)
    # =========================================================================

    def t_VARIABLE(self, t):
        r'\$[a-zA-Z_][a-zA-Z0-9_]*'
        t.value = str(t.value)
        return t

    def t_FLOAT(self, t):
        r'-?\d+\.\d+'
        t.value = float(t.value)
        return t

    def t_INTEGER(self, t):
        r'-?\d+'
        t.value = int(t.value)
        return t

    def t_STRING(self, t):
        r'\'.*?\'|\".*?\"'  # Se usa *? para que sea "non-greedy" y no junte múltiples strings en uno solo
        t.value = str(t.value)
        return t

    def t_BOOLEAN(self, t):
        r'true|false|TRUE|FALSE'
        t.value = t.value.lower() == 'true'
        return t

    def t_COMMENT(self, t):
        r'//[^\n]*|\#[^\n]*|/\*[\s\S]*?\*/'
        t.lexer.lineno += t.value.count('\n')
        t.value = str(t.value)
        return t

    # =========================================================================
    # APORTE DE GABRIEL TUMBACO ()
    # =========================================================================
    # Agregar aquí t_OPERATOR, t_KEYWORD, etc.

    # =========================================================================
    # MÉTODOS GLOBALES DE CONTROL
    # =========================================================================

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        t.type = 'ERROR'
        t.value = f"Illegal character '{t.value[0]}' in line {t.lexer.lineno}"
        t.lexer.skip(1)
        return t

    # Métodos auxiliares para interactuar desde el main.py
    def input(self, text):
        self.lexer.input(text)

    def token(self):
        return self.lexer.token()