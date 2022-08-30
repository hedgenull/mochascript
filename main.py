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
        ast = parser.parse(tokens)
        # Uncomment this line if you want to print the AST details for debugging
        # print(ast)
        try:
            result = ast.visit()
        except AttributeError as e:
            print(f"Error: {e}")
        else:
            print(result.repr())


if __name__ == "__main__":
    lexer, parser = Lexer(), Parser()
    if len(sys.argv) >= 2:
        with open(sys.argv[1]) as source:
            tokens = lexer.tokenize(source.read())
            ast = parser.parse(tokens)
            ast.visit()
    else:
        print("Starting interactive MochaScript interpreter.")
        shell(lexer, parser)
