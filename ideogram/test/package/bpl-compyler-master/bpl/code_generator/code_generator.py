"""
AUTHOR: Oren Shoham
DATE: 4/9/2014
"""

from bpl.parser.parsetree import *
from bpl.scanner.token import TokenType
from itertools import count

# Register names
SP = 'rsp'
FP = 'rbx'
ACC_64 = 'rax'
ACC_32 = 'eax'
ARG1_64 = 'rdi'
ARG1_32 = 'edi'
ARG2_64 = 'rsi'
ARG2_32 = 'esi'
ARG3_64 = 'rdx'
ARG3_32 = 'edx'
ARG4_64 = 'rcx'
ARG4_32 = 'ecx'
ARG5_64 = 'r8'
ARG5_32 = 'r8d'
ARG6_64 = 'r9'
ARG6_32 = 'r9d'
CALLEE_SAVED_1_64 = 'rbx'
CALLEE_SAVED_1_32 = 'ebx'
CALLEE_SAVED_2_64 = 'rbp'
CALLEE_SAVED_2_32 = 'ebp'
CALLEE_SAVED_3_64 = 'r10'
CALLEE_SAVED_3_32 = 'r10d'
CALLEE_SAVED_4_64 = 'r13'
CALLEE_SAVED_4_32 = 'r13d'
CALLEE_SAVED_5_64 = 'r14'
CALLEE_SAVED_5_32 = 'r14d'
CALLEE_SAVED_6_64 = 'r15'
CALLEE_SAVED_6_32 = 'r15d'

# infinite label generator
data_label = count()
next_label = lambda : '.L{}'.format(next(data_label))
string_label = count()

def generate_code(type_checked_parse_tree, output_file):
    """Top-level code generation function."""
    compute_offsets(type_checked_parse_tree)

    # build a dictionary whose keys are strings and whose values are header labels for those strings
    string_table = {}
    declaration = type_checked_parse_tree
    while declaration is not None:
        if declaration.kind == NodeType.FUN_DEC:
            string_table.update(build_string_table(declaration.body))
        declaration = declaration.next_node

    gen_header(type_checked_parse_tree, string_table, output_file)

    declaration = type_checked_parse_tree
    while declaration is not None:
        if declaration.kind == NodeType.FUN_DEC:
            gen_code_function(declaration, string_table, output_file)
        declaration = declaration.next_node

def build_string_table(node):
    if node.kind == NodeType.STR_EXP:
        return {node.string: '.S{}'.format(next(string_label))}

    elif node.kind in (NodeType.EXP_STATEMENT, NodeType.WRITE_STATEMENT):
        return build_string_table(node.expression)

    elif node.kind in (NodeType.ASSIGN_EXP, NodeType.COMP_EXP, NodeType.MATH_EXP):
        string_table = {}
        string_table.update(build_string_table(node.left))
        string_table.update(build_string_table(node.right))
        return string_table

    elif node.kind == NodeType.CMPND_STATEMENT:
        string_table = {}
        statement = node.statements
        while statement is not None:
            string_table.update(build_string_table(statement))
            statement = statement.next_node
        return string_table

    elif node.kind == NodeType.RETURN_STATEMENT:
        if node.expression is not None:
            return build_string_table(node.expression)
        return {}

    elif node.kind == NodeType.IF_STATEMENT:
        string_table = {}
        string_table.update(build_string_table(node.statement))
        if node.else_statement is not None:
            string_table.update(build_string_table(node.else_statement))
        return string_table
    
    elif node.kind == NodeType.WHILE_STATEMENT:
        return build_string_table(node.statement)

    elif node.kind == NodeType.FUN_CALL_EXP:
        string_table = {}
        arg = node.arguments
        while arg is not None:
            string_table.update(build_string_table(arg))
            arg = arg.next_node
        return string_table
    
    else:
        return {}

