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