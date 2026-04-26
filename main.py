import sys
from scanner import Scanner
from parser import Parser


def compile_file(jack_path, output_path):
    with open(jack_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # Scanner
    scanner = Scanner(code)
    tokens = scanner.tokenize()

    # Parser
    parser = Parser(tokens)
    parser.parse_class()

    # Salvar XML
    xml_content = parser.get_xml()

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)
        f.write('\n')

    print(f"✅ Compilado: {output_path}")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Uso: python main.py <arquivo.jack> <saida.xml>")
        sys.exit(1)
    compile_file(sys.argv[1], sys.argv[2])
