import sly


class Lexer(sly.Lexer):
    """MochaScript lexer class."""

    tokens = {
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
        EXP,
        DIV,
        MOD,
        ARROW,
        LINE_TERM,
        FALSE,
        TRUE,
        IF,
        ELSE,
        SAY,
        ASK,
        EXIT,
        FOR,
        WHILE,
        TO,
        IN,
        FN,
    }

    ignore = " \t\n"
    ignore_comment = r"#.*"

    NUMBER = r"([0-9]+\.?[0-9]*|\.[0-9]+)"
    IDENT = r"[a-zA-Z_][a-zA-Z0-9_]*"
    STRING = r"\"[^\"]*\""
    LPAREN = r"\("
    RPAREN = r"\)"
    LBRACK = r"\["
    RBRACK = r"\]"
    COMMA = r","
    ARROW = r"->"
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
    EXP = r"\*\*"
    MUL = r"\*"
    DIV = r"\/"
    MOD = r"\%"
    LINE_TERM = ";"

    # Special keywords
    IDENT["false"] = FALSE
    IDENT["true"] = TRUE
    IDENT["if"] = IF
    IDENT["else"] = ELSE
    IDENT["say"] = SAY
    IDENT["ask"] = ASK
    IDENT["exit"] = EXIT
    IDENT["for"] = FOR
    IDENT["while"] = WHILE
    IDENT["to"] = TO
    IDENT["in"] = IN
    IDENT["fn"] = FN
