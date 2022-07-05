"""LoxClass holds the meta implementation of class operations"""

from pylox.interpreter.lox_callable import LoxCallable
from pylox.interpreter.lox_function import LoxFunction
from pylox.interpreter.lox_instance import LoxInstance
from pylox.environment.environment import Environment


class LoxClass(LoxCallable):
    """Used to evaluate the classes"""
    def __init__(self, name, superclass, methods: dict) -> None:
        """Initilizes the class object.

        Args:
            name: name of the class
            superclass: super class if any
            methods (dict): methods of the class
        """
        self.name = name
        self.superclass = superclass
        self.methods: dict = methods
        
    def call(self, env: Environment, arguments) -> LoxInstance:
        """Calling the class to create an instance

        Args:
            env (Environment): Environment for the call operation.
            arguments: arguments to the constructor of the class.

        Returns:
            LoxInstance: returns the instance.
        """
        instance = LoxInstance(self)
        initializer: LoxFunction = self.find_method("init")
        if initializer: initializer.bind(instance).call(env, arguments)
        return instance
    
    def find_method(self, name):
        """To find the method in the class.

        Args:
            name: name of the method

        Returns:
            method: either method or None
        """
        if name in self.methods: return self.methods[name]
        if self.superclass: return self.superclass.find_method(name)
        return None
    
    def arity(self) -> int:
        """Return the length of the required arguments for the class constructor"""
        initializer: LoxFunction = self.find_method("init")
        if initializer: return initializer.arity()
        return 0
    
    def __repr__(self) -> str:
        return str(self.name)
    