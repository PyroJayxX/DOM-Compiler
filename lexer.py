##############
# IMPORTS
##############
from string_with_arrows import *
import string

############## 
# CONSTANTS - From the Regular definition from docu. 
##############
UPPER_LETTERS = string.ascii_uppercase
LOWER_LETTERS = string.ascii_lowercase
ALPHA = string.ascii_letters
ZERO = '0'
DIGIT = '123456789'
NUMERIC = ZERO + DIGIT
ALPHA_NUMERIC = ALPHA + NUMERIC
PUNCTUATION_SYMBOLS = string.punctuation
ASCII = ALPHA_NUMERIC + PUNCTUATION_SYMBOLS + ' \t'
ARITH_OP = '+-*/%='
RELATION_OP = '<>!&|'
ALL_OPERATOR = ARITH_OP + RELATION_OP


# FROM THE DELIMITERS 
delim_map = {
    'adr_delim':        set(ALPHA_NUMERIC + ' '),
    'arith_delim':      set(ALPHA_NUMERIC + ' ' + '-' + '('),
    'assign_delim':     set(ALPHA_NUMERIC + ' ' + '"' + '-' + '(' + ')' + '[' + '\n'),
    'boogie_delim':     {'(', ' ', '\n', '{'},
    'bool_delim':       {')', ']', ',', ' '},
    'clsbrace_delim':   set(ALPHA_NUMERIC + '}' + '\n' + '\t' + ' ' + ';'),
    'clsparen_delim':   {'+', '-', '*', '/', '%', ')', '{', '}', ',', ']', '\n', ' ', ';', ':', '&', '|'},
    'clssquare_delim':  {'+', '-', '*', '/', '%', ' !', '=', '<', '>', ')', ',', '[', ']', '\n', ' ', ';'},
    'codeblk_delim':    {'{', ' '},
    'col_delim':        set(ALPHA + '\n' + '\t' + ' '),
    'comma_delim':      set(ALPHA_NUMERIC + '"' + "'" + '(' + '[' + '-' + ' '),
    'comp_delim':       set(ALPHA_NUMERIC + '"' + "'" + '(' + '-' + ' '),
    'default_delim':    {' ', ':'},
    'ex_delim':         {' ', ';', '\n','\t'},
    'ident_delim':      {'+', '-', '*', '/', '%', '!', '=', '<', '>', '(', ')', ',', '[', ']', '\n', ' ', ';', '&', '|'},
    'incdec_delim':     set(ALPHA_NUMERIC + ')' + ' ' + ';'),
    'kword_delim':      {' ', '\t'},
    'lend_delim':       set(ALPHA_NUMERIC + '#' + '#$' + '\n' + '\t' + ' ' + '}'),
    'logic_delim':      set(ALPHA + ' '),
    'minus_delim':      set(ALPHA_NUMERIC + '-' + '(' + ' '),
    'num_delim':        set(ARITH_OP + ' ' + ')' + ',' + ';' + ':' + ']' + '}'),
    'opnbrace_delim':   set(ALPHA_NUMERIC + '\n' + '"' + ' '),
    'opnparen_delim':   set(ALPHA_NUMERIC + '"' + "'" + '-' + '(' + ')' + '\n' + ' '),
    'opnsquare_delim':  set(ALPHA_NUMERIC + '"' + "'" + '-' + '(' + '[' + ']' + ' '),
    'plus_delim':       set(ALPHA_NUMERIC + '"' + "'" + '-' + '(' + ',' + ' '),
    'para_delim':       {'(', ' ', '\n'},
    'recall_delim':     set(ALPHA + ' ' + ';'), 
    'str_delim':        {'+', ')', ']', '\n', ',', ';', ' ', ':'},
    'white_delim':      set(ASCII + ALL_OPERATOR + ' ' + '\n' + '\t' + '\0'),
    'woogie_delim':     set(NUMERIC + '(' + ' ')
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
        result += f'\nFile: {self.pos_start.fn}, line {self.pos_start.ln + 1}\n'
        result += string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end) + '\n'
        return result