def compute_offsets(parse_tree):
    """Walks through the top-level declarations in parse_tree, computing stack pointer offsets for function parameters and local variables."""
    declaration = parse_tree 
    while declaration is not None:
        if declaration.kind == NodeType.FUN_DEC:
            parameter_offset = 8
            param = declaration.params
            while param is not None:
                parameter_offset += 8
                param.offset = parameter_offset
                param = param.next_node
            declaration.local_var_offset = -1 * compute_offsets_statement(declaration.body, 0)
        declaration = declaration.next_node

def compute_offsets_statement(statement, offset):
    """Computes stack pointer offsets for local variable declarations and updates parse tree statement node fields appropriately."""
    if statement.kind == NodeType.CMPND_STATEMENT:
        dec = statement.local_declarations
        while dec is not None:
            if dec.kind == NodeType.ARRAY_DEC:
                offset -= 8 * dec.size
            else: # dec.kind == NodeType.VAR_DEC
                offset -= 8
            dec.offset = offset
            dec = dec.next_node

        total = offset
        stmnt = statement.statements
        while stmnt is not None:
            total += compute_offsets_statement(stmnt, offset)
            stmnt = stmnt.next_node
        return total
    
    elif statement.kind == NodeType.IF_STATEMENT:
        total = offset
        total += compute_offsets_statement(statement.statement, offset)
        if statement.else_statement is not None:
            total += compute_offsets_statement(statement.else_statement, offset)
        return total

    elif statement.kind == NodeType.WHILE_STATEMENT:
        total = offset
        total += compute_offsets_statement(statement.statement, offset)
        return total
    
    else: # return a total local variable offset of 0
        return 0

def gen_reg_reg(opcode, reg1, reg2, comment, output_file):
    output_file.write('\t{} %{}, %{} #{}\n'.format(opcode, reg1, reg2, comment))

def gen_immediate_reg(opcode, immediate, reg, comment, output_file):
    output_file.write('\t{} ${}, %{} #{}\n'.format(opcode, immediate, reg, comment))

def gen_indirect_reg(opcode, offset, reg1, reg2, comment, output_file):
    output_file.write('\t{} {}(%{}), %{} #{}\n'.format(opcode, offset, reg1, reg2, comment))

def gen_reg_indirect(opcode, reg1, offset, reg2, comment, output_file):
    output_file.write('\t{} %{}, {}(%{}) #{}\n'.format(opcode, reg1, offset, reg2, comment))

def gen_immediate_indirect(opcode, immediate, offset, reg, comment, output_file):
    output_file.write('\t{} ${}, {}(%{}) #{}\n'.format(opcode, immediate, offset, reg, comment))

def gen_no_operands(opcode, comment, output_file):
    output_file.write('\t{} #{}\n'.format(opcode, comment))

def gen_direct(opcode, operand, comment, output_file):
    output_file.write('\t{} {} #{}\n'.format(opcode, operand, comment))

def gen_reg(opcode, reg, comment, output_file):
    output_file.write('\t{} %{} #{}\n'.format(opcode, reg, comment))

def gen_header(parse_tree, string_table, output_file):
    # allocate global variables and arrays
    declaration = parse_tree
    while declaration is not None:
        # allocate space for a single variable
        if declaration.kind == NodeType.VAR_DEC:
            output_file.write('.comm {}, {}, {}\n'.format(declaration.name, 8, 32))
        # allocate space for an array
        elif declaration.kind == NodeType.ARRAY_DEC:
            output_file.write('.comm {}, {}, {}\n'.format(declaration.name, 8 * declaration.size, 32))
        declaration = declaration.next_node

    output_file.write('.section .rodata\n')
    output_file.write('.WriteIntString: .string "%d "\n')
    output_file.write('.WritelnString: .string "\\n"\n')
    output_file.write('.WriteStringString: .string "%s "\n')
    output_file.write('.ArrayOverflowString: .string "You fell off the end of an array.\\n"\n')
    output_file.write('.ReadIntString: .string "%d"\n')

    # store all strings used in the program as read-only data
    for string in string_table:
        output_file.write('{}: .string "{}"\n'.format(string_table[string], string))

    output_file.write('.text\n')
    output_file.write('.globl main\n')

