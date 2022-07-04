

from pylox.interpreter.lox_callable import Lox_callable
from pylox.interpreter.lox_function import Lox_function
from pylox.interpreter.lox_instance import LoxInstance


class LoxClass(Lox_callable):
    def __init__(self, name, methods: dict) -> None:
        self.name = name
        self.methods: dict = methods
        
    def call(self, env, arguments):
        instance = LoxInstance(self)
        initializer: Lox_function = self.find_method("init")
        if initializer: initializer.bind(instance).call(env, arguments)
        return instance
    
    def find_method(self, name):
        if name in self.methods: return self.methods[name]
        return None
    
    def arity(self):
        initializer: Lox_function = self.find_method("init")
        if initializer: return initializer.arity()
        return 0
    
    def __repr__(self) -> str:
        return str(self.name)