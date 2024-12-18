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
PUNCTUATION_SYMBOLS = '!@#$%^&*()-_=+[]{|};:’”,<>./?'
ASCII = ALPHA_NUMERIC + PUNCTUATION_SYMBOLS
ARITH_OP = '+-*/%'

delim_map = {
    'adr_delim': set(ALPHA_NUMERIC + ' '),
    'arith_delim':  set(ALPHA_NUMERIC + ' ' + '-' + '('),
    'assign_delim': set(ALPHA_NUMERIC + ' ' + '"' + '-' + '(' + '['),
    'bool_delim':   {')', ']', ',', ' '},
    'codeblk_delim': {'{', ' '},
    'comp_delim': set(ALPHA_NUMERIC + '"' + "'" + '(' + '-' + ' '),
    'clsbrace_delim': set(ALPHA_NUMERIC + '}' + '\n' + ' '),
    'clsparen_delim': {'+', '-', '*', '/', '%', ')', '{', '}', ',', ']', '\n', ' '},
    'clssquare_delim': {'+', '-', '*', '/', '%', '!', '=', '<', '>', ')', ',', '[', ']', '\n', ' '},
    'comma_delim': set(ALPHA_NUMERIC + '"' + "'" + '(' + '[' + '-' + ' '),
    'comp_delim': set(ALPHA_NUMERIC + '"' + "'" + '(' + '-' + ' '),
    'ident_delim': {'+', '-', '*', '/', '%', '!', '=', '<', '>', '(', ')', ',', '[', ']', '\n', ' '},
    'incdec_delim': set(ALPHA_NUMERIC + ')', ' '),
    'kword_delim': {' '},
    'lend_delim': set(ALPHA_NUMERIC + '#' + '#$' + '\n' + ' '),
    'minus_delim': set(ALPHA_NUMERIC + '-' + '(' + ' '),
    'num_delim': set(ARITH_OP + ' ' + ')' + ',' + ';'),
    'opnbrace_delim': set(ALPHA_NUMERIC + '\n' + '"' + ' '),
    'opnparen_delim': set(ALPHA_NUMERIC + '"', "'", '-', '(', ')', '\n', ' '),
    'opnsquare_delim': set(ALPHA_NUMERIC + '"', "'", '-', '(', '[', ']', ' '),
    'plus_delim': set(ALPHA_NUMERIC + '"', "'", '-', '('),
    'para_delim': {'(', ' ', '\n'},
    'recall_delim': set(ALPHA + ' ' + ';'), 
    'str_delim': {'+', ')', ']', '\n', ',', ' '},
    'woogie_delim': set(NUMERIC + '(' + ' ')
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
TT_SEMICOL  = 'SEMICOL' # ';'
TT_EOF      = 'EOF'     # End of Line

TT_KEYWORD  = 'KEYWORD' # Keywords
TT_IDENTIFIER = 'IDENTIFIER' # Identifiers

KEYWORDS = [ 
    'domain', 'null', 'int', 'float', 'char', 'string', 'bool', 'restrict', 'invoke', 
    'capture', 'true', 'false', 'vow', 'else vow', 'else', 'boogie', 'woogie', 'default', 
    'cycle', 'sustain', 'perform', 'dismiss', 'hop', 'recall', 'curse', 'VAR'
]

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
                tokens.append(self.make_number())
            elif self.current_char in ALPHA:
                tokens.append(self.make_identifier())
            elif self.current_char == '+':
                tokens.append(self.make_plus_equals())
                self.advance()
            elif self.current_char == '-':
                tokens.append(self.make_minus_equals())
                self.advance()
            elif self.current_char == '*':
                tokens.append(self.make_mul_equals())
                self.advance()
            elif self.current_char == '/':
                tokens.append(self.make_div_equals())
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == '!':
                tok, error = self.make_not_equals()
                if error: return [], error
                tokens.append(tok)
            elif self.current_char == '&':
                self.advance()
                if self.current_char == '&':
                    tokens.append(Token(TT_AND, pos_start=self.pos))
                else: return [], InvalidSyntaxError(pos_start, self.pos, "'&' is not a valid operator")
            elif self.current_char == '|':
                self.advance()
                if self.current_char == '|':
                    tokens.append(Token(TT_AND, pos_start=self.pos))
                else: return [], InvalidSyntaxError(pos_start, self.pos, "'|' is not a valid operator")
            elif self.current_char == '=':
                tokens.append(self.make_equals())
                self.advance()
            elif self.current_char == '<':
                tokens.append(self.make_less_than())
            elif self.current_char == '>':
                tokens.append(self.make_greater_than())
            elif self.current_char == ';':
                tokens.append(Token(TT_SEMICOL, pos_start=self.pos))
                self.advance()
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
            
        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start, self.pos)
        else:
            return Token(TT_FLOAT, float(num_str), pos_start, self.pos)

    def make_identifier(self):
        id_str = ''
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in ALPHA_NUMERIC + '_':
            id_str += self.current_char
            self.advance()

        tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
        return Token(tok_type, id_str, pos_start, self.pos)
    
    def make_plus_equals(self):
        tok_type = TT_PLUS
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_PLUSEQ
        
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_minus_equals(self):
        tok_type = TT_MINUS
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_MINUSEQ
        
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_mul_equals(self):
        tok_type = TT_MUL
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_MULEQ

        if self.current_char == '*':
            self.advance()
            tok_type = TT_POW
        
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_div_equals(self):
        tok_type = TT_DIV
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_DIVEQ
        
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_not_equals(self):
        tok_type = TT_NOT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_NE
        
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)
    
    def make_equals(self):
        tok_type = TT_ASSIGN
        pos_start = self.pos_copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_EQ
        
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)
    
    def make_less_than(self):
        tok_type = TT_LT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_LTE
        
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_greater_than(self):
        tok_type = TT_GT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_GTE
        
        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

