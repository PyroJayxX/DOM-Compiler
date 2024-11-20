##############
# IMPORTS
##############
from string_with_arrows import *
import string

##############
# CONSTANTS
##############
UPPER_LETTERS = string.ascii_uppercase
LOWER_LETTERS = string.ascii_lowercase
ALPHA = string.ascii_letters
ZERO = '0'
DIGIT = '123456789'
NUMERIC = ZERO + DIGIT
ALPHA_NUMERIC = ALPHA + NUMERIC
PUNCTUATION_SYMBOLS = string.punctuation
ASCII = ALPHA_NUMERIC + PUNCTUATION_SYMBOLS + ' '
ARITH_OP = '+-*/%'

delim_map = {
    'adr_delim':        set(ALPHA_NUMERIC + ' '),
    'arith_delim':      set(ALPHA_NUMERIC + ' ' + '-' + '('),
    'assign_delim':     set(ALPHA_NUMERIC + ' ' + '"' + '-' + '(' + '['),
    'bool_delim':       {')', ']', ',', ' '},
    'clsbrace_delim':   set(ALPHA_NUMERIC + '}' + '\n' + ' '),
    'clsparen_delim':   {'+', '-', '*', '/', '%', ')', '{', '}', ',', ']', '\n', ' ', ';', ':'},
    'clssquare_delim':  {'+', '-', '*', '/', '%', '!', '=', '<', '>', ')', ',', '[', ']', '\n', ' '},
    'codeblk_delim':    {'{', ' '},
    'comma_delim':      set(ALPHA_NUMERIC + '"' + "'" + '(' + '[' + '-' + ' '),
    'comp_delim':       set(ALPHA_NUMERIC + '"' + "'" + '(' + '-' + ' '),
    'ident_delim':      {'+', '-', '*', '/', '%', '!', '=', '<', '>', '(', ')', ',', '[', ']', '\n', ' ', ';'},
    'incdec_delim':     set(ALPHA_NUMERIC + ')' + ' '),
    'kword_delim':      {' '},
    'lend_delim':       set(ALPHA_NUMERIC + '#' + '#$' + '\n' + ' '),
    'minus_delim':      set(ALPHA_NUMERIC + '-' + '(' + ' '),
    'num_delim':        set(ARITH_OP + ' ' + ')' + ',' + ';' + ':'),
    'opnbrace_delim':   set(ALPHA_NUMERIC + '\n' + '"' + ' '),
    'opnparen_delim':   set(ALPHA_NUMERIC + '"' + "'" + '-' + '(' + ')' + '\n' + ' '),
    'opnsquare_delim':  set(ALPHA_NUMERIC + '"' + "'" + '-' + '(' + '[' + ']' + ' '),
    'plus_delim':       set(ALPHA_NUMERIC + '"' + "'" + '-' + '(' + ','),
    'para_delim':       {'(', ' ', '\n'},
    'recall_delim':     set(ALPHA + ' ' + ';'), 
    'str_delim':        {'+', ')', ']', '\n', ',', ' '},
    'woogie_delim':     set(NUMERIC + '(' + ' ')
}

keyword_delim_map = {
    'capture':      'para_delim',
    'cleave':       'para_delim',
    'cycle':        'para_delim',
    'domain':       'para_delim',
    'dismantle      ': 'para_delim',
    'vow':          'para_delim',
    'invoke':       'para_delim',
    'splice':       'para_delim',
    'sustain':      'para_delim',
    'curse':        'kword_delim',
    'float':        'kword_delim',
    'int':          'kword_delim',
    'restrict':     'kword_delim',
    'string':       'kword_delim',
    'dismiss':      [' ', ';'],  # Treat dismiss with space or semicolon
    'expansion':    [' ', ';'],
    'hop':          [' ', ';'],
    'null':         [' ', ';'],
    'boogie':       list(delim_map.get('para_delim', set()) | delim_map.get('codeblk_delim', set())),
    'else':         'codeblk_delim',
    'perform':      'codeblk_delim',
    'default':      [' ', ':'],  # Default keyword with space or colon
    'recall':       'recall_delim',
    'woogie':       'woogie_delim'
    }

