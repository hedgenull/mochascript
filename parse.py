import sly

from lex import Lexer
from obj_model import *


class Parser(sly.Parser):
    debugfile = "parser.debug"

    tokens = Lexer.tokens

    precedence = (
        ("left", PLUS, MINUS),
        ("left", MUL, DIV, MOD),
        ("left", EQEQ, NTEQ, LT, GT, LTEQ, GTEQ),
    )

    # Grammar rules and actions

    @_("IDENT LPAREN expr RPAREN")
    def expr(self, p):
        if not isinstance(ENV[-1][p.IDENT], Function):
            abort(f"Not a function: {p.IDENT}")
        else:
            fn = ENV[-1][p.IDENT]
            return fn.call(p.expr.visit())

    @_("FN LPAREN IDENT RPAREN ARROW LPAREN expr RPAREN")
    def expr(self, p):
        return UserDefinedFunction(p.IDENT, expr=p.expr)

    @_("IDENT EQ expr")
    def expr(self, p):
        """Assignment expression"""
        return Assignment(p.IDENT, p.expr.visit())

    @_("LPAREN expr IF expr ELSE expr RPAREN")
    def expr(self, p):
        """If-else expression"""
        return IfNode(p.expr1, p.expr0, p.expr2)

    @_("expr PLUS term")
    def expr(self, p):
        """Addition"""
        return BinOp("+", p.expr, p.term)

    @_("expr MINUS term")
    def expr(self, p):
        """Subtraction"""
        return BinOp("-", p.expr, p.term)

    @_("term")
    def expr(self, p):
        """Term"""
        return p.term

    @_("term MUL atom")
    def term(self, p):
        """Multiplication"""
        return BinOp("*", p.term, p.atom)

    @_("term DIV atom")
    def term(self, p):
        """Division"""
        return BinOp("/", p.term, p.atom)

    @_("atom")
    def term(self, p):
        """Atom"""
        return p.atom

    @_("NUMBER")
    def atom(self, p):
        """Number"""
        return Number(p.NUMBER)

    @_("MINUS NUMBER")
    def atom(self, p):
        """Negative number"""
        n = Number(p.NUMBER)
        n.value = -n.value
        return n

    @_("STRING")
    def atom(self, p):
        """String"""
        return String(p.STRING)

    @_("IDENT")
    def atom(self, p):
        """Variable reference"""
        if val := ENV[-1].get(p.IDENT):
            return val
        else:
            abort(f"Undefined variable {p.IDENT}")

    @_("LPAREN expr RPAREN")
    def atom(self, p):
        """Parenthesized expression"""
        return p.expr

    def error(self, tok):
        """Ruh roh"""
        print(f"Syntax error: Unexpected {tok.value}")
