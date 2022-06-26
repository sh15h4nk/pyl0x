
from pylox.exceptions.runtime_error import runtime_error


class Environment:
    values = dict()
    enclosing = None
    
    def __init__(self, enclose = None):
        self.enclosing = enclose
        
    
    def get(self, name):
        if name.lexeme in self.values:
            return self.values.get(name.lexeme)
        if self.enclosing is not None: return self.enclosing.get(name)
        raise runtime_error(name, "Undefined variable '" + name.lexeme + "'.")
    
    def assign(self, name, value):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return
        raise runtime_error(name, "Undefined variable '"+ name.lexeme + "'.")
    
    def define(self, name, value):
        self.values.update({name.lexeme: value})
