# Echo*

Echo* (pronounced "Echo-star") is a simple, interpreted programming language. The interpreter isn't a bytecode interpreter- it's an AST evaluator. So far, Echo* supports strings, numbers, booleans, if-else expressions, and variables. In Echo*, everything is an expression (like Lisp), which means that these are perfectly valid:

`x = y = z = 3 + 3`: will assign 6 to x, y, and z.

`x = 1 + y = 2`: will assign 2 to y, and 1 + y (so 3) to x.

`print x`: Prints and returns x.

`y = print x`: Prints x and assigns it to y.

I decided on the everything-is-an-expression rule because 1. it's cool, interesting, and unusual, and 2. it's harder in some ways but easier in others.
When I add them, everything from functions to loops will be expressions, meaning they have a return value. Echo* will most likely be a functional programming language.