##############
# NODES
##############

class NumberNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end
    
    def __repr__(self):
        return f'{self.tok}'
    
class VarAccessNode:
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end

class VarAssignNode:
    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end
    
class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
        
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'
    
class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node

        self.pos_start = self.op_tok.pos_start
        self.pos_end = node.pos_end
    
    def __repr__(self):
        return f'({self.op_tok}, {self.node})'

##############
# PARSER RESULT
##############

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0

    def register_advancement(self):
        self.advance_count += 1
    
    def register(self, res):
        self.advance_count += res.advance_count
        if res.error: self.error = res.error
        return res.node
    
    def success(self, node):
        self.node = node
        return self
    
    def failure(self, error):
        if not self.error or self.advance_count == 0:
            self.error = error
        return self

##############
# PARSER
##############

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def parse(self):
        res = self.expr()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Missing semicolon ';' at the end of the line"
            ))
        return res

#####################

    def atom(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_INT, TT_FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))
        
        elif tok.type == TT_IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(tok))
        
        elif tok.type == TT_LPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            if self.current_tok.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ')'"
                ))
            
        return res.failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end,
            "Expected int, float, identifier, '+', '-', or '('"
        ))
            

    def power(self):
        return self.bin_op(self.atom, (TT_POW, ), self.factor)

    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_PLUS, TT_MINUS):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))

        return self.power()
    
    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))

    def expr(self):
        res = ParseResult()

        if self.current_tok.matches(TT_KEYWORD, 'VAR'):
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end, 
                    "Expected identifier"))
            var_name = self.current_tok
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_ASSIGN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end, 
                    "Expected assignment operator '='"))
            res.register_advancement()
            self.advance()

            expr = res.register(self.expr())
            if res.error: return res

            # Ensure expr node has pos_end attribute before passing to VarAssignNode
            if expr:
                return res.success(VarAssignNode(var_name, expr))
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected expression after '='"))

        node = res.register(self.bin_op(self.term, (TT_PLUS, TT_MINUS)))
        
        if res.error: return res.failure(InvalidSyntaxError(
            self.current_tok.pos_start, self.current_tok.pos_end,
            "Expected 'VAR', int, float, identifier, '+', '-', or '('"
        ))

        return res.success(node)

    def program(self): # this is where the program starts, it should always parse 'expansion' first
        pass

    def global_dec(self): # this is for declarations outside functions; can be null
        # check for <global_choice> such as var_dec, curse_dec, clan_dec, and restrict_dec
        pass

    def body(self): # this is where statements are written, it should always end with ';', can be null
        # check for <statements> such as local dec, re-assign, expressions, comments, invoke(print), 
        # capture(scan), curse_call(function calls) conditional_stm, looping_stm; can be null
        pass

    def local_dec(self): # this is for declarations inside functions; can be null
        # check for <local_choice> such as var_dec, curse_dec, clan_dec, and restrict_dec
        pass

    def var_dec(self): # this is for parsing variable declaration, eg. int a = 1; , int a;
        # check for restrict(constant) keyword; can be null
        pass

    def clan_dec(self): # this is for parsing clan declarations, eg. int num[3] = {1,2,3,4}; int num[] = {1,2}; int num[5]; can be null
        pass

    def curse_dec(self): # this is for parsing curses (functions), eg. curse funcName(<param1, param2>){<body>}; can be null
        # check for parameters, recall statements
        pass

    def invoke_stm(self): # print statements
        pass

    def var_arith(self): # variable arithmetic eg. a+b
        pass

    def capture_stm(self):  # scan statements
        pass

    def conditional_stm(self): # vow-else(if-else) statements
        pass

    def boogie_woogie_stm(self): # boogie-woogie(switch-case) statements
        pass

    def boogie_true_stm(self): # boogie-true(switch-true) statements
        pass

    def cycle_loop(self): # for loop
        pass

    def sustain_loop(self): # while loop
        pass

    def persustain_loop(self): # do-while loop
        pass

    def unary_expr(self): # for unary_expressions eg. !varName, ++varName, varName--
        pass

    def arith_expr(self): # for arithmetic expressions eg. 1+1
        pass

    def relational_expr(self): # for logical expressions eg. '!', '&&', '||'
        pass

    def curse_call(self): # for calling curses(functions) eg. intSum = add(a, b);
        pass

    def length(self): # built-in function for strings and clans(arrays)
        pass
    
    def cleave(self): # built-in function for clans(arrays)
        pass

    def cleave_string(self): # built-in function for strings
        pass

    def dismantle(self): # built-in function for clans(arrays)
        pass

    def dismantle_string(self):  # built-in function for strings
        pass


