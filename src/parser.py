import ply.yacc as yacc
from src.lexer import PhpLexer

class PhpParser:

    def __init__(self):
        self.lexer = PhpLexer()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self)
        self.errors = []

    # =========================================================================
    # REGLAS ESTRUCTURALES (Para soportar múltiples líneas y bloques)
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
                    | echo_statement
                    | function_statement
                    | return_statement'''
        pass

    def p_block(self, p):
        '''block : LBRACE statement_list RBRACE'''
        pass

    # =========================================================================
    # APORTE DE DARWIN DÍAZ: ASIGNACIÓN SIMPLE
    # =========================================================================

    def p_simple_declaration(self, p):
        '''simple_declaration : VARIABLE ASSIGN expression SEMICOLON
                              | VARIABLE ASSIGN array_declaration SEMICOLON
                              | VARIABLE ASSIGN assoc_array_declaration SEMICOLON'''
        pass

    # =========================================================================
    # APORTE DE GABRIEL TUMBACO: ASIGNACIÓN COMPUESTA
    # =========================================================================

    def p_compound_declaration(self, p):
        '''compound_declaration : VARIABLE PLUS_ASSIGN expression SEMICOLON
                                | VARIABLE MINUS_ASSIGN expression SEMICOLON'''
        pass

    # =========================================================================
    # APORTE DE DARWIN DÍAZ: ASIGNACIÓN DE ARREGLOS INDEXADOS
    # =========================================================================

    def p_array_declaration(self, p):
        '''array_declaration : LBRACKET element_list RBRACKET'''
        pass

    def p_element_list(self, p):
        '''element_list : element_list COMMA expression
                        | expression
                        | empty'''
        pass

    # =========================================================================
    # APORTE DE GABRIEL TUMBACO: ASIGNACIÓN DE ARREGLOS ASOCIATIVOS
    # =========================================================================

    def p_assoc_array_declaration(self, p):
        '''assoc_array_declaration : LBRACKET assoc_element_list RBRACKET'''
        pass

    def p_assoc_element_list(self, p):
        '''assoc_element_list : assoc_element_list COMMA assoc_element
                                | assoc_element
                                | empty'''

    def p_assoc_element(self, p):
        '''assoc_element : STRING ARROW expression'''

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
    # APORTE DE DARWIN DÍAZ: FUNCIONES CON RETORNO Y EXPRESIONES DE LLAMADA
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
    # APORTE DE DARWIN DÍAZ: IMPRESIÓN (ECHO)
    # =========================================================================

    def p_echo_statement(self, p):
        '''echo_statement : ECHO expression SEMICOLON'''
        pass

    # =========================================================================
    # EXPRESIONES MATEMÁTICAS, LÓGICAS Y PRIMITIVOS
    # =========================================================================

    def p_expression(self, p):
        '''expression : expression PLUS term
                      | expression MINUS term
                      | expression GT term
                      | expression LT term
                      | expression EQ term
                      | expression GE term
                      | expression LE term
                      | expression NEQ term
                      | expression AND term
                      | expression OR term
                      | NOT expression
                      | term'''
        pass

    def p_term(self, p):
        '''term : term TIMES factor
                | term DIVIDE factor
                | term MODULO factor
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
                  | LPAREN expression RPAREN'''
        pass

    def p_call_function(self, p):
        '''call_function : ID LPAREN argument_list RPAREN'''
        pass

    def p_argument_list(self, p):
        '''argument_list : argument_list COMMA expression
                         | expression
                         | empty'''
        pass

    def p_empty(self, p):
        '''empty :'''
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
