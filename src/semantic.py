"""Fase 3: Analise semantica + tabela de simbolos."""
from .ast_nodes import Visitor


class ErroSemantico(Exception):
    def __init__(self, msg, linha):
        super().__init__(f'Erro Semântico (linha {linha}): {msg}')
        self.linha = linha


class TabelaDeSimbolos:
    def __init__(self):
        self.variaveis = {}

    def declarar(self, nome, tipo, linha):
        if nome in self.variaveis:
            raise ErroSemantico(f"variável '{nome}' já foi declarada", linha)
        self.variaveis[nome] = tipo

    def atualizar(self, nome, tipo, linha):
        if nome not in self.variaveis:
            raise ErroSemantico(f"use 'let {nome} = ...' antes de atribuir", linha)
        self.variaveis[nome] = tipo

    def buscar(self, nome, linha):
        if nome not in self.variaveis:
            raise ErroSemantico(f"variável '{nome}' usada antes de ser declarada", linha)
        return self.variaveis[nome]


class AnalisadorSemantico(Visitor):
    def __init__(self):
        self.tabela = TabelaDeSimbolos()

    def analisar(self, programa):
        self.visitar(programa)
        return self.tabela

    def visitar_Programa(self, no):
        for cmd in no.comandos:
            self.visitar(cmd)

    def visitar_DeclaracaoLet(self, no):
        tipo = self.visitar(no.valor)
        self.tabela.declarar(no.nome, tipo, no.linha)

    def visitar_Atribuicao(self, no):
        tipo = self.visitar(no.valor)
        self.tabela.atualizar(no.nome, tipo, no.linha)

    def visitar_ComandoPrint(self, no):
        self.visitar(no.valor)

    def visitar_OperacaoBinaria(self, no):
        tipo_esq = self.visitar(no.esquerda)
        tipo_dir = self.visitar(no.direita)
        # divisão sempre vira float
        if no.op == '/':
            return 'float'
        # se um dos lados for float, o resultado é float
        if 'float' in (tipo_esq, tipo_dir):
            return 'float'
        return 'int'

    def visitar_OperacaoUnaria(self, no):
        return self.visitar(no.operando)

    def visitar_LiteralInt(self, no):
        return 'int'

    def visitar_LiteralFloat(self, no):
        return 'float'

    def visitar_Variavel(self, no):
        return self.tabela.buscar(no.nome, no.linha)

