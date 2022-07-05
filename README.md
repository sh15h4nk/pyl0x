# Pyl0x
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/sh15h4nk/pyl0x/blob/main/LICENSE) [![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)

Python implementation of Lox language interpreter.\
This is tree walk interpreter is developed by following the [Crafting Interpreter](https://craftinginterpreters.com/) book.




## Installation
```sh
$ git clone https://github.com/sh15h4nk/pyl0x.git
$ pip install pyl0x/
```
Now you can use the interpreter with `pylox` command.

## Usage
For the repl, you can use the `pylox` command.
```sh
$ pylox             
> var a = 2;
> print a;
2
> print 5*2;
10
> print 1 == 1;
True
> Bye :)
```

For running a script, (the script must have .lox extension) and needs to be non empty

Empty source file
```sh
$ pylox empty_file.lox 
Your source file is empty :/
```

Sample source:
```lox
// * has higher precedence than +.
print 2 + 3 * 4; // expect: 14

// * has higher precedence than -.
print 20 - 3 * 4; // expect: 8

// / has higher precedence than +.
print 2 + 6 / 3; // expect: 4

// / has higher precedence than -.
print 2 - 6 / 3; // expect: 0

// < has higher precedence than ==.
print false == 2 < 1; // expect: true

// > has higher precedence than ==.
print false == 1 > 2; // expect: true

// <= has higher precedence than ==.
print false == 2 <= 1; // expect: true

// >= has higher precedence than ==.
print false == 1 >= 2; // expect: true

// 1 - 1 is not space-sensitive.
print 1 - 1; // expect: 0
print 1 -1;  // expect: 0
print 1- 1;  // expect: 0
print 1-1;   // expect: 0

// Using () for grouping.
print (2 * (6 - (2 + 2))); // expect: 4
```
```sh
$ pylox precedence.lox 
14
8
4
0
True
True
True
True
0
0
0
0
4
```

## Licence
This source code is licensed under MIT License.
