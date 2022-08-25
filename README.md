# MochaScript

- [MochaScript](#mochascript)
  - [Overview](#overview)
  - [Syntax example](#syntax-example)
  - [Documentation](#documentation)

## Overview
MochaScript is a simple, interpreted programming language made for fun and profit. So far, MochaScript supports strings, numbers, booleans, if-else expressions, arrays, constants, variables, functions, loops, and more. In MochaScript, everything is an expression (like Lisp). Really, assume MochaScript is a much more readable Lisp. Which means less parentheses.

I decided on the everything-is-an-expression rule because 1. it's cool, interesting, and unusual, and 2. it's harder in some ways but easier in others.
When I add them, everything from functions to loops will be expressions, meaning they have a return value. MochaScript will most likely be a functional programming language.

## Syntax example
```py
# Hello world!
say "Hello world!";

# Control flow
my_var = 10;

if my_var == 5 (
    my_second_var = 1.2;
) else (
    my_second_var = 5;
);

say my_second_var; # 5

# I/O
name = ask "What's your name? ";
say "Hello, {}!" % name;
```

## Documentation
For documentation, read the [wiki](../../wiki/).
