"""Fases 4+5: Gerador de codigo + Maquina Virtual."""
from .lexer import Lexer, ErroLexico
from .ast_nodes import Visitor, ImpressorAST
from .parser import Parser, ErroSintatico
from .semantic import AnalisadorSemantico, ErroSemantico


class GeradorDeCodigo(Visitor):
    def __init__(self):
        self.bytecode = []

    def emitir(self, *instrucao):
        self.bytecode.append(instrucao)

    def gerar(self, programa):
        self.visitar(programa)
        self.emitir('HALT')
        return self.bytecode

    def visitar_Programa(self, no):
        for cmd in no.comandos:
            self.visitar(cmd)

    def visitar_DeclaracaoLet(self, no):
        self.visitar(no.valor)
        self.emitir('GUARDAR', no.nome)

    def visitar_Atribuicao(self, no):
        self.visitar(no.valor)
        self.emitir('GUARDAR', no.nome)

    def visitar_ComandoPrint(self, no):
        self.visitar(no.valor)
        self.emitir('IMPRIMIR')

    def visitar_OperacaoBinaria(self, no):
        self.visitar(no.esquerda)
        self.visitar(no.direita)
        tabela_ops = {'+': 'SOMAR', '-': 'SUBTRAIR', '*': 'MULTIPLICAR', '/': 'DIVIDIR'}
        self.emitir(tabela_ops[no.op])

    def visitar_OperacaoUnaria(self, no):
        self.visitar(no.operando)
        self.emitir('NEGAR')

    def visitar_LiteralInt(self, no):
        self.emitir('EMPURRAR', no.valor)

    def visitar_LiteralFloat(self, no):
        self.emitir('EMPURRAR', no.valor)

    def visitar_Variavel(self, no):
        self.emitir('CARREGAR', no.nome)


class MaquinaVirtual:
    def __init__(self):
        self.pilha   = []
        self.memoria = {}
        self.saida   = []

    def rodar(self, bytecode):
        for instrucao in bytecode:
            op   = instrucao[0]
            args = instrucao[1:]

            if op == 'EMPURRAR':
                self.pilha.append(args[0])

            elif op == 'CARREGAR':
                self.pilha.append(self.memoria[args[0]])

            elif op == 'GUARDAR':
                self.memoria[args[0]] = self.pilha.pop()

            elif op == 'SOMAR':
                b = self.pilha.pop()
                a = self.pilha.pop()
                self.pilha.append(a + b)

            elif op == 'SUBTRAIR':
                b = self.pilha.pop()
                a = self.pilha.pop()
                self.pilha.append(a - b)

            elif op == 'MULTIPLICAR':
                b = self.pilha.pop()
                a = self.pilha.pop()
                self.pilha.append(a * b)

            elif op == 'DIVIDIR':
                b = self.pilha.pop()
                a = self.pilha.pop()
                if b == 0:
                    raise RuntimeError('divisão por zero')
                self.pilha.append(a / b)

            elif op == 'NEGAR':
                self.pilha.append(-self.pilha.pop())

            elif op == 'IMPRIMIR':
                valor = self.pilha.pop()
                texto = str(valor)
                self.saida.append(texto)
                print(texto)

            elif op == 'HALT':
                break

        return self.saida


def compilar_e_rodar(codigo, verbose=False):
    # fase 1 — lexer
    tokens = Lexer(codigo).tokenizar()
    if verbose:
        print('=== TOKENS ===')
        for t in tokens:
            print(' ', t)

    # fase 2 — parser
    arvore = Parser(tokens).parse()
    if verbose:
        print('\n=== AST ===')
        ImpressorAST().visitar(arvore)

    # fase 3 — semântica
    AnalisadorSemantico().analisar(arvore)

    # fase 4 — geração de código
    bytecode = GeradorDeCodigo().gerar(arvore)
    if verbose:
        print('\n=== BYTECODE ===')
        for i in bytecode:
            print(' ', i)

    # fase 5 — execução
    return MaquinaVirtual().rodar(bytecode)

