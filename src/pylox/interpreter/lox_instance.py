

from pylox.exceptions.runtime_error import runtime_error
from pylox.scanner.token import Token


class LoxInstance:
    def __init__(self, klass) -> None:
        self.klass = klass
        self.fields = {}
    
    def get(self, name: Token):
        if name.lexeme in self.fields: return self.fields[name.lexeme]
        method = self.klass.find_method(name.lexeme)
        if method: return method.bind(self)
        raise runtime_error(name, "Undefied property {}.".format(name.lexeme))
    
    def set(self, name: Token, value):
        self.fields[name.lexeme] = value
    
    def __repr__(self) -> str:
        return str(self.klass.name) + " instance"