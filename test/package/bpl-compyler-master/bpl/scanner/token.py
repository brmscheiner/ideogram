"""
AUTHOR: Oren Shoham
DATE: Feb. 20, 2014

Token class and associated methods for use in a compiler for the BPL
programming language. Implemented for CS331 at Oberlin College.
"""

# Hacking together an Enum data type
def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    enums['names'] = {
            value: key for key, value in enums.iteritems()
            if not key.startswith('__')
            and not key.endswith('__')
    }
    return type('Enum', (), enums)

# An "Enum" that maps Token types onto integers.
# TokenType.T_ID => 0, TokenType.T_NUM => 1, etc.
TokenType = enum('T_ID',
        'T_NUM',
        'T_INT',
        'T_VOID',
        'T_STRING',
        'T_IF',
        'T_ELSE',
        'T_WHILE',
        'T_RETURN',
        'T_WRITE',
        'T_WRITELN',
        'T_READ',
        'T_SEMICOLON',
        'T_COMMA',
        'T_LBRACKET',
        'T_RBRACKET', 
        'T_LBRACE', 
        'T_RBRACE',
        'T_LPAREN',
        'T_RPAREN',
        'T_LESS',
        'T_LEQ',
        'T_EQ',
        'T_NEQ',
        'T_GEQ',
        'T_GREATER',
        'T_ASSIGN',
        'T_PLUS',
        'T_MINUS',
        'T_MULT',
        'T_DIV',
        'T_MOD',
        'T_AND',
        'T_STRVAL',
        'T_EOF'
)

# A Token is the atomic unit of BPL. Each Token keeps track of its kind, 
# the actual string it represents, and the line number on which it occurs.
class Token(object):

    # kind should be a string that is a valid TokenType (see above)
    # value should be a string
    # line_number should be an integer
    def __init__(self, kind, value, line_number):
        self.kind = getattr(TokenType, kind)
        self.value = value
        self.line_number = line_number
    
    # Return a string representation that displays the Token's
    # kind, value, and line number.
    def __str__(self):
        return "Token " + str(self.kind) + ", string " + self.value + ", line number " + str(self.line_number)

def is_type_token(token):
    if not isinstance(token, Token):
        return False
    if token.kind is TokenType.T_INT or token.kind is TokenType.T_VOID or token.kind is TokenType.T_STRING:
        return True
    return False

def is_rel_op(token):
    if not isinstance(token, Token):
        return False
    if token.kind is TokenType.T_LESS or token.kind is TokenType.T_LEQ or \
            token.kind is TokenType.T_EQ or token.kind is TokenType.T_NEQ or \
            token.kind is TokenType.T_GEQ or token.kind is TokenType.T_GREATER:
        return True
    return False

def is_add_op(token):
    if not isinstance(token, Token):
        return False
    if token.kind is TokenType.T_PLUS or token.kind is TokenType.T_MINUS:
        return True
    return False

def is_mul_op(token):
    if not isinstance(token, Token):
        return False
    if token.kind is TokenType.T_MULT or token.kind is TokenType.T_DIV or \
            token.kind is TokenType.T_MOD:
        return True
    return False