def gen_code_function(function, string_table, output_file):
    output_file.write(function.name + ':\n')
    gen_reg_reg('movq', SP, FP, 'set up the frame pointer', output_file)
    gen_immediate_reg('sub', function.local_var_offset, SP, 'allocate local variables', output_file)
    # generate function body code
    gen_code_statement(function.body, function.local_var_offset, string_table, output_file)
    gen_immediate_reg('add', function.local_var_offset, SP, 'deallocate local variables', output_file)
    gen_no_operands('ret', 'return from function "{}"'.format(function.name), output_file)

def gen_code_statement(statement, local_var_offset, string_table, output_file):
    # generate code for compound statements
    if statement.kind == NodeType.CMPND_STATEMENT:
        stmnt = statement.statements
        while stmnt is not None:
            gen_code_statement(stmnt, local_var_offset, string_table, output_file)
            stmnt = stmnt.next_node
        
    # generate code for write statements
    elif statement.kind == NodeType.WRITE_STATEMENT:
        gen_code_expression(statement.expression, string_table, output_file)
        if statement.expression.type_string == 'int':
            gen_reg_reg('movl', ACC_32, ARG2_32, 'integer value to print = arg2', output_file)
            gen_immediate_reg('movq', '.WriteIntString', ARG1_64, 'printf integer formatting string = arg1', output_file)
        elif statement.expression.type_string == 'string':
            gen_reg_reg('movq', ACC_64, ARG2_64, 'string value to print = arg2', output_file)
            gen_immediate_reg('movq', '.WriteStringString', ARG1_64, 'printf string formatting string = arg1', output_file)
        gen_immediate_reg('movl', 0, ACC_32, 'clear the return value', output_file)
        gen_direct('call', 'printf', 'call the C-lib printf function', output_file)

    # generate code for writeln statements
    elif statement.kind == NodeType.WRITELN_STATEMENT:
        gen_immediate_reg('movq', '.WritelnString', ARG1_64, 'printf newline string = arg1', output_file)
        gen_immediate_reg('movl', 0, ACC_32, 'clear the return value', output_file)
        gen_direct('call', 'printf', 'call the C-lib printf function', output_file)

    # generate code for if statements
    elif statement.kind == NodeType.IF_STATEMENT:
        # create a label for the code that should be executed regardless of the condition's value
        continue_label = next_label()
        gen_code_expression(statement.condition, string_table, output_file)
        gen_immediate_reg('cmpl', 0, ACC_32, 'check whether the if condition evaluates to true or false', output_file)
        if statement.else_statement is not None:
            else_label = next_label()
            # generate jump to else if false code
            gen_direct('je', else_label, 'jump to else statement code if condition evaluates to false', output_file)
            gen_code_statement(statement.statement, local_var_offset, string_table, output_file)
            gen_direct('jmp', continue_label, 'jump to the end of the if statement code', output_file)
            output_file.write('{}:\n'.format(else_label))
            gen_code_statement(statement.else_statement, local_var_offset, string_table, output_file)
        else:
            # generate jump if true code
            gen_direct('je', continue_label, 'jump over if statement code if condition evaluates to false', output_file)
            gen_code_statement(statement.statement, local_var_offset, string_table, output_file)
        output_file.write('{}:\n'.format(continue_label))

    # generate code for return statements
    elif statement.kind == NodeType.RETURN_STATEMENT:
        # move the return value into the accumulator
        if statement.expression is not None:
            gen_code_expression(statement.expression, string_table, output_file)
        gen_immediate_reg('add', local_var_offset, SP, 'deallocate local variables', output_file)
        gen_no_operands('ret', 'return from the current function', output_file)

    # generate code for expression statements
    elif statement.kind == NodeType.EXP_STATEMENT:
        gen_code_expression(statement.expression, string_table, output_file)

    elif statement.kind == NodeType.WHILE_STATEMENT:
        loop_label = next_label()
        continue_label = next_label()
        output_file.write('{}:\n'.format(loop_label))
        gen_code_expression(statement.condition, string_table, output_file)
        gen_immediate_reg('cmpl', 0, ACC_32, 'check whether the while condition evaluates to true or false', output_file)
        gen_direct('je', continue_label, 'jump to the end of the while statement code if the condition evaluates to false', output_file)
        gen_code_statement(statement.statement, local_var_offset, string_table, output_file)
        gen_direct('jmp', loop_label, 'jump back to the beginning of the while loop', output_file)
        output_file.write('{}:\n'.format(continue_label))

