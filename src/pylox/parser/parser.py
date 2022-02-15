

from ast import arg
from pylox.scanner.token import token
from pylox.scanner.token_types import TOKEN_TYPES
import pylox.parser.expr as EXP
from pylox.error_reporter import error as lox_error
from types import SimpleNamespace

TOKEN_TYPE = SimpleNamespace(**TOKEN_TYPES.__dict__)
TOKEN_TYPE.BANG_EQUAL = "BANG_EQUAL"
TOKEN_TYPE.EQUAL_EQUAL = "EQUAL_EQUAL"
TOKEN_TYPE.GREATER = "GREATER"
TOKEN_TYPE.GREATER_EQUAL = "GREATER_EQUAL"
TOKEN_TYPE.LESS = "LESS"
TOKEN_TYPE.LESS_EQUAL = "LESS_EQUAL"
TOKEN_TYPE.MINUS = "MINUS"
TOKEN_TYPE.PLUS = "PLUS"
TOKEN_TYPE.SLASH = "SLASH"
TOKEN_TYPE.STAR = "STAR"
TOKEN_TYPE.BANG = "BANG"
TOKEN_TYPE.EQUAL = "EQUAL"
TOKEN_TYPE.LEFT_PAREN = "LEFT_PAREN"
TOKEN_TYPE.RIGHT_PAREN = "RIGHT_PAREN"
TOKEN_TYPE.COMA = "COMA"
TOKEN_TYPE.DOT = "DOT"
TOKEN_TYPE.SEMICOLON = "SEMICOLON"
TOKEN_TYPE.LEFT_BRACE = "LEFT_BRACE"
TOKEN_TYPE.RIGHT_BRACE = "RIGHT_BRACE"



class parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
    
    def parse(self):
        try:
            return self.expression()
        except self.parse_error: 
            return None
    
    def expression(self):
        return self.equality()
    
    def equality(self):
        expr = self.comparison()
        while(self.match(TOKEN_TYPE.BANG_EQUAL, TOKEN_TYPE.EQUAL_EQUAL)):
            operator = self.previous()
            right = self.comparison()
            expr = EXP.Binary(expr, operator, right)
        return expr
    
    def comparison(self):
        expr = self.term()
        while (self.match(TOKEN_TYPE.GREATER, TOKEN_TYPE.GREATER_EQUAL, TOKEN_TYPE.LESS, TOKEN_TYPE.LESS_EQUAL)):
            operator = self.previous()
            right = self.term()
            expr = EXP.Binary(expr, operator, right)
        return expr
    
    def term(self):
        expr = self.factor()
        while self.match(TOKEN_TYPE.MINUS, TOKEN_TYPE.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = EXP.Binary(expr, operator, right)
        return expr
    
    def factor(self):
        expr = self.unary()
        while self.match(TOKEN_TYPE.SLASH, TOKEN_TYPE.STAR):
            operator = self.previous()
            right = self.unary()
            expr = EXP.Binary(expr, operator, right)
        return expr
    
    def unary(self):
        if self.match(TOKEN_TYPE.BANG, TOKEN_TYPE.MINUS):
            operator = self.previous()
            right = self.unary()
            return EXP.Unary(operator, right)
        return self.primary()
    
    def primary(self):
        if self.match(TOKEN_TYPE.FALSE): return EXP.Literal(False)
        if self.match(TOKEN_TYPE.TRUE): return EXP.Literal(True)
        if self.match(TOKEN_TYPE.NIL): return EXP.Literal(None)
        if self.match(TOKEN_TYPE.NUMBER, TOKEN_TYPE.STRING): return EXP.Literal(self.previous().literal)
        if self.match(TOKEN_TYPE.LEFT_PAREN):
            expr = self.expression()
            self.consume(TOKEN_TYPE.RIGHT_PAREN, "Expect ')' after expression.")
            return EXP.Grouping(expr)
        raise self.error(self.peek(), "Expect expression.")
    
    def match(self, *args):
        for i in args:
            if (self.check(i)):
                self.advance()
                return True
        return False
    
    def check(self, type):
        if self.isAtEnd(): return False
        return self.peek().type == type
    
    def advance(self):
        if not self.isAtEnd(): self.current +=1
        return self.previous()
    
    def isAtEnd(self):
        return self.peek().type == "EOF"
    
    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current -1]

    def consume(self, type, message):
        if self.check(type): return self.advance()
        raise self.error(self.peek(), message)
    
    def error(self, token, message):
        lox_error(token, message)
        return self.parse_error()
    
    def synchronize(self):
        self.advance()
        while not self.isAtEnd():
            if (self.previous().type == TOKEN_TYPE.SEMICOLON): return
            if self.peek().type in ["CLASS", "FUN", "VAR", "FOR", "IF", "WHILE", "PRINT", "RETURN"]: return
            self.advance()
    
    class parse_error(Exception):
        pass


if __name__ == "__main__":
    pass