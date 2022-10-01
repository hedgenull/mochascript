import re

TOKENS = [
    (r"([0-9]+\.?[0-9]*|\.[0-9]+)", "NUMBER"),
    (r"\"[^\"]*\"", "STRING"),
    (r"[a-zA-Z_][a-zA-Z0-9_]*", "IDENT"),
    (r"\(", "LPAREN"),
    (r"\)", "RPAREN"),
    (r"\[", "LBRACK"),
    (r"\]", "RBRACK"),
    (r",", "COMMA"),
    (r"->", "ARROW"),
    (r";", "LINE_TERM"),
    (r"\+=", "PLUS_EQ"),
    (r"\-=", "MINUS_EQ"),
    (r"\*=", "MUL_EQ"),
    (r"\/=", "DIV_EQ"),
    (r"%=", "MOD_EQ"),
    (r"\*\*=", "EXP_EQ"),
    (r"\|\|=", "OR_EQ"),
    (r"&&=", "AND_EQ"),
    (r"==", "EQEQ"),
    (r"!=", "NTEQ"),
    (r"<=", "LTEQ"),
    (r">=", "GTEQ"),
    (r"<", "LT"),
    (r">", "GT"),
    (r"\|\|", "OR"),
    (r"&&", "AND"),
    (r"=", "EQ"),
    (r"([0-9]+\.?[0-9]*|\.[0-9]+)", "NUMBER"),
    (r"\"[^\"]*\"", "STRING"),
    (r"[a-zA-Z_][a-zA-Z0-9_]*", "IDENT"),
    (r"\+", "PLUS"),
    (r"\-", "MINUS"),
    (r"\*", "MUL"),
    (r"\/", "DIV"),
    (r"%", "MOD"),
    (r"\*\*", "EXP"),
    (r"true", "TRUE"),
    (r"false", "FALSE"),
    (r"if", "IF"),
    (r"else", "ELSE"),
    (r"say", "SAY"),
    (r"ask", "ASK"),
    (r"exit", "EXIT"),
    (r"while", "WHILE"),
    (r"for", "FOR"),
    (r"in", "IN"),
    (r"to", "TO"),
    (r"fn", "FN"),
]


class Token(object):
    """A simple Token structure.
    Contains the token type, value and position.
    """

    def __init__(self, type: str, val: str, pos: int) -> None:
        """
        Initialize the Token class.

        Args:
            type: The type of the token.
            val: The value of the token.
            pos: The position of the token.

        Returns:
            None
        """
        self.type = type
        self.val = val
        self.pos = pos

    def __str__(self) -> str:
        return f"{self.type}({self.val}) at {self.pos}"


class LexerError(Exception):
    pass


class Lexer(object):
    """A simple regex-based lexer/tokenizer for MochaScript.
    Adapted from https://gist.github.com/eliben/5797351 """

    def __init__(
        self,
        rules: list[tuple[str, str]],
        skip_whitespace: bool = True,
    ) -> None:
        """Create a lexer.
        rules:
            A list of rules. Each rule is a `regex, type`
            pair, where `regex` is the regular expression used
            to recognize the token and `type` is the type
            of the token to return when it's recognized.
        skip_whitespace:
            If True, whitespace (\s+) will be skipped and not
            reported by the lexer. Otherwise, you have to
            specify your rules for whitespace, or it will be
            flagged as an error.
        """
        regex_parts = []
        self.group_type = {}

        for idx, (regex, type) in enumerate(rules, start=1):
            groupname = f"GROUP{idx}"
            regex_parts.append(f"(?P<{groupname}>{regex})")
            self.group_type[groupname] = type
        self.regex = re.compile("|".join(regex_parts))
        self.skip_whitespace = skip_whitespace
        self.re_ws_skip = re.compile(" \t\n")

    def input(self, buf: str) -> None:
        """Initialize the lexer with a buffer as input."""
        self.buf = buf
        self.pos = 0

    def token(self) -> Token | None:
        """Return the next token (a Token object) found in the
        input buffer. None is returned if the end of the
        buffer was reached.
        In case of a lexing error (the current chunk of the
        buffer matches no rule), a LexerError is raised with
        the position of the error.
        """
        if self.pos >= len(self.buf):
            return None
        if self.skip_whitespace:
            if m := self.re_ws_skip.search(self.buf, self.pos):
                self.pos = m.start()
            else:
                return None

        if m := self.regex.match(self.buf, self.pos):
            groupname = m.lastgroup
            tok_type = self.group_type[groupname]
            tok = Token(tok_type, m.group(groupname), self.pos)
            self.pos = m.end()
            return tok

        # If we're here, no rule matched
        raise LexerError(f"Error at {self.pos}: {self.buf[self.pos]}")

    def tokens(self) -> Token | None:
        """Returns an iterator to the tokens found in the buffer."""
        while True:
            if tok := self.token():
                yield tok
            else:
                break


lexer = Lexer(TOKENS, True)

if __name__ == "__main__":
    lexer.input(
        """
    hello = "world";
    say 4 ** 2;
    ask hello;?
    << >= >
    == = != , //%"""
    )
    for token in lexer.tokens():
        print(token)
