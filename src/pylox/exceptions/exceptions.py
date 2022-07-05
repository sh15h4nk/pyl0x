"""This class raises Run time errors"""

class SyntaxError(Exception):
    def __init__(self, *args: object) -> None:
        pass

class RuntimeError(Exception):
    def __init__(self, token, message):
        super().__init__(message)
        self.token = token

class ParseError(Exception):
    def __init__(self, message, token) -> None:
        super().__init__(message)
        self.token = token
        
class ResolveError(Exception):
    def __init__(self, *args: object) -> None:
        pass
