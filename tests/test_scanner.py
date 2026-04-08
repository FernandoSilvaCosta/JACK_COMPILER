from scanner import Scanner
from jacktoken import TokenType
from xml_generator import token_to_xml

#TESTA UM NUMERO INTEIRO
def test_number():
  
    code = "157"
    scanner = Scanner(code)
    tokens = scanner.tokenize()

    assert tokens[0].type == TokenType.NUMBER
    assert tokens[0].lexeme == "157"
    assert token_to_xml(tokens[0]) == '<integerConstant> 157 </integerConstant>'
    print("Teste Finalizado e Aprovado!")

#TESTA VARIOS NUMEROS DE UMA VEZ
def test_numbers_xml():
    
    casos = [
        ("0",     '<integerConstant> 0 </integerConstant>'),
        ("157",   '<integerConstant> 157 </integerConstant>'),
        ("23",    '<integerConstant> 23 </integerConstant>'),
        ("  456  ", '<integerConstant> 456 </integerConstant>'),  # com espaços
    ]

    for code, xml_esperado in casos:
        scanner = Scanner(code)
        tokens = scanner.tokenize()

        token = tokens[0]  # ignora o EOF
        assert token_to_xml(token) == xml_esperado, f"Falhou para: {code}"

    print("Os testes de números com XML Foram Aprovados!")

# Testa o reconhecimento de uma string simples.
def test_string_basica():
    code = '"hello"'
    scanner = Scanner(code)
    tokens = scanner.tokenize()

    assert tokens[0].type == TokenType.STRING
    assert tokens[0].lexeme == "hello"
    assert token_to_xml(tokens[0]) == '<stringConstant> hello </stringConstant>'
    print("Teste de string básica aprovado!")
# Testa uma string com espaços.
def test_string_com_espacos():
    
    code = '"hello world"'
    scanner = Scanner(code)
    tokens = scanner.tokenize()

    assert tokens[0].type == TokenType.STRING
    assert tokens[0].lexeme == "hello world"
    assert token_to_xml(tokens[0]) == '<stringConstant> hello world </stringConstant>'
    print("Teste de string com espaços aprovado!")

def test_identificadores_e_keywords():
    """Testa identificadores e palavras reservadas."""
    
    # Teste 1: Identificador comum
    scanner = Scanner("minhaVar123")
    tokens = scanner.tokenize()
    assert tokens[0].type == TokenType.IDENT
    assert tokens[0].lexeme == "minhaVar123"
    assert token_to_xml(tokens[0]) == '<identifier> minhaVar123 </identifier>'

    # Teste 2: Palavra reservada - function
    scanner = Scanner("function")
    tokens = scanner.tokenize()
    assert tokens[0].type == TokenType.FUNCTION
    assert tokens[0].lexeme == "function"
    assert token_to_xml(tokens[0]) == '<keyword> function </keyword>'
    
    # Teste 3: Palavra reservada - return
    scanner = Scanner("return")
    tokens = scanner.tokenize()
    assert tokens[0].type == TokenType.RETURN
    assert tokens[0].lexeme == "return"
    assert token_to_xml(tokens[0]) == '<keyword> return </keyword>'
    
    print("✅ Teste de identificadores e keywords passou!")

def test_identificador_com_underscore():
    """Testa identificador com underscore."""
    scanner = Scanner("minha_variavel_123")
    tokens = scanner.tokenize()
    assert tokens[0].type == TokenType.IDENT
    assert tokens[0].lexeme == "minha_variavel_123"
    print("✅ Teste de identificador com underscore passou!")

