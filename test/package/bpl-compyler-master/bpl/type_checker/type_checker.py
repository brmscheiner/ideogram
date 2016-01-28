"""
AUTHOR: Oren Shoham
DATE: 4/5/2014
"""

from bpl.parser.parsetree import *
from bpl.scanner.token import TokenType

class TypeCheckerException(Exception):
    def __init__(self, line_number, message):
        message = 'Type Checking Error on line {}: {}'.format(line_number, message)
        Exception.__init__(self, message)

def type_check(parse_tree, debug=False):
    symbol_table = [{}] # this is meant to function as a stack of symbol tables
    # top down pass through the parse tree
    find_references(parse_tree, symbol_table, debug)
    # bottom up pass through the parse tree
    type_check_declarations(parse_tree, debug)

def lookup(symbol, symbol_table):
    """Check whether symbol is a key in any of the dictionaries in symbol table, starting at the top of stack.

    Return the parse tree node that is the value of symbol if symbol is a valid key, otherwise None.
    """
    for scope in reversed(list(range(len(symbol_table)))):
        if symbol in symbol_table[scope]:
            return symbol_table[scope][symbol]
    return None

def find_references(parse_tree, symbol_table, debug):
    """Iterate through the top-level declarations of the parse tree and create links between expressions and their declarations."""
    declaration = parse_tree
    while declaration is not None:
        # add the declaration to the top level of the symbol table (bottom of the stack)
        symbol_table[0][declaration.name] = declaration

        # skip variable and array declarations
        if declaration.kind in (NodeType.VAR_DEC, NodeType.ARRAY_DEC):
            declaration = declaration.next_node

        elif declaration.kind is NodeType.FUN_DEC:
            local_variables = {}
            param = declaration.params
            while param is not None:
                if param.kind not in (NodeType.VAR_DEC, NodeType.ARRAY_DEC):
                    raise TypeCheckerException(param.line_number, 'Function parameter is not a variable, pointer, or array.')
                if param.type_token.kind is TokenType.T_VOID:
                    raise TypeCheckerException(param.line_number, 'Cannot have a function parameter of type "void".')
                # add function parameter to function's local variables
                local_variables[param.name] = param
                param = param.next_node

            # push local variables onto the top of the symbol table stack
            symbol_table.append(local_variables)
            # link expressions in the function's body to their declarations
            find_references_statement(declaration.body, symbol_table, debug)
            # pop local variables off of the symbol table stack
            symbol_table.pop() 
            declaration = declaration.next_node

        else:
            raise TypeCheckerException(declaration.line_number, 'Top-level declaration is not a variable, pointer, array, or function.')

def find_references_statement(statement, symbol_table, debug):
    """Create links between expressions associated with a statement and their declarations in the symbol table."""
    if statement.kind is NodeType.EXP_STATEMENT:
        find_references_expression(statement.expression, symbol_table, debug)

    elif statement.kind is NodeType.WHILE_STATEMENT:
        find_references_expression(statement.condition, symbol_table, debug)
        find_references_statement(statement.statement, symbol_table, debug)

    elif statement.kind is NodeType.RETURN_STATEMENT:
        find_references_expression(statement.expression, symbol_table, debug)

    elif statement.kind is NodeType.WRITE_STATEMENT:
        find_references_expression(statement.expression, symbol_table, debug)

    elif statement.kind is NodeType.WRITELN_STATEMENT:
        pass

    elif statement.kind is NodeType.IF_STATEMENT:
        find_references_expression(statement.condition, symbol_table, debug)
        find_references_statement(statement.statement, symbol_table, debug)
        if statement.else_statement is not None:
            find_references_statement(statement.else_statement, symbol_table, debug)

    elif statement.kind is NodeType.CMPND_STATEMENT:
        local_variables = {}
        dec = statement.local_declarations
        # add local declarations to the symbol table
        while dec is not None:
            if dec.kind not in (NodeType.VAR_DEC, NodeType.ARRAY_DEC):
                raise TypeCheckerException(dec.line_number, 'Local declaration is not a variable, pointer, or array.')
            local_variables[dec.name] = dec
            dec = dec.next_node

        # push local variables onto the symbol table stack
        symbol_table.append(local_variables)
        stmnt = statement.statements # I regret my chosen variable names
        while stmnt is not None:
            # link expressions in the compound statement to their declarations
            find_references_statement(stmnt, symbol_table, debug)
            stmnt = stmnt.next_node
        # pop local variables off of the symbol table stack
        symbol_table.pop()

    else:
        raise TypeCheckerException(statement.line_number, 'Statement node is not a valid type of statement.')

