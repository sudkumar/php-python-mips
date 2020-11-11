# PHP to MIPS compiler written in Python

This project is purely for education purpose only. The project aims to provide a high level overview of compilers and their implementation.

## Introduction

At high level, a compiler is a program that takes a language code as its argument and return a desired language code. For example, given a peace of code in `C` language, we may want it to convert into `Javascript` code.

```c
#include<stdio.h>

int main {
  printf("Hello World");
  return 0;
}
```
The above `C` code can be converted to `Javascript` and we want following output.

```js
process.stdout.write("Hello World");
```

Once can write a program (compiler) to automate this conversion. Here `C` and `Javascript` are marely for demonstration purpose only and can be swapped with any language of choice. We can also use `Hindi` to `English` or `C` to `Machine Code` as input -> output languages for our compiler.

### Languages

As we already discussed, compilers needs languages. Each language has its own `Way of Saying or Doing` things. For example, to say `Hello World`, we use different ways (syntax) for different languages:

```
C       => printf("Hello World");
PHP     => echo "Hello World";
Java    => System.output.println("Hello World");
English => Hello World
Hindi   => नमस्ते दुनिया
```
But they all result (output) in the same thing.

We can not compile a language if we don't know the language itself! Our general speaking languages (e.g. Hindi, English, Korean etc.) are very hard to fully learn because people pronounce single language in differently which makes is even harder to write a compiler for it. But on the other side, computer languages are properly defined and writing it differently will cause errors. 

You may also have noticed that languages has a way to construct a particular statement. `Doing am I what ?` doesn't make any sense because it is not following something. That missing thing is `Grammar`. Along with grammer, misspelling words also causes issues. In computer programs, these words are called `Tokens`.

#### Grammar

A grammar defines the constructing rules for a language. Without it, the language simply can not exists without ambiguity. Writing `c int;` causes error in a `C` program because the grammar say to write `int c;`.


#### Token

Tokens are the basic building blocks of any languages. 

```c
int n = 10;
printf("%d", n);
```

Here `int`, `n`, `=`, `10`, `;`, `printf`, `(`, `"`, `%`, `d`, `"`, `,`, `n`,`)`,`;` are all tokens.

Some tokens are special. Here `int` is a language **keyword** and has special meaning for `C` language whereas `n` is not. We can put any values for `n` token like replace `n` with `x` and the meaning of program won't change.

To learn a language, we need to learn its grammar and tokens.


Now that we have a good understanding of languages and it's constructors, we are ready to write our compiler.

## Tokenization

> TODO:



