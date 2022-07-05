"""Interface for lox class instances (objects)"""

from pylox.exceptions.exceptions import RuntimeError
from pylox.scanner.token import Token


class LoxInstance:
    """Instance of lox classes"""
    def __init__(self, klass) -> None:
        """Intialization of class and fields"""
        self.klass = klass
        self.fields = {}
    
    def get(self, name: Token):
        """For getting the value of a property.

        Args:
            name (Token): the token of the property.

        Raises:
            RuntimeError: if the property is not defined in the class.
        """
        if name.lexeme in self.fields: return self.fields[name.lexeme]
        method = self.klass.find_method(name.lexeme)
        if method: return method.bind(self)
        raise RuntimeError(name, "Undefied property {}.".format(name.lexeme))
    
    def set(self, name: Token, value) -> None:
        """Sets the property of a field"""
        self.fields[name.lexeme] = value
    
    def __repr__(self) -> str:
        return str(self.klass.name) + " instance"