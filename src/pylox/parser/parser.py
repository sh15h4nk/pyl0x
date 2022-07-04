

from ast import arg, keyword, operator, stmt
from pylox.scanner.token import Token
from pylox.scanner.token_types import TOKEN_TYPES
import pylox.parser.expr as EXP
import pylox.parser.stmt as STMT
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
TOKEN_TYPE.PRINT = "PRINT"
TOKEN_TYPE.VAR = "VAR"
TOKEN_TYPE.IDENTIFIER = "IDENTIFIER"
TOKEN_TYPE.IF = "IF"
TOKEN_TYPE.ELSE = "ELSE"
TOKEN_TYPE.OR = "OR"
TOKEN_TYPE.AND = "AND"
TOKEN_TYPE.WHILE = "WHILE"
TOKEN_TYPE.FOR = "FOR"
TOKEN_TYPE.FUN = "FUN"
TOKEN_TYPE.RETURN = "RETURN"
TOKEN_TYPE.CLASS = "CLASS"
TOKEN_TYPE.THIS = "THIS"
TOKEN_TYPE.SUPER = "SUPER"



class parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
    
    def parse(self):
        statements = []
        while not self.isAtEnd():
            statements.append(self.declaration())
        return statements
    
    def declaration(self):
        try:
            if self.match(TOKEN_TYPE.CLASS): return self.class_declaration()
            if self.match(TOKEN_TYPE.FUN): return self.function("function")
            if self.match(TOKEN_TYPE.VAR): return self.var_declaration()
            return self.statement()
        except:
            self.synchronize()
            return None
    
    def class_declaration(self):
        name = self.consume(TOKEN_TYPE.IDENTIFIER, "Expected class name.")
        
        superclass = None
        if self.match(TOKEN_TYPE.LESS):
            self.consume(TOKEN_TYPE.IDENTIFIER, "Expect super class name.")
            superclass = EXP.Variable(self.previous())
        
        self.consume(TOKEN_TYPE.LEFT_BRACE, "Expect '{' before class body.")
        methods = []
        
        while not self.check(TOKEN_TYPE.RIGHT_BRACE) and not self.isAtEnd():
            methods.append(self.function("method"))
        
        self.consume(TOKEN_TYPE.RIGHT_BRACE, "Expect '}' after class body.")
        return STMT.Class(name, superclass, methods)
    
    def var_declaration(self):
        name = self.consume(TOKEN_TYPE.IDENTIFIER, "Expected variable name")
        
        initializer  = None
        if (self.match(TOKEN_TYPE.EQUAL)): initializer = self.expression()
        self.consume(TOKEN_TYPE.SEMICOLON, "Expected ';' after variable decleration")
        return STMT.Var(name, initializer)
    
    def statement(self):
        if self.match(TOKEN_TYPE.FOR): return self.for_statement()
        if self.match(TOKEN_TYPE.IF): return self.if_statement()
        if self.match(TOKEN_TYPE.PRINT): return self.print_statement()
        if self.match(TOKEN_TYPE.RETURN): return self.return_statement()
        if self.match(TOKEN_TYPE.WHILE): return self.while_statement()
        if self.match(TOKEN_TYPE.LEFT_BRACE): return STMT.Block(self.block())
        return self.expression_statement()
    
    def for_statement(self):
        self.consume(TOKEN_TYPE.LEFT_PAREN, "Expect '(' after 'for'.")
        
        initializer = None
        if self.match(TOKEN_TYPE.SEMICOLON): initializer = None
        elif self.match(TOKEN_TYPE.VAR): initializer = self.var_declaration()
        else: initializer = self.expression_statement()
        
        condition = None
        if not self.check(TOKEN_TYPE.SEMICOLON): condition = self.expression()
        self.consume(TOKEN_TYPE.SEMICOLON, "Expect ';' after loop condition.")
        
        increment = None
        if not self.check(TOKEN_TYPE.RIGHT_PAREN): increment = self.expression()
        self.consume(TOKEN_TYPE.RIGHT_PAREN, "Expect ')' after for clauses.")
        
        body = self.statement()
        if increment is not None:
            body = STMT.Block([body, STMT.Expression(increment)])
        
        if condition is None: condition = EXP.Literal(True)
        body = STMT.While(condition, body)
        
        if initializer is not None: body = STMT.Block([initializer, body])
        
        return body
    
    def while_statement(self):
        self.consume(TOKEN_TYPE.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(TOKEN_TYPE.RIGHT_PAREN, "Expect ')' after condition.")
        body = self.statement()
        return STMT.While(condition, body)
        
    
    def if_statement(self):
        self.consume(TOKEN_TYPE.LEFT_PAREN, "Expect '(' after if.")
        condition = self.expression()
        self.consume(TOKEN_TYPE.RIGHT_PAREN, "Expect ')' after if condition.")
        
        thenBranch = self.statement()
        elseBranch = None
        if self.match(TOKEN_TYPE.ELSE): elseBranch = self.statement
        
        return STMT.If(condition, thenBranch, elseBranch)
        

    def print_statement(self):
        value = self.expression()
        self.consume(TOKEN_TYPE.SEMICOLON, "Expected ';' after value.")
        return STMT.Print(value)
    
    def return_statement(self):
        keyword = self.previous()
        value = None
        if not self.check(TOKEN_TYPE.SEMICOLON): value = self.expression()
        self.consume(TOKEN_TYPE.SEMICOLON, "Expect ';' after return value")
        return STMT.Return(keyword, value)
    
    def expression_statement(self):
        expr = self.expression()
        self.consume(TOKEN_TYPE.SEMICOLON, "Expect ';' after expression.")
        return STMT.Expression(expr)
    
    def function(self, kind):
        name = self.consume(TOKEN_TYPE.IDENTIFIER, "Expect {} name".format(kind))
        self.consume(TOKEN_TYPE.LEFT_PAREN, "Expect '(' after {} name.".format(kind))
        parameters = []
        if not self.check(TOKEN_TYPE.RIGHT_PAREN):
            parameters.append(self.consume(TOKEN_TYPE.IDENTIFIER, "Expect parameter name."))
            while self.match(TOKEN_TYPE.COMA):
                if len(parameters) >= 255: self.error(self.peek(), "Can't have more than 255 parameters.")
                parameters.append(self.consume(TOKEN_TYPE.IDENTIFIER, "Expect parameter name."))

        self.consume(TOKEN_TYPE.RIGHT_PAREN, "Expect ')' after parameters.")
        self.consume(TOKEN_TYPE.LEFT_BRACE, "Expect '{' before "+ str(kind) +" body.")  ## Marking line [format string wired behaviour "Expcet '{' before {} body".format(kind)]
        body = self.block()
        return STMT.Function(name, parameters, body)
        
        
    def block(self):
        statements = []
        while not self.check(TOKEN_TYPE.RIGHT_BRACE) and not self.isAtEnd(): statements.append(self.declaration())
        self.consume(TOKEN_TYPE.RIGHT_BRACE, "Expect } after block.")
        return statements
    
    def assignment(self):
        expr = self._or()
        if self.match(TOKEN_TYPE.EQUAL):
            equals = self.previous()
            value = self.assignment()
            if type(expr) == EXP.Variable: return EXP.Assign(expr.name, value)
            elif type(expr) == EXP.Get: return EXP.Set(expr.object, expr.name, value)
            self.error(equals, "Invalid assignment target")
        return expr
    
    def _or(self):
        expr = self._and()
        while self.match(TOKEN_TYPE.OR):
            operator = self.previous()
            right = self._and()
            expr = EXP.Logical(expr, operator, right)
        return expr
    
    def _and(self):
        expr = self.equality()
        while self.match(TOKEN_TYPE.AND):
            operator = self.previous()
            right = self.equality()
            expr = EXP.Logical(expr, operator, right)
        return expr
    
    def expression(self):
        return self.assignment()
    
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
        return self.call()
    
    def call(self):
        expr = self.primary()
        while True:
            if self.match(TOKEN_TYPE.LEFT_PAREN): expr = self.finish_call(expr)
            elif self.match(TOKEN_TYPE.DOT):
                name = self.consume(TOKEN_TYPE.IDENTIFIER, "Expect property name after '.'.")
                expr = EXP.Get(expr, name)
            else: break
        return expr
    
    def finish_call(self, callee):
        arguments = []
        if not self.check(TOKEN_TYPE.RIGHT_PAREN):
            arguments.append(self.expression())
            while self.match(TOKEN_TYPE.COMA):
                if len(arguments) >= 255:   self.error(self.peek(), "Can't have more than 255 arguments.")
                arguments.append(self.expression())
        paren = self.consume(TOKEN_TYPE.RIGHT_PAREN, "Expect ')' after arguments.")
        return EXP.Call(callee, paren, arguments)
    
    def primary(self):
        if self.match(TOKEN_TYPE.FALSE): return EXP.Literal(False)
        if self.match(TOKEN_TYPE.TRUE): return EXP.Literal(True)
        if self.match(TOKEN_TYPE.NIL): return EXP.Literal(None)
        if self.match(TOKEN_TYPE.NUMBER, TOKEN_TYPE.STRING): return EXP.Literal(self.previous().literal)
        if self.match(TOKEN_TYPE.SUPER):
            keyword = self.previous()
            self.consume(TOKEN_TYPE.DOT, "Expect '.' after 'super'.")
            method = self.consume(TOKEN_TYPE.IDENTIFIER, "Expect superclass method name")
            return EXP.Super(keyword, method)
        if self.match(TOKEN_TYPE.THIS): return EXP.This(self.previous())
        if self.match(TOKEN_TYPE.IDENTIFIER): return EXP.Variable(self.previous())
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