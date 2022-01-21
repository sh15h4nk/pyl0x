
from scanner.token_types import TOKEN_TYPES, single_char_token, multi_char_token, keywords
from scanner.token import token

from error_reporter import error

from decimal import Decimal

class scanner:
    source = str()
    tokens = []
    start = 0
    current = 0
    line = 1

    def __init__(self, source) -> None:
        self.source = source
    
    def __repr__(self) -> str:
        return "source: {} tokens: {}".format(self.source, self.tokens)
    

    def scan_tokens(self):
        while(not self.is_at_end()):
            self.start = self.current
            self.scan_token()
        self.tokens.append(token("EOF", "", None, self.line))

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)
    
    def scan_token(self):
        c = self.advance()
        
        if c in list(single_char_token.values()):
            type = list(single_char_token.keys())[list(single_char_token.values()).index(c)]
            self.add_token(type, None)

        elif c in list(multi_char_token.values()):
            type = list(multi_char_token.keys())[list(multi_char_token.values()).index(c)]
            if self.match("="):
                type += "_EQUAL"
            self.add_token(type, None)
        
        elif c == "/":
            if (self.match("/")):
                while (self.peek() != "\n" and not self.is_at_end()):
                    self.advance()
            else:
                self.add_token({"SLASH": "/"}, None)
        
        elif c in [" ", "\r", "\t"]:
            pass
        elif c == "\n":
            self.line += 1
        
        elif c == '"':
            self.string()
        
        elif c.isdigit():
            self.number()
        
        elif c.isalpha() or c == "_":
            self.identifier()

        else:
            error(self.line, "Unexpected character")
    
    def identifier(self):
        while (self.peek().isalnum()): self.advance()

        lexeme = self.source[self.start: self.current]
        type = TOKEN_TYPES.IDENTIFIER
        if lexeme in list(keywords.values()):
            type = list(keywords.keys())[list(keywords.values()).index(lexeme)]

        self.add_token(type, None)

    
    def number(self):
        while (self.peek().isdigit()): self.advance()

        if (self.peek() == "." and self.peek_next().isdigit()):
            self.advance()
            while self.peek().isdigit(): self.advance()
        print("The number", self.source[self.start: self.current])
        self.add_token(TOKEN_TYPES.NUMBER, Decimal(self.source[self.start: self.current]))
    
    def string(self):
        while(self.peek() != '"' and not self.is_at_end()):
            if (self.peek() == "\n"): self.line += 1
            self.advance()
        if (self.is_at_end()):
            error(self.line, "Unterminated string")
            return
        
        self.advance()

        lexeme = self.source[self.start +1 : self.current -1]
        self.add_token(TOKEN_TYPES.STRING, lexeme)
    
    def peek(self):
        if (self.is_at_end()): return "\0"
        return self.source[self.current]
    
    def peek_next(self):
        if (self.current + 1 >= len(self.source)): return "\0"
        return self.source[self.current +1]
    
    def match(self, expected):
        if(self.is_at_end()):
            return False
        if (self.source[self.current] != expected):
            return False
        self.current += 1
        return True


    def advance(self):
        c = self.source[self.current]
        self.current += 1
        return c
    
    def add_token(self, type, literal):
        lexeme = self.source[self.start: self.current]
        self.tokens.append(token(type, lexeme, literal, self.line))
    

