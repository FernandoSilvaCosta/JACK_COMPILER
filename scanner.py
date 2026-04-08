from jacktoken import Token, TokenType

# CLASSE DE LEITURA DO CODIGO JACK


class Scanner:
    def __init__(self, code: str):
        self.code = code       # codigo fonte completo
        self.current = 0       # posição atual no código
        self.line = 1          # linha atual (para mensagens de erro)
        self.tokens = []       # lista de tokens reconhecidos

      # DEFIÇÃO DOS SIMBOLOS
        self.SYMBOLS = {
            '(': TokenType.LPAREN,    ')': TokenType.RPAREN,
            '{': TokenType.LBRACE,    '}': TokenType.RBRACE,
            '[': TokenType.LBRACKET,  ']': TokenType.RBRACKET,
            ',': TokenType.COMMA,     ';': TokenType.SEMICOLON,
            '.': TokenType.DOT,       '+': TokenType.PLUS,
            '-': TokenType.MINUS,     '*': TokenType.ASTERISK,
            '/': TokenType.SLASH,     '&': TokenType.AND,
            '|': TokenType.OR,        '<': TokenType.LT,
            '>': TokenType.GT,        '=': TokenType.EQ,
            '~': TokenType.NOT,
        }
      # DEFINIÇAO DAS KEYWORDS DA LINGUAGEM JACK
        self.KEYWORDS = {
            'class': TokenType.CLASS,           'constructor': TokenType.CONSTRUCTOR,
            'function': TokenType.FUNCTION,     'method': TokenType.METHOD,
            'field': TokenType.FIELD,           'static': TokenType.STATIC,
            'var': TokenType.VAR,               'int': TokenType.INT,
            'char': TokenType.CHAR,             'boolean': TokenType.BOOLEAN,
            'void': TokenType.VOID,             'true': TokenType.TRUE,
            'false': TokenType.FALSE,           'null': TokenType.NULL,
            'this': TokenType.THIS,             'let': TokenType.LET,
            'do': TokenType.DO,                 'if': TokenType.IF,
            'else': TokenType.ELSE,             'while': TokenType.WHILE,
            'return': TokenType.RETURN,
        }


# OLHAR O CARACTERE ATUAL E OS PROXIMOS


    def peek(self, offset=0) -> str:
        pos = self.current + offset
        if pos < len(self.code):
            return self.code[pos]
        return '\0'  # fim do código


# AVANÇA O CARACTERE


    def advance(self) -> None:
        if self.current < len(self.code):
            if self.code[self.current] == '\n':
                self.line += 1
            self.current += 1


# IGNORAR ESPAÇOS, TABS E QUEBRA DE LINHA


    def skip_whitespace(self) -> None:
        while True:
            c = self.peek()
            if c in (' ', '\t', '\r'):
                self.advance()
            elif c == '\n':
                self.line += 1
                self.advance()
            else:
                break

# LEITURA DE NUMEROS INTEIROS
    def read_number(self) -> Token:
        start = self.current
        # consome todos os dígitos consecutivos
        while self.peek().isdigit():
            self.advance()

        lexeme = self.code[start:self.current]
        return Token(TokenType.NUMBER, lexeme, self.line)
    
# LEITURA DE STRINGS
    def read_string(self) -> Token:
        """Lê uma constante de string delimitada por aspas duplas."""
        self.advance()  # consome aspa de abertura
        start = self.current
        
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                raise SyntaxError(f"Erro na linha {self.line}: String constante não pode conter quebra de linha.")
            self.advance()
        
        if self.is_at_end():
            raise SyntaxError(f"Erro na linha {self.line}: String não fechada (esperado '\"').")
        
        lexeme = self.code[start:self.current]
        self.advance()  # consome aspa de fechamento
        return Token(TokenType.STRING, lexeme, self.line)
    
    def read_identifier(self) -> Token:
        """Lê um identificador ou uma palavra-chave (keyword)."""
        # Define o ponto de início (onde está a primeira letra ou _)
        start = self.current
        
        # Continua consumindo enquanto for letra, número ou underscore
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()

        # Extrai o texto completo
        lexeme = self.code[start:self.current]
        
        # O pulo do gato: tenta buscar no dicionário de keywords.
        # Se não existir, o padrão (default) é TokenType.IDENT
        token_type = self.KEYWORDS.get(lexeme, TokenType.IDENT)
        
        return Token(token_type, lexeme, self.line)

    def is_at_end(self) -> bool:
        return self.current >= len(self.code)

# LEITURA DO CODIGO E TRANSFORMA EM UMA LISTA DE TOKENS
    def tokenize(self) -> list:
        while not self.is_at_end():
            self.skip_whitespace()
            
            if self.is_at_end():
                break

            ch = self.peek()

            if ch.isalpha() or ch == '_':
                self.tokens.append(self.read_identifier())
            
            elif ch.isdigit():
                self.tokens.append(self.read_number())
                
            elif ch == '"':
                self.tokens.append(self.read_string())
                
            elif ch in self.SYMBOLS:
                self.advance()  # Avança para consumir o símbolo
                self.tokens.append(Token(self.SYMBOLS[ch], ch, self.line))
                
            else:
                raise SyntaxError(f"Caractere ilegal '{ch}' na linha {self.line}")

        self.tokens.append(Token(TokenType.EOF, "", self.line))
        return self.tokens

