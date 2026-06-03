"""Compilador Aritmetico Didatico.

Pacote com as 5 fases classicas de um compilador para uma linguagem simples
que suporta declaracao de variaveis (let), reatribuicao, print(...) e as
quatro operacoes aritmeticas.
"""
from .lexer import TokenType, Token, Lexer, ErroLexico
from .ast_nodes import (
    No, LiteralInt, LiteralFloat, Variavel, OperacaoBinaria, OperacaoUnaria,
    DeclaracaoLet, Atribuicao, ComandoPrint, Programa, Visitor, ImpressorAST,
)
from .parser import Parser, ErroSintatico
from .semantic import AnalisadorSemantico, TabelaDeSimbolos, ErroSemantico
from .codegen import GeradorDeCodigo, MaquinaVirtual, compilar_e_rodar

__all__ = [
    "TokenType", "Token", "Lexer", "ErroLexico",
    "No", "LiteralInt", "LiteralFloat", "Variavel", "OperacaoBinaria",
    "OperacaoUnaria", "DeclaracaoLet", "Atribuicao", "ComandoPrint",
    "Programa", "Visitor", "ImpressorAST",
    "Parser", "ErroSintatico",
    "AnalisadorSemantico", "TabelaDeSimbolos", "ErroSemantico",
    "GeradorDeCodigo", "MaquinaVirtual", "compilar_e_rodar",
]
