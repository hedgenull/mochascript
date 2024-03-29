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
        return AssignmentNode(p.IDENT, p.expr)

    @_(
        "IDENT PLUSEQ or_expr",
        "IDENT MINUSEQ or_expr",
        "IDENT MULEQ or_expr",
        "IDENT DIVEQ or_expr",
        "IDENT MODEQ or_expr",
        "IDENT EXPEQ or_expr",
        "IDENT OREQ or_expr",
        "IDENT ANDEQ or_expr",
    )
    def expr(self, p):
        """In-place assignment expression"""
        return InPlaceAssignmentNode(p[1].strip("="), p.IDENT, p.or_expr)

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
            CallFunctionNode(p.or_expr, p.comma_sep)
            if isinstance(p.comma_sep, tuple)
            else CallFunctionNode(p.or_expr, [p.comma_sep])
        )

    @_("or_expr LPAREN RPAREN")
    def expr(self, p):
        """Function call, without arguments"""
        return CallFunctionNode(p.or_expr, [])

    @_("WHILE or_expr LPAREN expr RPAREN", "WHILE or_expr LPAREN program RPAREN")
    def expr(self, p):
        """While-loop expression"""
        return WhileNode(p.or_expr, p[-2])

    @_("LPAREN expr WHILE or_expr RPAREN", "LPAREN program WHILE or_expr RPAREN")
    def expr(self, p):
        """While-loop expression"""
        return WhileNode(p.or_expr, p[1])

    @_(
        "LPAREN expr IF or_expr ELSE expr RPAREN",
        "LPAREN program IF or_expr ELSE program RPAREN",
    )
    def expr(self, p):
        """If-expression"""
        return IfNode(p.or_expr, p[1], p[-2])

    @_(
        "IF or_expr LPAREN expr RPAREN ELSE LPAREN expr RPAREN",
        "IF or_expr LPAREN program RPAREN ELSE LPAREN program RPAREN",
    )
    def expr(self, p):
        """If-expression"""
        return IfNode(p.or_expr, p[3], p[-2])

    @_(
        "LPAREN expr FOR IDENT IN or_expr RPAREN",
        "LPAREN program FOR IDENT IN or_expr RPAREN",
    )
    def expr(self, p):
        """For-loop expression"""
        return ForNode(p[-2], p.IDENT, p[1])

    @_(
        "FOR IDENT IN or_expr LPAREN expr RPAREN",
        "FOR IDENT IN or_expr RPAREN program RPAREN",
    )
    def expr(self, p):
        """For-loop expression"""
        return ForNode(p.or_expr, p.IDENT, p[-2])

    @_("or_expr")
    def expr(self, p):
        """Or-expression"""
        return p.or_expr

    @_("or_expr OR and_expr")
    def or_expr(self, p):
        """Or-expression"""
        return BinOp("||", p.or_expr, p.and_expr)

    @_("and_expr")
    def or_expr(self, p):
        """And-expression"""
        return p.and_expr

    @_("and_expr AND equals_expr")
    def and_expr(self, p):
        """And-expression"""
        return BinOp("&&", p.and_expr, p.equals_expr)

    @_("equals_expr")
    def and_expr(self, p):
        """Equals or not-equals expression"""
        return p.equals_expr

    @_("equals_expr EQEQ comp_expr")
    def equals_expr(self, p):
        """Equals-expression"""
        return BinOp("==", p.equals_expr, p.comp_expr)

    @_("equals_expr NTEQ comp_expr")
    def equals_expr(self, p):
        """Not-equals expression"""
        return BinOp("!=", p.equals_expr, p.comp_expr)

    @_("comp_expr")
    def equals_expr(self, p):
        """Comparison expression"""
        return p.comp_expr

    @_("comp_expr LT plus_expr")
    def comp_expr(self, p):
        """Less-than expression"""
        return BinOp("<", p.comp_expr, p.plus_expr)

    @_("comp_expr GT plus_expr")
    def comp_expr(self, p):
        """Greater-than expression"""
        return BinOp(">", p.comp_expr, p.plus_expr)

    @_("comp_expr LTEQ plus_expr")
    def comp_expr(self, p):
        """Less-than expression"""
        return BinOp("<=", p.comp_expr, p.plus_expr)

    @_("comp_expr GTEQ plus_expr")
    def comp_expr(self, p):
        """Greater-than expression"""
        return BinOp(">=", p.comp_expr, p.plus_expr)

    @_("plus_expr")
    def comp_expr(self, p):
        """Addition or subtraction expression"""
        return p.plus_expr

    @_("plus_expr PLUS mul_expr")
    def plus_expr(self, p):
        """Addition expression"""
        return BinOp("+", p.plus_expr, p.mul_expr)

    @_("plus_expr MINUS mul_expr")
    def plus_expr(self, p):
        """Subtraction expression"""
        return BinOp("-", p.plus_expr, p.mul_expr)

    @_("mul_expr")
    def plus_expr(self, p):
        """Multiplication, division, modulus, or range expression"""
        return p.mul_expr

    @_("mul_expr MUL exp_expr")
    def mul_expr(self, p):
        """Multiplication expression"""
        return BinOp("*", p.mul_expr, p.exp_expr)

    @_("mul_expr DIV exp_expr")
    def mul_expr(self, p):
        """Division expression"""
        return BinOp("/", p.mul_expr, p.exp_expr)

    @_("mul_expr MOD exp_expr")
    def mul_expr(self, p):
        """Modulus expression"""
        return BinOp("%", p.mul_expr, p.exp_expr)

    @_("exp_expr")
    def mul_expr(self, p):
        """Exponent expression"""
        return p.exp_expr

    @_("exp_expr EXP rng_expr")
    def exp_expr(self, p):
        """Exponent expression"""
        return BinOp("**", p.exp_expr, p.rng_expr)

    @_("rng_expr")
    def exp_expr(self, p):
        """Range or containment expression"""
        return p.rng_expr

    @_("rng_expr TO atom")
    def rng_expr(self, p):
        """Range definition"""
        return RangeNode(p.rng_expr, p.atom)

    @_("rng_expr IN atom")
    def rng_expr(self, p):
        """Array-contains expression"""
        return BinOp("in", p.atom, p.rng_expr)

    @_("atom")
    def rng_expr(self, p):
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

    @_("expr DOT IDENT")
    def atom(self, p):
        """Getattr expression"""
        return BinOp(".", p.expr, p.IDENT)

    @_("IDENT")
    def atom(self, p):
        """Variable or constant reference"""
        return ReferenceNode(p.IDENT)

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

    @_("FN IDENT LPAREN func_params RPAREN ARROW LPAREN expr RPAREN")
    def atom(self, p):
        """Function definition"""
        return (
            Function(p.expr, list(p.func_params), name=p.IDENT)
            if isinstance(p.func_params, tuple)
            else Function(p.expr, [p.func_params], name=p.IDENT)
        )

    @_("FN IDENT LPAREN RPAREN ARROW LPAREN expr RPAREN")
    def atom(self, p):
        """Function definition"""
        return Function(p.expr, [], name=p.IDENT)

    @_("FN LPAREN func_params RPAREN ARROW LPAREN program RPAREN")
    def atom(self, p):
        """Function definition"""
        return (
            Function(p.program, list(p.func_params))
            if isinstance(p.func_params, tuple)
            else Function(p.program, [p.func_params])
        )

    @_("FN LPAREN RPAREN ARROW LPAREN program RPAREN")
    def atom(self, p):
        """Function definition"""
        return Function(p.expr, [])

    @_("FN IDENT LPAREN func_params RPAREN ARROW LPAREN program RPAREN")
    def atom(self, p):
        """Function definition"""
        return (
            Function(p.program, list(p.func_params), name=p.IDENT)
            if isinstance(p.func_params, tuple)
            else Function(p.program, [p.func_params], name=p.IDENT)
        )

    @_("FN IDENT LPAREN RPAREN ARROW LPAREN program RPAREN")
    def atom(self, p):
        """Function definition"""
        return Function(p.program, [], name=p.IDENT)

    @_("LBRACE key_val_pairs RBRACE")
    def atom(self, p):
        """Object"""
        return Object(p.key_val_pairs)

    @_("LBRACE RBRACE")
    def atom(self, p):
        """Empty object"""
        return Object()

    @_("FALSE")
    def atom(self, p):
        """False"""
        return Boolean(False)

    @_("TRUE")
    def atom(self, p):
        """True"""
        return Boolean(True)

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
        return p.IDENT

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

    @_("key_val_pair COMMA key_val_pairs")
    def key_val_pairs(self, p):
        return {**p.key_val_pair, **p.key_val_pairs}

    @_("key_val_pair", "key_val_pair COMMA")
    def key_val_pairs(self, p):
        return p.key_val_pair

    @_("STRING COLON expr")
    def key_val_pair(self, p):
        return {p.STRING: p.expr}
