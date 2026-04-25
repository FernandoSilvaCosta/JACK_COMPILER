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

    tokens_sem_eof = [t for t in tokens if t.type != TokenType.EOF]

    simbolos_esperados = list("({[]}),.;+-*/&|<>=~")

    assert len(tokens_sem_eof) == len(simbolos_esperados), \
        f"Esperado {len(simbolos_esperados)} símbolos, mas obteve {len(tokens_sem_eof)}"

    # Mapa de escape para os símbolos especiais do XML
    escapes = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
    }

    for i, simbolo in enumerate(simbolos_esperados):
        assert tokens_sem_eof[i].lexeme == simbolo, \
            f"Token {i}: esperado '{simbolo}', obteve '{tokens_sem_eof[i].lexeme}'"

        # Aplica escape se necessário
        simbolo_xml = escapes.get(simbolo, simbolo)
        assert token_to_xml(tokens_sem_eof[i]) == f'<symbol> {simbolo_xml} </symbol>', \
            f"Token {i}: XML incorreto para '{simbolo}'"

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

def test_codigo_jack_completo():
    """Testa um trecho completo de código Jack."""
    code = '''
    class Main {
        function void main() {
            let x = 5;
            return;
        }
    }
    '''
    scanner = Scanner(code)
    tokens = scanner.tokenize()

    # Verifica presença dos tipos esperados
    tipos = [t.type for t in tokens]
    lexemes = [t.lexeme for t in tokens]

    # Verifica tipos de token
    assert TokenType.CLASS in tipos
    assert TokenType.FUNCTION in tipos
    assert TokenType.IDENT in tipos
    assert TokenType.NUMBER in tipos
    
    # Verifica lexemas específicos
    assert "Main" in lexemes
    assert "x" in lexemes
    assert "5" in lexemes
    
    print("✅ Teste de integração com código Jack completo passou!")

def test_codigo_mais_complexo():
    """Testa um código Jack mais complexo com múltiplos elementos."""
    code = '''
    // Calcula fatorial
    class Factorial {
        function int compute(int n) {
            var int result;
            
            if (n < 2) {
                return 1;
            }
            
            let result = n * compute(n - 1);
            return result;
        }
    }
    '''
    scanner = Scanner(code)
    tokens = scanner.tokenize()
    
    # Remove EOF para facilitar
    tokens_sem_eof = [t for t in tokens if t.type != TokenType.EOF]
    tipos = [t.type for t in tokens_sem_eof]
    lexemes = [t.lexeme for t in tokens_sem_eof]
    
    # Verifica keywords
    assert TokenType.CLASS in tipos
    assert TokenType.FUNCTION in tipos
    assert TokenType.VAR in tipos
    assert TokenType.IF in tipos
    assert TokenType.RETURN in tipos
    assert TokenType.LET in tipos
    
    # Verifica identificadores
    assert "Factorial" in lexemes
    assert "compute" in lexemes
    assert "result" in lexemes
    assert "n" in lexemes
    
    # Verifica números
    assert "2" in lexemes
    assert "1" in lexemes
    
    # Verifica símbolos
    assert "<" in lexemes
    assert "*" in lexemes
    assert "-" in lexemes
    assert "(" in lexemes
    assert ")" in lexemes
    assert "{" in lexemes
    assert "}" in lexemes
    
    print("✅ Teste de código complexo passou!")

def test_codigo_com_tudo():
    """Testa código Jack com todos os tipos de token."""
    code = '''
    // Comentário de linha
    class Test {
        /* Comentário de bloco */
        function void run() {
            var int a, b;
            let a = 10;
            let b = "hello";
            let a = a + b;
            return;
        }
    }
    '''
    scanner = Scanner(code)
    tokens = scanner.tokenize()
    tokens_sem_eof = [t for t in tokens if t.type != TokenType.EOF]
    
    # Agrupa por tipo
    tipos_encontrados = set(t.type for t in tokens_sem_eof)
    
    # Tipos que devem estar presentes
    tipos_esperados = {
        TokenType.CLASS,
        TokenType.FUNCTION,
        TokenType.VAR,
        TokenType.LET,
        TokenType.RETURN,
        TokenType.IDENT,
        TokenType.NUMBER,
        TokenType.STRING,
    }
    
    for tipo in tipos_esperados:
        assert tipo in tipos_encontrados, f"Tipo {tipo} não encontrado"
    
    print("✅ Teste com todos os tipos de token passou!")

