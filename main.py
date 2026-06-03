"""Ponto de entrada para rodar programas da linguagem (.al).

Uso:
    python main.py                 # roda todos os exemplos de examples/
    python main.py caminho/arq.al  # roda um arquivo .al especifico
"""
import os
import sys

from src import compilar_e_rodar


def rodar_arquivo(caminho):
    with open(caminho, encoding="utf-8") as f:
        codigo = f.read()
    print(f"=== {caminho} ===")
    compilar_e_rodar(codigo)
    print()


def rodar_todos_exemplos():
    pasta = os.path.join(os.path.dirname(__file__), "examples")
    arquivos = sorted(f for f in os.listdir(pasta) if f.endswith(".al"))
    if not arquivos:
        print("Nenhum arquivo .al encontrado em examples/.")
        return
    for nome in arquivos:
        rodar_arquivo(os.path.join(pasta, nome))


def main():
    if len(sys.argv) > 1:
        rodar_arquivo(sys.argv[1])
    else:
        rodar_todos_exemplos()


if __name__ == "__main__":
    main()
