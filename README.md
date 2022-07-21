# ast-eval

ast-eval is a simple, interpreted programming language. The interpreter isn't a bytecode interpreter- it's an AST evaluator, hence the name. Eventually I'll change the name, but so far, ast-eval supports strings, numbers, and variables. In ast-eval, everything is an expression, which means that these are perfectly valid:

`x = y = z = 3 + 3` will assign 3 to x, y, and z.
`x = 1 + y = 2` will assign 2 to y, and 1 + y (so 3) to x.
