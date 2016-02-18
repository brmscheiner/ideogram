"""
AUTHOR: Oren Shoham
DATE: March 2, 2014

Parse Tree node classes for the BPL Parser. Implemented for CS331 at Oberlin College.
"""

from bpl.scanner.token import TokenType, Token, enum

NodeType = enum('VAR_DEC',
        'FUN_DEC',
        'ARRAY_DEC',
        'EXP_STATEMENT',
        'CMPND_STATEMENT',
        'WHILE_STATEMENT',
        'RETURN_STATEMENT',
        'IF_STATEMENT',
        'WRITE_STATEMENT',
        'WRITELN_STATEMENT',
        'VAR_EXP',
        'ASSIGN_EXP',
        'COMP_EXP',
        'ARRAY_EXP',
        'ADDRESS_EXP',
        'DEREF_EXP',
        'FUN_CALL_EXP',
        'MATH_EXP',
        'NEG_EXP',
        'NUM_EXP',
        'STR_EXP',
        'READ_EXP',
)

class TreeNode(object):
    """Base class for parse tree nodes. Inherited by more specific subclasses of nodes."""
    def __init__(self, kind, line_number, next_node=None):
        self.kind = getattr(NodeType, kind)
        self.line_number = line_number
        self.next_node = next_node
        self.base_string = 'Line {}: {}'.format(
                self.line_number,
                self.__class__.__name__
        )
        
# Declaration Nodes

class DecNode(TreeNode):
    """Base class for declaration nodes. Inherited by variable, function, and array declaration nodes."""
    def __init__(self, kind, line_number, name, type_token, next_node = None):
        TreeNode.__init__(self, kind, line_number, next_node)
        self.name = name
        self.type_token = type_token

class VarDecNode(DecNode):
    """Represents a variable declaration."""
    def __init__(self, kind, line_number, name, type_token, is_pointer = False, next_node = None):
        DecNode.__init__(self, kind, line_number, name, type_token, next_node)
        self.is_pointer = is_pointer
        self.offset = None

    def __str__(self):
        string = '{}{} id = {} type = {} ({}){}{}'.format(
                self.base_string,
                ' (pointer)' if self.is_pointer else '',
                self.name,
                self.type_token.kind,
                TokenType.names[self.type_token.kind],
                ' offset = ' + str(self.offset) if self.offset is not None else '',
                str_if_not_none(self.next_node)
        )
        return string

class FunDecNode(DecNode):
    """Represents a function declaration."""
    def __init__(self, kind, line_number, name, type_token, params, body, next_node = None):
        DecNode.__init__(self, kind, line_number, name, type_token, next_node)
        self.params = params
        self.body = body
        self.local_var_offsets = 0

    def __str__(self):
        string = '{} id = {} return type = {} ({})\nParams:\n{}{}Body:\n{}{}'.format(
                self.base_string,
                self.name,
                self.type_token.kind,
                TokenType.names[self.type_token.kind],
                indent(self.params),
                '\n' if self.params is not None else '',
                indent(self.body),
                str_if_not_none(self.next_node)
        )
        return string

class ArrayDecNode(VarDecNode):
    """Represents an array declaration."""
    def __init__(self, kind, line_number, name, type_token, size, is_pointer = False, next_node = None):
        VarDecNode.__init__(self, kind, line_number, name, type_token, is_pointer, next_node)
        self.size = size

    def __str__(self):
        string = '{}{} id = {} type = {} ({}) size = {}{}{}'.format(
                self.base_string,
                ' (pointer)' if self.is_pointer else '',
                self.name,
                self.type_token.kind,
                TokenType.names[self.type_token.kind],
                str(self.size),
                ' offset = ' + str(self.offset) if self.offset is not None else '',
                str_if_not_none(self.next_node)
        )
        return string

# Statement Nodes

class StatementNode(TreeNode):
    """Base class for statement nodes. Inherited by compound, while, if, write, writeln, return, and expression statement nodes."""
    def __init__(self, kind, line_number, next_node = None):
        TreeNode.__init__(self, kind, line_number, next_node)

class ExpressionStatementNode(StatementNode):
    """Represents an expression statement, which can essentially be any type of expression."""
    def __init__(self, kind, line_number, expression, next_node = None):
        StatementNode.__init__(self, kind, line_number, next_node)
        self.expression = expression

    def __str__(self):
        string = '{}\nExpression:\n{}{}'.format(
                self.base_string,
                indent(self.expression),
                str_if_not_none(self.next_node)
        )
        return string

class CompoundStatementNode(StatementNode):
    """Represents a compound statement, which contains local declarations followed by more statements, all inside curly braces."""
    def __init__(self, kind, line_number, local_declarations, statements, next_node = None):
        StatementNode.__init__(self, kind, line_number, next_node)
        self.local_declarations = local_declarations
        self.statements = statements

    def __str__(self):
        string = '{}\nLocal Declarations:\n{}{}Statements:\n{}{}'.format(
                self.base_string,
                indent(self.local_declarations),
                '\n' if self.local_declarations is not None else '',
                indent(self.statements),
                str_if_not_none(self.next_node)
        )
        return string

