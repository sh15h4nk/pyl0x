"""Parser class for the interpreter"""

from typing import List, Optional
from pylox.scanner.token import Token
from pylox.scanner.token_types import TOKEN_TYPES
import pylox.parser.expr as EXPR
import pylox.parser.stmt as STMT
from types import SimpleNamespace
from pylox.exceptions.exceptions import ParseError

# Token type definition
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


class Parser:
    """This class parses the tokens scanned by the scanner.
    """
    def __init__(self, tokens: List[Token]) -> None:
        """Initializes the list of tokens and sets the current pointer

        Args:
            tokens (List[Token]): list of tokens scanned by the scanner
        """
        self.tokens = tokens
        self.current = 0
    
    def parse(self) -> List:
        """Parses the tokens into a list of statements.

        Returns:
            List: parsed statements list.
        """
        statements = []
        while not self.isAtEnd():
            statements.append(self.declaration())
        return statements
    
    def declaration(self):
        """Matches the declaration statements based on the grammer"""
        try:
            if self.match(TOKEN_TYPE.CLASS): return self.class_declaration()
            if self.match(TOKEN_TYPE.FUN): return self.function("function")
            if self.match(TOKEN_TYPE.VAR): return self.var_declaration()
            return self.statement()
        except:
            self.synchronize()
            return None
    
    def class_declaration(self) -> STMT.Class:
        """Handler class declaration

        Returns:
            STMT.Class: returns the class node.
        """
        name = self.consume(TOKEN_TYPE.IDENTIFIER, "Expected class name.") 
        superclass = None
        
        if self.match(TOKEN_TYPE.LESS):
            self.consume(TOKEN_TYPE.IDENTIFIER, "Expect super class name.")
            superclass = EXPR.Variable(self.previous())
        
        self.consume(TOKEN_TYPE.LEFT_BRACE, "Expect '{' before class body.")
        methods = []
        
        while not self.check(TOKEN_TYPE.RIGHT_BRACE) and not self.isAtEnd():
            methods.append(self.function("method"))
        
        self.consume(TOKEN_TYPE.RIGHT_BRACE, "Expect '}' after class body.")
        return STMT.Class(name, superclass, methods)
    
    def var_declaration(self) -> STMT.Var:
        """Handles the variable declaration.

        Returns:
           STMT.Var: variable node.
        """
        name = self.consume(TOKEN_TYPE.IDENTIFIER, "Expected variable name")
        initializer  = None
        
        if (self.match(TOKEN_TYPE.EQUAL)): initializer = self.expression()
        self.consume(TOKEN_TYPE.SEMICOLON, "Expected ';' after variable decleration")
        return STMT.Var(name, initializer)
    
    def statement(self):
        """Handles the parsing of for, if, print, return, while and the block of statements"""
        if self.match(TOKEN_TYPE.FOR): return self.for_statement()
        if self.match(TOKEN_TYPE.IF): return self.if_statement()
        if self.match(TOKEN_TYPE.PRINT): return self.print_statement()
        if self.match(TOKEN_TYPE.RETURN): return self.return_statement()
        if self.match(TOKEN_TYPE.WHILE): return self.while_statement()
        if self.match(TOKEN_TYPE.LEFT_BRACE): return STMT.Block(self.block())
        return self.expression_statement()
    
    def for_statement(self) -> STMT.Block:
        """Handles the For loop parsing.

        Returns:
            STMT.Block: returns a block node which contains equivalent code for for loop.
        """
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
        
        if condition is None: condition = EXPR.Literal(True)
        body = STMT.While(condition, body)
        
        if initializer is not None: body = STMT.Block([initializer, body])
        return body
    
    def while_statement(self) -> STMT.While:
        """Handles the while loop parsing.

        Returns:
            STMT.While: returns a while block node.
        """
        self.consume(TOKEN_TYPE.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(TOKEN_TYPE.RIGHT_PAREN, "Expect ')' after condition.")
        body = self.statement()
        return STMT.While(condition, body)
        
    def if_statement(self) -> STMT.If:
        """Handles the parsing of if and else block.

        Returns:
            STMT.If: returns a if block node.
        """
        self.consume(TOKEN_TYPE.LEFT_PAREN, "Expect '(' after if.")
        condition = self.expression()
        self.consume(TOKEN_TYPE.RIGHT_PAREN, "Expect ')' after if condition.")
        thenBranch = self.statement()
        elseBranch = None
        if self.match(TOKEN_TYPE.ELSE): elseBranch = self.statement
        return STMT.If(condition, thenBranch, elseBranch)
        
    def print_statement(self) -> STMT.Print:
        """Handles the print statements.

        Returns:
            STMT.Print: returns a print node.
        """
        value = self.expression()
        self.consume(TOKEN_TYPE.SEMICOLON, "Expected ';' after value.")
        return STMT.Print(value)
    
    def return_statement(self) -> STMT.Return:
        """Parses a return statement.

        Returns:
            STMT.Return: returns a return node.
        """
        keyword = self.previous()
        value = None
        if not self.check(TOKEN_TYPE.SEMICOLON): value = self.expression()
        self.consume(TOKEN_TYPE.SEMICOLON, "Expect ';' after return value")
        return STMT.Return(keyword, value)
    
    def expression_statement(self) -> STMT.Expression:
        """Parses an expression.

        Returns:
            STMT.Expression: returns an expression node.
        """
        expr = self.expression()
        self.consume(TOKEN_TYPE.SEMICOLON, "Expect ';' after expression.")
        return STMT.Expression(expr)
    
    def function(self, kind: str) -> STMT.Function:
        """Parses a function block.

        Args:
            kind (str): "function" or "method".

        Returns:
            STMT.Function: returns a function block node.
        """
        name = self.consume(TOKEN_TYPE.IDENTIFIER, "Expect {} name".format(kind))
        self.consume(TOKEN_TYPE.LEFT_PAREN, "Expect '(' after {} name.".format(kind))
        parameters = []
        
        # parameters parsing.
        if not self.check(TOKEN_TYPE.RIGHT_PAREN):
            parameters.append(self.consume(TOKEN_TYPE.IDENTIFIER, "Expect parameter name."))
            while self.match(TOKEN_TYPE.COMA):
                if len(parameters) >= 255: self.error(self.peek(), "Can't have more than 255 parameters.")
                parameters.append(self.consume(TOKEN_TYPE.IDENTIFIER, "Expect parameter name."))

        self.consume(TOKEN_TYPE.RIGHT_PAREN, "Expect ')' after parameters.")
        self.consume(TOKEN_TYPE.LEFT_BRACE, "Expect '{' before "+ str(kind) +" body.")  ## Marking line [format string wired behaviour "Expcet '{' before {} body".format(kind)]
        body = self.block()
        return STMT.Function(name, parameters, body)
            
    def block(self) -> List:
        """Handles a block parsing.

        Returns:
            List: returns a list of statements embedded in a block.
        """
        statements = []
        while not self.check(TOKEN_TYPE.RIGHT_BRACE) and not self.isAtEnd(): statements.append(self.declaration())
        self.consume(TOKEN_TYPE.RIGHT_BRACE, "Expect } after block.")
        return statements
    
    def assignment(self):
        """Handles assignment operators expressions"""
        expr = self._or()
        if self.match(TOKEN_TYPE.EQUAL):
            equals = self.previous()
            value = self.assignment()
            if type(expr) == EXPR.Variable: return EXPR.Assign(expr.name, value)
            elif type(expr) == EXPR.Get: return EXPR.Set(expr.object, expr.name, value)
            self.error(equals, "Invalid assignment target")
        return expr
    
    def _or(self) -> EXPR.Logical:
        """Parses OR experssion.

        Returns:
            EXPR.Logical: Returns OR expresssion node.
        """
        expr = self._and()
        while self.match(TOKEN_TYPE.OR):
            operator = self.previous()
            right = self._and()
            expr = EXPR.Logical(expr, operator, right)
        return expr
    
    def _and(self) -> EXPR.Logical:
        """Parses AND expression.

        Returns:
            EXPR.Logical: Returns AND expression node.
        """
        expr = self.equality()
        while self.match(TOKEN_TYPE.AND):
            operator = self.previous()
            right = self.equality()
            expr = EXPR.Logical(expr, operator, right)
        return expr
    
    def expression(self):
        """Parses an expression"""
        return self.assignment()
    
    def equality(self) -> EXPR.Binary:
        """Parses equality expression.

        Returns:
            EXPR.Binary: returns equality expression node.
        """
        expr = self.comparison()
        while(self.match(TOKEN_TYPE.BANG_EQUAL, TOKEN_TYPE.EQUAL_EQUAL)):
            operator = self.previous()
            right = self.comparison()
            expr = EXPR.Binary(expr, operator, right)
        return expr
    
    def comparison(self) -> EXPR.Binary:
        """Parses comparsion expression.

        Returns:
            EXPR.Binary: returns a comparision node.
        """
        expr = self.term()
        while (self.match(TOKEN_TYPE.GREATER, TOKEN_TYPE.GREATER_EQUAL, TOKEN_TYPE.LESS, TOKEN_TYPE.LESS_EQUAL)):
            operator = self.previous()
            right = self.term()
            expr = EXPR.Binary(expr, operator, right)
        return expr
    
    def term(self) -> EXPR.Binary:
        """Parses term expresion.

        Returns:
            EXPR.Binary: returns a term node.
        """
        expr = self.factor()
        while self.match(TOKEN_TYPE.MINUS, TOKEN_TYPE.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = EXPR.Binary(expr, operator, right)
        return expr
    
    def factor(self) -> EXPR.Binary:
        """Parses factor expression.

        Returns:
            EXPR.Binary: returns factor node.
        """
        expr = self.unary()
        while self.match(TOKEN_TYPE.SLASH, TOKEN_TYPE.STAR):
            operator = self.previous()
            right = self.unary()
            expr = EXPR.Binary(expr, operator, right)
        return expr
    
    def unary(self) -> EXPR.Unary:
        """Parses unary expression.

        Returns:
            EXPR.Unary: returns unary expression node.
        """
        if self.match(TOKEN_TYPE.BANG, TOKEN_TYPE.MINUS):
            operator = self.previous()
            right = self.unary()
            return EXPR.Unary(operator, right)
        return self.call()
    
    def call(self) -> EXPR.Get:
        """Parses call expression of an object, like function calls and reading properties.

        Returns:
            EXPR.Call: returns a get node.
        """
        expr = self.primary()
        while True:
            if self.match(TOKEN_TYPE.LEFT_PAREN): expr = self.finish_call(expr)
            elif self.match(TOKEN_TYPE.DOT):
                name = self.consume(TOKEN_TYPE.IDENTIFIER, "Expect property name after '.'.")
                expr = EXPR.Get(expr, name)
            else: break
        return expr
    
    def finish_call(self, callee) -> EXPR.Call:
        """Parses a call expression.

        Args:
            callee (_type_): the callee object to be called

        Returns:
            EXPR.Call: returns a call node.
        """
        # parsing arguments
        arguments = []
        if not self.check(TOKEN_TYPE.RIGHT_PAREN):
            arguments.append(self.expression())
            while self.match(TOKEN_TYPE.COMA):
                if len(arguments) >= 255:   self.error(self.peek(), "Can't have more than 255 arguments.")
                arguments.append(self.expression())
        paren = self.consume(TOKEN_TYPE.RIGHT_PAREN, "Expect ')' after arguments.")
        return EXPR.Call(callee, paren, arguments)
    
    def primary(self):
        """Parses primary expressions such as literals, identifiers and expressions.

        Raises:
            self.error: if nothing is matched.

        Returns:
            EXPR | STMT : returns a node of the parsed object.
        """
        
        # Literals
        if self.match(TOKEN_TYPE.FALSE): return EXPR.Literal(False)
        if self.match(TOKEN_TYPE.TRUE): return EXPR.Literal(True)
        if self.match(TOKEN_TYPE.NIL): return EXPR.Literal(None)
        if self.match(TOKEN_TYPE.NUMBER, TOKEN_TYPE.STRING): return EXPR.Literal(self.previous().literal)
        
        # Class objects
        if self.match(TOKEN_TYPE.SUPER):
            keyword = self.previous()
            self.consume(TOKEN_TYPE.DOT, "Expect '.' after 'super'.")
            method = self.consume(TOKEN_TYPE.IDENTIFIER, "Expect superclass method name")
            return EXPR.Super(keyword, method)
        if self.match(TOKEN_TYPE.THIS): return EXPR.This(self.previous())
        
        if self.match(TOKEN_TYPE.IDENTIFIER): return EXPR.Variable(self.previous())
        
        if self.match(TOKEN_TYPE.LEFT_PAREN):
            expr = self.expression()
            self.consume(TOKEN_TYPE.RIGHT_PAREN, "Expect ')' after expression.")
            return EXPR.Grouping(expr)
        
        raise self.error(self.peek(), "Expect expression.")
    
    def match(self, *args) -> bool:
        """Matches the passed args with the current pointing token.

        Returns:
            bool: returns True if matched with the current token, else False
        """
        for i in args:
            if (self.check(i)):
                self.advance()
                return True
        return False
    
    def check(self, type: TOKEN_TYPE) -> bool:
        """Checks the type of the token

        Args:
            type (TOKEN_TYPE): expected type of the token

        Returns:
            bool: returns true if the type matched.
        """
        if self.isAtEnd(): return False
        return self.peek().type == type
    
    def advance(self):
        """Advances the token from the tokens list"""
        if not self.isAtEnd(): self.current +=1
        return self.previous()
    
    def isAtEnd(self) -> bool:
        """Checks it the parser has reached the end of tokens.

        Returns:
            bool: returs True if it reaches end, else False.
        """
        return self.peek().type == "EOF"
    
    def peek(self) -> Token:
        """Peeks the list and returns the current token.

        Returns:
            Token: The current pointing token.
        """
        return self.tokens[self.current]

    def previous(self) -> Token:
        """Previous token to the current token pointing.

        Returns:
            Token: one before token.
        """
        return self.tokens[self.current -1]
    
    def synchronize(self):
        """Syncs the tokens untils a certain node is parsed"""
        self.advance()
        while not self.isAtEnd():
            if (self.previous().type == TOKEN_TYPE.SEMICOLON): return
            if self.peek().type in ["CLASS", "FUN", "VAR", "FOR", "IF", "WHILE", "PRINT", "RETURN"]: return
            self.advance()

    def consume(self, type: TOKEN_TYPE, message: str):
        """checks and consumes the current token and advances the tokens from the list.

        Args:
            type (TOKEN_TYPE): The token type.
            message (str): Error message if not passed the check.

        Raises:
            self.error: if the check is not passed it raises Parse error exception.
        """
        if self.check(type): return self.advance()
        raise self.error(self.peek(), message)
    
    def error(self, token: TOKEN_TYPE, message: str):
        """Handles the Error raised by the parser and reports to user.

        Args:
            token (TOKEN_TYPE): The token raised the exception.
            message (str): message of the error.
        """
        raise ParseError(message, token)


if __name__ == "__main__":
    pass