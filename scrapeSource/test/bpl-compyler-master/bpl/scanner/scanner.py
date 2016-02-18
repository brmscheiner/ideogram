"""
AUTHOR: Oren Shoham
DATE: Feb. 16, 2014

A lexical scanner for the BPL programming language. Implemented for CS331 at Oberlin College.
"""

from bpl.scanner.token import TokenType, Token
import bpl.scanner.token

class ScannerException(Exception):
    def __init__(self, line_number, index, message):
        message = 'Scanner Error on line {}, index {}: {}'.format(line_number, index, message)
        Exception.__init__(self, message)

# The Scanner performs a lexical analysis of a BPL file. It keeps track of
# its current position in the file, and uses the variable next_token and the method 
# get_next_token() to step through the file, one Token at a time.
class Scanner(object):

    # Constructor for the Scanner. Takes a file object as the only parameter,
    # sets the current line to the first line of said file, initalizes next_token
    # to None, and sets up a dictionary of keywords mapped to their respective TokenTypes.
    def __init__(self, input_file):
        self.input_file = input_file
        self.current_line = self.input_file.readline()
        self.line_number = 1
        self.next_token = None
        self.keywords = ["int", "void", "string", "if", "else", "while",
                "return", "write", "writeln", "read"]
        keyword_tokens = ['T_INT', 'T_VOID', 'T_STRING', 'T_IF', 'T_ELSE',
                'T_WHILE', 'T_RETURN', 'T_WRITE', 'T_WRITELN', 'T_READ']
        self.keyword_hash = dict(zip(self.keywords, keyword_tokens)) 

    # Sets next_token to be the next Token in the input file.
    # This method is one giant if/elif/else statement and I wish
    # it were cleaner, but there aren't a lot of better ways to do this.
    def get_next_token(self):
        i = 0
        # skip over whitespace
        while(i < len(self.current_line) and self.current_line[i].isspace()):
            i += 1
        if(i == len(self.current_line)):
            # advance to the next line of the file
            self.current_line = self.input_file.readline()
            if not self.current_line: # we've hit the end of the file
                self.next_token = Token('T_EOF', "", self.line_number)
                self.input_file.close()
            else: # there's still another line to read
                self.line_number += 1
                self.get_next_token()
        else: # i < len(self.current_line)
            # handle number Tokens
            if(self.current_line[i].isdigit()):
                j = i+1
                # keep going until we hit something that's not a number
                while(j < len(self.current_line) and self.current_line[j].isdigit()):
                    j += 1
                token_string = self.current_line[i:j]
                self.next_token = Token('T_NUM', token_string, self.line_number)
                # discard the part of the current line that we've already read
                self.current_line = self.current_line[j:]
            # handle identifier and keyword Tokens
            elif(self.current_line[i].isalpha()):
                j = i+1
                # keep going until we hit something that's not alphanumeric
                while(j < len(self.current_line) and self.current_line[j].isalnum()):
                    j += 1
                token_string = self.current_line[i:j]
                # check token_string to see if it's actually a BPL keyword
                if(token_string in self.keywords):
                    # set next_token to be the appropriate keyword Token
                    self.next_token = Token(self.keyword_hash[token_string], token_string, self.line_number)
                else:
                    self.next_token = Token('T_ID', token_string, self.line_number)
                self.current_line = self.current_line[j:]
            # handle '+' Tokens
            elif(self.current_line[i] == '+'):
                self.next_token = Token('T_PLUS', "+", self.line_number)
                self.current_line = self.current_line[i+1:]
            # handle '-' Tokens
            elif(self.current_line[i] == '-'):
                self.next_token = Token('T_MINUS', "-", self.line_number)
                self.current_line = self.current_line[i+1:]
            # handle ';' Tokens
            elif(self.current_line[i] == ';'):
                self.next_token = Token('T_SEMICOLON', ";", self.line_number)
                self.current_line = self.current_line[i+1:]
            # handle ',' Tokens
            elif(self.current_line[i] == ','):
                self.next_token = Token('T_COMMA', ",", self.line_number)
                self.current_line = self.current_line[i+1:]
            # handle '[' Tokens
            elif(self.current_line[i] == '['):
                self.next_token = Token('T_LBRACKET', "[", self.line_number)
                self.current_line = self.current_line[i+1:]
            # handle ']' Tokens
            elif(self.current_line[i] == ']'):
                self.next_token = Token('T_RBRACKET', "]", self.line_number)
                self.current_line = self.current_line[i+1:]
            # handle '{' Tokens
            elif(self.current_line[i] == '{'):
                self.next_token = Token('T_LBRACE', "{", self.line_number)
                self.current_line = self.current_line[i+1:]
            # handle '}' Tokens
            elif(self.current_line[i] == '}'):
                self.next_token = Token('T_RBRACE', "}", self.line_number)
                self.current_line = self.current_line[i+1:]
            # handle '(' Tokens
            elif(self.current_line[i] == '('):
                self.next_token = Token('T_LPAREN', "(", self.line_number)
                self.current_line = self.current_line[i+1:]
            # handle ')' Tokens
            elif(self.current_line[i] == ')'):
                self.next_token = Token('T_RPAREN', ")", self.line_number)
                self.current_line = self.current_line[i+1:]
            # handle '<' and '<=' Tokens
            elif(self.current_line[i] == '<'):
                j = i+1
                if(self.current_line[j] == '='):
                    self.next_token = Token('T_LEQ', "<=", self.line_number)
                    self.current_line = self.current_line[j+1:]
                else:
                    self.next_token = Token('T_LESS', "<", self.line_number)
                    self.current_line = self.current_line[i+1:]
            # handle '>' and '>=' Tokens
            elif(self.current_line[i] == '>'):
                j = i+1
                if(self.current_line[j] == '='):
                    self.next_token = Token('T_GEQ', ">=", self.line_number)
                    self.current_line = self.current_line[j+1:]
                else:
                    self.next_token = Token('T_GREATER', ">", self.line_number)
                    self.current_line = self.current_line[i+1:]
            # handle '=' and '==' Tokens
            elif(self.current_line[i] == '='):
                j = i+1
                if(self.current_line[j] == '='):
                    self.next_token = Token('T_EQ', "==", self.line_number)
                    self.current_line = self.current_line[j+1:]
                else:
                    self.next_token = Token('T_ASSIGN', "=", self.line_number)
                    self.current_line = self.current_line[i+1:]
            # handle '!=' Tokens
            elif(self.current_line[i] == '!'):
                j = i+1
                if(self.current_line[j] == '='):
                    self.next_token = Token('T_NEQ', "!=", self.line_number)
                    self.current_line = self.current_line[j+1:]
                else: 
                    raise ScannerException(self.line_number, i, "Unidentifiable token.")
            # handle '*' Tokens
            elif(self.current_line[i] == '*'):
                self.next_token = Token('T_MULT', "*", self.line_number)
                self.current_line = self.current_line[i+1:]
            # handle '/' Tokens and comments
            elif(self.current_line[i] == '/'):
                j = i+1
                if(self.current_line[j] == '*'): # we're at the start of a comment block
                    j += 1
                    new_line_number = self.line_number # account for comments spanning multiple lines
                    while(self.current_line[j:j+2] != '*/'): # should not cause error if j+2 > len(self.current_line)
                        if(j == len(self.current_line)):
                            self.current_line = self.input_file.readline()
                            if not self.current_line:
                                raise ScannerException(self.line_number, i, 'Expected an additional "*/" to close the comment block.')
                                #print("Scanning Error: Expected an additional '/*' to close the comment block beginning at line " + str(self.line_number) + ", index " + str(i) + ".")
                                #exit()
                            else:
                                new_line_number += 1
                                j = 0
                        else: # j < len(self.current_line)
                            j += 1
                    self.line_number = new_line_number
                    self.current_line = self.current_line[j+2:]
                    self.get_next_token()
                else:
                    self.next_token = Token('T_DIV', "/", self.line_number)
                    self.current_line = self.current_line[i+1:]
            # handle '%' Tokens
            elif(self.current_line[i] == '%'):
                self.next_token = Token('T_MOD', "%", self.line_number)
                self.current_line = self.current_line[i+1:]
            # handle '&' Tokens
            elif(self.current_line[i] == '&'):
                self.next_token = Token('T_AND', "&", self.line_number)
                self.current_line = self.current_line[i+1:]
            elif(self.current_line[i] == '"'):
                j = i+1
                while(self.current_line[j] != '"'):
                    j += 1
                    if(j == len(self.current_line)):
                        raise ScannerException(self.line_number, i, "Expected an additional '\"' to close the string.")
                        #print("Scanning Error: Expected an additional '\"' to close the string beginning at line " + str(self.line_number) + ", index " + str(i) + ".")
                        #exit()
                token_string = self.current_line[i+1:j]
                self.next_token = Token('T_STRVAL', token_string, self.line_number)
                self.current_line = self.current_line[j+1:]
            # we've hit something we can't recognize
            else:
                raise ScannerException(self.line_number, i, "Unidentifiable token.")
                #print("Scanning Error: Unidentifiable token at line " + str(self.line_number) + ", index " + str(i) + ".")
                #exit()
