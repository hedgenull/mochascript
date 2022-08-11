# MochaScript

MochaScript is a simple, interpreted programming language made for fun and profit. So far, MochaScript supports strings, numbers, booleans, if-else expressions, arrays, constants, variables, and more. In MochaScript, everything is an expression (like Lisp).

I decided on the everything-is-an-expression rule because 1. it's cool, interesting, and unusual, and 2. it's harder in some ways but easier in others.
When I add them, everything from functions to loops will be expressions, meaning they have a return value. MochaScript will most likely be a functional programming language.

### Syntax example

```py
say "Hello world!";

my_var = 10;
my_second_var = (10 if my_var == 20 else 5);

# This is a comment!

say my_second_var; # 5

name = ask "What's your name? ";
say "Hello, {}!" % name;
```
