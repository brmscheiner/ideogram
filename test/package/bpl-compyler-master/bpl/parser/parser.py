"""
AUTHOR: Oren Shoham
DATE: Feb. 16, 2014

A Parser for the BPL programming language. Implemented for CS331 at Oberlin College.
"""

import sys
from bpl.scanner.scanner import Scanner
from bpl.scanner.token import TokenType, Token, is_type_token, is_rel_op, is_add_op, is_mul_op
from bpl.parser.parsetree import *


class ParserException(Exception):
    def __init__(self, line_number, message):
        message = 'Parser Error on line {}: {}'.format(line_number, message)
        Exception.__init__(self, message)

class Parser(object):

    def __init__(self, input_file):
        """Initialize a Scanner using 'input_file' and set its current token to the first token in 'input_file'."""
        self.scanner = Scanner(input_file)
        self.scanner.get_next_token()

    def parse(self):
        """Parse the Parser's input file."""
        return self.program()

    def program(self):
        """Return a complete parse tree."""
        return self.declaration_list()

    def expect(self, token, message):
        """Consume the current token, raising an error if it does not match the expected token."""
        current_token = self.scanner.next_token
        if current_token.kind != getattr(TokenType, token):
            raise ParserException(self.scanner.line_number, message)
        self.scanner.get_next_token()
        return current_token

    def declaration_list(self):
        """Return a linked list of declaration nodes."""
        d = self.declaration()
        head = d
        while self.scanner.next_token.kind != TokenType.T_EOF:
            d1 = self.declaration()
            d.next_node = d1
            d = d1
        return head

    def declaration(self, local=False):
        """Return a single variable, array, or function declaration node."""
        is_pointer = False
        line_number = self.scanner.line_number
        if not is_type_token(self.scanner.next_token):
            raise ParserException(line_number, 'Expected a type token to begin a declaration.')
        type_token = self.scanner.next_token
        self.scanner.get_next_token()

        if self.scanner.next_token.kind == TokenType.T_MULT:
            is_pointer = True
            self.scanner.get_next_token()
        
        id_token = self.expect('T_ID', 'Expected an identifier as part of the declaration.')

        # handle variable declarations
        if self.scanner.next_token.kind == TokenType.T_SEMICOLON:
           self.scanner.get_next_token() 
           return VarDecNode('VAR_DEC', line_number, id_token.value, type_token, is_pointer)

        # handle array declarations
        elif self.scanner.next_token.kind == TokenType.T_LBRACKET:
            if is_pointer:
                raise ParserException(line_number, 'Cannot declare a pointer to an array.')
            self.scanner.get_next_token()
            size = int(self.expect('T_NUM', 'Expected an integer size as part of the array declaration.').value)
            self.expect('T_RBRACKET', 'Expected a right bracket as part of the array declaration.')
            self.expect('T_SEMICOLON', 'Expected a semicolon to end the array declaration.')
            return ArrayDecNode('ARRAY_DEC', line_number, id_token.value, type_token, size, is_pointer)

        # handle function delcarations
        elif self.scanner.next_token.kind == TokenType.T_LPAREN:
            if is_pointer:
                raise ParserException(line_number, 'Cannot declare a pointer to a function.')
            if local:
                raise ParserException(line_number, 'Cannot declare a function inside a compound statement.')
            self.scanner.get_next_token()
            parameters = self.param_list()
            self.expect('T_RPAREN', 'Expected a right parenthesis to end the function parameter declarations.')
            body = self.compound_statement()
            return FunDecNode('FUN_DEC', line_number, id_token.value, type_token, parameters, body)

        else:
            raise ParserException(line_number, 'Unexpected token in declaration.')

    def statement(self):
        """Return a single statement node, which can be one of many types."""
        if self.scanner.next_token.kind == TokenType.T_LBRACE:
            return self.compound_statement()
        elif self.scanner.next_token.kind == TokenType.T_IF:
            return self.if_statement()
        elif self.scanner.next_token.kind == TokenType.T_WHILE:
            return self.while_statement()
        elif self.scanner.next_token.kind == TokenType.T_RETURN:
            return self.return_statement()
        elif self.scanner.next_token.kind == TokenType.T_WRITE:
            return self.write_statement()
        elif self.scanner.next_token.kind == TokenType.T_WRITELN:
            return self.writeln_statement()
        else:
            return self.expression_statement()

    def expression_statement(self):
        """Return an expression statement node that points to an expression node."""
        exp = None
        line_number = self.scanner.line_number
        if self.scanner.next_token.kind != TokenType.T_SEMICOLON:
            exp = self.expression()
        self.expect('T_SEMICOLON', 'Expected a semicolon to end the expression.')
        return ExpressionStatementNode('EXP_STATEMENT', line_number, exp)

    def statement_list(self):
        """Return a linked list of statement nodes within a compound statement."""
        line_number = self.scanner.line_number
        head = None
        if self.scanner.next_token.kind != TokenType.T_RBRACE:
            s = self.statement()
            head = s
            while self.scanner.next_token.kind != TokenType.T_RBRACE:
                if self.scanner.next_token.kind == TokenType.T_EOF:
                    raise ParserException(line_number, 'Expected a right curly brace to close the compound statement.')
                s1 = self.statement()
                s.next_node = s1
                s = s1
        return head

    def local_decs(self):
        """Return a linked list of local declaration nodes within a compound statement."""
        head = None
        if is_type_token(self.scanner.next_token):
            l = self.declaration(local=True)
            head = l
            while is_type_token(self.scanner.next_token):
                l1 = self.declaration(local=True)
                l.next_node = l1
                l = l1
        return head

    def param_list(self):
        """Return a linked list of function parameters, or None if the only parameter is the keyword 'void'."""
        head = None
        if self.scanner.next_token.kind == TokenType.T_VOID:
            self.scanner.get_next_token()
        else:
            p = self.param()
            head = p
            while self.scanner.next_token.kind == TokenType.T_COMMA:
                self.expect('T_COMMA', 'Expected a comma between each function parameter.')
                p1 = self.param()
                p.next_node = p1
                p = p1
        return head

    def param(self):
        """Return a single function parameter node, which may be a variable, pointer, or array declaration."""
        line_number = self.scanner.line_number
        if not is_type_token(self.scanner.next_token):
            raise ParserException(self.scanner.line_number, 'Expected a type keyword as part of the function parameter.')
        type_token = self.scanner.next_token
        self.scanner.get_next_token()
        is_pointer = False
        if self.scanner.next_token.kind == TokenType.T_MULT:
            is_pointer = True
            self.scanner.get_next_token()
        id_token = self.expect('T_ID', 'Expected an identifier as part of the function parameter.')
        if self.scanner.next_token.kind == TokenType.T_LBRACKET:
            if is_pointer:
                raise ParserException(line_number, 'Cannot pass a pointer to an array as a parameter.')
            self.scanner.get_next_token()
            self.expect('T_RBRACKET', 'Expected a right bracket as part of the array parameter.')
            return ArrayDecNode('ARRAY_DEC', line_number, id_token.value, type_token, -1, is_pointer)
        else:
            return VarDecNode('VAR_DEC', line_number, id_token.value, type_token, is_pointer)

    def compound_statement(self):
        """Return a single compound statement node with local declarations and statements."""
        line_number = self.scanner.line_number
        self.expect('T_LBRACE', 'Expected a left curly brace to begin the compound statement.')
        local_declarations = self.local_decs()
        statements = self.statement_list()
        self.expect('T_RBRACE', 'Expected a right curly brace to end the compound statement.')
        return CompoundStatementNode('CMPND_STATEMENT', line_number, local_declarations, statements)

    def if_statement(self):
        """Return an if statement node with a condition, statement, and optional else statement."""
        line_number = self.scanner.line_number
        self.expect('T_IF', 'Expected the keyword "if" to begin the if statement.')
        self.expect('T_LPAREN', 'Expected a left parenthesis as part of the if statement.')
        cond = self.expression()
        self.expect('T_RPAREN', 'Expected a right parenthesis as part of the if statement.')
        stmnt = self.statement()
        else_stmnt = None
        if self.scanner.next_token.kind == TokenType.T_ELSE:
            self.scanner.get_next_token()
            else_stmnt = self.statement()
        return IfStatementNode('IF_STATEMENT', line_number, cond, stmnt, else_stmnt)

    def while_statement(self):
        """Return a while statement node with a condition and a statement."""
        line_number = self.scanner.line_number
        self.expect('T_WHILE', 'Expected the keyword "while" to begin the while statement.')
        self.expect('T_LPAREN', 'Expected a left parenthesis as part of the while statement.')
        cond = self.expression()
        self.expect('T_RPAREN', 'Expected a right parenthesis as part of the while statement.')
        stmnt = self.statement()
        return WhileStatementNode('WHILE_STATEMENT', line_number, cond, stmnt)

    def return_statement(self):
        """Return a return statement node, either with or without an expression."""
        line_number = self.scanner.line_number
        self.expect('T_RETURN', 'Expected the keyword "return" to begin the return statement.')
        exp = None
        if self.scanner.next_token.kind != TokenType.T_SEMICOLON:
            exp = self.expression()
        self.expect('T_SEMICOLON', 'Expected a semicolon to end the return statement.')
        return ReturnStatementNode('RETURN_STATEMENT', line_number, exp)

    def write_statement(self):
        """Return a write statement node with an expression to be written."""
        line_number = self.scanner.line_number
        self.expect('T_WRITE', 'Expected the keyword "write" to begin the write statement.')
        self.expect('T_LPAREN', 'Expected a left parenthesis as part of the write statement.')
        exp = self.expression()
        self.expect('T_RPAREN', 'Expected a right parenthesis as part of the write statement.')
        self.expect('T_SEMICOLON', 'Expected a semicolon to end the write statement.')
        return WriteStatementNode('WRITE_STATEMENT', line_number, exp)

    def writeln_statement(self):
        """Return a writeln statement node."""
        line_number = self.scanner.line_number
        self.expect('T_WRITELN', 'Expected the keyword "writeln" to begin the writeln statement.')
        self.expect('T_LPAREN', 'Expected a left parenthesis as part of the writeln statement.')
        self.expect('T_RPAREN', 'Expected a right parenthesis as part of the writeln statement.')
        self.expect('T_SEMICOLON', 'Expected a semicolon to end the writeln statement.')
        return WritelnStatementNode('WRITELN_STATEMENT', line_number)

    def expression(self):
        """Return a single expression node."""
        line_number = self.scanner.line_number

        left = self.E()
        
        # handle assignment expressions
        if self.scanner.next_token.kind == TokenType.T_ASSIGN:
            # do some type checking stuff on left here to make sure it's a variable
            if not (left.kind is NodeType.VAR_EXP or left.kind is NodeType.ARRAY_EXP or
                    left.kind is NodeType.DEREF_EXP):
                raise ParserException(line_number, 'Left side of assignment expression must be a variable, array reference, or pointer dereference.')
            op_token = self.expect('T_ASSIGN', 'Expected an "=" as part of the assignment expression.')
            right = self.expression()
            return OpNode('ASSIGN_EXP', line_number, op_token, left, right)

        # handle comparison expressions
        elif is_rel_op(self.scanner.next_token):
            op_token = self.scanner.next_token
            self.scanner.get_next_token()
            right = self.E()
            return OpNode('COMP_EXP', line_number, op_token, left, right)

        # handle single E expressions
        else:
            return left

    def E(self):
        """Return an expression node representing an addition or subtraction operation."""
        line_number = self.scanner.line_number
        t = self.T()
        while is_add_op(self.scanner.next_token):
            op_token = self.scanner.next_token
            self.scanner.get_next_token()
            t1 = OpNode('MATH_EXP', line_number, op_token, None, None)
            t1.left = t
            t1.right = self.T()
            t = t1
        return t

    def T(self):
        """Return an expression node representing a multiplication, division, or modulo operation."""
        line_number = self.scanner.line_number
        f = self.F()
        while is_mul_op(self.scanner.next_token):
            op_token = self.scanner.next_token
            self.scanner.get_next_token()
            f1 = OpNode('MATH_EXP', line_number, op_token, None, None)
            f1.left = f
            f1.right = self.F()
            f = f1
        return f

    def F(self):
        """Return an expression node representing a negative, address, or dereference operation."""
        line_number = self.scanner.line_number
        if self.scanner.next_token.kind == TokenType.T_MINUS:
            self.scanner.get_next_token()
            f = self.F()
            return NegExpNode('NEG_EXP', line_number, f)
        
        elif self.scanner.next_token.kind == TokenType.T_AND:
            self.scanner.get_next_token()
            fac = self.factor()
            return AddressExpNode('ADDRESS_EXP', line_number, fac)

        elif self.scanner.next_token.kind == TokenType.T_MULT:
            self.scanner.get_next_token()
            fac = self.factor()
            return DerefExpNode('DEREF_EXP', line_number, fac)

        else:
            return self.factor()

    def factor(self):
        """Return a factor, which may be one of many types of expressions."""
        line_number = self.scanner.line_number

        # handle parenthesized expressions
        if self.scanner.next_token.kind == TokenType.T_LPAREN:
            self.scanner.get_next_token()
            exp = self.expression()
            self.expect('T_RPAREN', 'Expected a right parenthesis to close the expression.')
            return exp
        
        # handle number expressions
        elif self.scanner.next_token.kind == TokenType.T_NUM:
            number = self.expect('T_NUM', 'Expected a number as part of the expression.')
            return NumExpNode('NUM_EXP', line_number, number.value)

        # handle string expressions
        elif self.scanner.next_token.kind == TokenType.T_STRVAL:
            string = self.expect('T_STRVAL', 'Expected a string literal as part of the expression.')
            return StringExpNode('STR_EXP', line_number, string.value)

        # handle read expressions
        elif self.scanner.next_token.kind == TokenType.T_READ:
            self.scanner.get_next_token()
            self.expect('T_LPAREN', 'Expected a left parenthesis as part of the read expression.')
            self.expect('T_RPAREN', 'Expected a right parenthesis as part of the read expression.')
            return ReadExpNode('READ_EXP', line_number)

        # handle pointer dereference expressions
        elif self.scanner.next_token.kind == TokenType.T_MULT:
            self.scanner.get_next_token()
            id_token = self.expect('T_ID', 'Expected an identifier as part of the pointer dereference.')
            v = VarExpNode('VAR_EXP', line_number, id_token.value)
            return DerefExpNode('DEREF_EXP', line_number, v)

        else:
            id_token = self.expect('T_ID', 'Expected an identifier as part of the expression.')

            # handle array reference expressions
            if self.scanner.next_token.kind == TokenType.T_LBRACKET:
                self.scanner.get_next_token()
                exp = self.expression()
                self.expect('T_RBRACKET', 'Expected a right bracket to close the array reference.')
                return ArrayExpNode('ARRAY_EXP', line_number, id_token.value, exp)

            # handle function call expressions
            elif self.scanner.next_token.kind == TokenType.T_LPAREN:
                self.scanner.get_next_token()
                arguments = self.args()
                self.expect('T_RPAREN', 'Expected a right parenthesis to close the function call.')
                return FunCallExpNode('FUN_CALL_EXP', line_number, id_token.value, arguments)

            # handle variable expressions
            else:
                return VarExpNode('VAR_EXP', line_number, id_token.value)

    def args(self):
        """Return a linked list of function arguments, each of which is an expression."""
        head = None
        if self.scanner.next_token.kind != TokenType.T_RPAREN:
            a = self.expression()
            head = a
            while self.scanner.next_token.kind != TokenType.T_RPAREN:
                self.expect('T_COMMA', 'Expected a comma between each function argument.')
                a1 = self.expression()
                a.next_node = a1
                a = a1
        return head
