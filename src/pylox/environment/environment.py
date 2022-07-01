"""This class holds the structure of the environment(state) where the variables are stored in a dictionary

    Raises:
        runtime_error: In get() function if it encounters getting a undefined variable
        runtime_error: In assign() function if it encounters assigning a undefined variable

    Returns:
        Environment: The state enclosed in a scope
"""
from pylox.exceptions.runtime_error import runtime_error
from pylox.scanner.token import token

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
    
    def define(self, name, value) -> None:
        self.values.update({name.lexeme: value})
    
    def ancestor(self, distance: int):
        environment = self
        for i in range(distance):
            environment = environment.enclosing
        return environment
        
    def get_at(self, distance: int, name: token):
        return self.ancestor(distance).values.get(name.lexeme)
    
    def assign_at(self, distance: int, name: token, value) -> None:
        self.ancestor(distance).values[name.lexeme] = value