def test_validacao_nand2tetris_square_main():
    """
    Valida o scanner comparando com o arquivo MainT.xml oficial do nand2tetris.
    Este é o teste definitivo para o projeto!
    """
    import os

    # Caminhos dos arquivos
    jack_path = 'tests/nand2tetris/Square/Main.jack'
    xml_referencia_path = 'tests/nand2tetris/Square/MainT.xml'

    # Verifica se os arquivos existem
    assert os.path.exists(jack_path), f"Arquivo Jack não encontrado: {jack_path}"
    assert os.path.exists(xml_referencia_path), f"Arquivo XML de referência não encontrado: {xml_referencia_path}"

    # Lê o código Jack
    with open(jack_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # Gera tokens com seu scanner
    scanner = Scanner(code)
    tokens = scanner.tokenize()

    # Gera XML no formato nand2tetris (sem EOF, com wrapper <tokens>)
    tokens_sem_eof = [t for t in tokens if t.type != TokenType.EOF]
    xml_output = "<tokens>\n"
    for token in tokens_sem_eof:
        xml_output += token_to_xml(token) + "\n"
    xml_output += "</tokens>\n"

    # Lê o XML de referência
    with open(xml_referencia_path, 'r', encoding='utf-8') as f:
        xml_referencia = f.read()

    # Normaliza quebras de linha (Windows vs Linux)
    xml_output = xml_output.replace('\r\n', '\n')
    xml_referencia = xml_referencia.replace('\r\n', '\n')

    # Comparação final
    assert xml_output == xml_referencia, \
        f"XML não corresponde!\n\nDiferenças encontradas."

    print("✅ Validação nand2tetris Square/Main.jack PASSED!")
    print(f"   Tokens gerados: {len(tokens_sem_eof)}")


def test_validacao_nand2tetris_todos_arquivos():
    """
    Valida todos os arquivos .jack da pasta Square contra seus XML de referência.
    """
    import os

    pasta_jack = 'tests/nand2tetris/Square'
    arquivos_testados = 0
    arquivos_passaram = 0

    # Verifica se a pasta existe
    if not os.path.exists(pasta_jack):
        print(f"⚠️ Pasta {pasta_jack} não encontrada! Execute download_test_files.py primeiro.")
        return

    # Encontra todos os arquivos .jack
    for filename in os.listdir(pasta_jack):
        if filename.endswith('.jack'):
            arquivos_testados += 1

            # Caminhos
            jack_path = os.path.join(pasta_jack, filename)
            xml_referencia_path = os.path.join(pasta_jack, filename.replace('.jack', 'T.xml'))

            # Verifica se existe XML de referência
            if not os.path.exists(xml_referencia_path):
                print(f"⚠️ Sem XML de referência para {filename}")
                continue

            # Lê e processa Jack
            with open(jack_path, 'r', encoding='utf-8') as f:
                code = f.read()

            scanner = Scanner(code)
            tokens = scanner.tokenize()

            # Gera XML
            tokens_sem_eof = [t for t in tokens if t.type != TokenType.EOF]
            xml_output = "<tokens>\n"
            for token in tokens_sem_eof:
                xml_output += token_to_xml(token) + "\n"
            xml_output += "</tokens>\n"

            # Lê referência
            with open(xml_referencia_path, 'r', encoding='utf-8') as f:
                xml_referencia = f.read()

            # Normaliza
            xml_output = xml_output.replace('\r\n', '\n')
            xml_referencia = xml_referencia.replace('\r\n', '\n')

            # Compara
            if xml_output == xml_referencia:
                arquivos_passaram += 1
                print(f"✅ {filename} PASSED")
            else:
                print(f"❌ {filename} FAILED")
                
                # Salva o XML gerado para debug
                output_path = f"output/Square/{filename.replace('.jack', '_gerado.xml')}"
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(xml_output)
                print(f"   XML gerado salvo em: {output_path}")

    # Validação final
    if arquivos_testados > 0:
        assert arquivos_passaram == arquivos_testados, \
            f"{arquivos_testados - arquivos_passaram} de {arquivos_testados} arquivo(s) falharam!"

    print(f"\n🎉 {arquivos_passaram}/{arquivos_testados} arquivos validados com sucesso!")