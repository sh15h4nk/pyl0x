"""LoxFunction class holds the interface of a lox class object"""

from typing import List
from pylox.interpreter.lox_callable import LoxCallable
from pylox.interpreter.lox_instance import LoxInstance
import pylox.parser.stmt as STMT
import pylox.interpreter.interpreter as interepreter
from pylox.environment.environment import Environment
from pylox.interpreter.function_return import FunctionReturn

class LoxFunction(LoxCallable):
    """Class which provides interface to lox functions while evaluation"""
    def __init__(self, declaration: STMT.Function, closure: Environment, is_initializer: bool) -> None:
        """Initialization of lox function.

        Args:
            declaration (STMT.Function): function declaration.
            closure (Environment): The enviroment which is bounded to the function (scope env).
            is_initializer (bool): if the function is initializer or not.
        """
        self.declaration = declaration
        self.closure = closure
        self.is_initializer = is_initializer
    
    def arity(self) -> int:
        """Returns the lenght of the required parameters"""
        return len(self.declaration.params)
    
    def __repr__(self) -> str:
        return "<fn {}>".format(self.declaration.name)
    
    def bind(self, instance: LoxInstance):
        """Binds the given interface to a function"""
        env = Environment(self.closure)
        env.define("this", instance)
        return LoxFunction(self.declaration, env, self.is_initializer)
    
    def call(self, globals: Environment, arguments: List):
        """The call interface of the lox function.

        Args:
            globals (Environment): the scope env.
            arguments (List): arguments to the function call.
        """
        env = Environment(self.closure)
        for i in range(len(self.declaration.params)):
            env.define(self.declaration.params[i], arguments[i])
                
        try:
            interepreter.execute_block(self.declaration.body, env)
        except FunctionReturn as return_value:
            if self.is_initializer: self.closure.get_at(0, "this")
            return return_value.value
        
        if self.is_initializer: return self.closure.get_at(0, "this")
        return None
    
    
