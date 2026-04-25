from jacktoken import Token, TokenType
from xml_generator import token_to_xml
from typing import List

OPS = {'+', '-', '*', '/', '&', '|', '<', '>', '='}


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

    def parse_term(self):
        """term → integerConstant | stringConstant | keywordConstant | varName"""

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
        elif token.type == TokenType.IDENT:
            self.match(TokenType.IDENT)
        else:
            raise SyntaxError(
                f"Termo esperado na linha {token.line}, "
                f"encontrado: '{token.lexeme}'"
            )

        self.close_tag("term")


    def parse_expression(self):
       """expression → term (op term)*"""
       self.open_tag("expression")
       self.parse_term()

       while self.peek() and self.peek().lexeme in OPS:
           self.write_token(self.advance())  # escreve o operador
           self.parse_term()

       self.close_tag("expression")

    def parse_let(self):
       """letStatement → 'let' varName ('[' expression ']')? '=' expression ';'"""
       self.open_tag("letStatement")
       self.match(TokenType.LET)        # let

       self.match(TokenType.IDENT)      # varName

       # opcional: '[' expression ']'
       if self.peek() and self.peek().lexeme == '[':
           self.match_symbol('[')
           self.parse_expression()
           self.match_symbol(']')

       self.match_symbol('=')           # =
       self.parse_expression()          # expression
       self.match_symbol(';')           # ;
       self.close_tag("letStatement")

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

    def parse_if(self):
       """ifStatement → 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?"""
       self.open_tag("ifStatement")
       self.match(TokenType.IF)         # if
       self.match_symbol('(')           # (
       self.parse_expression()          # expression
       self.match_symbol(')')           # )
       self.match_symbol('{')           # {
       self.parse_statements()          # statements
       self.match_symbol('}')           # }

       if self.peek() and self.peek().type == TokenType.ELSE:
           self.match(TokenType.ELSE)   # else
           self.match_symbol('{')       # {
           self.parse_statements()      # statements
           self.match_symbol('}')       # }

       self.close_tag("ifStatement")


    def parse_while(self):
       """lê um while (expressão) { statements }"""
       self.open_tag("whileStatement")
       self.match(TokenType.WHILE)      # while
       self.match_symbol('(')           # (
       self.parse_expression()          # expression
       self.match_symbol(')')           # )
       self.match_symbol('{')           # {
       self.parse_statements()          # statements
       self.match_symbol('}')           # }
       self.close_tag("whileStatement")

    def parse_expression_list(self):
       """lê zero ou mais expressões separadas por vírgula"""
       self.open_tag("expressionList")
       if self.peek() and self.peek().lexeme != ')':
           self.parse_expression()
           while self.peek() and self.peek().lexeme == ',':
               self.match_symbol(',')
               self.parse_expression()
       self.close_tag("expressionList")

    def parse_subroutine_call(self):
       """lê uma chamada de função: foo() ou obj.foo()"""
       self.match(TokenType.IDENT)      # nome da função ou objeto
       if self.peek() and self.peek().lexeme == '.':
           self.match_symbol('.')       # .
           self.match(TokenType.IDENT)  # nome do método
       self.match_symbol('(')           # (
       self.parse_expression_list()     # expressionList
       self.match_symbol(')')           # )

    def parse_do(self):
       """lê um do subroutineCall ;"""
       self.open_tag("doStatement")
       self.match(TokenType.DO)         # do
       self.parse_subroutine_call()     # subroutineCall
       self.match_symbol(';')           # ;
       self.close_tag("doStatement")


    def parse_return(self):
       """lê um return expression? ;"""
       self.open_tag("returnStatement")
       self.match(TokenType.RETURN)     # return

       # expressão é opcional
       if self.peek() and self.peek().lexeme != ';':
           self.parse_expression()

       self.match_symbol(';')           # ;
       self.close_tag("returnStatement")


