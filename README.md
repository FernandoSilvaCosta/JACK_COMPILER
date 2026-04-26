# PROJETO_COMPILADOR
## Projeto de Compilador da linguagem Jack para disciplina de Compiladores 2026.1 - UFMA

### NOMES DOS INTEGRANTES :
- FERNANDO DA SILVA COSTA
- DAVI OLIVEIRA CORTES

### LINGUAGEM DE PROGRAMAÇÃO USADA:
- Python

## 📁 Estrutura do Projeto

jack-compiler/
├── scanner.py          # Analisador Léxico
├── jacktoken.py        # Token + TokenType
├── xml_generator.py    # Geração de XML
├── parser.py           # Analisador Sintático
├── main.py             # Execução
│
├── tests/
│   ├── test_scanner.py
│   ├── test_parser.py
│   └── nand2tetris/
│       └── Square/
│           ├── Main.jack
│           ├── MainT.xml
│           ├── Square.jack
│           ├── SquareT.xml
│           ├── SquareGame.jack
│           └── SquareGame.xml
│
└── output/
    └── Square/

---

## 🧠 Como Funciona

### Etapa 1 — Analisador Léxico (Scanner)

Lê o código-fonte Jack e transforma em uma sequência de **tokens**, ignorando espaços em branco e comentários.

### Tipos de Tokens Suportados

| Tipo | Exemplos |
|------|----------|
| `keyword` | `class`, `if`, `while`, `return` |
| `symbol` | `{`, `}`, `+`, `;`, `<`, `>` |
| `identifier` | `myVar`, `Main`, `SquareGame` |
| `integerConstant` | `0`, `42`, `289` |
| `stringConstant` | `"hello world"` |

### Etapa 2 — Analisador Sintático (Parser)

Recebe a lista de tokens e verifica se obedecem a gramática da linguagem Jack, produzindo uma **árvore sintática em XML**.

### Gramática Suportada

| Construção | Regra |
|------------|-------|
| class | 'class' className '{' classVarDec* subroutineDec* '}' |
| classVarDec | ('static' ou 'field') type varName (',' varName)* ';' |
| subroutineDec | ('constructor' ou 'function' ou 'method') type name '(' parameterList ')' subroutineBody |
| letStatement | 'let' varName ('[' expression ']')? '=' expression ';' |
| ifStatement | 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')? |
| whileStatement | 'while' '(' expression ')' '{' statements '}' |
| doStatement | 'do' subroutineCall ';' |
| returnStatement | 'return' expression? ';' |
| expression | term (op term)* |
| term | integerConstant ou stringConstant ou varName ou subroutineCall |


### Saída XML do Analisador Léxico

Para cada token, o scanner gera uma linha XML no formato:

```xml
<tokens>
<keyword> class </keyword>
<identifier> Main </identifier>
<symbol> { </symbol>
<integerConstant> 42 </integerConstant>
<stringConstant> hello world </stringConstant>
</tokens>
```

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.12+
- pytest

### Instalando o pytest

pip install pytest

### Compilando um arquivo Jack

python main.py caminho/arquivo.jack saida.xml

### Rodando os Testes

python -m pytest tests/ -v -s

python -m pytest tests/test_scanner.py -v -s

python -m pytest tests/test_parser.py -v -s

---

## 🧪 Testes

O projeto segue a metodologia **TDD (Test Driven Development)**.

### Scanner
- ✅ Números inteiros
- ✅ Símbolos
- ✅ Keywords
- ✅ Identificadores
- ✅ Strings
- ✅ Comentários de linha e bloco
- ✅ Validação com arquivos reais do nand2tetris

### Parser
- ✅ parse_term() — termos simples
- ✅ parse_expression() — expressões com operadores
- ✅ parse_let() — atribuição de variáveis
- ✅ parse_if() — estrutura condicional
- ✅ parse_while() — estrutura de repetição
- ✅ parse_do() — chamada de subrotina
- ✅ parse_return() — retorno de função
- ✅ Estrutura completa de classes
- ✅ Validação com arquivos reais do nand2tetris (Square, SquareGame, Main)

---

## 📦 Arquivos Principais

### jacktoken.py
Define TokenType (enum com todos os tipos de tokens) e Token (dataclass com type, lexeme e line).

### xml_generator.py
Converte tokens em XML, incluindo escape de caracteres especiais (&, <, >, ").

### scanner.py
Lê o código-fonte caractere por caractere e produz a lista de tokens.

### parser.py
Recebe a lista de tokens e produz a árvore sintática em XML usando recursive descent parsing — uma função por não-terminal da gramática.

### main.py
Ponto de entrada do compilador. Recebe um arquivo .jack e gera o XML correspondente.

---

## 📚 Referências

- [Nand2Tetris](https://www.nand2tetris.org/)
- [The Elements of Computing Systems — Nisan & Schocken](https://www.nand2tetris.org/book)
