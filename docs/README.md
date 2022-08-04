# Echo* Documentation

Echo* is a simple, dynamically typed, very basic language that doesn't really serve any special purpose. I made it for fun and profit. However, despite its lack of new features, you should still learn it.


## 1: Basic Math + Numbers

### Disclaimer:
In Echo*, numbers are represented as floats. There is no native integer type, but it's not a big deal. In the interactive REPL, whole numbers' `repr()` method chops off the '.0' at the end for a nicer string representation.

### Basic Math:
Echo*'s mathematical expressions look just like any others. Here are the math operators:

- `+`: Addition
- `-`: Subtraction
- `*`: Multiplication
- `/`: Division
- `%`: Modulus

Currently, Echo* doesn't have an exponentiation operator, but if I add it it will most likely be `**`, similar to Python and other languages. Here are some examples of Echo*'s math:

```py
>>> 1 + 1
2
>>> 4 - 3
1
>>> 9 * 10
90
>>> 5 / 2
2.5
>>> 6 % 3
0
```

More complex operations are allowed, such as `2 + (3 * (10 - 9))`, which evaluates to 5. Echo* follows the order of operations, so to execute the addition first in `2 + 3 * 5`, you must put parentheses around the `2 + 3`.


## 2: Strings

In Echo*, strings are very simple objects. You don't have to worry about encodings or memory allocation- they're just as simple as numbers. A string is created like `"this"`. Double quotes and single quotes are both allowed. However, it's worth noting that escaped quotes are not supported in Echo*, so if you want to use an apostrophe inside your string, you must instantiate the string with double quotes. This is like many other programming languages.

### String formatting
Currently, Echo* supports very basic string formatting. This is done using the modulo operator (`%`) and curly brackets (`{}`) inside a string. Modding a string _s_ with a value _v_ replaces any occurrences of `{}` in _s_ with the `repr()` of _v_. Here's an example:

```py
>>> "Hello, {}!" % "world"
"Hello, world!"

>>> "2 plus 3 is: {}" % (2 + 3)
"2 plus 3 is: 5"
```

### String concatenation
Echo* supports string concatenation- strings, like in JavaScript, can be added to any other value. However, this must be done with the string on the left, as that will call the string's `add` method.

```py
>>> "Hello " + "world!"
"Hello, world!"
>>> "My favorite number is " + 4
"My favorite number is 4"
```

### String subtraction
In most programming languages, the minus operator (`-`) has no use on strings. However, in Echo*, two strings can be subtracted, which removes all occurrences of the second string from the first.

```py
>>> "Hello there!" - " there"
"Hello!"
```


### String multiplication
Like in Python, strings can be multiplied with numbers. Here's an example:

```py
>>> "Hello" * 3
"HelloHelloHello"
```


## 3: Variables + constants

Echo*'s variables are no different than Python's, and they are defined in just the same way. No `var` keywords, no type-casting, no declaration _then_ definition- variables in Echo* can be used as simply as this:

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

Echo* also supports constants. These are variables that, once defined, can't be changed. `true`, `false`, and `null` are some built-in constants. Constants can be defined like this:

```py
>>> CONST_my_constant = 10
10
```

This defines a constant named `my_constant`. It's important to recognize that the `CONST_` part of the name is chopped off.

```py
>>> CONST_my_constant = "a constant"
"a constant"
>>> my_constant
"a constant"
>>> my_constant = 4 # Trying to reassign a constant fails
"a constant"
>>> my_constant
"a constant"
```

## 4: The `say` keyword

The `say` keyword is the print function of Echo*: it prints the value given and then returns it. `say` can accept any data type, as it calls the value's `repr()` method. In an interactive shell, the `say` keyword isn't so useful, since return values are already printed. This means that using `say` in a shell will print your value twice.

```py
>>> say 4
4
4
```

## 5: Arrays

Echo*'s arrays are similar to lists in Python or arrays in Ruby. They are defined using the same `[..., ..., ...]` syntax and can contain any number of elements, and any types. Individual elements of arrays are 0-indexed and accessed with the modulo operator. For example:

```py
>>> my_array = [1, 2, 3, 4, 5]
[1, 2, 3, 4, 5]
>>> my_array % 0
1
>>> my_array % 3
4
>>> my_array % -1
5
```

### Appending values
Values can be appended to arrays with the addition operator.

```py
>>> [1, 2, 3] + 4
[1, 2, 3, 4]
```

### Multiplying arrays
Arrays can be multiplied with numbers like so:

```py
>>> [1, 2, 3] * 3
[1, 2, 3, 1, 2, 3, 1, 2, 3]
```
### Reversing arrays
Negating arrays using the unary minus operator (`-`) reverses their elements.

```py
>>> -["a", "b", 3]
[3, "b", "a"]
```

## 6: Booleans and if-expressions

Booleans- `true` and `false`- are a simple data type in Echo*. They are _not_ related to numbers, so math can't be used directly on booleans. The main use of booleans is in if-expressions, Echo*'s only control flow so far. If-expressions have the structure `([true_expr] if [condition] else [false_expr])`. For example:

```py
>>> a = 2
10
>>> b = (10 if a == 1 else 20)
20
```

This assigns `b` to 20, because the condition `a == 1` evaluates to false. Here's a quick list of logical/comparison operators.

`==`: Equality operator.

`!=`: Negated equality operator (not-equal).

`&&`: And operator.

`||`: Or operator.

`>`: Greater-than operator.

`<`: Less-than operator.

`>=`: Greater-than or equal to operator.

`<=`: Less-than or equal to operator.

There is no `elif` or `else if` keyword/construct in Echo*, but it can be simulated with multiple if-expressions.

```py
>>> # If-else if-else demo in Echo*
>>> a = 5
>>> b = (2 if a < 5 else (3 if a == 5 else 4))
```

## 7: A quick note on `null`

The `null` value in Echo* is equivalent to `None` in Python, `void` in C/C++, and `nil` in Ruby. It's a falsy value and doesn't have much use, but it exists nonetheless.

## 8: The `exit` keyword

The `exit` keyword simply aborts the program with the given message- it prints and then exits.

```py
>>> exit "Bye bye"
Bye bye
```