def find_references_expression(expression, symbol_table, debug):
    """Create links between expressions and their declarations in the symbol table."""
    if expression.kind in (NodeType.VAR_EXP, NodeType.ARRAY_EXP):
        # look up expression's declaration in the symbol table
        dec = lookup(expression.name, symbol_table)
        if dec is None:
            raise TypeCheckerException(
                    expression.line_number, 
                    'Undeclared variable or array with name {}.'.format(expression.name)
            )
        # set expression's declaration field
        expression.declaration = dec
        if expression.kind is NodeType.ARRAY_EXP:
            # link expressions in array reference to their declarations
            find_references_expression(expression.expression, symbol_table, debug)
        if debug:
            print('{} {} on line {} linked to declaration on line {}.'.format(
                    'Variable' if expression.kind is NodeType.VAR_EXP else 'Array',
                    expression.name,
                    expression.line_number,
                    dec.line_number
            ))

    elif expression.kind is NodeType.FUN_CALL_EXP:
        if expression.name not in symbol_table[0]:
            raise TypeCheckerException(
                    expression.line_number, 
                    'Undeclared function with name {}.'.format(expression.name)
            )

        # look up function declaration in top-level symbol table
        expression.declaration = symbol_table[0][expression.name]
        if debug:
            print('Function call {} on line {} linked to declaration on line {}.'.format(
                    expression.name,
                    expression.line_number,
                    expression.declaration.line_number
            ))

        arg = expression.arguments
        while arg is not None:
            # link expressions in function call arguments to their declarations
            find_references_expression(arg, symbol_table, debug)
            arg = arg.next_node
    
    elif expression.kind in (NodeType.ASSIGN_EXP, NodeType.COMP_EXP, NodeType.MATH_EXP):
        find_references_expression(expression.left, symbol_table, debug)
        find_references_expression(expression.right, symbol_table, debug)

    elif expression.kind in (NodeType.ADDRESS_EXP, NodeType.DEREF_EXP, NodeType.NEG_EXP):
        find_references_expression(expression.expression, symbol_table, debug) # again, regretting my chosen variable names
    
    elif expression.kind in (NodeType.NUM_EXP, NodeType.STR_EXP, NodeType.READ_EXP):
        pass

    else:
        raise TypeCheckerException(expression.line_number, 'Expression node is not a valid type of expression.')

def type_check_declarations(parse_tree, debug):
    """Type check top-level declarations of the parse tree"""
    declaration = parse_tree
    while declaration is not None:
        if declaration.kind in (NodeType.VAR_DEC, NodeType.ARRAY_DEC):
            if declaration.type_token.kind is TokenType.T_VOID:
                raise TypeCheckerException(declaration.line_number, 'Cannot have a variable or array of type "void".')
            declaration = declaration.next_node

        elif declaration.kind is NodeType.FUN_DEC:
            if declaration.type_token.kind not in (TokenType.T_INT, TokenType.T_STRING, TokenType.T_VOID):
                raise TypeCheckerException(declaration.line_number, 'Function declaration must have a type of "int", "string", or "void".')
            # type check function body
            type_check_statement(declaration.body, declaration.type_token.kind, debug)
            declaration = declaration.next_node

        else:
            raise TypeCheckerException(declaration.line_number, 'Top-level declaration is not a variable, pointer, array, or function.')

