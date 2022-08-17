import sly

from lex import Lexer
from obj_model import *


class Parser(sly.Parser):
    tokens = Lexer.tokens

    @_("expr LINE_TERM program")
    def program(self, p):
        return BlockNode(p.expr, p.program)

    @_("expr LINE_TERM")
    def program(self, p):
        return p.expr

    @_("IDENT EQ expr")
    def expr(self, p):
        """Assignment expression"""
        return Assignment(p.IDENT, p.expr)

    @_("EXIT")
    def expr(self, p):
        """Exit-expression"""
        return ExitNode()

    @_("EXIT expr")
    def expr(self, p):
        """Exit-expression"""
        return ExitNode(p.expr)

    @_("ASK expr")
    def expr(self, p):
        """Ask-expression"""
        return AskNode(p.expr)

    @_("SAY expr")
    def expr(self, p):
        """Say-expression"""
        return SayNode(p.expr)

    @_("or_expr LPAREN comma_sep RPAREN")
    def expr(self, p):
        """Function call, with arguments"""
        return (
            CallNode(p.or_expr, p.comma_sep)
            if isinstance(p.comma_sep, tuple)
            else CallNode(p.or_expr, [p.comma_sep])
        )

    @_("or_expr LPAREN RPAREN")
    def expr(self, p):
        """Function call, without arguments"""
        return CallNode(p.or_expr, [])

    @_("LPAREN expr IF or_expr ELSE expr RPAREN")
    def expr(self, p):
        """If-expression"""
        return IfNode(p.expr0, p.or_expr, p.expr1)

    @_("LPAREN expr WHILE or_expr LPAREN")
    def expr(self, p):
        """While-expression"""
        return WhileNode(p.or_expr0, p.or_expr1)

    @_("or_expr")
    def expr(self, p):
        """Or-expression"""
        return p.or_expr

    @_("and_expr OR and_expr")
    def or_expr(self, p):
        """Or-expression"""
        return BinOp("||", p.and_expr0, p.and_expr1)

    @_("and_expr")
    def or_expr(self, p):
        """And-expression"""
        return p.and_expr

    @_("equals_expr AND equals_expr")
    def and_expr(self, p):
        """And-expression"""
        return BinOp("&&", p.equals_expr0, p.equals_expr1)

    @_("equals_expr")
    def and_expr(self, p):
        """Equals or not-equals expression"""
        return p.equals_expr

    @_("comp_expr EQEQ comp_expr")
    def equals_expr(self, p):
        """Equals-expression"""
        return BinOp("==", p.comp_expr0, p.comp_expr1)

    @_("comp_expr NTEQ comp_expr")
    def equals_expr(self, p):
        """Not-equals expression"""
        return BinOp("!=", p.comp_expr0, p.comp_expr1)

    @_("comp_expr")
    def equals_expr(self, p):
        """Comparison expression"""
        return p.comp_expr

    @_("plus_expr LT plus_expr")
    def comp_expr(self, p):
        """Less-than expression"""
        return BinOp("<", p.plus_expr0, p.plus_expr1)

    @_("plus_expr GT plus_expr")
    def comp_expr(self, p):
        """Greater-than expression"""
        return BinOp(">", p.plus_expr0, p.plus_expr1)

    @_("plus_expr LTEQ plus_expr")
    def comp_expr(self, p):
        """Less-than expression"""
        return BinOp("<=", p.plus_expr0, p.plus_expr1)

    @_("plus_expr GTEQ plus_expr")
    def comp_expr(self, p):
        """Greater-than expression"""
        return BinOp(">=", p.plus_expr0, p.plus_expr1)

    @_("plus_expr")
    def comp_expr(self, p):
        """Addition or subtraction expression"""
        return p.plus_expr

    @_("mul_expr PLUS mul_expr")
    def plus_expr(self, p):
        """Addition expression"""
        return BinOp("+", p.mul_expr0, p.mul_expr1)

    @_("mul_expr MINUS mul_expr")
    def plus_expr(self, p):
        """Subtraction expression"""
        return BinOp("-", p.mul_expr0, p.mul_expr1)

    @_("mul_expr")
    def plus_expr(self, p):
        """Multiplication, division, or modulus expression"""
        return p.mul_expr

    @_("atom MUL atom")
    def mul_expr(self, p):
        """Multiplication expression"""
        return BinOp("*", p.atom0, p.atom1)

    @_("atom DIV atom")
    def mul_expr(self, p):
        """Division expression"""
        return BinOp("/", p.atom0, p.atom1)

    @_("atom MOD atom")
    def mul_expr(self, p):
        """Modulus expression"""
        return BinOp("%", p.atom0, p.atom1)

    @_("atom")
    def mul_expr(self, p):
        """Atomic expression"""
        return p.atom

    @_("MINUS atom")
    def atom(self, p):
        """Negated atom"""
        return UnOp("-", p.atom)

    @_("PLUS atom")
    def atom(self, p):
        """Positive atom"""
        return UnOp("+", p.atom)

    @_("LPAREN program RPAREN")
    def atom(self, p):
        """Parenthesized block"""
        return p.program

    @_("LPAREN expr RPAREN")
    def atom(self, p):
        """Parenthesized expression"""
        return p.expr

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
        """Variable or constant reference"""
        return Reference(p.IDENT)

    @_("array")
    def atom(self, p):
        """Array"""
        return p.array

    @_("FN LPAREN func_params RPAREN ARROW LPAREN expr RPAREN")
    def atom(self, p):
        """Function definition"""
        return (
            Function(p.expr, list(p.func_params))
            if isinstance(p.func_params, tuple)
            else Function(p.expr, [p.func_params])
        )

    @_("FN LPAREN RPAREN ARROW LPAREN expr RPAREN")
    def atom(self, p):
        """Function definition"""
        return Function(p.expr, [])

    @_("IDENT COMMA func_params")
    def func_params(self, p):
        """Function parameters"""
        if isinstance(p.func_params, tuple):
            return p.IDENT, *p.func_params
        else:
            return p.IDENT, p.func_params

    @_("IDENT COMMA")
    def func_params(self, p):
        """Function parameters"""
        if isinstance(p.func_params, tuple):
            return p.IDENT, *p.func_params
        else:
            return p.IDENT, p.func_params

    @_("IDENT")
    def func_params(self, p):
        """Function parameters"""
        return Assignment(p.IDENT, Boolean(False))

    @_("LBRACK comma_sep RBRACK")
    def array(self, p):
        """Array"""
        if isinstance(p.comma_sep, Atom):
            return Array([p.comma_sep])
        return Array(p.comma_sep)

    @_("LBRACK RBRACK")
    def array(self, p):
        """Empty array"""
        return Array()

    @_("expr COMMA comma_sep")
    def comma_sep(self, p):
        """Comma-separated list"""
        if isinstance(p.comma_sep, tuple):
            return p.expr, *p.comma_sep
        else:
            return p.expr, p.comma_sep

    @_("expr COMMA")
    def comma_sep(self, p):
        """Comma-separated list"""
        return p.expr

    @_("expr")
    def comma_sep(self, p):
        """Comma-separated list"""
        return p.expr
