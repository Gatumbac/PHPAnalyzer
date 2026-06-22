import ply.yacc as yacc
from src.lexer import PhpLexer

# =========================================================================
# APORTE DE GABRIEL TUMBACO: PRECEDENCIA (4.2.2)
# =========================================================================

class PhpParser:

    precedence = (
        ('left', 'OR', 'AND'),
        ('nonassoc', 'GT', 'LT', 'EQ', 'GE', 'LE', 'NEQ'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE', 'MODULO'),
        ('right', 'NOT'),
        ('right', 'UMINUS'),
    )

    def __init__(self):
        self.lexer = PhpLexer()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self)
        self.errors = []

    # =========================================================================
    # REGLAS ESTRUCTURALES (Base del Programa)
    # =========================================================================

    def p_program(self, p):
        '''program : PHP_OPEN statement_list PHP_CLOSE
                    | statement_list'''
        pass

    def p_statement_list(self, p):
        '''statement_list : statement_list statement
                        | statement
                        | empty'''
        pass

    def p_statement(self, p):
        '''statement : simple_declaration
                    | compound_declaration
                    | while_statement
                    | break_statement
                    | if_statement
                    | echo_statement
                    | function_statement
                    | return_statement
                    | call_function_statement'''
        pass

    def p_block(self, p):
        '''block : LBRACE statement_list RBRACE'''
        pass

    def p_empty(self, p):
        '''empty :'''
        pass

    # =========================================================================
    # DECLARACIÓN DE VARIABLES (4.2.1)
    # =========================================================================

    # =========================================================================
    # APORTE DE DARWIN DÍAZ: ASIGNACIÓN SIMPLE
    # =========================================================================

    def p_simple_declaration(self, p):
        '''simple_declaration : VARIABLE ASSIGN expression SEMICOLON
                              | VARIABLE ASSIGN array_declaration SEMICOLON'''
        pass

    # =========================================================================
    # APORTE DE GABRIEL TUMBACO: ASIGNACIÓN COMPUESTA
    # =========================================================================

    def p_compound_declaration(self, p):
        '''compound_declaration : VARIABLE PLUS_ASSIGN expression SEMICOLON
                                | VARIABLE MINUS_ASSIGN expression SEMICOLON'''
        pass

    # =========================================================================
    # EXPRESIONES MATEMÁTICAS, LÓGICAS Y PRIMITIVOS (4.2.2 y 4.2.3)
    # Aporte de Darwin Díaz y Gabriel Tumbaco
    # 4.2.2 -> Operaciones básicas, operaciones con agrupaciones y precedencia
    # 4.3.3 -> Operadores relacionales y operadores lógicos (Combinación de condiciones)
    # Precedencia se resuelve mediante la tupla "precedence"
    # =========================================================================

    def p_expression(self, p):
        '''expression : expression AND expression
                    | expression OR expression
                    | expression PLUS expression
                    | expression MINUS expression
                    | expression TIMES expression
                    | expression DIVIDE expression
                    | expression MODULO expression
                    | MINUS expression %prec UMINUS
                    | expression GT expression
                    | expression LT expression
                    | expression EQ expression
                    | expression GE expression
                    | expression LE expression
                    | expression NEQ expression
                    | NOT expression
                    | factor'''
        pass

    def p_factor(self, p):
        '''factor : INTEGER
                | FLOAT
                | STRING
                | TRUE
                | FALSE
                | VARIABLE
                | call_function
                | http_request
                | LPAREN expression RPAREN'''
        pass

    # =========================================================================
    # ESTRUCTURAS DE CONTROL (4.2.4)
    # =========================================================================

    # =========================================================================
    # APORTE DE DARWIN DÍAZ: BUCLE WHILE Y BREAK
    # =========================================================================

    def p_while_statement(self, p):
        '''while_statement : WHILE LPAREN expression RPAREN block'''
        pass

    def p_break_statement(self, p):
        '''break_statement : BREAK SEMICOLON'''
        pass

    # =========================================================================
    # APORTE DE GABRIEL TUMBACO: CONDICIONAL IF - ELSE
    # =========================================================================

    def p_if_statement(self, p):
        '''if_statement : IF LPAREN expression RPAREN block
                        | IF LPAREN expression RPAREN block ELSE block'''
        pass

    # =========================================================================
    # ESTRUCTURAS DE DATOS (4.2.5)
    # =========================================================================

    # =========================================================================
    # APORTE DE DARWIN DÍAZ: ASIGNACIÓN DE ARREGLOS INDEXADOS (4.2.5)
    # =========================================================================

    def p_array_declaration(self, p):
        '''array_declaration : LBRACKET element_list RBRACKET
                            | LBRACKET assoc_element_list RBRACKET
                            | LBRACKET RBRACKET'''
        pass

    def p_element_list(self, p):
        '''element_list : element_list COMMA expression
                        | expression'''
        pass

    # =========================================================================
    # APORTE DE GABRIEL TUMBACO: ASIGNACIÓN DE ARREGLOS ASOCIATIVOS (4.2.5)
    # =========================================================================

    def p_assoc_element_list(self, p):
        '''assoc_element_list : assoc_element_list COMMA assoc_element
                                | assoc_element'''
        pass

    def p_assoc_element(self, p):
        '''assoc_element : STRING ARROW expression'''
        pass

    # =========================================================================
    # FUNCIONES (4.2.6)
    # =========================================================================

    # =========================================================================
    # APORTE DE DARWIN DÍAZ: FUNCIONES CON RETORNO
    # =========================================================================

    def p_function_statement(self, p):
        '''function_statement : FUNCTION ID LPAREN parameter_list RPAREN block'''
        pass

    def p_parameter_list(self, p):
        '''parameter_list : parameter_list COMMA VARIABLE
                          | VARIABLE
                          | empty'''
        pass

    def p_return_statement(self, p):
        '''return_statement : RETURN expression SEMICOLON'''
        pass

    # =========================================================================
    # APORTE DE GABRIEL TUMBACO: LLAMADA A FUNCIONES
    # =========================================================================

    def p_function_identifier(self, p):
        '''function_identifier : ID
                                | READLINE'''
        pass

    def p_call_function(self, p):
        '''call_function : function_identifier LPAREN argument_list RPAREN'''
        pass

    def p_call_function_statement(self, p):
        '''call_function_statement : call_function SEMICOLON'''
        pass

    def p_argument_list(self, p):
        '''argument_list : argument_list COMMA expression
                         | expression
                         | empty'''
        pass

    # =========================================================================
    # IMPRESION Y SOLICITUD DE DATOS (4.2.7)
    # =========================================================================

    # =========================================================================
    # APORTE DE DARWIN DÍAZ: IMPRESIÓN (ECHO)
    # =========================================================================

    def p_echo_statement(self, p):
        '''echo_statement : ECHO expression SEMICOLON'''
        pass

    # =========================================================================
    # APORTE DE GABRIEL TUMBACO: SOLICITUD DE DATOS (PETICION HTTP)
    # PHP soporta la función readline que lee datos desde la consola
    # El soporte para esta función se dió en la sección de Funciones
    # =========================================================================

    def p_http_request(self, p):
        '''http_request : POST LBRACKET STRING RBRACKET'''
        pass

    # =========================================================================
    # MANEJO DE ERRORES SINTÁCTICOS
    # =========================================================================

    def p_error(self, p):
        if p:
            error_msg = f"Error de sintaxis: Problemas con el token '{p.value}' (Línea {p.lineno})"
        else:
            error_msg = "Error de sintaxis: Fin de archivo inesperado (EOF)."
        print(error_msg)
        self.errors.append(error_msg)

    def parse(self, text):
        self.errors = []
        self.parser.parse(text, lexer=self.lexer.lexer)
        return self.errors
