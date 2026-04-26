from jacktoken import Token, TokenType
from xml_generator import token_to_xml
from typing import List

OPS = {'+', '-', '*', '/', '&', '|', '<', '>', '='}
UNARY_OPS = {'-', '~'}


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0       # índice do token atual
        self.xml_output = []   # lista para construir o XML
        self.indent_level = 0  # nível de indentação XML

    def peek(self) -> Token:
        """Retorna o token atual sem avançar."""
        if self.current < len(self.tokens):
            return self.tokens[self.current]
        return None

    def peek_next(self) -> Token:
        """Retorna o próximo token (lookahead de 2)."""
        if self.current + 1 < len(self.tokens):
            return self.tokens[self.current + 1]
        return None

    def advance(self) -> Token:
        """Avança para o próximo token e retorna o atual."""
        token = self.peek()
        self.current += 1
        return token

    def match(self, expected_type: TokenType) -> Token:
       """Verifica se o token atual é do tipo esperado e avança."""
       token = self.peek()
       if token is None:
           raise SyntaxError(
               f"Erro de sintaxe: Esperado {expected_type}, encontrado fim do arquivo"
           )
       if token.type == expected_type:
           self.write_token(token)
           self.advance()
           return token
       raise SyntaxError(
           f"Erro de sintaxe na linha {token.line}: "
           f"Esperado {expected_type}, encontrado '{token.lexeme}'"
       )

    def match_keyword(self, *types: TokenType) -> Token:
        """Verifica se o token atual é uma das keywords esperadas e avança."""
        token = self.peek()
        if token and token.type in types:
            self.write_token(token)
            self.advance()
            return token
        raise SyntaxError(
            f"Erro de sintaxe na linha {token.line}: "
            f"Esperado um de {types}, encontrado '{token.lexeme}'"
        )

    def match_type(self) -> Token:
        """Verifica se o token atual é um tipo válido (int, char, boolean ou className)."""
        token = self.peek()
        if token and token.type in (TokenType.INT, TokenType.CHAR, TokenType.BOOLEAN):
            self.write_token(token)
            self.advance()
            return token
        elif token and token.type == TokenType.IDENT:
            self.write_token(token)
            self.advance()
            return token
        raise SyntaxError(
            f"Erro de sintaxe na linha {token.line}: "
            f"Tipo esperado, encontrado '{token.lexeme}'"
        )

    def match_symbol(self, symbol: str) -> Token:
        """Verifica se o token atual é o símbolo esperado e avança."""
        token = self.peek()
        if token is None:
            raise SyntaxError(
                f"Erro de sintaxe: Esperado '{symbol}', encontrado fim do arquivo"
            )
        if token.lexeme == symbol:
            self.write_token(token)
            self.advance()
            return token
        raise SyntaxError(
            f"Erro de sintaxe na linha {token.line}: "
            f"Esperado '{symbol}', encontrado '{token.lexeme}'"
        )

    # --- Helpers de XML ---

    def open_tag(self, tag_name: str):
        """Abre uma tag XML com indentação."""
        indent = "  " * self.indent_level
        self.xml_output.append(f"{indent}<{tag_name}>")
        self.indent_level += 1

    def close_tag(self, tag_name: str):
        """Fecha uma tag XML com indentação."""
        self.indent_level -= 1
        indent = "  " * self.indent_level
        self.xml_output.append(f"{indent}</{tag_name}>")

    def write_token(self, token: Token):
        """Escreve o token no XML com indentação."""
        indent = "  " * self.indent_level
        self.xml_output.append(f"{indent}{token_to_xml(token)}")

    def get_xml(self) -> str:
        """Retorna o XML completo como string."""
        return "\n".join(self.xml_output)

    # ===========================
    # Fase 4: Estrutura de Classe
    # ===========================

    def parse_class(self):
        """class → 'class' className '{' classVarDec* subroutineDec* '}'"""
        self.open_tag("class")
        self.match(TokenType.CLASS)
        self.match(TokenType.IDENT)    # className
        self.match(TokenType.LBRACE)   # {

        while self.peek() and self.peek().type in (TokenType.STATIC, TokenType.FIELD):
            self.parse_class_var_dec()

        while self.peek() and self.peek().type in (TokenType.CONSTRUCTOR, TokenType.FUNCTION, TokenType.METHOD):
            self.parse_subroutine()

        self.match(TokenType.RBRACE)   # }
        self.close_tag("class")

    def parse_class_var_dec(self):
        """classVarDec → ('static'|'field') type varName (',' varName)* ';'"""
        self.open_tag("classVarDec")
        self.match_keyword(TokenType.STATIC, TokenType.FIELD)
        self.match_type()
        self.match(TokenType.IDENT)
        while self.peek() and self.peek().type == TokenType.COMMA:
            self.match(TokenType.COMMA)
            self.match(TokenType.IDENT)
        self.match(TokenType.SEMICOLON)
        self.close_tag("classVarDec")

    def parse_subroutine(self):
        """subroutineDec → ('constructor'|'function'|'method') ('void'|type) subroutineName '(' parameterList ')' subroutineBody"""
        self.open_tag("subroutineDec")
        self.match_keyword(TokenType.CONSTRUCTOR, TokenType.FUNCTION, TokenType.METHOD)

        if self.peek().type == TokenType.VOID:
            self.match(TokenType.VOID)
        else:
            self.match_type()

        self.match(TokenType.IDENT)      # subroutineName
        self.match(TokenType.LPAREN)     # (
        self.parse_parameter_list()
        self.match(TokenType.RPAREN)     # )
        self.parse_subroutine_body()
        self.close_tag("subroutineDec")

    def parse_parameter_list(self):
        """parameterList → ((type varName) (',' type varName)*)?"""
        self.open_tag("parameterList")
        if self.peek() and self.peek().type != TokenType.RPAREN:
            self.match_type()
            self.match(TokenType.IDENT)
            while self.peek() and self.peek().type == TokenType.COMMA:
                self.match(TokenType.COMMA)
                self.match_type()
                self.match(TokenType.IDENT)
        self.close_tag("parameterList")

    def parse_subroutine_body(self):
        """subroutineBody → '{' varDec* statements '}'"""
        self.open_tag("subroutineBody")
        self.match(TokenType.LBRACE)
        while self.peek() and self.peek().type == TokenType.VAR:
            self.parse_var_dec()
        self.parse_statements()
        self.match(TokenType.RBRACE)
        self.close_tag("subroutineBody")

    def parse_var_dec(self):
        """varDec → 'var' type varName (',' varName)* ';'"""
        self.open_tag("varDec")
        self.match(TokenType.VAR)
        self.match_type()
        self.match(TokenType.IDENT)
        while self.peek() and self.peek().type == TokenType.COMMA:
            self.match(TokenType.COMMA)
            self.match(TokenType.IDENT)
        self.match(TokenType.SEMICOLON)
        self.close_tag("varDec")

    # ===========================
    # Statements
    # ===========================

    def parse_statements(self):
        """statements → statement*"""
        self.open_tag("statements")
        stmt_types = (TokenType.LET, TokenType.IF,
                      TokenType.WHILE, TokenType.DO, TokenType.RETURN)
        while self.peek() and self.peek().type in stmt_types:
            self.parse_statement()
        self.close_tag("statements")

    def parse_statement(self):
        """statement → letStatement | ifStatement | whileStatement | doStatement | returnStatement"""
        t = self.peek().type
        if   t == TokenType.LET:    self.parse_let()
        elif t == TokenType.IF:     self.parse_if()
        elif t == TokenType.WHILE:  self.parse_while()
        elif t == TokenType.DO:     self.parse_do()
        elif t == TokenType.RETURN: self.parse_return()

    def parse_let(self):
        """letStatement → 'let' varName ('[' expression ']')? '=' expression ';'"""
        self.open_tag("letStatement")
        self.match(TokenType.LET)
        self.match(TokenType.IDENT)

        if self.peek() and self.peek().type == TokenType.LBRACKET:
            self.match(TokenType.LBRACKET)
            self.parse_expression()
            self.match(TokenType.RBRACKET)

        self.match(TokenType.EQ)
        self.parse_expression()
        self.match(TokenType.SEMICOLON)
        self.close_tag("letStatement")

    def parse_if(self):
        """ifStatement → 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?"""
        self.open_tag("ifStatement")
        self.match(TokenType.IF)
        self.match(TokenType.LPAREN)
        self.parse_expression()
        self.match(TokenType.RPAREN)
        self.match(TokenType.LBRACE)
        self.parse_statements()
        self.match(TokenType.RBRACE)

        if self.peek() and self.peek().type == TokenType.ELSE:
            self.match(TokenType.ELSE)
            self.match(TokenType.LBRACE)
            self.parse_statements()
            self.match(TokenType.RBRACE)

        self.close_tag("ifStatement")

    def parse_while(self):
        """whileStatement → 'while' '(' expression ')' '{' statements '}'"""
        self.open_tag("whileStatement")
        self.match(TokenType.WHILE)
        self.match(TokenType.LPAREN)
        self.parse_expression()
        self.match(TokenType.RPAREN)
        self.match(TokenType.LBRACE)
        self.parse_statements()
        self.match(TokenType.RBRACE)
        self.close_tag("whileStatement")

    def parse_do(self):
        """doStatement → 'do' subroutineCall ';'"""
        self.open_tag("doStatement")
        self.match(TokenType.DO)
        self.parse_subroutine_call()
        self.match(TokenType.SEMICOLON)
        self.close_tag("doStatement")

    def parse_return(self):
        """returnStatement → 'return' expression? ';'"""
        self.open_tag("returnStatement")
        self.match(TokenType.RETURN)

        if self.peek() and self.peek().type != TokenType.SEMICOLON:
            self.parse_expression()

        self.match(TokenType.SEMICOLON)
        self.close_tag("returnStatement")

    # ===========================
    # Expressions
    # ===========================

    def parse_expression(self):
        """expression → term (op term)*"""
        self.open_tag("expression")
        self.parse_term()

        while self.peek() and self.peek().lexeme in OPS:
            self.write_token(self.advance())  # escreve o operador
            self.parse_term()

        self.close_tag("expression")

    def parse_term(self):
        """term → integerConstant | stringConstant | keywordConstant
               | varName | varName '[' expression ']'
               | subroutineCall | '(' expression ')' | unaryOp term"""
        self.open_tag("term")
        token = self.peek()

        if token.type == TokenType.NUMBER:
            self.match(TokenType.NUMBER)

        elif token.type == TokenType.STRING:
            self.match(TokenType.STRING)

        elif token.type in (TokenType.TRUE, TokenType.FALSE,
                            TokenType.NULL, TokenType.THIS):
            self.match_keyword(TokenType.TRUE, TokenType.FALSE,
                               TokenType.NULL, TokenType.THIS)

        elif token.type == TokenType.LPAREN:
            # '(' expression ')'
            self.match(TokenType.LPAREN)
            self.parse_expression()
            self.match(TokenType.RPAREN)

        elif token.lexeme in UNARY_OPS:
            # unaryOp term
            self.write_token(self.advance())
            self.parse_term()

        elif token.type == TokenType.IDENT:
            next_token = self.peek_next()
            if next_token and next_token.type == TokenType.LBRACKET:
                # varName '[' expression ']'
                self.match(TokenType.IDENT)
                self.match(TokenType.LBRACKET)
                self.parse_expression()
                self.match(TokenType.RBRACKET)
            elif next_token and (next_token.type == TokenType.LPAREN or next_token.type == TokenType.DOT):
                # subroutineCall
                self.parse_subroutine_call()
            else:
                # varName simples
                self.match(TokenType.IDENT)
        else:
            raise SyntaxError(
                f"Termo esperado na linha {token.line}, "
                f"encontrado: '{token.lexeme}'"
            )

        self.close_tag("term")

    def parse_expression_list(self):
        """expressionList → (expression (',' expression)*)?"""
        self.open_tag("expressionList")
        if self.peek() and self.peek().type != TokenType.RPAREN:
            self.parse_expression()
            while self.peek() and self.peek().type == TokenType.COMMA:
                self.match(TokenType.COMMA)
                self.parse_expression()
        self.close_tag("expressionList")

    def parse_subroutine_call(self):
        """subroutineCall → subroutineName '(' expressionList ')'
                          | (className|varName) '.' subroutineName '(' expressionList ')'"""
        self.match(TokenType.IDENT)
        if self.peek() and self.peek().type == TokenType.DOT:
            self.match(TokenType.DOT)
            self.match(TokenType.IDENT)
        self.match(TokenType.LPAREN)
        self.parse_expression_list()
        self.match(TokenType.RPAREN)
