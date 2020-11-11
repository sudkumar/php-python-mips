# A Simple Cross compiler for PHP, build with Python

## Dependencies

- python-ply v2.5: a token generator
- pyinstaller: for creating executable binary file from python
- python-tabulate: for tabular view of results

## File Structure
- src
    - ply/*: necessary plugin for python-ply
    - lexer.py: code for token generation
- test: Contains some test cases as input for lexer
- makefile: To wrap all things and running

## Running the test cases

```sh
make clean
make
```

This will create our executable binary lexer file in a bin folder.

To run test cases.

```sh
./bin/lexer ./test/test1.php
```
