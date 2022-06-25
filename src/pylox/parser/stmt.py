"""Node classes(stmt classes) definition"""
"""This is a generated file, from tools/generate_ast.py script"""

class Block:
	#Constructor
	def __init__(self, statements):
		self.statements = statements

	#Visitor Method
	def accept(self, visitor):
		return visitor.visit()

class Expression:
	#Constructor
	def __init__(self, expression):
		self.expression = expression

	#Visitor Method
	def accept(self, visitor):
		return visitor.visit()

class Print:
	#Constructor
	def __init__(self, expression):
		self.expression = expression

	#Visitor Method
	def accept(self, visitor):
		return visitor.visit()

class Var:
	#Constructor
	def __init__(self, name,initializer):
		self.name = name
		self.initializer = initializer

	#Visitor Method
	def accept(self, visitor):
		return visitor.visit()

