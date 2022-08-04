# Echo*

Echo* (pronounced "Echo-star") is a simple, interpreted programming language made for fun and profit. So far, Echo* supports strings, numbers, booleans, if-else expressions, arrays, constants, variables, and more. In Echo*, everything is an expression (like Lisp).

I decided on the everything-is-an-expression rule because 1. it's cool, interesting, and unusual, and 2. it's harder in some ways but easier in others.
When I add them, everything from functions to loops will be expressions, meaning they have a return value. Echo* will most likely be a functional programming language.

## Syntax example:

```py
say "Hello world!"

my_var = 10

my_second_var = (10 if my_var == 20 else 5)

say my_second_var
```

## Current problems/issues

- Functions don't work.
