import sly

from lex import Lexer
from obj_model import *


class Parser(sly.Parser):
    debugfile = "parser.debug"

    tokens = Lexer.tokens

    @_("exprs")
    def exprs(self, p):
        return BlockNode(p.exprs, p.expr1)

    @_("expr1 LINE_TERM exprs")
    def exprs(self, p):
        return BlockNode(p.expr1, p.exprs)

    @_("expr1 LINE_TERM")
    def exprs(self, p):
        return p.expr1

    @_("IDENT EQ expr1")
    def expr1(self, p):
        """Assignment expression"""
        return Assignment(p.IDENT, p.expr1)

    @_("expr2")
    def expr1(self, p):
        """Expression"""
        return p.expr2

    @_("EXIT expr1")
    def expr2(self, p):
        """Exit the program"""
        return ExitNode(p.expr1)

    @_("ASK expr1")
    def expr2(self, p):
        """Ask-expression"""
        return AskNode(p.expr1)

    @_("SAY expr1")
    def expr2(self, p):
        """Say-expression"""
        return SayNode(p.expr1)

    @_("FOR IDENT EQ expr1 TO expr1 LPAREN exprs RPAREN")
    def expr2(self, p):
        """For-to loop"""
        return ForExpression(p.IDENT, p.expr10, p.expr11, p.exprs)

    @_("LPAREN exprs IF cmp1 ELSE exprs RPAREN")
    def expr2(self, p):
        """If-else expression"""
        return IfExpression(p[1], p.cmp1, p[-2])

    @_("expr1 PLUS cmp1")
    def expr2(self, p):
        """Addition"""
        return BinOp("+", p.expr1, p.cmp1)

    @_("expr1 MINUS cmp1")
    def expr2(self, p):
        """Subtraction"""
        return BinOp("-", p.expr1, p.cmp1)

    @_("cmp1")
    def expr2(self, p):
        """Component-1"""
        return p.cmp1

    @_("cmp1 AND term")
    def cmp1(self, p):
        """And"""
        return BinOp("&&", p.cmp1, p.term)

    @_("cmp1 OR term")
    def cmp1(self, p):
        """Or"""
        return BinOp("||", p.cmp1, p.term)

    @_("term")
    def cmp1(self, p):
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

    @_("factor EQEQ cmp2")
    def factor(self, p):
        """Equal to"""
        return BinOp("==", p.factor, p.cmp2)

    @_("factor NTEQ cmp2")
    def factor(self, p):
        """Not equal to"""
        return BinOp("!=", p.factor, p.cmp2)

    @_("cmp2")
    def factor(self, p):
        """Component-2"""
        return p.cmp2

    @_("cmp2 LT atom")
    def cmp2(self, p):
        """Less than"""
        return BinOp("<", p.cmp2, p.atom)

    @_("cmp2 GT atom")
    def cmp2(self, p):
        """Greater than"""
        return BinOp(">", p.cmp2, p.atom)

    @_("cmp3")
    def cmp2(self, p):
        """Component-3"""
        return p.cmp3

    @_("cmp3 LTEQ atom")
    def cmp3(self, p):
        """Less than or equal to"""
        return BinOp("<=", p.cmp3, p.atom)

    @_("cmp3 GTEQ atom")
    def cmp3(self, p):
        """Greater than or equal to"""
        return BinOp(">=", p.cmp3, p.atom)

    @_("atom")
    def cmp3(self, p):
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

    @_("LPAREN expr1 RPAREN")
    def atom(self, p):
        """Parenthesized expression"""
        return p.expr1

    @_("MINUS expr1")
    def atom(self, p):
        """Negated expression"""
        return UnOp("-", p.expr2)

    @_("PLUS expr2")
    def atom(self, p):
        """Negated expression"""
        return UnOp("+", p.expr2)

    @_("array")
    def atom(self, p):
        """Array"""
        return p.array

    @_("LBRACK list RBRACK")
    def array(self, p):
        """Array"""
        return Array(p.list)

    @_("expr2 COMMA list")
    def list(self, p):
        """Comma-separated list"""
        if isinstance(p.list, tuple):
            return p.expr2, *p.list
        else:
            return p.expr2, p.list

    @_("expr2 COMMA")
    def list(self, p):
        """Comma-separated list"""
        return p.expr

    @_("expr2")
    def list(self, p):
        """Comma-separated list"""
        return p.expr2
