# lextab.py.  This file automatically created by PLY. Don't edit.
_lexre = '(?P<t_COMMENT_FORMULA>;?[Cc]omment\\s*{[^}]*})|(?P<t_FORM_ID>[^\\r\\n;"\\{]+{)|(?P<t_NUMBER>(?=\\d|\\.\\d)\\d*(\\.\\d*)?([Ee]([+-]?\\d+))?i?)|(?P<t_SECT_SET>(([Dd][Ee][Ff][Aa][Uu][Ll][Tt])|([Ss][Ww][Ii][Tt][Cc][Hh])|([Bb][Uu][Ii][Ll][Tt][Ii][Nn])):)|(?P<t_SECT_PARMS>(([Gg][Rr][Aa][Dd][Ii][Ee][Nn][Tt])|([Ff][Rr][Aa][Cc][Tt][Aa][Ll])|([Ll][Aa][Yy][Ee][Rr])|([Mm][Aa][Pp][Pp][Ii][Nn][Gg])|([Ff][Oo][Rr][Mm][Uu][Ll][Aa])|([Ii][Nn][Ss][Ii][Dd][Ee])|([Oo][Uu][Tt][Ss][Ii][Dd][Ee])|([Aa][Ll][Pp][Hh][Aa])|([Oo][Pp][Aa][Cc][Ii][Tt][Yy])):)|(?P<t_SECT_STM>(([Gg][Ll][Oo][Bb][Aa][Ll])|([Tt][Rr][Aa][Nn][Ss][Ff][Oo][Rr][Mm])|([Ii][Nn][Ii][Tt])|([Ll][Oo][Oo][Pp])|([Ff][Ii][Nn][Aa][Ll])|([Bb][Aa][Ii][Ll][Oo][Uu][Tt]))?:)|(?P<t_ID>[@#]?[a-zA-Z_][a-zA-Z0-9_]*)|(?P<t_ESCAPED_NL>\\\\\\r?\\s*\\n)|(?P<t_COMMENT>;[^\\n]*)|(?P<t_NEWLINE>\\r*\\n)|(?P<t_STRING>"[^"]*")|(?P<t_BOOL_OR>\\|\\|)|(?P<t_RARRAY>\\])|(?P<t_PLUS>\\+)|(?P<t_POWER>\\^)|(?P<t_GTE>>=)|(?P<t_LPAREN>\\()|(?P<t_LTE><=)|(?P<t_TIMES>\\*)|(?P<t_BOOL_AND>&&)|(?P<t_LARRAY>\\[)|(?P<t_NEQ>!=)|(?P<t_MAG>\\|)|(?P<t_RPAREN>\\))|(?P<t_EQ>==)|(?P<t_FORM_END>\\})|(?P<t_LT><)|(?P<t_COMMA>,)|(?P<t_DIVIDE>/)|(?P<t_ASSIGN>=)|(?P<t_MINUS>-)|(?P<t_MOD>%)|(?P<t_BOOL_NEG>!)|(?P<t_GT>>)'
_lextab = [
  None,
  ('t_COMMENT_FORMULA','COMMENT_FORMULA'),
  ('t_FORM_ID','FORM_ID'),
  ('t_NUMBER','NUMBER'),
  None,
  None,
  None,
  ('t_SECT_SET','SECT_SET'),
  None,
  None,
  None,
  None,
  ('t_SECT_PARMS','SECT_PARMS'),
  None,
  None,
  None,
  None,
  None,
  None,
  None,
  None,
  None,
  None,
  ('t_SECT_STM','SECT_STM'),
  None,
  None,
  None,
  None,
  None,
  None,
  None,
  ('t_ID','ID'),
  ('t_ESCAPED_NL','ESCAPED_NL'),
  ('t_COMMENT','COMMENT'),
  ('t_NEWLINE','NEWLINE'),
  ('t_STRING','STRING'),
  (None,'BOOL_OR'),
  (None,'RARRAY'),
  (None,'PLUS'),
  (None,'POWER'),
  (None,'GTE'),
  (None,'LPAREN'),
  (None,'LTE'),
  (None,'TIMES'),
  (None,'BOOL_AND'),
  (None,'LARRAY'),
  (None,'NEQ'),
  (None,'MAG'),
  (None,'RPAREN'),
  (None,'EQ'),
  (None,'FORM_END'),
  (None,'LT'),
  (None,'COMMA'),
  (None,'DIVIDE'),
  (None,'ASSIGN'),
  (None,'MINUS'),
  (None,'MOD'),
  (None,'BOOL_NEG'),
  (None,'GT'),
]
_lextokens = {'FUNC': None, 'CONST': None, 'LPAREN': None, 'BOOL_NEG': None, 'SECT_STM': None, 'NUMBER': None, 'UNTIL': None, 'BOOL_AND': None, 'COMPLEX': None, 'REPEAT': None, 'BOOL_OR': None, 'MINUS': None, 'NEQ': None, 'COMMENT': None, 'RPAREN': None, 'POWER': None, 'NEWLINE': None, 'ENDHEADING': None, 'LT': None, 'RARRAY': None, 'PLUS': None, 'GTE': None, 'COMMA': None, 'STRING': None, 'SECT_PARMS': None, 'FORM_ID': None, 'ASSIGN': None, 'ENDPARAM': None, 'FORM_END': None, 'GT': None, 'DIVIDE': None, 'HEADING': None, 'PARAM': None, 'TIMES': None, 'LARRAY': None, 'LTE': None, 'ENDIF': None, 'ENDFUNC': None, 'ELSE': None, 'EQ': None, 'ID': None, 'IF': None, 'ENDWHILE': None, 'ESCAPED_NL': None, 'TYPE': None, 'WHILE': None, 'MAG': None, 'ELSEIF': None, 'COMMENT_FORMULA': None, 'SECT_SET': None, 'MOD': None}
_lexignore = ' \t\r'
_lexerrorf = 't_error'
