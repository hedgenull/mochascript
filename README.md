# MochaScript

- [MochaScript](#mochascript)
  - [Overview](#overview)
  - [Syntax example](#syntax-example)
  - [Documentation](#documentation)

## Overview
MochaScript is a simple, interpreted programming language made for fun and profit. So far, MochaScript supports strings, numbers, booleans, if-else expressions, arrays, comments, variables, functions, loops, and more. In MochaScript, everything is an expression (like Lisp). You can safely assume that MochaScript is three parts Python and one part Lisp.

I decided on the everything-is-an-expression rule because 1. it's cool, interesting, and unusual, and 2. it's harder in some ways but easier in others.
When I add them, everything from functions to loops will be expressions, meaning they have a return value. MochaScript will most likely be a functional programming language.

## Syntax example
```py
# Hello world!
say "Hello world!";

# Control flow
my_var = 10;

my_2nd_var = if my_var == 5 (
  1.2
) else (
  5
);

say my_2nd_var; # 5

# I/O
name = ask "What's your name? ";
say "Hello, {}!" % name;
```

## Documentation
For documentation, read the [wiki](../../wiki/).
