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
        ARROW,
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

    # Literals and identifiers
    NUMBER = r"([0-9]+\.?[0-9]*|\.[0-9]+)"
    STRING = r"\"[^\"]*\""
    IDENT = r"[a-zA-Z_][a-zA-Z0-9_]*"

    # Parentheses types
    LPAREN = r"\("
    RPAREN = r"\)"
    LBRACK = r"\["
    RBRACK = r"\]"

    # Special
    COMMA = r","
    ARROW = r"->"
    LINE_TERM = ";"

    # Operator-assignments
    PLUSEQ = r"\+="
    MINUSEQ = r"\-="
    MULEQ = r"\*="
    DIVEQ = r"\/="
    MODEQ = r"%="
    EXPEQ = r"\*\*="
    OREQ = r"\|\|="
    ANDEQ = r"&&="

    # Comparison operators
    EQEQ = r"=="
    NTEQ = r"!="
    LTEQ = r"<="
    GTEQ = r">="
    LT = r"<"
    GT = r">"

    # Logical operators
    AND = r"\&\&"
    OR = r"\|\|"

    # Mathematical operators
    PLUS = r"\+"
    MINUS = r"\-"
    MUL = r"\*"
    DIV = r"\/"
    MOD = r"\%"
    EXP = r"\*\*"

    # Assignment operator
    EQ = r"="

    # Keywords
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
