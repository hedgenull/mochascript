import sys

from lex import Lexer
from parse import Parser
from utils import PROMPT


def shell(lexer: Lexer, parser: Parser):
    """Start the interactive shell."""
    while True:
        source = input(PROMPT).strip()
        if not source:
            continue

        if not source.endswith(";"):
            source += ";"

        tokens = lexer.tokenize(source)

        if ast := parser.parse(tokens):
            result = ast.visit()
            # Uncomment next line for debugging purposes
            # print(ast)
            print(result.repr())


if __name__ == "__main__":
    lexer, parser = Lexer(), Parser()
    if len(sys.argv) >= 2:
        with open(sys.argv[1]) as source:
            tokens = lexer.tokenize(source.read())
            ast = parser.parse(tokens)
            ast.visit() if ast else ...
    else:
        print("Starting interactive MochaScript interpreter.")
        shell(lexer, parser)
