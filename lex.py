import sly


class Lexer(sly.Lexer):
    tokens = {NUMBER, IDENT, EQ, STRING, PLUS, MINUS, MUL, DIV, MOD, LPAREN, RPAREN, PRINT}

    ignore = " \t"

    NUMBER = r"\d+"
    IDENT = r"[a-zA-Z_][a-zA-Z0-9_]*"
    STRING = r"(\"[^\"]*\"|\'[^\']*\')"
    LPAREN = r"\("
    RPAREN = r"\)"
    EQ = r"="
    PLUS = r"\+"
    MINUS = r"\-"
    MUL = r"\*"
    DIV = r"\/"
    MOD = r"\%"

    # Special keywords
    IDENT["print"] = PRINT