class WhileStatementNode(StatementNode):
    """Reprsents a while statement with a condition and a statement to executed."""
    def __init__(self, kind, line_number, condition, statement, next_node = None):
        StatementNode.__init__(self, kind, line_number, next_node)
        self.condition = condition
        self.statement = statement

    def __str__(self):
        string = '{}\nCondition:\n{}\nStatement:\n{}{}'.format(
                self.base_string,
                indent(self.condition),
                indent(self.statement),
                str_if_not_none(self.next_node)
        )
        return string

class ReturnStatementNode(StatementNode):
    """Represents a return statement with an optional expression to be returned."""
    def __init__(self, kind, line_number, expression, next_node = None):
        StatementNode.__init__(self, kind, line_number, next_node)
        self.expression = expression

    def __str__(self):
        string = '{}{}{}{}'.format(
                self.base_string,
                '\nExpression:\n' if self.expression is not None else '',
                indent(self.expression),
                str_if_not_none(self.next_node)
        )
        return string

class IfStatementNode(StatementNode):
    """Represents an if statement with a condition, a statement to executed, and an optional else statement."""
    def __init__(self, kind, line_number, condition, statement, else_statement, next_node = None):
        StatementNode.__init__(self, kind, line_number, next_node)
        self.condition = condition
        self.statement = statement
        self.else_statement = else_statement

    def __str__(self):
        string = '{}\nCondition:\n{}\nStatement:\n{}{}{}{}'.format(
                self.base_string,
                indent(self.condition),
                indent(self.statement),
                '\nElse Statement:\n' if self.else_statement is not None else '',
                indent(self.else_statement),
                str_if_not_none(self.next_node)
        )
        return string

class WriteStatementNode(StatementNode):
    """Represents a write statement with an expression to be written."""
    def __init__(self, kind, line_number, expression, next_node = None):
        StatementNode.__init__(self, kind, line_number, next_node)
        self.expression = expression

    def __str__(self):
        string = '{}\nExpression:\n{}{}'.format(
                self.base_string,
                indent(self.expression),
                str_if_not_none(self.next_node)
        )
        return string

class WritelnStatementNode(StatementNode):
    """Represents a writeln statement."""
    def __init__(self, kind, line_number, next_node = None):
        StatementNode.__init__(self, kind, line_number, next_node)

    def __str__(self):
        string = '{}{}'.format(
                self.base_string,
                str_if_not_none(self.next_node)
        )
        return string

# Expression Nodes

class ExpressionNode(TreeNode):
    """Base class for expression nodes. Inherited by variable, operation, array, dereference, address, \
            negative, number, string, read, and function call expression nodes."""
    def __init__(self, kind, line_number, next_node = None):
        TreeNode.__init__(self, kind, line_number, next_node)
        self.type_string = None

class VarExpNode(ExpressionNode):
    """Represents a variable."""
    def __init__(self, kind, line_number, name, next_node = None):
        ExpressionNode.__init__(self, kind, line_number, next_node)
        self.name = name
        self.declaration = None

    def __str__(self):
        string = '{} id = {}{}{}{}'.format(
                self.base_string,
                self.name,
                ' type = {}'.format(self.type_string) if self.type_string is not None else '',
                '\nDeclaration:\n'+indent(dec_info(self.declaration))+'\n' if self.declaration is not None else '',
                str_if_not_none(self.next_node)
        )
        return string

class OpNode(ExpressionNode):
    """Represents an infix operation, which can be any one of addition, subtraction, multiplication, \
            division, assignment, or modulo."""
    def __init__(self, kind, line_number, token, left, right, next_node = None):
        ExpressionNode.__init__(self, kind, line_number, next_node)
        self.token = token
        self.left = left
        self.right = right

    def __str__(self):
        string = '{} token = {} ({}){}\nLeft:\n{}\nRight:\n{}{}'.format(
                self.base_string,
                self.token.kind,
                TokenType.names[self.token.kind],
                ' type = {}'.format(self.type_string) if self.type_string is not None else '',
                indent(self.left),
                indent(self.right),
                str_if_not_none(self.next_node)
        ) 
        return string

class ArrayExpNode(VarExpNode):
    """Represents an array indexing expression, e.g. arr[x+1]."""
    def __init__(self, kind, line_number, name, expression, next_node = None):
        VarExpNode.__init__(self, kind, line_number, name, next_node)
        self.expression = expression
        self.declaration = None

    def __str__(self):
        string = '{} id = {}{}\nIndex Expression:\n{}{}{}'.format(
                self.base_string,
                self.name,
                ' type = {}'.format(self.type_string) if self.type_string is not None else '',
                indent(self.expression),
                '\nDeclaration:\n'+indent(dec_info(self.declaration))+'\n' if self.declaration is not None else '',
                str_if_not_none(self.next_node)
        )
        return string

