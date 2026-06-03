"""Definicao dos nos da AST + classe base Visitor."""
from dataclasses import dataclass, field


# classe base pra todos os nós da árvore
class No: pass

@dataclass
class LiteralInt(No):
    valor: int

@dataclass
class LiteralFloat(No):
    valor: float

@dataclass
class Variavel(No):
    nome:  str
    linha: int

@dataclass
class OperacaoBinaria(No):
    op:      str
    esquerda: No
    direita:  No

@dataclass
class OperacaoUnaria(No):
    op:      str
    operando: No

@dataclass
class DeclaracaoLet(No):
    nome:  str
    valor: No
    linha: int

@dataclass
class Atribuicao(No):
    nome:  str
    valor: No
    linha: int

@dataclass
class ComandoPrint(No):
    valor: No
    linha: int

@dataclass
class Programa(No):
    comandos: list = field(default_factory=list)


# padrão visitor — despacha pro método certo automaticamente
class Visitor:
    def visitar(self, no):
        metodo = getattr(self, f'visitar_{type(no).__name__}', self.generico)
        return metodo(no)

    def generico(self, no):
        raise NotImplementedError(f'visitar_{type(no).__name__} não implementado')


class ImpressorAST(Visitor):
    def __init__(self):
        self.nivel = 0

    def _print(self, texto):
        print('  ' * self.nivel + texto)

    def visitar_Programa(self, no):
        self._print('Programa')
        self.nivel += 1
        for cmd in no.comandos:
            self.visitar(cmd)
        self.nivel -= 1

    def visitar_DeclaracaoLet(self, no):
        self._print(f'let {no.nome} =')
        self.nivel += 1
        self.visitar(no.valor)
        self.nivel -= 1

    def visitar_Atribuicao(self, no):
        self._print(f'{no.nome} =')
        self.nivel += 1
        self.visitar(no.valor)
        self.nivel -= 1

    def visitar_ComandoPrint(self, no):
        self._print('print')
        self.nivel += 1
        self.visitar(no.valor)
        self.nivel -= 1

    def visitar_OperacaoBinaria(self, no):
        self._print(f'op: {no.op}')
        self.nivel += 1
        self.visitar(no.esquerda)
        self.visitar(no.direita)
        self.nivel -= 1

    def visitar_OperacaoUnaria(self, no):
        self._print(f'unario: {no.op}')
        self.nivel += 1
        self.visitar(no.operando)
        self.nivel -= 1

    def visitar_LiteralInt(self, no):
        self._print(f'int: {no.valor}')

    def visitar_LiteralFloat(self, no):
        self._print(f'float: {no.valor}')

    def visitar_Variavel(self, no):
        self._print(f'var: {no.nome}')
