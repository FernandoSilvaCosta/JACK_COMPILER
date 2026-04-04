from scanner import Scanner
from jacktoken import TokenType
from xml_generator import token_to_xml

def test_number():
    """Testa o reconhecimento de um número inteiro simples."""
    code = "157"
    scanner = Scanner(code)
    tokens = scanner.tokenize()

    assert tokens[0].type == TokenType.NUMBER
    assert tokens[0].lexeme == "157"
    assert token_to_xml(tokens[0]) == '<integerConstant> 289 </integerConstant>'
    print("Teste Finalizado e Aprovado!")