#######################

    def bin_op(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a
        res = ParseResult()
        left = res.register(func_a())
        if res.error: return res

        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register_advancement()
            self.advance() 
            right = res.register(func_b())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)

##############
# RUNTIME Result
##############

class RTResult: 
    def __init__(self):
        self.value = None
        self.error = None

    def register(self, res):
        if res.error: self.error = res.error
        return res.value
    
    def success(self, value):
        self.value = value
        return self
    
    def failure(self, error):
        self.error = error
        return self

##############
# VALUES
##############

class Number:
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start = None, pos_end = None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self
    
    def set_context(self, context = None):
        self.context = context
        return self

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
        
    def subtracted_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
        
    def multiplied_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
        
    def divided_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    'Division by zero',
                    self.context
                )
            return Number(self.value / other.value).set_context(self.context), None
    
    def power_of(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return str(self.value)

##############
# CONTEXT
##############

class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None

##############
# SYMBOL TABLE
##############

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.parent = None
    
    def get(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value
    
    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]

##############
# INTERPRETER
##############

class Interpreter:
    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)
    
    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')
    
    ########################

    def visit_NumberNode(self, node, context):
        return RTResult().success(
            Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )
    
    def visit_VarAccessNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                f"'{var_name}' is not defined",
                context
            ))
        value = value.copy().set_pos(node.pos_start, node.pos_end)
        return res.success(value)
    
    def visit_VarAssignNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.error: return res
        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_BinOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error: return res
        right = res.register(self.visit(node.right_node, context))
        if res.error: return res

        if node.op_tok.type == TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == TT_MINUS:
            result, error = left.subtracted_by(right)
        elif node.op_tok.type == TT_MUL:
            result, error = left.multiplied_by(right)
        elif node.op_tok.type == TT_DIV:
            result, error = left.divided_by(right)
        elif node.op_tok.type == TT_POW:
            result, error = left.power_of(right)

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.error: return res
        
        error = None

        if node.op_tok.type == TT_MINUS:
            number, error = number.multiplied_by(Number(-1))

        if error: 
            return res.failure()
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))

##############
# RUN Function
##############

global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number(0))

def run(fn, text):
    # Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error

    return tokens, error

    # # Generate AST
    # parser = Parser(tokens)
    # ast = parser.parse()
    # if ast.error: return None, ast.error

    # # Run program
    # interpreter = Interpreter()
    # context = Context('<program>')
    # context.symbol_table = global_symbol_table
    # result = interpreter.visit(ast.node, context)

    # return result.value, result.error