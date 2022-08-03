import sys

from lex import Lexer
from parse import Parser


def shell(lexer: Lexer, parser: Parser):
    """Start the interactive shell."""
    while True:
        source = input(">>> ").strip().split("#")[0]
        if source == "exit":
            break
        elif source == "":
            continue
        tokens = lexer.tokenize(source)
        ast = parser.parse(tokens)
        result = ast.visit()

        print(result.repr())


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        print("Starting Echo* interpreter.")
        with open(sys.argv[1]) as source:
            Parser().parse(Lexer().tokenize(source.read())).visit()
    else:
        print("Starting interactive Echo* interpreter.")
        shell(Lexer(), Parser())
