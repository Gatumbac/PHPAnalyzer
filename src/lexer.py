import ply.lex as lex

class PhpLexer:

    reserved = {
        'if': 'IF',
        'else': 'ELSE',
        'while': 'WHILE',
        'break': 'BREAK',
        'function': 'FUNCTION',
        'return': 'RETURN',
        'echo': 'ECHO',
        'true': 'TRUE',
        'false': 'FALSE',
    }

    tokens = [
        # --- TOKENS DE DARWIN DÍAZ ---
        'VARIABLE',
        'INTEGER',
        'FLOAT',
        'STRING',
        'COMMENT',
        # --- TOKENS DE GABRIEL TUMBACO ---
        'ID',
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'MODULO',
        'EQ',
        'NEQ',
        'LE',
        'GE',
        'LT',
        'GT',
        'AND',
        'OR',
        'NOT',
        'ASSIGN',
        'PLUS_ASSIGN',
        'MINUS_ASSIGN',
        'SEMICOLON',
        'LBRACE',
        'RBRACE',
        'LPAREN',
        'RPAREN',
        'LBRACKET',
        'RBRACKET',
        'COMMA',
        'COLON',
        'ARROW',
        'PHP_OPEN',
        'PHP_CLOSE',
        # --- TOKEN DE CONTROL DE ERRORES ---
        'ERROR'
    ] + list(reserved.values())

    # Caracteres a ignorar (espacios y tabulaciones)
    t_ignore = ' \t'

    # =========================================================================
    # APORTE DE GABRIEL TUMBACO (Operadores, Palabras Reservadas, Delimitadores)
    # =========================================================================

    # Operadores multi-carácter (reglas string, PLY ordena por longitud decreciente)
    t_ARROW        = r'=>'
    t_PLUS_ASSIGN  = r'\+='
    t_MINUS_ASSIGN = r'-='
    t_EQ           = r'=='
    t_NEQ          = r'!='
    t_LE           = r'<='
    t_GE           = r'>='
    t_AND          = r'&&'
    t_OR           = r'\|\|'

    # Operadores de un solo carácter (reglas string)
    t_PLUS    = r'\+'
    t_MINUS   = r'-'
    t_TIMES   = r'\*'
    t_DIVIDE  = r'/'
    t_MODULO  = r'%'
    t_LT      = r'<'
    t_GT      = r'>'
    t_NOT     = r'!'
    t_ASSIGN  = r'='

    # Delimitadores (reglas string)
    t_SEMICOLON = r';'
    t_LBRACE    = r'\{'
    t_RBRACE    = r'\}'
    t_LPAREN    = r'\('
    t_RPAREN    = r'\)'
    t_LBRACKET  = r'\['
    t_RBRACKET  = r'\]'
    t_COMMA     = r','
    t_COLON     = r':'

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
        r'\d+\.\d+'
        t.value = float(t.value)
        return t

    def t_INTEGER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_STRING(self, t):
        r'\'.*?\'|\".*?\"'  # Se usa *? para que sea "non-greedy" y no junte múltiples strings en uno solo
        t.value = str(t.value)
        return t

    def t_COMMENT(self, t):
        r'//[^\n]*|\#[^\n]*|/\*[\s\S]*?\*/'
        t.lexer.lineno += t.value.count('\n')
        pass

    # =========================================================================
    # APORTE DE GABRIEL TUMBACO (Identificadores y Palabras Reservadas)
    # =========================================================================

    def t_PHP_OPEN(self, t):
        r'<\?php'
        return t

    def t_PHP_CLOSE(self, t):
        r'\?>'
        return t

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = self.reserved.get(t.value, 'ID')
        return t

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
