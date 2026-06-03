"""Casos de teste automatizados do compilador (>= 20 casos)."""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.lexer import Lexer, ErroLexico
from src.parser import Parser, ErroSintatico
from src.semantic import AnalisadorSemantico, ErroSemantico
from src.codegen import compilar_e_rodar


testes = [
    ('adicao',              lambda: compilar_e_rodar('let a=3\nlet b=4\nprint(a+b)') == ['7']),
    ('subtracao',           lambda: compilar_e_rodar('let a=10\nlet b=3\nprint(a-b)') == ['7']),
    ('multiplicacao',       lambda: compilar_e_rodar('let a=6\nlet b=7\nprint(a*b)') == ['42']),
    ('divisao float',       lambda: compilar_e_rodar('print(10/4)') == ['2.5']),
    ('divisao sempre float',lambda: compilar_e_rodar('print(10/2)') == ['5.0']),
    ('precedencia *>+',     lambda: compilar_e_rodar('print(2+3*4)') == ['14']),
    ('parenteses',          lambda: compilar_e_rodar('print((2+3)*4)') == ['20']),
    ('encadeado',           lambda: compilar_e_rodar('print(10-3-2)') == ['5']),
    ('parenteses aninhados',lambda: compilar_e_rodar('print((2+(3*4))-1)') == ['13']),
    ('let basico',          lambda: compilar_e_rodar('let x=42\nprint(x)') == ['42']),
    ('atribuicao',          lambda: compilar_e_rodar('let x=10\nx=x+5\nprint(x)') == ['15']),
    ('float',               lambda: compilar_e_rodar('let pi=3.14\nprint(pi)') == ['3.14']),
    ('multiplos prints',    lambda: compilar_e_rodar('let a=10\nlet b=3\nprint(a+b)\nprint(a-b)') == ['13','7']),
    ('int+float=float',     lambda: compilar_e_rodar('let x=1+0.5\nprint(x)') == ['1.5']),
    ('negacao unaria',      lambda: compilar_e_rodar('let x=5\nprint(-x+10)') == ['5']),
    ('comentario',          lambda: compilar_e_rodar('let x=10 # ok\nprint(x)') == ['10']),
]

erros = [
    ('erro lexico @',       lambda: (Lexer('let x=10@5').tokenizar(), False),         ErroLexico),
    ('erro lexico $',       lambda: (Lexer('$10').tokenizar(), False),                ErroLexico),
    ('erro sintatico paren',lambda: (Parser(Lexer('print(10+5').tokenizar()).parse(), False),   ErroSintatico),
    ('erro sintatico expr', lambda: (Parser(Lexer('let x=2+').tokenizar()).parse(), False),     ErroSintatico),
    ('erro sem nao decl',   lambda: (AnalisadorSemantico().analisar(Parser(Lexer('print(y)').tokenizar()).parse()), False),               ErroSemantico),
    ('erro sem redecl',     lambda: (AnalisadorSemantico().analisar(Parser(Lexer('let x=1\nlet x=2').tokenizar()).parse()), False),       ErroSemantico),
    ('erro sem sem let',    lambda: (AnalisadorSemantico().analisar(Parser(Lexer('z=10').tokenizar()).parse()), False),                   ErroSemantico),
    ('divisao por zero',    lambda: (compilar_e_rodar('print(1/0)'), False),          RuntimeError),
]


def rodar_testes():
    ok = 0
    falhou = 0

    for nome, fn in testes:
        try:
            assert fn()
            print(f"  [OK] {nome}")
            ok += 1
        except Exception as e:
            print(f"  [FALHOU] {nome}: {e}")
            falhou += 1

    for nome, fn, tipo_erro in erros:
        try:
            fn()
            print(f"  [FALHOU] {nome}: deveria ter lancado {tipo_erro.__name__}")
            falhou += 1
        except tipo_erro:
            print(f"  [OK] {nome}")
            ok += 1
        except Exception as e:
            print(f"  [FALHOU] {nome}: erro inesperado - {e}")
            falhou += 1

    print(f"\nResultado: {ok}/{ok + falhou} testes passaram")
    return falhou == 0


def test_suite_completa():
    """Ponto de entrada para o pytest."""
    assert rodar_testes()


if __name__ == "__main__":
    sucesso = rodar_testes()
    sys.exit(0 if sucesso else 1)