def gen_code_expression(expression, string_table, output_file):
    if expression.kind == NodeType.NUM_EXP:
        gen_immediate_reg('movl', expression.number, ACC_32, 'put an integer value into the accumulator', output_file)

    elif expression.kind == NodeType.STR_EXP: 
        gen_immediate_reg('movq', string_table[expression.string], ACC_64, 'put the address of the string "{}" into the accumulator'.format(expression.string), output_file)

    # generate code for arithmetic expressions
    elif expression.kind == NodeType.MATH_EXP:
        gen_code_expression(expression.left, string_table, output_file)
        gen_reg('push', ACC_64, 'push the value of the left side of arithmetic expression onto the stack', output_file)
        gen_code_expression(expression.right, string_table, output_file)

        # addition
        if expression.token.kind == TokenType.T_PLUS:
            gen_indirect_reg('addl', 0, SP, ACC_32, 'add the left side of the arithmetic expression to the right side', output_file)

        # subtraction
        elif expression.token.kind == TokenType.T_MINUS:
            gen_reg_indirect('sub', ACC_32, 0, SP, 'subtract the right side of the arithmetic expression from the left side', output_file)
            gen_indirect_reg('movl', 0, SP, ACC_32, 'put the result of the subtraction into the accumulator', output_file)

        # multiplication
        elif expression.token.kind == TokenType.T_MULT:
            gen_indirect_reg('imul', 0, SP, ACC_32, 'multiply the left side of the arithmetic expression by the right side', output_file)

        # division
        elif expression.token.kind in (TokenType.T_DIV, TokenType.T_MOD):
            gen_reg('push', CALLEE_SAVED_2_64, 'save the value in the %ebp register on the stack', output_file)
            gen_reg_reg('movl', ACC_32, CALLEE_SAVED_2_32, 'put the divisor into the %ebp register', output_file)
            gen_indirect_reg('movl', 8, SP, ACC_32, 'put the dividend into the accumulator', output_file)
            gen_no_operands('cltq', 'sign-extend dividend to rax', output_file)
            gen_no_operands('cqto', 'sign_extend dividend to rdx', output_file)
            gen_reg('idivl', CALLEE_SAVED_2_32, 'perform the division operation', output_file)

            if expression.token.kind == TokenType.T_MOD:
                # place the remainder into the accumulator instead of the quotient
                gen_reg_reg('movl', ARG3_32, ACC_32, 'put the remainder into the accumulator', output_file)

            gen_reg('pop', CALLEE_SAVED_2_64, 'restore %ebp\'s original value', output_file)

        gen_immediate_reg('addq', 8, SP, 'pop the left side of the arithmetic expression off of the stack', output_file)

    # generate code for comparison expressions
    elif expression.kind == NodeType.COMP_EXP:
        gen_code_expression(expression.left, string_table, output_file)
        gen_reg('push', ACC_64, 'push the value of the left side of the comparison expression onto the stack', output_file)
        gen_code_expression(expression.right, string_table, output_file)
        gen_indirect_reg('cmpl', 0, SP, ACC_32, 'compare the two sides of the comparison expression', output_file)

        false_label = next_label()
        true_label = next_label()

        # less than
        if expression.token.kind == TokenType.T_LESS:
            gen_direct('jle', false_label, 'jump to false label if right side of expression is less than or equal to left side'.format(false_label), output_file)

        # less than or equal
        elif expression.token.kind == TokenType.T_LEQ:
            gen_direct('jl', false_label, 'jump to false label if right side of expression is less than left side'.format(false_label), output_file)

        # equal
        elif expression.token.kind == TokenType.T_EQ:
            gen_direct('jne', false_label, 'jump to false label if right side of expression is not equal to left side'.format(false_label), output_file)

        # not equal
        elif expression.token.kind == TokenType.T_NEQ:
            gen_direct('je', false_label, 'jump to false label if right side of expression is equal to left side'.format(false_label), output_file)

        # greater than or equal
        elif expression.token.kind == TokenType.T_GEQ:
            gen_direct('jg', false_label, 'jump to false label if right side of expression is greater than left side'.format(false_label), output_file)

        # greater than
        elif expression.token.kind == TokenType.T_GREATER:
            gen_direct('jge', false_label, 'jump to false label if right side of expression is greater than or equal to left side'.format(false_label), output_file)

        gen_immediate_reg('movl', 1, ACC_32, 'put a non-zero value into the accumulator to indicate that the comparison was true', output_file)
        gen_direct('jmp', true_label, 'skip over code at false label', output_file)
        output_file.write('{}:\n'.format(false_label))
        gen_immediate_reg('movl', 0, ACC_32, 'put zero into the accumulator to indicate that the comparison was false', output_file)
        output_file.write('{}:\n'.format(true_label))
        gen_immediate_reg('addq', 8, SP, 'pop the left side of the comparison expression off of the stack', output_file)

    # generate code for function calls
    elif expression.kind == NodeType.FUN_CALL_EXP:
        args = []
        arg = expression.arguments
        num_args = 0
        while arg is not None:
            args.append(arg)
            arg = arg.next_node
            num_args += 1
        # push the function arguments onto the stack in reverse order
        while len(args) != 0:
            arg = args.pop()
            if arg.type_string in ('int array', 'string array'):
                gen_l_value(arg, string_table, output_file)
            else:
                gen_code_expression(arg, string_table, output_file)
            gen_reg('push', ACC_64, 'push the function argument onto the stack', output_file)
        gen_reg('push', FP, 'push the frame pointer onto the stack', output_file)
        gen_direct('call', expression.name, 'call function {}'.format(expression.name), output_file)
        gen_reg('pop', FP, 'restore the frame pointer', output_file)
        gen_immediate_reg('addq', num_args*8, SP, 'pop the function arguments off of the stack', output_file)

    # generate code for variable references
    elif expression.kind == NodeType.VAR_EXP:
        # move the address of the variable into the accumulator   
        gen_l_value(expression, string_table, output_file)
        # move the variable's value into the accumulator
        gen_indirect_reg('movq', 0, ACC_64, ACC_64, 'put the value of the variable into the accumulator', output_file)

    # generate code for array reference expressions
    elif expression.kind == NodeType.ARRAY_EXP:
        # move the address of the array cell at the appropriate index into the accumulator
        gen_l_value(expression, string_table, output_file)
        gen_indirect_reg('movq', 0, ACC_64, ACC_64, 'put the value of the array cell into the accumulator', output_file)

    # generate code for assignment expressions
    elif expression.kind == NodeType.ASSIGN_EXP:

        # move the address of the left side of the assignment expression into the accumulator
        gen_l_value(expression.left, string_table, output_file)
        gen_reg('push', ACC_64, 'push the address of the left side of the assignment expression onto the stack', output_file)
        gen_code_expression(expression.right, string_table, output_file)
        gen_indirect_reg('movq', 0, SP, ARG2_64, 'put the address of the left side of the assignment expression into %rsi', output_file)
        gen_reg_indirect('movq', ACC_64, 0, ARG2_64, 'perform the assignment', output_file)
        gen_immediate_reg('addq', 8, SP, 'pop the left side of the assignment expression off of the stack', output_file)

    # generate code for negation expressions
    elif expression.kind == NodeType.NEG_EXP:
        gen_code_expression(expression.expression, string_table, output_file)
        gen_immediate_reg('imul', -1, ACC_32, 'multiply the value of the expression by negative one', output_file)

    # generate code for pointer dereferencing expressions
    elif expression.kind == NodeType.DEREF_EXP:
        # move the value of the pointer (an address) into the accumulator
        gen_code_expression(expression.expression, string_table, output_file)
        # get the value at the address in the accumulator
        gen_indirect_reg('movq', 0, ACC_64, ACC_64, 'move the value at the address stored in the pointer into the accumulator', output_file)

    # generate code for address expressions
    elif expression.kind == NodeType.ADDRESS_EXP:
        # move the variable or array's address into the accumulator
        gen_l_value(expression.expression, string_table, output_file)

    # generate code for reading integer input from stdin
    elif expression.kind == NodeType.READ_EXP:
        gen_immediate_reg('movl', 0, ACC_32, 'clear the return value', output_file)
        gen_immediate_reg('sub', 40, SP, 'decrement the stack pointer by 40 bytes', output_file)
        gen_reg_reg('movq', SP, ARG2_64, 'move the stack pointer into %rsi', output_file)
        gen_immediate_reg('addq', 24, ARG2_64, 'set %rsi to contain the address 24 bytes below the stack pointer', output_file)
        gen_immediate_reg('movq', '.ReadIntString', ARG1_64, 'put .ReadIntString into %rdi', output_file)
        gen_direct('call', 'scanf', 'call the C-lib scanf function', output_file)
        gen_indirect_reg('movl', 24, SP, ACC_32, 'move the integer read from stdin into the accumulator', output_file)
        gen_immediate_reg('addq', 40, SP, 'increment the stack pointer by 40 bytes', output_file)

