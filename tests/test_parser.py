from parser import Parser
from scanner import Scanner
from jacktoken import TokenType

def test_parse_term_integer():
    """Testa o reconhecimento de um termo inteiro simples."""
    code = "10"
    tokens = [t for t in Scanner(code).tokenize() if t.type != TokenType.EOF]

    parser = Parser(tokens)
    parser.parse_term()
    xml = parser.get_xml()

    assert "<term>" in xml
    assert "<integerConstant> 10 </integerConstant>" in xml
    print("✅ Teste de term inteiro passou!")

def test_parse_expression():
    """Testa o reconhecimento de uma expressão simples."""
    code = "10 + 20"
    tokens = [t for t in Scanner(code).tokenize() if t.type != TokenType.EOF]

    parser = Parser(tokens)
    parser.parse_expression()
    xml = parser.get_xml()

    assert "<expression>" in xml
    assert "<integerConstant> 10 </integerConstant>" in xml
    assert "<symbol> + </symbol>" in xml
    assert "<integerConstant> 20 </integerConstant>" in xml
    print("✅ Teste de expression passou!")

def test_parse_let():
    """Testa o reconhecimento de um letStatement simples."""
    code = "let x = 10;"
    tokens = [t for t in Scanner(code).tokenize() if t.type != TokenType.EOF]

    parser = Parser(tokens)
    parser.parse_let()
    xml = parser.get_xml()

    assert "<letStatement>" in xml
    assert "<keyword> let </keyword>" in xml
    assert "<identifier> x </identifier>" in xml
    assert "<symbol> = </symbol>" in xml
    assert "<integerConstant> 10 </integerConstant>" in xml
    assert "<symbol> ; </symbol>" in xml
    print("✅ Teste de letStatement passou!")

def test_parse_if():
    """Testa o reconhecimento de um ifStatement simples."""
    code = "if (x) { let y = 1; }"
    tokens = [t for t in Scanner(code).tokenize() if t.type != TokenType.EOF]

    parser = Parser(tokens)
    parser.parse_if()
    xml = parser.get_xml()

    assert "<ifStatement>" in xml
    assert "<keyword> if </keyword>" in xml
    assert "<symbol> ( </symbol>" in xml
    assert "<symbol> ) </symbol>" in xml
    assert "<symbol> { </symbol>" in xml
    assert "<symbol> } </symbol>" in xml
    print("✅ Teste de ifStatement passou!")


def test_parse_while():
    """Testa o reconhecimento de um whileStatement simples."""
    code = "while (x) { let y = 1; }"
    tokens = [t for t in Scanner(code).tokenize() if t.type != TokenType.EOF]

    parser = Parser(tokens)
    parser.parse_while()
    xml = parser.get_xml()

    assert "<whileStatement>" in xml
    assert "<keyword> while </keyword>" in xml
    print("✅ Teste de whileStatement passou!")

