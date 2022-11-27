# MochaScript

- [MochaScript](#mochascript)
  - [Overview](#overview)
  - [Syntax example](#syntax-example)
  - [Documentation](#documentation)
  - [Problems](#problems)

## Overview
MochaScript is a simple, interpreted programming language that I made for fun and profit. So far, MochaScript supports strings, numbers, booleans, if-else expressions, arrays, comments, variables, functions, loops, and more. In MochaScript, everything is an expression (like Lisp). You can safely assume that MochaScript is three parts Python and one part Lisp.

I decided on the everything-is-an-expression rule because 1. it's cool, interesting, and unusual, and 2. it's easier (sometimes) to write an expression-based language then a statement-based language.

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

## Problems
MochaScript is not perfect and has a few issues, some of which are not going to be fixed any time soon.
- Error handling is trash
- Error messages are trash
- Few elements of the language are extensively tested
- The MochaScript parser is based off of a third-party library (`sly`) and gives unimportant yet annoying error messages
- I don't know if I will ever finish MochaScript. At least it works (mostly) and has the most vital features to a language...