def gen_l_value(expression, string_table, output_file):
    if expression.kind == NodeType.VAR_EXP:
        if expression.declaration.offset is not None:
            gen_reg_reg('movq', FP, ACC_64, 'move the frame pointer into the accumulator', output_file)
            gen_immediate_reg('addq', expression.declaration.offset, ACC_64, 'update the accumulator to contain the address of the local variable "{}"'.format(expression.name), output_file)
        else: # the variable is global
            gen_immediate_reg('movq', expression.name, ACC_64, 'move the address of the global variable\'s label into the accumulator', output_file)

    elif expression.kind == NodeType.ARRAY_EXP:
        gen_code_expression(expression.expression, string_table, output_file)
        gen_reg_reg('movl', ACC_32, ARG2_32, 'temporarily store the value of the array indexing expression %esi', output_file)
        gen_immediate_reg('imul', 8, ARG2_32, 'convert the array index to an offset', output_file)

        # if the array is local
        if expression.declaration.offset is not None:
            gen_reg_reg('movq', FP, ACC_64, 'move the frame pointer into the accumulator', output_file)
            gen_immediate_reg('addq', expression.declaration.offset, ACC_64, 'update the accumulator to contain the address of the local array "{}"'.format(expression.name), output_file)
            # if the array is a function parameter
            if expression.declaration.size == -1:
                gen_indirect_reg('movq', 0, ACC_64, ACC_64, 'move the address of the function parameter array into the accumulator', output_file)
        else: # the array is global
            gen_immediate_reg('movq', expression.name, ACC_64, 'move the address of the global array\'s label into the accumulator', output_file)
        gen_reg_reg('addq', ARG2_64, ACC_64, 'add the array index (as an offset) to the address of the first element of the array', output_file)

    elif expression.kind == NodeType.DEREF_EXP:
        gen_l_value(expression.expression, string_table, output_file)
        gen_indirect_reg('movq', 0, ACC_64, ACC_64, 'move the address stored in the pointer into the accumulator', output_file)
