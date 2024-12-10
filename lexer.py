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

keywords = [
    "domain", "expansion", "null", "int", "float", "string", "bool", 
    "restrict", "invoke", "capture", "true", "false", 
    "vow", "else vow", "else", "boogie", "woogie", 
    "default", "cycle", "sustain", "perform", 
    "dismiss", "hop", "recall", "cleave", 
    "dismantle", "len", "curse"
]

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
    'str_delim':        {'+', ')', ']', '\n', ',', ';', ' ', ':', '}'},
    'white_delim':      set(ASCII + ALL_OPERATOR + ' ' + '\n' + '\t' + '\0'),
    'woogie_delim':     set(NUMERIC + '(' + ' ')
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
TT_SPACE    = 'SPACE'   # Space ' '
TT_TAB      = 'TAB'     # Newline '\n'
TT_NEWLINE  = 'NEWLINE' # Tab '\t'


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
        if self.value: return f'{self.type}: {self.value}'
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
        errors = []

        while self.current_char is not None:
            
            if self.current_char in ALPHA:
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
                                        if self.current_char in delim_map['boogie_delim']:
                                            tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                            continue
                                        elif self.current_char not in delim_map['boogie_delim'] and self.current_char in ALPHA + '_':
                                            pass
                                        else: 
                                            errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'"))
                            if self.current_char == 'l':
                                ident_str += self.current_char
                                ident_count+=1
                                self.advance()
                                if self.current_char in delim_map['kword_delim']:
                                    tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                    continue 
                                elif self.current_char not in delim_map['kword_delim'] and self.current_char in ALPHA + '_':
                                    pass
                                else:
                                    errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'"))
                
                                
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
                                            if self.current_char in delim_map['para_delim']:
                                                tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                                continue 
                                            elif self.current_char not in delim_map['para_delim'] and self.current_char in ALPHA + '_':
                                                pass
                                            else:
                                                errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'"))
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
                                        if self.current_char in delim_map['para_delim']:
                                            tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                            continue
                                        elif self.current_char not in delim_map['para_delim'] and self.current_char in ALPHA + '_':
                                            pass
                                        else:
                                            errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'"))
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
                                    if self.current_char in delim_map['white_delim']:
                                        tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos)) 
                                        continue
                                    if self.current_char not in delim_map['white_delim'] and self.current_char in ALPHA + '_':
                                        pass
                                    else:
                                        errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'"))
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
                                    if self.current_char in delim_map['para_delim']:
                                        tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                        continue 
                                    if self.current_char not in delim_map['para_delim'] and self.current_char in ALPHA + '_':
                                        pass
                                    else:
                                        errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'"))
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
                                            if self.current_char in delim_map['default_delim']:
                                                tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                                continue
                                            elif self.current_char not in delim_map['default_delim'] and self.current_char in ALPHA + '_':
                                                pass
                                            else:
                                                errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'"))
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
                                                    if self.current_char in delim_map['para_delim']:
                                                        tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                                        continue
                                                    elif self.current_char not in delim_map['para_delim'] and self.current_char in ALPHA + '_':
                                                        pass
                                                    else:
                                                        errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'"))
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
                                                        tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                                        continue
                                                    elif self.current_char not in delim_map['ex_delim'] and self.current_char in ALPHA + '_':
                                                        pass
                                                    else:
                                                        errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'"))
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
                                        if self.current_char in delim_map['para_delim']:
                                            tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                            continue
                                        elif self.current_char not in delim_map['para_delim'] and self.current_char in ALPHA + '_':
                                            pass
                                        else:
                                            errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'"))
            
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
                                if self.current_char in delim_map['codeblk_delim']: 
                                    tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                    continue
                                elif self.current_char not in delim_map['codeblk_delim'] and self.current_char in ALPHA + '_':
                                    pass
                                else:
                                    errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'"))
                                
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
                                                    if self.current_char in delim_map['ex_delim']:
                                                        tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                                        continue
                                                    elif self.current_char not in delim_map['ex_delim'] and self.current_char in ALPHA + '_':
                                                        pass
                                                    else:
                                                        errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'"))
                
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
                                    if self.current_char in delim_map['bool_delim']:
                                        tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                        continue
                                    elif self.current_char not in delim_map['bool_delim'] and self.current_char in ALPHA + '_':
                                        pass
                                    else:
                                        errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'"))
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
                                    if self.current_char in delim_map['kword_delim']:
                                        tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                        continue
                                    elif self.current_char not in delim_map['kword_delim'] and self.current_char in ALPHA + '_':
                                        pass
                                    else:
                                        errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'"))

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
                            if self.current_char in delim_map['ex_delim']: 
                                tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                continue
                            elif self.current_char not in delim_map['ex_delim'] and self.current_char in ALPHA + '_':
                                pass
                            else:
                                errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'"))
                
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
                                        if self.current_char in delim_map['para_delim']:
                                            tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                            continue
                                        elif self.current_char not in delim_map['para_delim'] and self.current_char in ALPHA + '_':
                                            pass
                                        else:
                                            errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'"))
                        if self.current_char == "t":
                            ident_str += self.current_char
                            ident_count+=1
                            self.advance()  
                            if self.current_char in delim_map['kword_delim']:
                                tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                continue
                            elif self.current_char not in delim_map['kword_delim'] and self.current_char in ALPHA + '_':
                                pass
                            else: 
                                errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'"))
                
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
                            if self.current_char in delim_map['para_delim']:
                                tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                continue
                            elif self.current_char not in delim_map['para_delim'] and self.current_char in ALPHA + '_':
                                pass
                            else: 
                                errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'"))

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
                                if self.current_char in delim_map['white_delim']:
                                    tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                    continue
                                elif self.current_char not in delim_map['white_delim'] and self.current_char in ALPHA + '_':
                                    pass
                                else:
                                    errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'"))
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
                                            if self.current_char in delim_map['codeblk_delim']:
                                                tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                                continue
                                            elif self.current_char not in delim_map['codeblk_delim'] and self.current_char in ALPHA + '_':
                                                pass
                                            else:
                                                errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'"))
                                    
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
                                        if self.current_char in delim_map['recall_delim']:
                                            tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                            continue
                                        elif self.current_char not in delim_map['recall_delim'] and self.current_char in ALPHA + '_':
                                            pass
                                        else:
                                            errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'"))
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
                                                if self.current_char in delim_map['kword_delim']:
                                                    tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                                    continue
                                                elif self.current_char not in delim_map['kword_delim']:
                                                    pass
                                                else:
                                                    errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'"))

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
                                        if self.current_char in delim_map['kword_delim']:
                                            tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                            continue
                                        elif self.current_char not in delim_map['kword_delim'] and self.current_char in ALPHA + '_':
                                            pass
                                        else:
                                            errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'"))
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
                                            if self.current_char in delim_map['para_delim']:
                                                tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                                continue
                                            elif self.current_char not in delim_map['para_delim'] and self.current_char in ALPHA + '_':
                                                pass
                                            else:
                                                errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'"))

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
                                if self.current_char in delim_map['bool_delim']:
                                    tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                    continue
                                elif self.current_char not in delim_map['bool_delim'] and self.current_char in ALPHA + '_':
                                    pass
                                else:
                                    errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'"))

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
                            if self.current_char in delim_map['para_delim']:
                                tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                continue
                            elif self.current_char not in delim_map['para_delim'] and self.current_char in ALPHA + '_':
                                pass
                            else:
                                errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'"))

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
                                        if self.current_char in delim_map['woogie_delim']:
                                            tokens.append(Token(TT_KEYWORD, ident_str, pos_start=pos_start, pos_end=self.pos))
                                            continue
                                        elif self.current_char not in delim_map['woogie_delim'] and self.current_char in ALPHA + '_':
                                            pass
                                        else: 
                                            errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after keyword '{ident_str}'"))
                 
                while self.current_char != None and self.current_char in ALPHA_NUMERIC + '_':
                    ident_str+=self.current_char
                    ident_count+=1
                    self.advance()
                    pos_end = self.pos.copy()
                ident_lower = ident_str.lower()
                if ident_lower in keywords:
                    errors.append(LexicalError(pos_start, pos_end, f"Keyword '{ident_str}' cannot be used as identifiers regardless of letter-casing"))
                if self.current_char not in delim_map['ident_delim']:
                    errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after identifier '{ident_str}'"))
                if ident_count>25:
                    errors.append(LexicalError(pos_start, self.pos, "Identifier exceeded maximum character limit of 25"))
                tokens.append(Token(TT_IDENTIFIER, ident_str, pos_start=pos_start, pos_end=self.pos)) 


            elif self.current_char == '=':      # assignment operator, equals 
                tok_type = TT_ASSIGN
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    tok_type = TT_EQ

                if tok_type == TT_ASSIGN:
                    if self.current_char not in delim_map['assign_delim']:
                        errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator"))
                    tokens.append(Token(tok_type, '=', pos_start=self.pos))
                if tok_type == TT_EQ:
                    if self.current_char not in delim_map['comp_delim']:
                        errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator"))
                    tokens.append(Token(tok_type, '==', pos_start=pos_start, pos_end=self.pos))


            elif self.current_char == '+':          # plus, increment, plus equals
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
                        errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator"))
                    tokens.append(Token(tok_type, '+', pos_start=pos_start, pos_end=self.pos))
                if tok_type == TT_UNARY:
                    if self.current_char not in delim_map['incdec_delim']:
                        errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator"))
                    tokens.append(Token(tok_type, '++', pos_start=pos_start, pos_end=self.pos))
                if tok_type == TT_PLUSEQ:
                    if self.current_char not in delim_map['assign_delim']:
                        errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator"))
                    tokens.append(Token(tok_type, '+=', pos_start=pos_start, pos_end=self.pos))
                

            elif self.current_char == '-':          # minus, decrement, minus equals
                pos_start = self.pos.copy()
                self.advance()

                if self.current_char == '-':
                    self.advance()
                    tok_type = TT_UNARY  #  -- operator
                    if self.current_char not in delim_map['incdec_delim']:
                        errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator"))
                    tokens.append(Token(tok_type, '--', pos_start=pos_start, pos_end=self.pos))

                elif self.current_char == '=':
                    self.advance()
                    tok_type = TT_MINUSEQ  # -= operator
                    if self.current_char not in delim_map['assign_delim']:
                        errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator"))
                    tokens.append(Token(tok_type, '-=', pos_start=pos_start, pos_end=self.pos))
                    
                else:
                    if len(tokens) > 0 and tokens[-1].type in [TT_INT, TT_FLOAT, TT_IDENTIFIER, TT_RPAREN]:
                        tokens.append(Token(TT_MINUS, '-', pos_start=pos_start, pos_end=self.pos))
                    else:
                        if self.current_char in NUMERIC: 
                            tok, error = self.make_number(is_negative=True)
                            if error: errors.append(error)
                            else: tokens.append(tok)
                        else:
                            errors.append(LexicalError(pos_start, self.pos, f"Unexpected '-' without a valid number or identifier."))

        
            elif self.current_char == '*':      # multiply, power operator, multiply equals,
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
                        errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator"))
                    tokens.append(Token(tok_type, '*', pos_start=self.pos))
                if tok_type == TT_POW:
                    if self.current_char not in delim_map['arith_delim']:
                        errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator"))
                    tokens.append(Token(tok_type, '**', pos_start=pos_start, pos_end=self.pos))
                if tok_type == TT_MULEQ:
                    if self.current_char not in delim_map['assign_delim']:
                        errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator"))   
                    tokens.append(Token(tok_type, '*=', pos_start=pos_start, pos_end=self.pos))


            elif self.current_char == '/':      # divide, divide equals
                tok_type = TT_DIV
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    tok_type = TT_DIVEQ

                if tok_type == TT_DIV:
                    if self.current_char not in delim_map['arith_delim']:
                        errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator"))
                    tokens.append(Token(tok_type, '/', pos_start=self.pos))
                if tok_type == TT_DIVEQ:
                    if self.current_char not in delim_map['assign_delim']:
                        errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator"))
                    tokens.append(Token(tok_type, '/=', pos_start=pos_start, pos_end=self.pos))


            elif self.current_char == '%':      # modulo, modulo equals
                tok_type = TT_MOD
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    tok_type = TT_MODEQ

                if tok_type == TT_DIV:
                    if self.current_char not in delim_map['arith_delim']:
                        errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator"))
                    tokens.append(Token(tok_type, '%', pos_start=self.pos))
                if tok_type == TT_MODEQ:
                    if self.current_char not in delim_map['assign_delim']:
                        errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator"))
                    tokens.append(Token(tok_type, '%=', pos_start=pos_start, pos_end=self.pos))
            

            elif self.current_char == '!':      # not, not equals
                tok_type = TT_NOT
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    tok_type = TT_NE

                if tok_type == TT_NOT:
                    if self.current_char not in delim_map['logic_delim']:
                        errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator"))
                    tokens.append(Token(tok_type, '!', pos_start=self.pos))
                if tok_type == TT_NE:
                    if self.current_char not in delim_map['assign_delim']:
                        errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator"))
                    tokens.append(Token(tok_type, '!=', pos_start=pos_start, pos_end=self.pos))


            elif self.current_char == '<':      # less than, less than or equal
                tok_type = TT_LT
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    tok_type = TT_LTE

                if tok_type == TT_LT:
                    if self.current_char not in delim_map['comp_delim']:
                        errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator"))
                    tokens.append(Token(tok_type, '<', pos_start=self.pos))
                if tok_type == TT_LTE:
                    if self.current_char not in delim_map['comp_delim']:
                        errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator"))
                    tokens.append(Token(tok_type, '<=', pos_start=pos_start, pos_end=self.pos))


            elif self.current_char == '>':          # greater than, greater than or equal
                tok_type = TT_GT
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    tok_type = TT_GTE

                if tok_type == TT_GT:
                    if self.current_char not in delim_map['comp_delim']:
                        errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator"))
                    tokens.append(Token(tok_type, '>', pos_start=self.pos))
                if tok_type == TT_GTE:
                    if self.current_char not in delim_map['comp_delim']:
                        errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator"))
                    tokens.append(Token(tok_type, '>=', pos_start=pos_start, pos_end=self.pos))


            elif self.current_char == '&':          # and operator
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '&':
                    self.advance()
                    if self.current_char not in delim_map['logic_delim']:
                        errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator"))
                    tokens.append(Token(TT_AND, '&&', pos_start=pos_start, pos_end=self.pos))
                else: errors.append(InvalidSyntaxError(pos_start, self.pos, "'&' is not a valid operator"))


            elif self.current_char == '|':          # or operator
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char == '|':
                    self.advance()
                    if self.current_char not in delim_map['logic_delim']:
                        errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after operator"))
                    else: tokens.append(Token(TT_OR, '||', pos_start=pos_start, pos_end=self.pos))
                else: errors.append(InvalidSyntaxError(pos_start, self.pos, "'|' is not a valid operator"))
    

            elif self.current_char == '(':          # left parenthesis
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char not in delim_map['opnparen_delim']:
                    errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after parentheses"))
                else: tokens.append(Token(TT_LPAREN, '(', pos_start=self.pos))


            elif self.current_char == ')':          # right parenthesis
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char not in delim_map['clsparen_delim']:
                    errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after parentheses"))
                else: tokens.append(Token(TT_RPAREN, ')', pos_start=self.pos))


            elif self.current_char == '[':          # left bracket
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char not in delim_map['opnsquare_delim']:
                    errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after brackets"))
                else: tokens.append(Token(TT_LSQUARE, '[', pos_start=self.pos))


            elif self.current_char == ']':          # right bracket
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char not in delim_map['clssquare_delim']:
                    errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after brackets"))
                else: tokens.append(Token(TT_RSQUARE, ']', pos_start=self.pos))


            elif self.current_char == '{':          # left brace
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char not in delim_map['opnbrace_delim']:
                    errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after braces"))
                else: tokens.append(Token(TT_LBRACE, '{', pos_start=self.pos))


            elif self.current_char == '}':          # right brace
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char != None and self.current_char not in delim_map['clsbrace_delim']:
                    errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after braces"))
                else: tokens.append(Token(TT_RBRACE, '}', pos_start=self.pos))


            elif self.current_char == ',':          # comma
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char not in delim_map['comma_delim']:
                    errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after comma"))
                else: tokens.append(Token(TT_COMMA, ',', pos_start=self.pos))


            elif self.current_char == ':':          # colon
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char not in delim_map['col_delim']:
                    errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after colon"))
                else: tokens.append(Token(TT_COL, ':', pos_start=self.pos))


            elif self.current_char == ';':          # semicolon
                pos_start = self.pos.copy()
                self.advance()
                if self.current_char != None and self.current_char not in delim_map['lend_delim']:
                    errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after semicolon"))
                else: tokens.append(Token(TT_SEMICOL, ';', pos_start=self.pos))


            elif self.current_char in NUMERIC:
                tok, error = self.make_number()     # function for making integer and float tokens
                if error: errors.append(error)
                else: tokens.append(tok)


            elif self.current_char == '"':          # function for making string
                tok, error = self.make_string()
                if error: errors.append(error)      
                else: tokens.append(tok)


            elif self.current_char == '#':          # ignore single and multi-line comments
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
            

            elif self.current_char in ' \t\n':        # whitespace, newline, tab
                pos_start = self.pos

                # check for space
                if self.current_char == ' ':
                    while self.current_char == ' ':
                        self.advance()
                    if self.current_char not in delim_map['white_delim']:
                        errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after space"))
                    else:
                        tokens.append(Token(TT_SPACE, '␣', pos_start=pos_start, pos_end=self.pos))
                        continue
                # check for tab
                if self.current_char == '\t':
                    while self.current_char == '\t':
                        self.advance()
                    if self.current_char not in delim_map['white_delim']:
                        errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after tab"))
                    else:
                        tokens.append(Token(TT_TAB, '\\t', pos_start=pos_start, pos_end=self.pos))
                        continue
                # check for newline
                if self.current_char == '\n':
                    while self.current_char == '\n':
                        self.advance()
                    if self.current_char not in delim_map['white_delim']:
                        errors.append(LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after newline"))
                    else:
                        tokens.append(Token(TT_NEWLINE, '\\n', pos_start=pos_start, pos_end=self.pos))
                        continue

            else: 
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
        
        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, errors
                

    def make_number(self, is_negative=False):  # for making numbers: int and float
        num_str = ''
        int_count = 0
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
                    return [], LexicalError(pos_start, pos_end, "Invalid float assignment")
                elif self.current_char == None or self.current_char not in NUMERIC:
                    pos_end = self.pos.copy()  
                    return [], LexicalError(pos_start, pos_end, "Invalid float assignment")
                dot_count += 1
                num_str += '.'
            else:
                # checks dot count to see if num is int or float,
                # if dot count is 0, num is int, increment num_count and int_count
                # if dot count is 1, num is float and were in the least significat, increment dec_count
                if dot_count == 0:
                    num_count += 1
                    int_count +=1
                if dot_count == 1:
                    dec_count += 1

                # checks if num_count exceeds limit of 17 if number is an int
                if dot_count == 0 and num_count > 17:
                    pos_end = self.pos.copy()
                    return [], LexicalError(pos_start, pos_end, "Whole number exceeded maximum character limit of 17")
                
                # checks if num_count exceeds limit of 9 if number is a float
                if dot_count == 1 and num_count > 9:
                    pos_end = self.pos.copy()
                    return [], LexicalError(pos_start, pos_end, "Whole number exceeded maximum character limit of 17")
                
                # checks if dec_count exceeds limit of 7 if number is a float, if it exceeds then just ignore
                if dot_count == 1 and dec_count > 7:
                    self.advance()
                # append the latest character to the number string
                else:
                    num_str += self.current_char
                    self.advance()

        if self.current_char not in delim_map['num_delim']:
            pos_end = self.pos.copy()
            return [], LexicalError(pos_start, pos_end, f"Invalid delimiter '{self.current_char}' after number")

        if dot_count > 1:
            pos_end = self.pos.copy()
            return [], LexicalError(pos_start, pos_end, f"Multiple period '.' in a float assignment")
        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start, self.pos), None
        else:
            return Token(TT_FLOAT, float(num_str), pos_start, self.pos), None
        
    def make_string(self):
        id_str = ''
        pos_start = self.pos.copy()
        self.advance()

        while self.current_char != None and self.current_char in ASCII:
            if self.current_char != '\n':
                pos_end = self.pos.copy()
            if self.current_char == '"':
                self.advance() 
                if self.current_char not in delim_map['str_delim']:
                    return [], LexicalError(pos_start, self.pos, f"Invalid delimiter '{self.current_char}' after string '{id_str}'")
                return Token(TT_STRING, id_str, pos_start, self.pos), None
            id_str += self.current_char
            self.advance()

        return [], InvalidSyntaxError(pos_start, pos_end, 'String not properly closed with double quotes (")')


def run(fn, text):
        lexer = Lexer(fn, text)
        tokens, error = lexer.make_tokens()
        return tokens, error