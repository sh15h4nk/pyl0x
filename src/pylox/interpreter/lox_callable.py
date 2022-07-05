"""LoxCallable is an interface for a callable lox object"""

class LoxCallable:
    def arity(self):
        pass
    def call(self, globals, arguments):
        pass
    def __repr__(self):
        return "<native fn>"
    