
from pylox.exceptions.runtime_error import runtime_error

class Environment:
    enclosing = None
    
    def __init__(self, enclose = None) -> None:
        self.enclosing = enclose
        self.values = dict()
    
    def __repr__(self) -> str:
        return str(self.values)
        
    
    def get(self, name):
        if name.lexeme in self.values:
            return self.values.get(name.lexeme)
        if self.enclosing is not None: return self.enclosing.get(name)
        raise runtime_error(name, "Undefined variable '" + name.lexeme + "'.")
    
    def assign(self, name, value) -> None:
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return
        raise runtime_error(name, "Undefined variable '"+ name.lexeme + "'.")
    
    def define(self, name, value):
        self.values.update({name.lexeme: value})
