"""Node classes(expr classes) definition"""
"""This is a generated file, from tools/generate_ast.py script"""

class Assign:
	#Constructor
	def __init__(self, name,value):
		self.name = name
		self.value = value

	#Visitor Method
	def accept(self, visitor):
		return visitor.visit()

class Binary:
	#Constructor
	def __init__(self, left,operator,right):
		self.left = left
		self.operator = operator
		self.right = right

	#Visitor Method
	def accept(self, visitor):
		return visitor.visit()

class Call:
	#Constructor
	def __init__(self, callee,paren,arguments):
		self.callee = callee
		self.paren = paren
		self.arguments = arguments

	#Visitor Method
	def accept(self, visitor):
		return visitor.visit()

class Get:
	#Constructor
	def __init__(self, object,name):
		self.object = object
		self.name = name

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

class Logical:
	#Constructor
	def __init__(self, left,operator,right):
		self.left = left
		self.operator = operator
		self.right = right

	#Visitor Method
	def accept(self, visitor):
		return visitor.visit()

class Set:
	#Constructor
	def __init__(self, object,name,value):
		self.object = object
		self.name = name
		self.value = value

	#Visitor Method
	def accept(self, visitor):
		return visitor.visit()

class This:
	#Constructor
	def __init__(self, keyword):
		self.keyword = keyword

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

class Variable:
	#Constructor
	def __init__(self, name):
		self.name = name

	#Visitor Method
	def accept(self, visitor):
		return visitor.visit()

