import sly

from lex import Lexer
from obj_model import *


class Parser(sly.Parser):
    debugfile = "parser.debug"

    tokens = Lexer.tokens

    # Grammar rules and actions

    @_("IDENT EQ expr")
    def expr(self, p):
        """Assignment expression"""
        return Assignment(p.IDENT, p.expr)

    @_("LPAREN expr IF comp ELSE expr RPAREN")
    def expr(self, p):
        """If-else expression"""
        return IfNode(p.expr1, p.expr0, p.expr2)

    @_("expr PLUS comp")
    def expr(self, p):
        """Addition"""
        return BinOp("+", p.expr, p.comp)

    @_("expr MINUS comp")
    def expr(self, p):
        """Subtraction"""
        return BinOp("-", p.expr, p.comp)

    @_("comp")
    def expr(self, p):
        """Comparison"""
        return p.comp

    @_("comp AND term")
    def comp(self, p):
        """And"""
        return BinOp("&&", p.comp, p.term)

    @_("comp OR term")
    def comp(self, p):
        """Or"""
        return BinOp("||", p.comp, p.term)

    @_("term")
    def comp(self, p):
        """Term"""
        return p.term

    @_("term MUL factor")
    def term(self, p):
        """Multiplication"""
        return BinOp("*", p.term, p.atom)

    @_("term DIV factor")
    def term(self, p):
        """Division"""
        return BinOp("/", p.term, p.atom)

    @_("term MOD factor")
    def term(self, p):
        """Modulus"""
        return BinOp("%", p.term, p.atom)

    @_("factor")
    def term(self, p):
        """Factor"""
        return p.factor

    @_("factor EQEQ atom")
    def factor(self, p):
        """Equal to"""
        return BinOp("==", p.factor, p.atom)

    @_("factor NTEQ atom")
    def factor(self, p):
        """Not equal to"""
        return BinOp("!=", p.factor, p.atom)

    @_("factor LT atom")
    def factor(self, p):
        """Less than"""
        return BinOp("<", p.factor, p.atom)

    @_("factor GT atom")
    def factor(self, p):
        """Greater than"""
        return BinOp(">", p.factor, p.atom)

    @_("factor LTEQ atom")
    def factor(self, p):
        """Less than or equal to"""
        return BinOp("<=", p.factor, p.atom)

    @_("factor GTEQ atom")
    def factor(self, p):
        """Greater than or equal to"""
        return BinOp(">=", p.factor, p.atom)

    @_("atom")
    def factor(self, p):
        """Atom"""
        return p.atom

    @_("NUMBER")
    def atom(self, p):
        """Number"""
        return Number(p.NUMBER.replace("~", "-"))

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
