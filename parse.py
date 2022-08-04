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

    @_("EXIT expr")
    def expr(self, p):
        """Exit the program"""
        return ExitNode(p.expr)

    @_("SAY expr")
    def expr(self, p):
        """Say-expression"""
        return SayNode(p.expr)

    @_("LPAREN expr IF comp ELSE expr RPAREN")
    def expr(self, p):
        """If-else expression"""
        return IfExpression(p.expr1, p.expr0, p.expr1)

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
        return BinOp("*", p.term, p.factor)

    @_("term DIV factor")
    def term(self, p):
        """Division"""
        return BinOp("/", p.term, p.factor)

    @_("term MOD factor")
    def term(self, p):
        """Modulus"""
        return BinOp("%", p.term, p.factor)

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
        return Number(p.NUMBER)

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

    @_("MINUS expr")
    def atom(self, p):
        """Negated expression"""
        return UnOp("-", p.expr)

    @_("PLUS expr")
    def atom(self, p):
        """Negated expression"""
        return UnOp("+", p.expr)

    @_("array")
    def atom(self, p):
        """Array"""
        return p.array

    @_("LBRACK list RBRACK")
    def array(self, p):
        """Array"""
        return Array(p.list)

    @_("expr COMMA list")
    def list(self, p):
        """Comma-separated list"""
        if isinstance(p.list, tuple):
            return p.expr, *p.list
        else:
            return p.expr, p.list

    @_("expr COMMA")
    def list(self, p):
        """Comma-separated list"""
        return p.expr

    @_("expr")
    def list(self, p):
        """Comma-separated list"""
        return p.expr
