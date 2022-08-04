import sly


class Lexer(sly.Lexer):
    tokens = {
        NEWLINE,
        NUMBER,
        IDENT,
        STRING,
        LPAREN,
        RPAREN,
        LBRACK,
        RBRACK,
        COMMA,
        EQEQ,
        NTEQ,
        LTEQ,
        GTEQ,
        LT,
        GT,
        EQ,
        AND,
        OR,
        PLUS,
        MINUS,
        MUL,
        DIV,
        MOD,
        ARROW,
        IF,
        ELSE,
        SAY,
        ASK,
        EXIT,
    }

    ignore = " \t"
    ignore_comment = r"#.*"

    NEWLINE = "\n"
    NUMBER = r"([0-9]+\.?[0-9]*|\.[0-9]+)"
    IDENT = r"[a-zA-Z_][a-zA-Z0-9_]*"
    STRING = r"\"[^\"]*\""
    LPAREN = r"\("
    RPAREN = r"\)"
    LBRACK = r"\["
    RBRACK = r"\]"
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
    ARROW = r"=>"

    # Special keywords
    IDENT["if"] = IF
    IDENT["else"] = ELSE
    IDENT["say"] = SAY
    IDENT["ask"] = ASK
    IDENT["exit"] = EXIT