first_set_map = {
    'fs_program':           {'expansion', '#', '#$'},
    'fs_global_dec':        {'int', 'string', 'float', 'bool', 'curse', 'restrict', '#', '#$', None}, # + id
    'fs_body':              {'int', 'string', 'float', 'bool', 'curse', 'restrict', 'invoke', 'cycle', 'vow', 'while', '#', '#$', None}, # +id
    'fs_local_dec':         {'int', 'string', 'float', 'bool', 'curse', 'restrict', '#', '#$', None}, # + id
    'fs_var_dec':           {'int', 'string', 'float', 'bool', 'restrict'},
    'fs_clan_dec':          {'int', 'string', 'float'},
    'fs_curse_dec':         {'curse'},
    'fs_invoke_stm':        {'invoke'},
    'fs_capture_stm':       {'capture'},
    'fs_conditional_stm':   {'vow'},
    'fs_boogie_woogie_stm': {'boogie'},
    'fs_cycle_loop':        {'cycle'},
    'fs_sustain_loop':      {'sustain'},
    'fs_persustain_loop':   {'perform'},
    'fs_unary_expr':        {'++', '--', '!'},
    'fs_arith_expr':        {'('},
    'fs_relational_expr':   {'len', '('},
    'fs_length':            {'len'},
    'fs_cleave':            {'cleave'},
    'fs_dismantle':         {'dismantle'}
    }

##############
# ERRORS
##############
class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        result += f' File: {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'Invalid Syntax', details)

class RTError(Error):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, 'Runtime Error', details)
        self.context = context

    def as_string(self):
        result = self.generate_traceback()
        result += f'{self.error_name}: {self.details}'
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result
    
    def generate_traceback(self):
        result = ''
        pos = self.pos_start
        ctx = self.context

        while ctx:
            result = f' File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.display_name}\n' + result
            pos = ctx.parent_entry_pos
            ctx = ctx.parent
        
        return 'Traceback (most recent call last):\n' + result

##############
# POSITION
##############

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0
    
    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

#############
# TOKENS
#############

TT_INT      = 'INT'     # Whole Numbers '3'
TT_FLOAT    = 'FLOAT'   # Decimal Numbers '3.14'
TT_STRING   = 'STRING'  # String 

TT_PLUS     = 'PLUS'    # '+'
TT_MINUS    = 'MINUS'   # '-'
TT_MUL      = 'MUL'     # '*'
TT_DIV      = 'DIV'     # '/'
TT_ASSIGN   = 'ASSIGN'  # '='

TT_EQ       = 'EQ'      # '=='  
TT_NE       = 'NE'      # '!='
TT_PLUSEQ   = 'PLUSE'   # '+='  
TT_MINUSEQ  = 'MINUSEQ' # '-='
TT_MULEQ    = 'MULEQ'   # '*='
TT_DIVEQ    = 'DIVEQ'   # '/='

TT_NOT      = 'NOT'     # '!'
TT_AND      = 'AND'     # '&&'
TT_OR       = 'OR'      # '||'
TT_LT       = 'LT'      # '<'
TT_GT       = 'GT'      # '>'
TT_LTE      = 'LTE'     # '<='
TT_GTE      = 'GTE'     # '>='

TT_POW      = 'POW'     # '**'

TT_LPAREN   = 'LPAREN'  # '('
TT_RPAREN   = 'RPAREN'  # ')'
TT_LSQUARE  = 'LSQUARE' # '['
TT_RSQUARE  = 'RSQUARE' # ']'
TT_LBRACE   = 'LBRACE'  # '{'
TT_RBRACE   = 'RBRACE'  # '}'
TT_SEMICOL  = 'SEMICOL' # ';'
TT_COL      = 'COLON'   # ':'
TT_COMMA    = 'COMMA'   # ','

TT_EOF      = 'EOF'     # End of File

TT_KEYWORD  = 'KEYWORD' # Keywords
TT_IDENTIFIER = 'IDENTIFIER' # Identifiers

class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end

    def matches(self, type_, value):
        return self.type == type_ and self.value == value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'
        
