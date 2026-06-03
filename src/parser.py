"""Fase 2: Parser de descida recursiva."""
from .lexer import TokenType
from .ast_nodes import (
    LiteralInt, LiteralFloat, Variavel, OperacaoBinaria, OperacaoUnaria,
    DeclaracaoLet, Atribuicao, ComandoPrint, Programa,
)


class ErroSintatico(Exception):
    def __init__(self, msg, linha):
        super().__init__(f'Erro Sintático (linha {linha}): {msg}')
        self.linha = linha


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos    = 0

    def atual(self):
        return self.tokens[self.pos]

    def tipo_atual(self):
        return self.tokens[self.pos].tipo

    def avancar(self):
        tok = self.tokens[self.pos]
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return tok

    def esperar(self, tipo):
        tok = self.atual()
        if tok.tipo != tipo:
            raise ErroSintatico(
                f"esperava '{tipo.name}', encontrei '{tok.valor}'", tok.linha
            )
        return self.avancar()

    def pular_newlines(self):
        while self.tipo_atual() == TokenType.NEWLINE:
            self.avancar()

    def bater(self, *tipos):
        return self.tipo_atual() in tipos

    def parse(self):
        arvore = Programa()
        self.pular_newlines()
        while not self.bater(TokenType.EOF):
            cmd = self.parse_comando()
            if cmd is not None:
                arvore.comandos.append(cmd)
            self.pular_newlines()
        return arvore

    def parse_comando(self):
        tok = self.atual()

        if tok.tipo == TokenType.LET:
            return self.parse_let()
        elif tok.tipo == TokenType.PRINT:
            return self.parse_print()
        elif tok.tipo == TokenType.IDENTIFIER:
            # verifica se é atribuição (x = ...) ou só uma expressão
            proximo = self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None
            if proximo and proximo.tipo == TokenType.ASSIGN:
                return self.parse_atribuicao()
            return self.parse_expr()
        elif tok.tipo in (TokenType.NEWLINE, TokenType.SEMICOLON):
            self.avancar()
            return None
        else:
            raise ErroSintatico(f"não esperava '{tok.valor}' aqui", tok.linha)

    def parse_let(self):
        tok_let = self.avancar()
        nome    = self.esperar(TokenType.IDENTIFIER)
        self.esperar(TokenType.ASSIGN)
        valor = self.parse_expr()
        return DeclaracaoLet(nome.valor, valor, tok_let.linha)

    def parse_atribuicao(self):
        nome = self.avancar()
        self.avancar()  # pula o '='
        valor = self.parse_expr()
        return Atribuicao(nome.valor, valor, nome.linha)

    def parse_print(self):
        tok = self.avancar()
        self.esperar(TokenType.LPAREN)
        valor = self.parse_expr()
        self.esperar(TokenType.RPAREN)
        return ComandoPrint(valor, tok.linha)

    # cuida de + e - (menor prioridade)
    def parse_expr(self):
        esq = self.parse_termo()
        while self.bater(TokenType.PLUS, TokenType.MINUS):
            op  = self.avancar()
            dir = self.parse_termo()
            esq = OperacaoBinaria(op.valor, esq, dir)
        return esq

    # cuida de * e / (maior prioridade)
    def parse_termo(self):
        esq = self.parse_unario()
        while self.bater(TokenType.STAR, TokenType.SLASH):
            op  = self.avancar()
            dir = self.parse_unario()
            esq = OperacaoBinaria(op.valor, esq, dir)
        return esq

    def parse_unario(self):
        if self.bater(TokenType.MINUS):
            op = self.avancar()
            return OperacaoUnaria(op.valor, self.parse_unario())
        return self.parse_primario()

    def parse_primario(self):
        tok = self.atual()

        if tok.tipo == TokenType.INTEGER:
            self.avancar()
            return LiteralInt(tok.valor)
        elif tok.tipo == TokenType.FLOAT:
            self.avancar()
            return LiteralFloat(tok.valor)
        elif tok.tipo == TokenType.IDENTIFIER:
            self.avancar()
            return Variavel(tok.valor, tok.linha)
        elif tok.tipo == TokenType.LPAREN:
            self.avancar()
            expr = self.parse_expr()
            self.esperar(TokenType.RPAREN)
            return expr
        elif tok.tipo == TokenType.EOF:
            raise ErroSintatico('fim de arquivo inesperado', tok.linha)
        else:
            raise ErroSintatico(f"não esperava '{tok.valor}' aqui", tok.linha)

