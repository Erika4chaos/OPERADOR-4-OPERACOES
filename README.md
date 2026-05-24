# OPERADOR-4-OPERACOES
# ArithLang Compiler (compilador_aritmetico)

Este projeto consiste na implementação de um compilador completo, funcional e desenvolvido do zero para a mini-linguagem aritmética **ArithLang**. O compilador foi estruturado seguindo um pipeline de 5 fases independentes e uma arquitetura modular em Python, culminando na execução de instruções customizadas em uma Máquina Virtual baseada em pilha.

Projeto prático desenvolvido para a disciplina de **Compiladores e Linguagens Formais** do curso de Engenharia da Computação.

## 👥 Grupo
* Erika Oliveira Silva
* Henrique Souza Uchida
* Hian Araujo Damaceno

---

## 🚀 Funcionalidades da ArithLang

A **ArithLang** é uma linguagem simples projetada com o objetivo de demonstrar todos os conceitos clássicos de engenharia de compiladores. Suas principais características incluem:
* **Tipos de Dados:** Suporte a números inteiros (`int`) e números reais de ponto flutuante de 64 bits (`float`).
* **Operações Aritméticas:** Implementação das quatro operações elementares (`+`, `-`, `*`, `/`) respeitando a precedência matemática e agrupamento explícito por parênteses `(...)`.
* **Gerenciamento de Variáveis:** Declaração explícita de variáveis de escopo global único via palavra-chave `let` e reatribuição dinâmica através do operador `=`.
* **Saída Padrão:** Comando nativo `print(...)` para exibição e avaliação de expressões.
* **Comentários de Linha:** Ignorados em tempo de compilação quando iniciados pelo caractere `#`.

---

## 🏗️ Estrutura do Projeto

O repositório está organizado conforme a estrutura modular estrita exigida pelas diretrizes do projeto:

```text
compilador_aritmetico/
├── src/
│   ├── __init__.py         # Exports públicos do pacote do compilador
│   ├── lexer.py            # Fase 1: Analisador Léxico manual
│   ├── ast_nodes.py        # Nós da AST e definição do Padrão Visitor
│   ├── parser.py           # Fase 2: Analisador Sintático (Descida Recursiva)
│   ├── semantic.py         # Fase 3: Analisador Semântico e Tabela de Símbolos
│   └── codegen.py          # Fase 4 e 5: Gerador de Bytecode e Máquina Virtual (VM)
├── tests/
│   └── test_compiler.py    # Suíte de testes automatizados (24 cenários)
├── examples/
│   ├── exemplo1.al         # Código fonte de exemplo: Operações Básicas
│   ├── exemplo2.al         # Código fonte de exemplo: Precedência e Parênteses
│   └── exemplo3.al         # Código fonte de exemplo: Programa acumulador completo
├── docs/
│   └── relatorio.pdf       # Relatório técnico do projeto
└── README.md               # Instruções de instalação e execução
