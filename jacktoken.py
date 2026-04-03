from enum import Enum

class TokenType(Enum):
    
    """TOKENS DA LINGUAGEM JACK"""

    #NUMEROS-STRINGS-IDENTIFICADORES
    NUMBER = "integerConstant"
    STRING = "stringConstant"
    IDENT = "identifier"

    #SIMBOLOS  
    LPAREN = "symbol"      # (
    RPAREN = "symbol"      # )
    LBRACE = "symbol"      # {
    RBRACE = "symbol"      # }
    LBRACKET = "symbol"    # [
    RBRACKET = "symbol"    # ]
    COMMA = "symbol"       # ,
    SEMICOLON = "symbol"   # ;
    DOT = "symbol"         # .
    PLUS = "symbol"        # +
    MINUS = "symbol"       # -
    ASTERISK = "symbol"    # *
    SLASH = "symbol"       # /
    AND = "symbol"         # &
    OR = "symbol"          # |
    NOT = "symbol"         # ~
    LT = "symbol"          # <
    GT = "symbol"          # >
    EQ = "symbol"          # =

    #PALAVRAS DA LINGUAGEM
    CLASS = "keyword"
    CONSTRUCTOR = "keyword"
    FUNCTION = "keyword"
    METHOD = "keyword"
    FIELD = "keyword"
    STATIC = "keyword"
    VAR = "keyword"
    INT = "keyword"
    CHAR = "keyword"
    BOOLEAN = "keyword"
    VOID = "keyword"
    TRUE = "keyword"
    FALSE = "keyword"
    NULL = "keyword"
    THIS = "keyword"
    LET = "keyword"
    DO = "keyword"
    IF = "keyword"
    ELSE = "keyword"
    WHILE = "keyword"
    RETURN = "keyword"
    EOF = "eof"


class Token:
    def __init__(self,type: TokenType, value: str):
       self.type = type
       self.value = value
    def __repr__(self):
        return f"Token ({self.type.name}, {self.value!r})"
       
        