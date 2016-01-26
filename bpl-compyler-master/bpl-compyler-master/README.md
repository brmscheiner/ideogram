bpl
===

A compiler for Bob's Programming Language, a simple, C-like language. Implemented for the Spring 2014 CS331 course at Oberlin College.

Currently, this compiler generates GAS instructions, so it is only capable of running on Linux machines that are capable of compiling GAS instructions.

Written in Python 2.7.6. 

### Structure

The compiler consists of 4 modules: 

1. a lexical scanner that tokenizes text files
2. a recursive descent parser that constructs abstract syntax trees from token streams
3. a type checker that traverses abstract syntax trees to catch type errors
4. a code generator that converts type-correct ASTs to GNU AS instructions.

The code is organized as follows:

    .                           # top-level directory.  Run tests from here!
    ├── README.md
    ├── bplc                    # bpl compilation script. Use this to compile .bpl files!
    ├── setup.py                # installation script
    └── bpl                     # bpl python package
        ├── __init__.py
        |
        ├── compiler.py         # compiler module, combines scanner, parser, type checker, and code generator
        |
        ├── scanner             # scanner package
        │   ├── __init__.py
        │   ├── scanner.py
        │   ├── token.py
        |
        |── parser              # parser package
        │   ├── __init__.py
        |   |── parser.py
        |   |── parsetree.py
        |
        |── type_checker        # type checker package
        │   ├── __init__.py
        |   |── type_checker.py
        |
        |── code_generator      # code generator package
        │   ├── __init__.py
        |   |── code_generator.py
        |
        └── test                # test package
            ├── __init__.py
            ├── example.bpl
            ├── scanner_test.py
            ├── parser_test.py
            ├── type_checker_test.py
            └── code_generator_test.py

(credit to [@dan-f](https://github.com/dan-f/) for this diagram and the structure of this README)

### Installation

To install the bpl package and bplc compiler script, run the setup.py script from the top-level directory as follows:

```
$ python setup.py install
```

### Running the Compiler

To run the compiler, run the `bplc` script as follows:

```
$ bplc <filename>
```

If you can't install bpl or simply don't want to, you can still run the `bplc` script from the top-level directory: 

```
$ ./bplc <filename>
```

This will generate a binary output file named a.out. If you want to specify an output file name, you can use the "-o" flag as follows:

```
$ bplc <filename> -o <output_filename>
```

If you want to stop the compilation process at assembly generation, you can use the "-s" flag:

```
$ bplc <filename> -s
```

This will generate a GAS file named \<filename\>.s.

### Tests

To test a module `foo`, run the following command from the top-level directory:

```
$ python -m bpl.test.foo_test <filename>
```
