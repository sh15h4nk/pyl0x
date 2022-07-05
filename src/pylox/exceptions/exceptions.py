"""Base exceptions of the lox"""

from email import message


class SyntaxError(Exception):
    def __init__(self, line, char, message ) -> None:
        super().__init__(message)
        self.line = line
        self.char = char

class RuntimeError(Exception):
    def __init__(self, token, message) -> None:
        super().__init__(message)
        self.token = token

class ParseError(Exception):
    def __init__(self, token, message) -> None:
        super().__init__(message)
        self.token = token
        