class LexicalError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Lexical Error', details)

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
            
        return self
    
    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

#############
# TOKENS
#############

TT_INT      = 'INT'     # Whole Numbers '3'
TT_FLOAT    = 'FLOAT'   # Decimal Numbers '3.14'
TT_STRING   = 'STRING'  # Strings 

TT_PLUS     = 'PLUS'    # '+'
TT_MINUS    = 'MINUS'   # '-'
TT_MUL      = 'MUL'     # '*'
TT_DIV      = 'DIV'     # '/'
TT_MOD      = 'MODULO'  # '%'
TT_ASSIGN   = 'ASSIGN'  # '='

TT_EQ       = 'EQ'      # '=='  
TT_NE       = 'NE'      # '!='
TT_PLUSEQ   = 'PLUSEQ'   # '+='  
TT_MINUSEQ  = 'MINUSEQ' # '-='
TT_MULEQ    = 'MULEQ'   # '*='
TT_DIVEQ    = 'DIVEQ'   # '/='
TT_MODEQ    = 'MODEQ'   # '%='

TT_NOT      = 'NOT'     # '!'
TT_AND      = 'AND'     # '&&'
TT_OR       = 'OR'      # '||'
TT_LT       = 'LT'      # '<'
TT_GT       = 'GT'      # '>'
TT_LTE      = 'LTE'     # '<='
TT_GTE      = 'GTE'     # '>='