def type_check_statement(statement, return_type, debug):
    """Type check statements using declaration links created by find_references."""
    if statement.kind is NodeType.EXP_STATEMENT:
        type_check_expression(statement.expression, debug)

    elif statement.kind is NodeType.WHILE_STATEMENT:
        type_check_expression(statement.condition, debug)
        if statement.condition.type_string is not 'int':
            raise TypeCheckerException(statement.line_number, 'Type of while condition is "{}", but should be "int".'.format(statement.condition.type_string))
        type_check_statement(statement.statement, return_type, debug)

    elif statement.kind is NodeType.RETURN_STATEMENT:
        type_check_expression(statement.expression, debug)
        if return_type is TokenType.T_INT:
            if statement.expression.type_string is not 'int':
                raise TypeCheckerException(statement.line_number, 'Function has a return type of int, but returns {}.'.format(statement.expression.type_string))
        elif return_type is TokenType.T_STRING:
            if statement.expression.type_string is not 'string':
                raise TypeCheckerException(statement.line_number, 'Function has a return type of string, but returns {}.'.format(statement.expression.type_string))
        else:
            raise TypeCheckerException(statement.line_number, 'Function has a return type of void, but returns {}.'.format(statement.expression.type_string))

    elif statement.kind is NodeType.WRITE_STATEMENT:
        type_check_expression(statement.expression, debug)
        if statement.expression.type_string not in ('int', 'string'):
            raise TypeCheckerException(statement.line_number, 'Cannot write an expression of type "{}".'.format(statement.expression.type_string))

    elif statement.kind is NodeType.WRITELN_STATEMENT:
        pass

    elif statement.kind is NodeType.IF_STATEMENT:
        type_check_expression(statement.condition, debug)
        if statement.condition.type_string is not 'int':
            raise TypeCheckerException(statement.line_number, 'Type of if condition is "{}", but should be "int".'.format(statement.condition.type_string))
        type_check_statement(statement.statement, return_type, debug)
        if statement.else_statement is not None:
            type_check_statement(statement.else_statement, return_type, debug)

    elif statement.kind is NodeType.CMPND_STATEMENT:
        dec = statement.local_declarations
        while dec is not None:
            if dec.type_token.kind is TokenType.T_VOID:
                raise TypeCheckerException(dec.line_number, 'Cannot have a variable or array of type "void".')
            dec = dec.next_node

        stmnt = statement.statements 
        while stmnt is not None:
            type_check_statement(stmnt, return_type, debug)
            stmnt = stmnt.next_node

    else:
        raise TypeCheckerException(statement.line_number, 'Statement node is not a valid type of statement.')

