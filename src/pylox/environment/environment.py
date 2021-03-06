"""This class holds the structure of the environment(state) where the variables are stored in a dictionary

    Raises:
        RuntimeError: In get() function if it encounters getting a undefined variable
        RuntimeError: In assign() function if it encounters assigning a undefined variable

    Returns:
        Environment: The state enclosed in a scope
"""
from pylox.exceptions.exceptions import RuntimeError
from pylox.scanner.token import Token

class Environment:
    """This class holds the environment of the program"""
    def __init__(self, enclose = None) -> None:
        """Initializing the environment

        Args:
            enclose (Environment, optional): Environment to enclose. Defaults to None.
        """
        self.enclosing = enclose
        self.values = dict()
    
    def __repr__(self) -> str:
        return str(self.values)
    
    def get(self, name: Token):
        """To get a value of an identifier from the envorinment.

        Args:
            name (Token): token of the identifier.

        Raises:
            RuntimeError: if the name is not found in the env as well as in the enclosing env.
        """
        if type(name) is str: name = Token(None, name, None, None)
        if name.lexeme in self.values:
            return self.values.get(name.lexeme)
        if self.enclosing is not None: return self.enclosing.get(name)
        raise RuntimeError(name, "Undefined variable '" + name.lexeme + "'.")
    
    def assign(self, name: Token, value) -> None:
        """To assign a value to the identifier in the environment.

        Args:
            name (Token): token of the identifier.
            value: value to assign.

        Raises:
            RuntimeError: if the identifier is not defined in the env, as well as in the enclosing env.
        """
        if type(name) is str: name = Token(None, name, None, None)
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return
        raise RuntimeError(name, "Undefined variable '"+ name.lexeme + "'.")
    
    def define(self, name: Token, value) -> None:
        """Defines a indentifier in the environment.

        Args:
            name (Token): token of the identifier.
            value : value of the identifier.
        """
        if type(name) is str: name = Token(None, name, None, None)
        self.values.update({name.lexeme: value})
    
    def ancestor(self, distance: int):
        """Getting the enclosed environment at a distance.

        Args:
            distance (int): distance of the enclosed env from the current env.

        Returns:
            Environment: returns the enclosed env at a the given distance.
        """
        environment = self
        for i in range(distance):
            environment = environment.enclosing
        return environment
        
    def get_at(self, distance: int, name: Token):
        """Getting a value from an environment at the given distance.

        Args:
            distance (int): distance of the enclosed env.
            name (Token): name of the identifier to get.

        Returns:
            value: returns the value of the name at the given enclosed env distace.
        """
        if type(name) is str: name = Token(None, name, None, None)
        return self.ancestor(distance).values.get(name.lexeme)
    
    def assign_at(self, distance: int, name: Token, value) -> None:
        """Assigning a value to the environment at the given distance.

        Args:
            distance (int): distance of the enclosed env.
            name (Token): name of the identifier to assign.
            value (_type_): value to the identifier to assign.
        """
        if type(name) is str: name = Token(None, name, None, None)
        self.ancestor(distance).values[name.lexeme] = value
