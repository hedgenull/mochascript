from lex import Lexer
from parse import Parser

if __name__ == "__main__":
    lexer = Lexer()
    parser = Parser()

    while True:
        source = input(">>> ").strip()
        if source == "exit":
            break
        elif source == "":
            continue
        tokens = lexer.tokenize(source)
        ast = parser.parse(tokens)
        result = ast.visit()

        print(result)
