from typing import List
from pylox.interpreter.lox_callable import Lox_callable
from pylox.interpreter.lox_instance import LoxInstance
import pylox.parser.stmt as STMT
import pylox.interpreter.interpreter as interepreter
from pylox.environment.environment import Environment
from pylox.interpreter.function_return import function_return


class Lox_function(Lox_callable):
    def __init__(self, declaration: STMT.Function, closure: Environment, is_initializer: bool) -> None:
        self.declaration = declaration
        self.closure = closure
        self.is_initializer = is_initializer
    
    def arity(self) -> int:
        return len(self.declaration.params)
    
    def to_str(self) -> str:
        return "<fn {}>".format(self.declaration.name)
    
    def call(self, globals: Environment, arguments: List):
        env = Environment(self.closure)
        for i in range(len(self.declaration.params)):
            env.define(self.declaration.params[i], arguments[i])
                
        try:
            interepreter.execute_block(self.declaration.body, env)
        except function_return as return_value:
            if self.is_initializer: self.closure.get_at(0, "this")
            return return_value.value
        
        if self.is_initializer: return self.closure.get_at(0, "this")
        return None
    
    def bind(self, instance: LoxInstance):
        env = Environment(self.closure)
        env.define("this", instance)
        return Lox_function(self.declaration, env, self.is_initializer)
