# Compilador Aritmetico Didatico

Trabalho da disciplina de **Linguagens Formais e Compiladores**.

Implementacao, do zero e em Python, de um compilador para uma linguagem
simples que demonstra as **5 fases classicas** de um compilador.

**Grupo:** Erika Oliveira Silva, Henrique Souza Uchida, Hian Araujo Damaceno.

## A linguagem

A linguagem aceita:

- Declaracao de variaveis com `let` (ex.: `let x = 10`)
- Reatribuicao de variaveis (ex.: `x = x + 5`)
- Impressao com `print(...)`
- As 4 operacoes aritmeticas: `+`, `-`, `*`, `/`
- Numeros inteiros e decimais
- Comentarios iniciados por `#`

## As 5 fases

1. **Analise Lexica** (`src/lexer.py`) - o `Lexer` le o codigo e separa em tokens.
2. **Analise Sintatica** (`src/parser.py`) - o `Parser` monta a AST (descida recursiva).
3. **Analise Semantica** (`src/semantic.py`) - o `AnalisadorSemantico` valida o programa.
4. **Geracao de Codigo** (`src/codegen.py`) - o `GeradorDeCodigo` produz o bytecode.
5. **Execucao** (`src/codegen.py`) - a `MaquinaVirtual` executa o bytecode.

## Estrutura do projeto

```
compilador_aritmetico/
|-- src/
|   |-- __init__.py      # exports publicos do pacote
|   |-- lexer.py         # Fase 1: Analise Lexica
|   |-- ast_nodes.py     # Nos da AST + classe Visitor
|   |-- parser.py        # Fase 2: Parser de descida recursiva
|   |-- semantic.py      # Fase 3: Analise semantica + tabela de simbolos
|   |-- codegen.py       # Fases 4+5: Gerador de codigo + Maquina Virtual
|-- tests/
|   |-- test_compiler.py # Casos de teste automatizados
|-- examples/
|   |-- exemplo1.al      # Operacoes basicas
|   |-- exemplo2.al      # Precedencia e parenteses
|   |-- exemplo3.al      # Programa mais elaborado
|-- docs/
|   |-- relatorio.pdf    # Relatorio tecnico do grupo
|-- README.md
```

## Instalacao

Requisitos: Python 3.8 ou superior (nao depende de bibliotecas externas).

```bash
git clone https://github.com/Erika4chaos/OPERADOR-4-OPERACOES.git
cd OPERADOR-4-OPERACOES
```

## Como executar

Use o pacote diretamente no Python:

```python
from src import compilar_e_rodar

compilar_e_rodar("let x = 10\nprint(x + 5)")
```

Para ver os tokens, a AST e o bytecode, passe `verbose=True`:

```python
compilar_e_rodar("print((2 + 3) * 4)", verbose=True)
```

## Testes

```bash
python tests/test_compiler.py
```

Ou, se tiver o pytest instalado:

```bash
pytest tests/
```