def test_simbolos_xml():
    """Testa o reconhecimento de símbolos validando a saída XML."""
    code = "x + y;"
    scanner = Scanner(code)
    tokens = scanner.tokenize()

    # ✅ Formato XML esperado (com espaços dentro das tags)
    esperado_xml = [
        '<identifier> x </identifier>',
        '<symbol> + </symbol>',
        '<identifier> y </identifier>',
        '<symbol> ; </symbol>',
    ]
    
    # Ignora o token EOF no final
    tokens_sem_eof = [t for t in tokens if t.type != TokenType.EOF]
    
    for i, xml_esperado in enumerate(esperado_xml):
        assert token_to_xml(tokens_sem_eof[i]) == xml_esperado, \
            f"Token {i} não corresponde:\n  Esperado: {xml_esperado}\n  Obtido:   {token_to_xml(tokens_sem_eof[i])}"
    
    print("✅ Teste de símbolos com XML passou!")

def test_varios_simbolos():
    """Testa vários símbolos diferentes."""
    code = "({[]}),.;+-*/&|<>=~"
    scanner = Scanner(code)
    tokens = scanner.tokenize()
    
    # Pega todos os tokens exceto EOF
    tokens_sem_eof = [t for t in tokens if t.type != TokenType.EOF]
    
    # Deve ter um token para cada símbolo
    simbolos_esperados = list("({[]}),.;+-*/&|<>=~")
    
    assert len(tokens_sem_eof) == len(simbolos_esperados), \
        f"Esperado {len(simbolos_esperados)} símbolos, mas obteve {len(tokens_sem_eof)}"
    
    for i, simbolo in enumerate(simbolos_esperados):
        assert tokens_sem_eof[i].lexeme == simbolo, \
            f"Token {i}: esperado '{simbolo}', obteve '{tokens_sem_eof[i].lexeme}'"
        assert token_to_xml(tokens_sem_eof[i]) == f'<symbol> {simbolo} </symbol>'
    
    print("✅ Teste de vários símbolos passou!")


def test_comentarios_ignorados():
    """Testa que comentários são ignorados."""
    code = "let x = 5; // isto some"
    scanner = Scanner(code)
    tokens = [t for t in scanner.tokenize() if t.type != TokenType.EOF]

    # Nenhum token de comentário deve aparecer
    tipos = [t.type for t in tokens]

    # Mas os tokens válidos permanecem
    lexemes = [t.lexeme for t in tokens]
    assert "let" in lexemes
    assert "x" in lexemes
    assert "5" in lexemes
    
    print("✅ Teste de comentário de linha passou!")

def test_comentario_bloco():
    """Testa comentário de bloco /* ... */."""
    code = "let /* comentário */ x = 5;"
    scanner = Scanner(code)
    tokens = [t for t in scanner.tokenize() if t.type != TokenType.EOF]
    
    lexemes = [t.lexeme for t in tokens]
    assert "let" in lexemes
    assert "x" in lexemes
    assert "5" in lexemes
    # A palavra 'comentário' não deve aparecer
    assert "comentário" not in lexemes
    
    print("✅ Teste de comentário de bloco passou!")

def test_comentario_aninhado():
    """Testa comentários múltiplos."""
    code = """
    // comentário linha 1
    let a = 10;
    /* comentário bloco */
    let b = 20;
    """
    scanner = Scanner(code)
    tokens = [t for t in scanner.tokenize() if t.type != TokenType.EOF]
    
    lexemes = [t.lexeme for t in tokens]
    assert lexemes.count("let") == 2
    assert "a" in lexemes
    assert "b" in lexemes
    assert "10" in lexemes
    assert "20" in lexemes
    
    print("✅ Teste de comentários múltiplos passou!")

def test_slash_divisao():
    """Testa que '/' sozinho é reconhecido como símbolo de divisão."""
    code = "a / b"
    scanner = Scanner(code)
    tokens = [t for t in scanner.tokenize() if t.type != TokenType.EOF]
    
    assert tokens[0].lexeme == "a"
    assert tokens[1].lexeme == "/"
    assert tokens[1].type == TokenType.SLASH
    assert tokens[2].lexeme == "b"
    
    print("✅ Teste do símbolo de divisão passou!")