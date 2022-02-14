"""Node classes(expression classes) definition"""
"""This is a generated file, from tools/generate_ast.py script"""

class Binary:
	#Constructor
	def __init__(self, left,operator,right):
		self.left = left
		self.operator = operator
		self.right = right

	#Visitor Method
	def accept(self, visitor):
		return visitor.visit()

class Grouping:
	#Constructor
	def __init__(self, expression):
		self.expression = expression

	#Visitor Method
	def accept(self, visitor):
		return visitor.visit()

class Literal:
	#Constructor
	def __init__(self, value):
		self.value = value

	#Visitor Method
	def accept(self, visitor):
		return visitor.visit()

class Unary:
	#Constructor
	def __init__(self, operator,right):
		self.operator = operator
		self.right = right

	#Visitor Method
	def accept(self, visitor):
		return visitor.visit()

