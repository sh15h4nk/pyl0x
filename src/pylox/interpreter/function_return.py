"""Function return class: Derived from exception"""

class FunctionReturn(Exception):
    def __init__(self, value):
        self.value = value
        