class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
        
    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in NUMERIC:
                tok, error = self.make_number()
                if error: return [], error
                tokens.append(tok)
            elif self.current_char in ALPHA:
                tok, error = self.make_identifier()
                if error: return [], error
                tokens.append(tok)
            elif self.current_char == '+':
                tok, error = self.make_plus_equals()
                if error: return [], error
                tokens.append(tok)
            elif self.current_char == '-':
                tok, error = self.make_minus_equals()
                if error: return [], error
                tokens.append(tok)
            elif self.current_char == '*':
                tok, error = self.make_mul_equals()
                if error: return [], error
                tokens.append(tok)
            elif self.current_char == '/':
                tok, error = self.make_div_equals()
                if error: return [], error
                tokens.append(tok)
            elif self.current_char == '!':
                tok, error = self.make_not_equals()
                if error: return [], error
                tokens.append(tok)
            elif self.current_char == '=':
                tok, error = self.make_equals()
                if error: return [], error
                tokens.append(tok)
            elif self.current_char == '<':
                tok, error = self.make_less_than()
                if error: return [], error
                tokens.append(tok)
            elif self.current_char == '>':
                tok, error = self.make_greater_than()
                if error: return [], error
                tokens.append(tok)
            elif self.current_char == '"':
                tok, error = self.make_string()
                if error: return [], error
                tokens.append(tok)
            elif self.current_char == '#':
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '$':
                    self.advance()
                    while self.current_char in ASCII + ' ' + '\t' + '\n':
                        self.advance()
                        if self.current_char == '$':
                            self.advance()
                            if self.current_char == '#':
                                break
                while self.current_char != None and self.current_char in ASCII + ' \t':
                    self.advance()
            elif self.current_char in ' \t\n':  
                self.advance()
            elif self.current_char == '[':
                pos_start = self.pos.copy()
                tokens.append(Token(TT_LSQUARE, pos_start=self.pos))
                self.advance()
                if self.current_char not in delim_map['opnsquare_delim']:
                        return [], IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after brackets")
            elif self.current_char == ']':
                pos_start = self.pos.copy()
                tokens.append(Token(TT_RSQUARE, pos_start=self.pos))
                self.advance()
                if self.current_char not in delim_map['clssquare_delim']:
                        return [], IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after brackets")
            elif self.current_char == '(':
                pos_start = self.pos.copy()
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()
                if self.current_char not in delim_map['opnparen_delim']:
                        return [], IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after parentheses")
            elif self.current_char == ')':
                pos_start = self.pos.copy()
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                self.advance()
                if self.current_char not in delim_map['clsparen_delim']:
                        return [], IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after parentheses")
            elif self.current_char == '{':
                pos_start = self.pos.copy()
                tokens.append(Token(TT_LBRACE, pos_start=self.pos))
                self.advance()
                if self.current_char not in delim_map['opnbrace_delim']:
                        return [], IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after braces")
            elif self.current_char == '}':
                pos_start = self.pos.copy()
                tokens.append(Token(TT_RBRACE, pos_start=self.pos))
                self.advance()
                if self.current_char != None and self.current_char not in delim_map['clsbrace_delim']:
                        return [], IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after braces")
            elif self.current_char == ',':
                pos_start = self.pos.copy()
                tokens.append(Token(TT_COMMA, pos_start=self.pos))
                self.advance()
                if self.current_char not in delim_map['comma_delim']:
                        return [], IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after comma")
            elif self.current_char == ';':
                pos_start = self.pos.copy()
                tokens.append(Token(TT_SEMICOL, pos_start=self.pos)) # WALA PANG DELIMITER SEMICOL
                self.advance()
            elif self.current_char == ':':
                pos_start = self.pos.copy()
                tokens.append(Token(TT_COL, pos_start=self.pos)) # WALA PANG DELIMITER COL
                self.advance()
            elif self.current_char == '&':
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '&':
                    self.advance()
                    if self.current_char not in delim_map['assign_delim']:
                        return [], IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                    tokens.append(Token(TT_AND, pos_start=self.pos))
                else: return [], InvalidSyntaxError(pos_start, self.pos, "'&' is not a valid operator")
            elif self.current_char == '|':
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '|':
                    self.advance()
                    if self.current_char not in delim_map['assign_delim']:
                        return [], IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                    tokens.append(Token(TT_OR, pos_start=self.pos))
                else: return [], InvalidSyntaxError(pos_start, self.pos, "'|' is not a valid operator")
            else: 
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, f"'{char}'")
        
        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None
                

    def make_number(self):
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in NUMERIC + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else: 
                num_str += self.current_char
            self.advance()
        
        if self.current_char not in delim_map['num_delim']:
            return [], IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after number")
            
        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start, self.pos), None
        else:
            return Token(TT_FLOAT, float(num_str), pos_start, self.pos), None

    def make_identifier(self): # For making identifiers/keywords
        id_str = ''
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in ALPHA_NUMERIC + '_':
            id_str += self.current_char
            self.advance()

        tok_type = TT_KEYWORD if id_str in keyword_delim_map else TT_IDENTIFIER

        if tok_type == TT_IDENTIFIER:
             if self.current_char not in delim_map['ident_delim']:
                return [], IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after identifier")
        elif tok_type == TT_KEYWORD:
            delim_type = keyword_delim_map[id_str]
            if isinstance(delim_type, list):  # if it's a list of delimiters from delim map
                valid_delims = delim_type
            else:  # if it's not from delim map
                valid_delims = delim_map.get(delim_type)

            if self.current_char not in valid_delims:
                return [], IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{id_str}'")

        return Token(tok_type, id_str, pos_start, self.pos), None
    
    def make_string(self):
        id_str = ''
        pos_start = self.pos.copy()
        self.advance()

        while self.current_char != None and self.current_char in ASCII + ' ':
            if self.current_char == '"':
                # Closing quote found, break out of the loop
                self.advance() 
                if self.current_char not in delim_map['str_delim']:
                    return [], IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after string '{id_str}'")
                return Token(TT_STRING, id_str, pos_start, self.pos), None
            id_str += self.current_char
            self.advance()

        return None, InvalidSyntaxError(pos_start, self.pos, 'String not properly closed with double quotes (")')
    
    def make_plus_equals(self):
        tok_type = TT_PLUS
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_PLUSEQ

        if self.current_char not in delim_map['assign_delim']:
            return [], IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
        
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos), None

    def make_minus_equals(self):
        tok_type = TT_MINUS
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_MINUSEQ
        
        if self.current_char not in delim_map['assign_delim']:
            return [], IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
        
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos), None

    def make_mul_equals(self):
        tok_type = TT_MUL
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_MULEQ
            if self.current_char not in delim_map['assign_delim']:
                return [], IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
        
        if self.current_char == '*':
            self.advance()
            tok_type = TT_POW
            if self.current_char not in delim_map['arith_delim']:
                return [], IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
        
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos), None

    def make_div_equals(self):
        tok_type = TT_DIV
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_DIVEQ
            if self.current_char not in delim_map['comp_delim']:
                return [], IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
        
        if self.current_char not in delim_map['assign_delim']:
            return [], IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
        
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos), None

    def make_not_equals(self):
        tok_type = TT_NOT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_NE
            if self.current_char not in delim_map['comp_delim']:
                return [], IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
        
        if self.current_char not in delim_map['assign_delim']:
            return [], IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
        
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos), None
    
    def make_equals(self):
        tok_type = TT_ASSIGN
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_EQ
            if self.current_char not in delim_map['comp_delim']:
                return [], IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
        
        if self.current_char not in delim_map['assign_delim']:
            return [], IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
        
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos), None
    
    def make_less_than(self):
        tok_type = TT_LT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_LTE

        if self.current_char not in delim_map['comp_delim']:
            return [], IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
        
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos), None

    def make_greater_than(self):
        tok_type = TT_GT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_GTE
        
        if self.current_char not in delim_map['comp_delim']:
            return [], IllegalCharError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
        
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos), None
    
def run(fn, text):
        # Generate tokens
        lexer = Lexer(fn, text)
        tokens, error = lexer.make_tokens()
        if error: return None, error

        return tokens, error