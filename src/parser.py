import ply.yacc as yacc
from lexer import PhpLexer

class PhpParser:
    
    def __init__(self):
        self.lexer = PhpLexer()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self)

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
    # APORTE DE DARWIN DÍAZ: ASIGNACIÓN SIMPLE Y ARREGLOS INDEXADOS
    # =========================================================================

    def p_simple_declaration(self, p):
        '''simple_declaration : VARIABLE ASSIGN expression SEMICOLON
                              | VARIABLE ASSIGN array_declaration SEMICOLON'''
        pass

    def p_array_declaration(self, p):
        '''array_declaration : LBRACKET element_list RBRACKET'''
        pass

    def p_element_list(self, p):
        '''element_list : element_list COMMA expression
                        | expression
                        | empty'''
        pass

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
                      | term'''
        pass

    def p_term(self, p):
        '''term : term TIMES factor
                | term DIVIDE factor
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
            print(f"Error de sintaxis 'Hubo un error, papus' en el token '{p.value}' (Línea {p.lineno})")
        else:
            print("Error de sintaxis: Fin de archivo inesperado (EOF).")

    def parse(self, text):
        return self.parser.parse(text, lexer=self.lexer.lexer)

if __name__ == '__main__':
    php_parser = PhpParser()
    while True:
        try:
            s = input('php-parser > ')
        except EOFError:
            break
        if not s: 
            continue
        result = php_parser.parse(s)
        print("Resultado del análisis:", result)