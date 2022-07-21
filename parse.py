import sly

from lex import Lexer
from obj_model import *


class Parser(sly.Parser):
    debugfile = "parser.debug"

    tokens = Lexer.tokens

    precedence = (
        ("left", PLUS, MINUS),
        ("left", MUL, DIV),
    )

    # Grammar rules and actions

    @_("SHOW expr")
    def expr(self, p):
        print(p.expr.visit())
        return p.expr

    @_("expr PLUS expr")
    def expr(self, p):
        return BinOp("+", p.expr0, p.expr1)

    @_("expr MINUS expr")
    def expr(self, p):
        return BinOp("-", p.expr0, p.expr1)

    @_("expr MUL expr")
    def expr(self, p):
        return BinOp("*", p.expr0, p.expr1)

    @_("expr DIV expr")
    def expr(self, p):
        return BinOp("/", p.expr0, p.expr1)

    @_("expr MOD expr")
    def expr(self, p):
        return BinOp("%", p.expr0, p.expr1)

    @_("NUMBER")
    def expr(self, p):
        return Number(p.NUMBER)

    @_("MINUS NUMBER")
    def expr(self, p):
        n = Number(p.NUMBER)
        n.value = -n.value
        return n

    @_("STRING")
    def expr(self, p):
        return String(p.STRING)

    @_("LPAREN expr RPAREN")
    def expr(self, p):
        return p.expr

    def error(self, tok):
        print(f"Syntax error: Unexpected {tok.value}")
