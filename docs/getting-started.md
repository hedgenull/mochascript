# Echo*: Getting Started

Echo* is a simple, dynamically typed, very basic language to learn, and here I'll explain the basics of the language.


## #1: Basic Math + Numbers

### Disclaimer:
In Echo*, numbers are represented as floats. There is no native integer type, but it's not a big deal. In the interactive REPL, whole numbers' `repr()` method chops off the '.0' at the end for a nicer string representation.

### Basic Math:
Echo*'s mathematical expressions look just like any others. Here are the math operators:

- `+`: Addition
- `-`: Subtraction
- `*`: Multiplication
- `/`: Division
- `%`: Modulus

Currently, I don't have an exponentiation operator, but when I add it it will most likely be `**`, similar to Python and other languages. Here are some examples of Echo*'s math:

`>>> 1 + 1`: 2

`>>> 4 - 3`: 1

`>>> 9 * 10`: 90

`>>> 5 / 2`: 2.5

`>>> 6 % 3`: 0

More complex operations are allowed, such as `2 + (3 * (10 - 9))`, which evaluates to 5. Echo* follows the order of operations, so to execute the addition first in `2 + 3 * 5`, you must put parentheses around the `2 + 3`.


## #2: Strings

In Echo*, strings are very simple objects. You don't have to worry about encodings or memory allocation- they're just as simple as numbers. A string is created like `"this"`. Double quotes and single quotes are both allowed. However, it's worth noting that escaped quotes are not supported in Echo*, so if you want to use an apostrophe inside your string, you must instantiate the string with double quotes. This is like many other programming languages.

### String formatting
Currently, Echo* supports very basic string formatting. This is done using the modulo operator (`%`) and brackets (`{}`) inside a string. Modding a string _s_ with a value _v_ replaces any occurrences of `{}` in _s_ with the `repr()` of _v_. Here's an example:

```py
>>> "Hello, {}!" % "world"
"Hello, world!"

>>> "2 plus 3 is: {}" % (2 + 3)
"2 plus 3 is: 5"
```


## #3: Variables

Echo*'s variables are no different than Python's, and they are defined in just the same way. No `var` keywords, no type hinting, no declaration _then_ definition- variables in Echo* can be used as simply as this:

```py
>>> x = 3
3
>>> x
3
```

An interesting side effect of everything in Echo* being an expression is that variable assignments _have a return value_. This is possibly the biggest difference from Python. So it's possible to define a variable in an equation:

```py
>>>  4 - (x = 2 + 3)
-1
>>> x
5
```

Assignments return the value of the variable just assigned. Multiple assignments are possible at once, then, like `x = y = z = 10`, which assigns 10 to `x`, `y`, and `z`. More complex assignments are permitted- `x = 1 + y = 3` assigns `y` to 3 and `x` to `1 + y`.