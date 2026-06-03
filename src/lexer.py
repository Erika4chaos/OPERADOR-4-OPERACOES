"""Fase 1: Analise Lexica."""
from enum import Enum, auto
from dataclasses import dataclass


# tipos de token que a linguagem aceita
class TokenType(Enum):
    # literais
    INTEGER  = auto()
    FLOAT    = auto()

    # nome de variavel
    IDENTIFIER = auto()

    # palavras reservadas
    LET   = auto()
    PRINT = auto()

    # operadores
    PLUS  = auto()
    MINUS = auto()
    STAR  = auto()
    SLASH = auto()

    # outros simbolos
    ASSIGN    = auto()
    LPAREN    = auto()
    RPAREN    = auto()
    SEMICOLON = auto()
    NEWLINE   = auto()
    EOF       = auto()


@dataclass
class Token:
    tipo: TokenType
    valor: any
    linha: int
    coluna: int


class ErroLexico(Exception):
    def __init__(self, msg, linha, col):
        super().__init__(f'Erro Léxico (linha {linha}, col {col}): {msg}')
        self.linha = linha
        self.col   = col


class Lexer:
    def __init__(self, codigo):
        self.codigo = codigo
        self.pos    = 0
        self.linha  = 1
        self.col    = 1

    def char_atual(self):
        if self.pos >= len(self.codigo):
            return None
        return self.codigo[self.pos]

    def proximo_char(self):
        if self.pos + 1 >= len(self.codigo):
            return None
        return self.codigo[self.pos + 1]

    def avancar(self):
        ch = self.codigo[self.pos]
        self.pos += 1
        if ch == '\n':
            self.linha += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def pular_espacos_e_comentarios(self):
        while self.char_atual() in (' ', '\t', '\r', '#'):
            if self.char_atual() == '#':
                # ignora o resto da linha
                while self.char_atual() is not None and self.char_atual() != '\n':
                    self.avancar()
            else:
                self.avancar()

    def ler_numero(self):
        col_inicio = self.col
        numero = ''
        while self.char_atual() and self.char_atual().isdigit():
            numero += self.avancar()

        # se tiver ponto, é float
        if self.char_atual() == '.':
            numero += self.avancar()
            while self.char_atual() and self.char_atual().isdigit():
                numero += self.avancar()
            return Token(TokenType.FLOAT, float(numero), self.linha, col_inicio)

        return Token(TokenType.INTEGER, int(numero), self.linha, col_inicio)

    def ler_identificador(self):
        col_inicio = self.col
        palavra = ''
        while self.char_atual() and (self.char_atual().isalnum() or self.char_atual() == '_'):
            palavra += self.avancar()

        # verifica se é palavra reservada
        palavras_reservadas = {
            'let':   TokenType.LET,
            'print': TokenType.PRINT
        }
        tipo = palavras_reservadas.get(palavra, TokenType.IDENTIFIER)
        return Token(tipo, palavra, self.linha, col_inicio)

    def tokenizar(self):
        lista_tokens = []

        while True:
            self.pular_espacos_e_comentarios()

            if self.char_atual() is None:
                lista_tokens.append(Token(TokenType.EOF, 'EOF', self.linha, self.col))
                break

            ch  = self.char_atual()
            lin = self.linha
            col = self.col

            if ch == '\n':
                self.avancar()
                lista_tokens.append(Token(TokenType.NEWLINE, '\n', lin, col))

            elif ch.isdigit():
                lista_tokens.append(self.ler_numero())

            elif ch == '-' and self.proximo_char() and self.proximo_char().isdigit():
                # decide se é operador ou número negativo
                tipo_anterior = lista_tokens[-1].tipo if lista_tokens else None
                if tipo_anterior in (TokenType.INTEGER, TokenType.FLOAT,
                                     TokenType.IDENTIFIER, TokenType.RPAREN):
                    self.avancar()
                    lista_tokens.append(Token(TokenType.MINUS, '-', lin, col))
                else:
                    self.avancar()
                    tok = self.ler_numero()
                    tok.valor = -tok.valor
                    tok.coluna = col
                    lista_tokens.append(tok)

            elif ch.isalpha() or ch == '_':
                lista_tokens.append(self.ler_identificador())

            elif ch == '+':
                self.avancar()
                lista_tokens.append(Token(TokenType.PLUS, '+', lin, col))
            elif ch == '-':
                self.avancar()
                lista_tokens.append(Token(TokenType.MINUS, '-', lin, col))
            elif ch == '*':
                self.avancar()
                lista_tokens.append(Token(TokenType.STAR, '*', lin, col))
            elif ch == '/':
                self.avancar()
                lista_tokens.append(Token(TokenType.SLASH, '/', lin, col))
            elif ch == '=':
                self.avancar()
                lista_tokens.append(Token(TokenType.ASSIGN, '=', lin, col))
            elif ch == '(':
                self.avancar()
                lista_tokens.append(Token(TokenType.LPAREN, '(', lin, col))
            elif ch == ')':
                self.avancar()
                lista_tokens.append(Token(TokenType.RPAREN, ')', lin, col))
            elif ch == ';':
                self.avancar()
                lista_tokens.append(Token(TokenType.SEMICOLON, ';', lin, col))
            else:
                raise ErroLexico(f"caractere '{ch}' não reconhecido", lin, col)

        return lista_tokens

print('Lexer carregado')