class DerefExpNode(ExpressionNode):
    """Represents a pointer dereference, e.g. *x."""
    def __init__(self, kind, line_number, expression, next_node = None):
        ExpressionNode.__init__(self, kind, line_number, next_node)
        self.expression = expression

    def __str__(self):
        string = '{}{}\nPointer Expression:\n{}{}'.format(
                self.base_string,
                ' type = {}'.format(self.type_string) if self.type_string is not None else '',
                indent(self.expression),
                str_if_not_none(self.next_node)
        )
        return string

class AddressExpNode(ExpressionNode):
    """Represents a memory address reference, e.g. &x."""
    def __init__(self, kind, line_number, expression, next_node = None):
        ExpressionNode.__init__(self, kind, line_number, next_node)
        self.expression = expression

    def __str__(self):
        string = '{}{}\nReference Expression:\n{}{}'.format(
                self.base_string,
                ' type = {}'.format(self.type_string) if self.type_string is not None else '',
                indent(self.expression),
                str_if_not_none(self.next_node)
        )
        return string

class NegExpNode(ExpressionNode):
    """Represents applying the negative operator to a value, e.g -x."""
    def __init__(self, kind, line_number, expression, next_node = None):
        ExpressionNode.__init__(self, kind, line_number, next_node)
        self.expression = expression

    def __str__(self):
        string = '{}{}\nNegative Expression:\n{}{}'.format(
                self.base_string,
                ' type = {}'.format(self.type_string) if self.type_string is not None else '',
                indent(self.expression),
                str_if_not_none(self.next_node)
        )
        return string

class NumExpNode(ExpressionNode):
    """Represents an integer."""
    def __init__(self, kind, line_number, number, next_node = None):
        ExpressionNode.__init__(self, kind, line_number, next_node)
        self.number = number
    
    def __str__(self):
        string = '{} number = {}{}{}'.format(
                self.base_string,
                self.number,
                ' type = {}'.format(self.type_string) if self.type_string is not None else '',
                str_if_not_none(self.next_node)
        )
        return string

class StringExpNode(ExpressionNode):
    """Represents a string."""
    def __init__(self, kind, line_number, string, next_node = None):
        ExpressionNode.__init__(self, kind, line_number, next_node)
        self.string = string
    
    def __str__(self):
        string = '{} string = {}{}{}'.format(
                self.base_string,
                self.string,
                ' type = {}'.format(self.type_string) if self.type_string is not None else '',
                str_if_not_none(self.next_node)
        )
        return string

class ReadExpNode(ExpressionNode):
    """Represents a read operation."""
    def __init__(self, kind, line_number, next_node = None):
        ExpressionNode.__init__(self, kind, line_number, next_node)

    def __str__(self):
        string = '{}{}{}'.format(
                self.base_string,
                ' type = {}'.format(self.type_string) if self.type_string is not None else '',
                str_if_not_none(self.next_node)
        )
        return string

class FunCallExpNode(ExpressionNode):
    """Represents a function call, e.g. f(x)."""
    def __init__(self, kind, line_number, name, arguments, next_node = None):
        ExpressionNode.__init__(self, kind, line_number, next_node)
        self.name = name
        self.arguments = arguments
        self.declaration = None

    def __str__(self):
        string = '{} name = {}{}{}{}{}{}'.format(
                self.base_string,
                self.name,
                ' type = {}'.format(self.type_string) if self.type_string is not None else '',
                '\nArguments:\n' if self.arguments is not None else '',
                indent(self.arguments),
                '\nDeclaration:\n'+indent(dec_info(self.declaration))+'\n' if self.declaration is not None else '',
                str_if_not_none(self.next_node)
        )
        return string

# Helper Functions

def str_if_not_none(x):
    """Return str(x) with a preceding newline if x is not None. Otherwise, return an empty string."""
    string = ''
    if x is not None:
        string += '\n{}'.format(str(x))
    return string

def indent(s):
    """Return each line of s indented with a preceding '| ' if s is not None. Otherwise, return an emptry string."""
    indented_string = ''
    if s is None:
        return indented_string
    for line in str(s).splitlines():
        indented_string += '| {}\n'.format(line)
    return indented_string[:-1]

def dec_info(dec):
    """Return a string containing information about a declaration (for use in an expression node's __str__ function)."""
    if not isinstance(dec, DecNode):
        return ''
    if dec.kind is NodeType.VAR_DEC:
        return '{}{} id = {} type = {} ({})'.format(
                dec.base_string,
                ' (pointer)' if dec.is_pointer else '',
                dec.name,
                dec.type_token.kind,
                TokenType.names[dec.type_token.kind]
        )
    elif dec.kind is NodeType.ARRAY_DEC:
        return '{}{} id = {} type = {} ({}) size = {}'.format(
                dec.base_string,
                ' (pointer)' if dec.is_pointer else '',
                dec.name,
                dec.type_token.kind,
                TokenType.names[dec.type_token.kind],
                str(dec.size)
        )
    elif dec.kind is NodeType.FUN_DEC:
        return '{} id = {} return type = {} ({})'.format(
                dec.base_string,
                dec.name,
                dec.type_token.kind,
                TokenType.names[dec.type_token.kind],
        )
