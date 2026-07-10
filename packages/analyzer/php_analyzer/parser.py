import ply.yacc as yacc

from .lexer import PhpLexer
from .models import AnalysisError
from .semantic import SemanticAnalyzer


class PhpParser:
    precedence = (
        ("left", "OR", "AND"),
        ("nonassoc", "GT", "LT", "EQ", "GE", "LE", "NEQ"),
        ("left", "PLUS", "MINUS"),
        ("left", "TIMES", "DIVIDE", "MODULO"),
        ("right", "NOT"),
        ("right", "UMINUS"),
    )

    def __init__(self):
        self.lexer = PhpLexer()
        self.tokens = self.lexer.tokens
        self.syntactic_errors: list[AnalysisError] = []
        self.semantic_errors: list[AnalysisError] = []
        self.semantic = SemanticAnalyzer(self.semantic_errors)
        self.parser = yacc.yacc(
            module=self,
            write_tables=False,
            debug=False,
            errorlog=yacc.NullLogger(),
        )

    def reset_state(self):
        self.syntactic_errors.clear()
        self.semantic_errors.clear()
        self.semantic = SemanticAnalyzer(self.semantic_errors)
        self.lexer.lexer.lineno = 1

    def p_program(self, p):
        """program : PHP_OPEN statement_list PHP_CLOSE
                   | statement_list"""
        pass

    def p_statement_list(self, p):
        """statement_list : statement_list statement
                          | statement
                          | empty"""
        pass

    def p_statement(self, p):
        """statement : simple_declaration
                     | compound_declaration
                     | while_statement
                     | break_statement
                     | if_statement
                     | echo_statement
                     | function_statement
                     | return_statement
                     | call_function_statement"""
        pass

    def p_block(self, p):
        """block : LBRACE statement_list RBRACE"""
        pass

    def p_empty(self, p):
        """empty :"""
        pass

    def p_enter_loop(self, p):
        """enter_loop :"""
        self.semantic.enter_loop()

    def p_exit_loop(self, p):
        """exit_loop :"""
        self.semantic.exit_loop()

    def p_simple_declaration(self, p):
        """simple_declaration : VARIABLE ASSIGN expression SEMICOLON
                              | VARIABLE ASSIGN array_declaration SEMICOLON"""
        self.semantic.declare_variable(p[1], p.lineno(1), p[3])

    def p_compound_declaration(self, p):
        """compound_declaration : VARIABLE PLUS_ASSIGN expression SEMICOLON
                                | VARIABLE MINUS_ASSIGN expression SEMICOLON"""
        self.semantic.check_variable_usage(p[1], p.lineno(1))
        self.semantic.check_arithmetic_types(
            self.semantic.get_variable_type(p[1]), p[3], p[2], p.lineno(2)
        )

    def p_expression(self, p):
        """expression : expression AND expression
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
                      | factor"""
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 3:
            p[0] = p[2]
        else:
            op = p[2]
            if op in ("+", "-", "*", "/", "%"):
                self.semantic.check_arithmetic_types(p[1], p[3], op, p.lineno(2))
                if p[1] == "float" or p[3] == "float":
                    p[0] = "float"
                elif p[1] == "integer" and p[3] == "integer":
                    p[0] = "integer"
                else:
                    p[0] = p[1]
            else:
                p[0] = "boolean"

    def p_factor(self, p):
        """factor : INTEGER
                  | FLOAT
                  | STRING
                  | TRUE
                  | FALSE
                  | factor_variable
                  | call_function
                  | http_request
                  | LPAREN expression RPAREN"""
        if len(p) == 4:
            p[0] = p[2]
        else:
            type_map = {
                "INTEGER": "integer",
                "FLOAT": "float",
                "STRING": "string",
                "TRUE": "boolean",
                "FALSE": "boolean",
            }
            p[0] = type_map.get(p.slice[1].type, p[1])

    def p_factor_variable(self, p):
        """factor_variable : VARIABLE"""
        self.semantic.check_variable_usage(p[1], p.lineno(1))
        p[0] = self.semantic.get_variable_type(p[1])

    def p_while_statement(self, p):
        """while_statement : WHILE LPAREN expression RPAREN enter_loop block exit_loop"""
        pass

    def p_break_statement(self, p):
        """break_statement : BREAK SEMICOLON"""
        self.semantic.check_break_context(p.lineno(1))

    def p_if_statement(self, p):
        """if_statement : IF LPAREN expression RPAREN block
                        | IF LPAREN expression RPAREN block ELSE block"""
        pass

    def p_array_declaration(self, p):
        """array_declaration : LBRACKET element_list RBRACKET
                             | LBRACKET assoc_element_list RBRACKET
                             | LBRACKET RBRACKET"""
        p[0] = "array"

    def p_element_list(self, p):
        """element_list : element_list COMMA expression
                        | expression"""
        pass

    def p_assoc_element_list(self, p):
        """assoc_element_list : assoc_element_list COMMA assoc_element
                              | assoc_element"""
        pass

    def p_assoc_element(self, p):
        """assoc_element : STRING ARROW expression"""
        pass

    def p_function_statement(self, p):
        """function_statement : FUNCTION ID LPAREN parameter_list RPAREN block"""
        self.semantic.declare_function(p[2], p.lineno(2))

    def p_parameter_list(self, p):
        """parameter_list : parameter_list COMMA VARIABLE
                          | VARIABLE
                          | empty"""
        if len(p) == 4:
            self.semantic.declare_variable(p[3], p.lineno(3))
        elif len(p) == 2 and p[1] is not None:
            self.semantic.declare_variable(p[1], p.lineno(1))

    def p_return_statement(self, p):
        """return_statement : RETURN expression SEMICOLON"""
        pass

    def p_function_identifier(self, p):
        """function_identifier : ID
                               | READLINE"""
        pass

    def p_call_function(self, p):
        """call_function : function_identifier LPAREN argument_list RPAREN"""
        pass

    def p_call_function_statement(self, p):
        """call_function_statement : call_function SEMICOLON"""
        pass

    def p_argument_list(self, p):
        """argument_list : argument_list COMMA expression
                         | expression
                         | empty"""
        pass

    def p_echo_statement(self, p):
        """echo_statement : ECHO expression SEMICOLON"""
        pass

    def p_http_request(self, p):
        """http_request : POST LBRACKET STRING RBRACKET"""
        p[0] = "string"

    def p_error(self, p):
        if p:
            self.syntactic_errors.append(
                AnalysisError(
                    phase="syntactic",
                    line=p.lineno,
                    code="SYN_UNEXPECTED_TOKEN",
                    message=f"Error de sintaxis: Problemas con el token '{p.value}' (Linea {p.lineno})",
                )
            )
        else:
            self.syntactic_errors.append(
                AnalysisError(
                    phase="syntactic",
                    line=0,
                    code="SYN_UNEXPECTED_EOF",
                    message="Error de sintaxis: Fin de archivo inesperado (EOF).",
                )
            )

    def parse(self, text: str):
        self.reset_state()
        self.parser.parse(text, lexer=self.lexer.lexer)
        return self.syntactic_errors, self.semantic_errors
