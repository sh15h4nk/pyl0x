"""Node classes(stmt classes) definition"""
"""This is a generated file, from tools/generate_ast.py script"""

class Expression:
	#Constructor
	def __init__(self, expression):
		self.expression = expression

	#Visitor Method
	def accept(self, visitor):
		return visitor.visit()
	
	#Repr
	def __repr__(self) -> str:
		return "{}".format(self.expression)

class Print:
	#Constructor
	def __init__(self, expression):
		self.expression = expression

	#Visitor Method
	def accept(self, visitor):
		return visitor.visit()

	#Repr
	def __repr__(self) -> str:
		return "{}".format(self.expression)

