from jacktoken import Token, TokenType
from xml_generator import token_to_xml
from typing import List


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
        if token and token.type == expected_type:
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
