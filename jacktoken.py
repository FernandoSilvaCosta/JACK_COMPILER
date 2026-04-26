from enum import Enum, unique
from dataclasses import dataclass


@unique
class TokenType(Enum):
    """TOKENS DA LINGUAGEM JACK - cada membro tem valor único."""

    # NUMEROS-STRINGS-IDENTIFICADORES
    NUMBER = "integerConstant"
    STRING = "stringConstant"
    IDENT = "identifier"

    # SIMBOLOS (valores únicos para evitar aliases)
    LPAREN    = "sym_lparen"       # (
    RPAREN    = "sym_rparen"       # )
    LBRACE    = "sym_lbrace"       # {
    RBRACE    = "sym_rbrace"       # }
    LBRACKET  = "sym_lbracket"     # [
    RBRACKET  = "sym_rbracket"     # ]
    COMMA     = "sym_comma"        # ,
    SEMICOLON = "sym_semicolon"    # ;
    DOT       = "sym_dot"          # .
    PLUS      = "sym_plus"         # +
    MINUS     = "sym_minus"        # -
    ASTERISK  = "sym_asterisk"     # *
    SLASH     = "sym_slash"        # /
    AND       = "sym_and"          # &
    OR        = "sym_or"           # |
    NOT       = "sym_not"          # ~
    LT        = "sym_lt"           # <
    GT        = "sym_gt"           # >
    EQ        = "sym_eq"           # =

    # PALAVRAS DA LINGUAGEM (valores únicos)
    CLASS       = "kw_class"
    CONSTRUCTOR = "kw_constructor"
    FUNCTION    = "kw_function"
    METHOD      = "kw_method"
    FIELD       = "kw_field"
    STATIC      = "kw_static"
    VAR         = "kw_var"
    INT         = "kw_int"
    CHAR        = "kw_char"
    BOOLEAN     = "kw_boolean"
    VOID        = "kw_void"
    TRUE        = "kw_true"
    FALSE       = "kw_false"
    NULL        = "kw_null"
    THIS        = "kw_this"
    LET         = "kw_let"
    DO          = "kw_do"
    IF          = "kw_if"
    ELSE        = "kw_else"
    WHILE       = "kw_while"
    RETURN      = "kw_return"

    EOF = "eof"


"""REPRESENTAR OS TOKENS"""
@dataclass
class Token:
    type: TokenType
    lexeme: str
    line: int
