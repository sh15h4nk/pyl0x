"""This class raises Run time errors"""

class runtime_error(Exception):
    def __init__(self, token, message):
        super().__init__(message)
        self.token = token

class ParseError(Exception):
    def __init__(self, message, token) -> None:
        super().__init__(message)
        self.token = token
        