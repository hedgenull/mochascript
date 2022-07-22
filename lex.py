import sly


class Lexer(sly.Lexer):
    tokens = {
        NUMBER,
        IDENT,
        EQ,
        EQEQ,
        NTEQ,
        LT,
        GT,
        LTEQ,
        GTEQ,
        STRING,
        PLUS,
        MINUS,
        MUL,
        DIV,
        MOD,
        LPAREN,
        RPAREN,
        IF,
        ELSE,
        ARROW,
        FN,
        COMMA,
        AND,
        OR
    }

    ignore = " \t"
    ignore_comment = r"#.*"

    NUMBER = r"\d+"
    IDENT = r"[a-zA-Z_][a-zA-Z0-9_]*"
    STRING = r"(\"[^\"]*\"|\'[^\']*\')"
    LPAREN = r"\("
    RPAREN = r"\)"
    ARROW = r"=>"
    COMMA = r","
    EQEQ = r"=="
    NTEQ = r"!="
    LTEQ = r"<="
    GTEQ = r">="
    LT = r"<"
    GT = r">"
    EQ = r"="
    AND = r"\&\&"
    OR = r"\|\|"
    PLUS = r"\+"
    MINUS = r"\-"
    MUL = r"\*"
    DIV = r"\/"
    MOD = r"\%"

    # Special keywords
    IDENT["if"] = IF
    IDENT["else"] = ELSE
    IDENT["fn"] = FN