TT_POW      = 'POW'     # '**'
TT_UNARY    = 'UNARY'   # '++', '--'

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

        while self.current_char is not None:
            if self.current_char in ' \t\n':
                self.advance()
                if self.current_char not in delim_map['white_delim']:
                    return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after space, newline, or tab'")

            elif self.current_char in ALPHA:
                ident_str = ''
                ident_count = 0
                pos_start = self.pos.copy()

                if self.current_char == 'b':
                    ident_str += self.current_char
                    ident_count+=1
                    self.advance()
                    if self.current_char == 'o':
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()
                        if self.current_char == 'o':
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()
                            if self.current_char == 'g':
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()
                                if self.current_char == 'i':
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()
                                    if self.current_char == 'e':
                                        ident_str += self.current_char
                                        ident_count+=1
                                        self.advance()
                                        if self.current_char not in delim_map['boogie_delim']:
                                            return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                                            continue
                                        tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                        continue
                            if self.current_char == 'l':
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()
                                if self.current_char not in delim_map['kword_delim']:
                                    return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                                    continue
                                tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                continue 
                elif self.current_char == "c":
                    ident_str += self.current_char
                    ident_count+=1
                    self.advance()
                    if self.current_char == "a":
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()
                        if self.current_char == "p":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()
                            if self.current_char == "t":
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()  
                                if self.current_char == "u":
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance() 
                                    if self.current_char == "r":
                                        ident_str += self.current_char
                                        ident_count+=1
                                        self.advance()  
                                        if self.current_char == "e":
                                            ident_str += self.current_char
                                            ident_count+=1
                                            self.advance() 
                                            if self.current_char not in delim_map['para_delim']:
                                                return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                                            tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                            continue 
                    if self.current_char == "l":
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance() 
                        if self.current_char == "e":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance() 
                            if self.current_char == "a":
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance() 
                                if self.current_char == "v":
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance() 
                                    if self.current_char == "e":
                                        ident_str += self.current_char
                                        ident_count+=1
                                        self.advance() 
                                        if self.current_char not in delim_map['para_delim']:
                                            return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                                        tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                        continue
                    if self.current_char == "u":
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance() 
                        if self.current_char == "r":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance() 
                            if self.current_char == "s":
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance() 
                                if self.current_char == "e":
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()
                                    if self.current_char not in delim_map['white_delim']:
                                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                                    tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos)) 
                                    continue
                    if self.current_char == "y":
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance() 
                        if self.current_char == "c":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance() 
                            if self.current_char == "l":
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance() 
                                if self.current_char == "e":    
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance() 
                                    if self.current_char not in delim_map['para_delim']:
                                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                                    tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                    continue
                elif self.current_char == "d":
                    ident_str += self.current_char
                    ident_count+=1
                    self.advance() 
                    if self.current_char == "e":
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance() 
                        if self.current_char == "f":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char == "a":
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()   
                                if self.current_char == "u":
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()  
                                    if self.current_char == "l":
                                        ident_str += self.current_char
                                        ident_count+=1
                                        self.advance()  
                                        if self.current_char == "t":
                                            ident_str += self.current_char
                                            ident_count+=1
                                            self.advance()  
                                            if self.current_char not in delim_map['default_delim']:
                                                return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                                            tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                            continue
                    if self.current_char == "i":
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()  
                        if self.current_char == "s":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char == "m":
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()  
                                if self.current_char == "a":
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()  
                                    if self.current_char == "n":
                                        ident_str += self.current_char
                                        ident_count+=1
                                        self.advance()  
                                        if self.current_char == "t":
                                            ident_str += self.current_char
                                            ident_count+=1
                                            self.advance()  
                                            if self.current_char == "l":
                                                ident_str += self.current_char
                                                ident_count+=1
                                                self.advance()  
                                                if self.current_char == "e":
                                                    ident_str += self.current_char
                                                    ident_count+=1
                                                    self.advance()  
                                                    if self.current_char not in delim_map['para_delim']:
                                                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                                                    tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                                    continue
                                if self.current_char == "i":
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()
                                    if self.current_char == "m":
                                        ident_str += self.current_char
                                        ident_count+=1
                                        self.advance()  
                                        if self.current_char == "i":
                                            ident_str += self.current_char
                                            ident_count+=1
                                            self.advance()  
                                            if self.current_char == "s":
                                                ident_str += self.current_char
                                                ident_count+=1
                                                self.advance()  
                                                if self.current_char == "s":
                                                    ident_str += self.current_char
                                                    ident_count+=1
                                                    self.advance()
                                                    if self.current_char not in delim_map['ex_delim']:
                                                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                                                    tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                                    continue
                    if self.current_char == "o":
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()      
                        if self.current_char == "m":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char == "a":
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()  
                                if self.current_char == "i":
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()  
                                    if self.current_char == "n":
                                        ident_str += self.current_char
                                        ident_count+=1
                                        self.advance()  
                                        if self.current_char not in delim_map['para_delim']:
                                            return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                                        tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                        continue
            
                elif self.current_char == "e":
                    ident_str += self.current_char
                    ident_count+=1
                    self.advance()  
                    if self.current_char == "l":
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()  
                        if self.current_char == "s":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char == "e":
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()
                                if self.current_char not in delim_map['codeblk_delim']:
                                    return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                                tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                continue
                                
                    if self.current_char == "x":
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()  
                        if self.current_char == "p":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char == "a":
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()  
                                if self.current_char == "n":
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()  
                                    if self.current_char == "s":
                                        ident_str += self.current_char
                                        ident_count+=1
                                        self.advance()  
                                        if self.current_char == "i":
                                            ident_str += self.current_char
                                            ident_count+=1
                                            self.advance()  
                                            if self.current_char == "o":
                                                ident_str += self.current_char
                                                ident_count+=1
                                                self.advance()  
                                                if self.current_char == "n":
                                                    ident_str += self.current_char
                                                    ident_count+=1
                                                    self.advance()  
                                                    if self.current_char not in delim_map['ex_delim']:
                                                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                                                    tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                                    continue
                
                elif self.current_char == "f":
                    ident_str += self.current_char
                    ident_count+=1
                    self.advance() 
                    if self.current_char == "a":
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance() 
                        if self.current_char == "l":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance() 
                            if self.current_char == "s":
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()    
                                if self.current_char == "e":
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()  
                                    if self.current_char not in delim_map['bool_delim']:
                                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                                    tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                    continue
                    if self.current_char == "l":
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()  
                        if self.current_char == "o":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char == "a":
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()  
                                if self.current_char == "t":
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()  
                                    if self.current_char not in delim_map['kword_delim']:
                                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                                    tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                    continue

                elif self.current_char == "h":
                    ident_str += self.current_char
                    ident_count+=1
                    self.advance()  
                    if self.current_char == "o":
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()  
                        if self.current_char == "p":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char not in delim_map['ex_delim']:
                                return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                            tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                            continue
                
                elif self.current_char == "i":
                    ident_str += self.current_char
                    ident_count+=1
                    self.advance()  
                    if self.current_char == "n":
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()  
                        if self.current_char == "v":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char == "o":
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()  
                                if self.current_char == "k":
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()  
                                    if self.current_char == "e":
                                        ident_str += self.current_char
                                        ident_count+=1
                                        self.advance()  
                                        if self.current_char not in delim_map['para_delim']:
                                            return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                                        tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                        continue
                        if self.current_char == "t":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char not in delim_map['kword_delim']:
                                return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                            tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                            continue
                
                elif self.current_char == "l":
                    ident_str += self.current_char
                    ident_count+=1
                    self.advance()  
                    if self.current_char == "e":
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()  
                        if self.current_char == "n":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char not in delim_map['para_delim']:
                                return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                            tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                            continue

                elif self.current_char == "n":
                    ident_str += self.current_char
                    ident_count+=1
                    self.advance()  
                    if self.current_char == "u":
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()  
                        if self.current_char == "l":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char == "l":
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()  
                                if self.current_char not in delim_map['white_delim']:
                                    return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                                tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                continue
                                
                elif self.current_char == "p":
                    ident_str += self.current_char
                    ident_count+=1
                    self.advance()  
                    if self.current_char == "e":
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()  
                        if self.current_char == "r":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char == "f":
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()  
                                if self.current_char == "o":
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()  
                                    if self.current_char == "r":
                                        ident_str += self.current_char
                                        ident_count+=1
                                        self.advance()  
                                        if self.current_char == "m":
                                            ident_str += self.current_char
                                            ident_count+=1
                                            self.advance()  
                                            if self.current_char not in delim_map['codeblk_delim']:
                                                return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                                            tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                            continue
                                    
                elif self.current_char == "r":
                    ident_str += self.current_char
                    ident_count+=1
                    self.advance()  
                    if self.current_char == "e":
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()  
                        if self.current_char == "c":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char == "a":
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()  
                                if self.current_char == "l":
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()  
                                    if self.current_char == "l":
                                        ident_str += self.current_char
                                        ident_count+=1
                                        self.advance()  
                                        if self.current_char not in delim_map['recall_delim']:
                                            return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                                        tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                        continue
                        if self.current_char == "s":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char == "t":
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()  
                                if self.current_char == "r":
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()  
                                    if self.current_char == "i":
                                        ident_str += self.current_char
                                        ident_count+=1
                                        self.advance()  
                                        if self.current_char == "c":
                                            ident_str += self.current_char
                                            ident_count+=1
                                            self.advance()  
                                            if self.current_char == "t":
                                                ident_str += self.current_char
                                                ident_count+=1
                                                self.advance()  
                                                if self.current_char not in delim_map['kword_delim']:
                                                    return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                                                tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                                continue

                elif self.current_char == "s":
                    ident_str += self.current_char
                    ident_count+=1
                    self.advance()  
                    if self.current_char == "t":
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()  
                        if self.current_char == "r":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char == "i":
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()  
                                if self.current_char == "n":
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()  
                                    if self.current_char == "g":
                                        ident_str += self.current_char
                                        ident_count+=1
                                        self.advance()  
                                        if self.current_char not in delim_map['kword_delim']:
                                            return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                                        tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                        continue
                    if self.current_char == "u":
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()  
                        if self.current_char == "s":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char == "t":
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()  
                                if self.current_char == "a":
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()  
                                    if self.current_char == "i":
                                        ident_str += self.current_char
                                        ident_count+=1
                                        self.advance()  
                                        if self.current_char == "n":
                                            ident_str += self.current_char
                                            ident_count+=1
                                            self.advance()  
                                            if self.current_char not in delim_map['para_delim']:
                                                return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                                            tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                            continue

                elif self.current_char == "t":
                    ident_str += self.current_char
                    ident_count+=1
                    self.advance()  
                    if self.current_char == "r":
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()  
                        if self.current_char == "u":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char == "e":
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()  
                                if self.current_char not in delim_map['bool_delim']:
                                    return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                                tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                continue

                elif self.current_char == "v":
                    ident_str += self.current_char
                    ident_count+=1
                    self.advance()  
                    if self.current_char == "o":
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()  
                        if self.current_char == "w":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char not in delim_map['para_delim']:
                                return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                            tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                            continue

                elif self.current_char == "w":
                    ident_str += self.current_char
                    ident_count+=1
                    self.advance()  
                    if self.current_char == "o":
                        ident_str += self.current_char
                        ident_count+=1
                        self.advance()  
                        if self.current_char == "o":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char == "g":
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()  
                                if self.current_char == "i":
                                    ident_str += self.current_char
                                    ident_count+=1
                                    self.advance()  
                                    if self.current_char == "e":
                                        ident_str += self.current_char
                                        ident_count+=1
                                        self.advance()  
                                        if self.current_char not in delim_map['woogie_delim']:
                                            return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'")
                                        tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                        continue
                 
                while self.current_char != None and self.current_char in ALPHA_NUMERIC + '_':
                    ident_str+=self.current_char
                    ident_count+=1
                    self.advance()
                if self.current_char not in delim_map['ident_delim']:
                    return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after identifier '{ident_str}'")
                if ident_count>25:
                    return tokens, LexicalError(pos_start, self.pos, "Identifier exceeded maximum character limit of 25")
                tokens.append(Token(TT_IDENTIFIER, ident_str, pos_start=pos_start, pos_end=self.pos)) 


            elif self.current_char == '"':
                tok, error = self.make_string()
                if error: return tokens, error
                tokens.append(tok)


            elif self.current_char == '=':
                tok_type = TT_ASSIGN
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    tok_type = TT_EQ

                if tok_type == TT_ASSIGN:
                    if self.current_char not in delim_map['assign_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                if tok_type == TT_EQ:
                    if self.current_char not in delim_map['comp_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                tokens.append(Token(tok_type, pos_start=pos_start, pos_end=self.pos))


            elif self.current_char == '+':
                tok_type = TT_PLUS
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '+':        
                    self.advance()
                    tok_type = TT_UNARY
                if self.current_char == '=':        
                    self.advance()
                    tok_type = TT_PLUSEQ

                if tok_type == TT_PLUS:
                    if self.current_char not in delim_map['plus_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                    tokens.append(Token(tok_type, pos_start=pos_start, pos_end=self.pos))
                if tok_type == TT_UNARY:
                    if self.current_char not in delim_map['incdec_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                    tokens.append(Token(tok_type, '++', pos_start=pos_start, pos_end=self.pos))
                if tok_type == TT_PLUSEQ:
                    if self.current_char not in delim_map['assign_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                    tokens.append(Token(tok_type, pos_start=pos_start, pos_end=self.pos))
        
                

            elif self.current_char == '-': 
                pos_start = self.pos.copy()
                self.advance()

                # Check if this is a decrement operator (--), assignment operator (-=), or standalone '-'
                if self.current_char == '-':
                    self.advance()
                    tok_type = TT_UNARY  # Decrement (-- operator)
                    if self.current_char not in delim_map['incdec_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                    tokens.append(Token(tok_type, '--', pos_start=pos_start, pos_end=self.pos))

                elif self.current_char == '=':
                    self.advance()
                    tok_type = TT_MINUSEQ  # -= operator
                    if self.current_char not in delim_map['assign_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                    tokens.append(Token(tok_type, pos_start=pos_start, pos_end=self.pos))
                    
                else:
                    # Determine if this is unary or binary minus
                    if len(tokens) > 0 and tokens[-1].type in [TT_INT, TT_FLOAT, TT_IDENTIFIER, TT_RPAREN]:
                        # If the last token is a number, identifier, or closing parenthesis, treat as binary minus
                        tokens.append(Token(TT_MINUS, pos_start=pos_start, pos_end=self.pos))
                    else:
                        # Otherwise, treat as unary minus
                        if self.current_char in NUMERIC:
                            # Make a negative number token
                            tok, error = self.make_number(is_negative=True)
                            if error: return tokens, error
                            tokens.append(tok)
                        else:
                            return tokens, LexicalError(pos_start, self.pos, f"Unexpected '-' without a valid number or identifier.")

            
            elif self.current_char in NUMERIC:
                tok, error = self.make_number()     # function for making integer and float tokens
                if error: return tokens, error
                tokens.append(tok)

        
            elif self.current_char == '*':
                tok_type = TT_MUL
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '*':
                    self.advance()
                    tok_type = TT_POW
                if self.current_char == '=':
                    self.advance()
                    tok_type = TT_MULEQ

                if tok_type == TT_MUL:
                    if self.current_char not in delim_map['arith_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                if tok_type == TT_POW:
                    if self.current_char not in delim_map['arith_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                if tok_type == TT_MULEQ:
                    if self.current_char not in delim_map['assign_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")   
                tokens.append(Token(tok_type, pos_start=pos_start, pos_end=self.pos))


            elif self.current_char == '/':
                tok_type = TT_DIV
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    tok_type = TT_DIVEQ

                if tok_type == TT_DIV:
                    if self.current_char not in delim_map['arith_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                if tok_type == TT_DIVEQ:
                    if self.current_char not in delim_map['assign_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                tokens.append(Token(tok_type, pos_start=pos_start, pos_end=self.pos))


            elif self.current_char == '%':
                tok_type = TT_MOD
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    tok_type = TT_MODEQ

                if tok_type == TT_DIV:
                    if self.current_char not in delim_map['arith_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                if tok_type == TT_MODEQ:
                    if self.current_char not in delim_map['assign_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                tokens.append(Token(tok_type, pos_start=pos_start, pos_end=self.pos))
            

            elif self.current_char == '!':
                tok_type = TT_NOT
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    tok_type = TT_NE

                if tok_type == TT_NOT:
                    if self.current_char not in delim_map['logic_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                if tok_type == TT_NE:
                    if self.current_char not in delim_map['assign_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                tokens.append(Token(tok_type, pos_start=pos_start, pos_end=self.pos))


            elif self.current_char == '<':
                tok_type = TT_LT
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    tok_type = TT_LTE

                if tok_type == TT_LT:
                    if self.current_char not in delim_map['comp_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                if tok_type == TT_LTE:
                    if self.current_char not in delim_map['comp_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                tokens.append(Token(tok_type, pos_start=pos_start, pos_end=self.pos))


            elif self.current_char == '>':
                tok_type = TT_GT
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    tok_type = TT_GTE

                if tok_type == TT_GT:
                    if self.current_char not in delim_map['comp_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                if tok_type == TT_GTE:
                    if self.current_char not in delim_map['comp_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                tokens.append(Token(tok_type, pos_start=pos_start, pos_end=self.pos))


            elif self.current_char == '&':
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '&':
                    self.advance()
                    if self.current_char not in delim_map['logic_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                    tokens.append(Token(TT_AND, pos_start=self.pos))
                else: return tokens, InvalidSyntaxError(pos_start, self.pos, "'&' is not a valid operator")


            elif self.current_char == '|':
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '|':
                    self.advance()
                    if self.current_char not in delim_map['logic_delim']:
                        return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator")
                    tokens.append(Token(TT_OR, pos_start=self.pos))
                else: return tokens, InvalidSyntaxError(pos_start, self.pos, "'|' is not a valid operator")
    

            elif self.current_char == '(':
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char not in delim_map['opnparen_delim']:
                    return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after parentheses")
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))


            elif self.current_char == ')':
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char not in delim_map['clsparen_delim']:
                    return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after parentheses")
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))


            elif self.current_char == '[':
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char not in delim_map['opnsquare_delim']:
                    return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after brackets")
                tokens.append(Token(TT_LSQUARE, pos_start=self.pos))


            elif self.current_char == ']':
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char not in delim_map['clssquare_delim']:
                    return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after brackets")
                tokens.append(Token(TT_RSQUARE, pos_start=self.pos))


            elif self.current_char == '{':
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char not in delim_map['opnbrace_delim']:
                    return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after braces")
                tokens.append(Token(TT_LBRACE, pos_start=self.pos))


            elif self.current_char == '}':
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char != None and self.current_char not in delim_map['clsbrace_delim']:
                    return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after braces")
                tokens.append(Token(TT_RBRACE, pos_start=self.pos))


            elif self.current_char == ',':
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char not in delim_map['comma_delim']:
                    return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after comma")
                tokens.append(Token(TT_COMMA, pos_start=self.pos))


            elif self.current_char == ':':
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char not in delim_map['col_delim']:
                    return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after colon")
                tokens.append(Token(TT_COL, pos_start=self.pos))


            elif self.current_char == ';':
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char != None and self.current_char not in delim_map['lend_delim']:
                    return tokens, LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after semicolon")
                tokens.append(Token(TT_SEMICOL, pos_start=self.pos))


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

            else: 
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                self.errors.append(LexicalError(pos_start, self.pos, f"Invalid Character '{char}'"))
        
        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None
                

    def make_number(self, is_negative=False):  # for making numbers: int and float
        num_str = ''
        num_count = 0
        dec_count = 0
        dot_count = 0
        pos_start = self.pos.copy()

        if is_negative:  # Prepend '-' to handle negative numbers
            num_str = '-'

        while self.current_char != None and self.current_char in NUMERIC + '.':
            if self.current_char == '.':
                self.advance()
                if self.current_char == '.':
                    pos_end = self.pos.copy()
                    return [], LexicalError(pos_start, pos_end, f"Multiple period '.' in a float assignment")
                elif self.current_char == None or self.current_char not in NUMERIC:
                    pos_end = self.pos.copy()  
                    return [], LexicalError(pos_start, pos_end, "Incomplete float assignment")
                dot_count += 1
                num_str += '.'
            else:
                if dot_count == 0:
                    num_count += 1
                if dot_count == 1:
                    dec_count += 1
                if num_count > 9:
                    pos_end = self.pos.copy()
                    return [], LexicalError(pos_start, pos_end, "Whole number exceeded maximum character limit of 17")
                if dot_count == 1 and dec_count > 7:
                    self.advance()
                else:
                    num_str += self.current_char
                    self.advance()

        if self.current_char not in delim_map['num_delim']:
            pos_end = self.pos.copy()
            return [], LexicalError(pos_start, pos_end, f"Invalid delimiter '{self.current_char}' after number")

        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start, self.pos), None
        else:
            return Token(TT_FLOAT, float(num_str), pos_start, self.pos), None

    
def run(fn, text):
        # Generate tokens
        lexer = Lexer(fn, text)
        tokens, error = lexer.make_tokens()
        return tokens, error