def type_check_expression(expression, debug):
    """Type check expressions using declaration links created by find_references."""
    if expression.kind is NodeType.VAR_EXP:
        if expression.declaration.kind is NodeType.VAR_DEC:
            if expression.declaration.type_token.kind is TokenType.T_INT:
                if expression.declaration.is_pointer:
                    expression.type_string = 'pointer to int'
                else:
                    expression.type_string = 'int'
            elif expression.declaration.type_token.kind is TokenType.T_STRING:
                if expression.declaration.is_pointer:
                    expression.type_string = 'pointer to string'
                else:
                    expression.type_string = 'string'
            else:
                raise TypeCheckerException(expression.line_number, 'Cannot have a variable of type "void".')
        elif expression.declaration.kind is NodeType.ARRAY_DEC:
            if expression.declaration.is_pointer:
                raise TypeCheckerException(expression.line_number, 'Cannot have a pointer to an array.')
            if expression.declaration.type_token.kind is TokenType.T_INT:
                expression.type_string = 'int array'
            elif expression.declaration.type_token.kind is TokenType.T_STRING:
                expression.type_string = 'string array'
            else:
                raise TypeCheckerException(expression.line_number, 'Cannot have a variable of type "void".')

        if debug:
            print('Variable {} on line {} assigned type "{}".'.format(
                    expression.name,
                    expression.line_number,
                    expression.type_string
            ))

    elif expression.kind is NodeType.ARRAY_EXP:
        if expression.declaration.kind is not NodeType.ARRAY_DEC:
            raise TypeCheckerException(expression.line_number, 'Cannot take an element reference of a non-array.')
        type_check_expression(expression.expression, debug)
        if expression.expression.type_string != 'int':
            raise TypeCheckerException(expression.line_number, 'Array element reference expression must be of type "int".')
        if expression.declaration.type_token.kind is TokenType.T_INT:
            expression.type_string = 'int'
        elif expression.declaration.type_token.kind is TokenType.T_STRING:
            expression.type_string = 'string'
        else:
            raise TypeCheckerException(expression.line_number, 'Cannot have an array of type "void".')

        if debug:
            print('Array {} on line {} assigned type "{}".'.format(
                    expression.name,
                    expression.line_number,
                    expression.type_string
            ))
    
    elif expression.kind is NodeType.FUN_CALL_EXP:
        num_params = 0
        num_args = 0
        param = expression.declaration.params
        arg = expression.arguments
        while arg is not None and param is not None:
            type_check_expression(arg, debug)
            
            # check that arg and param have the same type
            if param.kind is NodeType.VAR_DEC:
                if param.is_pointer:
                    if param.type_token.kind is TokenType.T_INT and arg.type_string != 'pointer to int':
                        raise TypeCheckerException(arg.line_number, 'Function parameter has type "pointer to int", but argument has type "{}".'.format(
                            arg.type_string
                            )
                        )
                    elif param.type_token.kind is TokenType.T_STRING and arg.type_string != 'pointer to string':
                        raise TypeCheckerException(arg.line_number, 'Function parameter has type "pointer to string", but argument has type "{}".'.format(
                            arg.type_string
                            )
                        )
                else:
                    if param.type_token.kind is TokenType.T_INT and arg.type_string != 'int':
                        raise TypeCheckerException(arg.line_number, 'Function parameter has type "int", but argument has type "{}".'.format(
                            arg.type_string
                            )
                        )
                    elif param.type_token.kind is TokenType.T_STRING and arg.type_string != 'string':
                        raise TypeCheckerException(arg.line_number, 'Function parameter has type "string", but argument has type "{}".'.format(
                            arg.type_string
                            )
                        )
            else: # param.kind is ARRAY_DEC
                if param.is_pointer:
                    raise TypeCheckerException(param.line_number, 'Cannot have a pointer to an array.')
                if param.type_token.kind is TokenType.T_INT and arg.type_string != 'int array':
                    raise TypeCheckerException(arg.line_number, 'Function parameter has type "int array", but argument has type "{}".'.format(
                        arg.type_string
                        )
                    )
                elif param.type_token.kind is TokenType.T_STRING and arg.type_string != 'string array':
                    raise TypeCheckerException(arg.line_number, 'Function parameter has type "string array", but argument has type "{}".'.format(
                        arg.type_string
                        )
                    )
            num_params += 1
            num_args += 1
            param = param.next_node
            arg = arg.next_node

        # check that the lengths of the parameter and argument lists are equal
        if (arg is None and param is not None) or (param is None and arg is not None):
            while arg is not None:
                arg = arg.next_node
                num_args += 1
            while param is not None:
                param = param.next_node
                num_params += 1
            raise TypeCheckerException(expression.line_number, 'Function {} takes {} parameters, but is called with {} arguments.'.format(
                expression.name,
                num_params,
                num_args
                )
            )

        if expression.declaration.type_token.kind is TokenType.T_INT:
            expression.type_string = 'int'
        elif expression.declaration.type_token.kind is TokenType.T_STRING:
            expression.type_string = 'string'
        else: # expression.declaration.type_token.kind is TokenType.T_VOID
            expression.type_string = 'void'

        if debug:
            print('Call to function {} on line {} assigned type "{}".'.format(
                    expression.name,
                    expression.line_number,
                    expression.type_string
            ))
    
    elif expression.kind is NodeType.ASSIGN_EXP:
        type_check_expression(expression.left, debug)
        type_check_expression(expression.right, debug)
        if not is_l_value(expression.left):
            raise TypeCheckerException(expression.line_number, 'Left side of assignment expression is not an assignable value.')
        if expression.left.type_string != expression.right.type_string:
            raise TypeCheckerException(expression.line_number, 'Left side of assignment expression has type "{}", but right side has type "{}".'.format(
                expression.left.type_string,
                expression.right.type_string
                )
            )
        expression.type_string = expression.left.type_string

        if debug:
            print('Assignment expression on line {} assigned type "{}".'.format(
                    expression.line_number,
                    expression.type_string
            ))

    elif expression.kind in (NodeType.COMP_EXP, NodeType.MATH_EXP):
        expression_type = 'comparison' if expression.kind == NodeType.COMP_EXP else 'arithmetic'
        type_check_expression(expression.left, debug)
        type_check_expression(expression.right, debug)
        if expression.left.type_string != 'int':
            raise TypeCheckerException(expression.line_number, 'Left side of {} expression has type "{}", but should have type "int".'.format(
                expression_type,
                expression.left.type_string
                )
            )

        if expression.right.type_string != 'int':
            raise TypeCheckerException(expression.line_number, 'Right side of {} expression has type "{}", but should have type "int".'.format(
                expression_type,
                expression.right.type_string
                )
            )
        expression.type_string = 'int' 

        if debug:
            print('{} expression on line {} assigned type "{}".'.format(
                    expression_type.capitalize(),
                    expression.line_number,
                    expression.type_string
            ))

    elif expression.kind is NodeType.ADDRESS_EXP:
        type_check_expression(expression.expression, debug)
        if expression.expression.kind not in (NodeType.VAR_EXP, NodeType.ARRAY_EXP):
            raise TypeCheckerException(expression.line_number, 'Can only take the address of a variable or array element.')
        if expression.expression.type_string == 'int':
            expression.type_string = 'pointer to int'
        else: # expression.expression.type_string == 'string'
            expression.type_string = 'pointer to string'

        if debug:
            print('Address expression on line {} assigned type "int".'.format(expression.line_number))

    elif expression.kind is NodeType.DEREF_EXP:
        type_check_expression(expression.expression, debug)
        if expression.expression.type_string == 'pointer to int':
            expression.type_string = 'int'
        elif expression.expression.type_string == 'pointer to string':
            expression.type_string = 'string'
        else:
            raise TypeCheckerException(expression.line_number, 'Can only dereference pointers to integers or strings.')

        if debug:
            print('Pointer dereference expression on line {} assigned type "{}".'.format(
                    expression.line_number,
                    expression.type_string
            ))

    elif expression.kind is NodeType.NEG_EXP:
        type_check_expression(expression.expression, debug)
        if expression.expression.type_string != 'int':
            raise TypeCheckerException(expression.line_number, 'Cannot take the negative of a non-integer value.')
        expression.type_string = 'int'

        if debug:
            print('Negative expression on line {} assigned type "int".'.format(expression.line_number))
    
    elif expression.kind in (NodeType.NUM_EXP, NodeType.READ_EXP):
        expression.type_string = 'int'

        if debug:
            print('{} expression on line {} assigned type "int".'.format(
                    'Integer' if expression.kind is NodeType.NUM_EXP else 'Read',
                    expression.line_number
            ))

    elif expression.kind is NodeType.STR_EXP:
        expression.type_string = 'string'

        if debug:
            print('String expression on line {} assigned type "string".'.format(expression.line_number))

    else:
        raise TypeCheckerException(expression.line_number, 'Expression node is not a valid type of expression.')

def is_l_value(node):
    """Returns True if node is an assignable value, otherwise False."""
    if node.kind in (NodeType.VAR_EXP, NodeType.ARRAY_EXP, NodeType.DEREF_EXP):
        return True
    return False
