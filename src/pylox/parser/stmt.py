"""Node classes(stmt classes) definition"""
"""This is a generated file, from tools/generate_ast.py script"""

class Block:
	#Constructor
	def __init__(self, statements):
		self.statements = statements

	#Visitor Method
	def accept(self, visitor):
		return visitor.visit()

class Class:
	#Constructor
	def __init__(self, name,methods):
		self.name = name
		self.methods = methods

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

class Function:
	#Constructor
	def __init__(self, name,params,body):
		self.name = name
		self.params = params
		self.body = body

	#Visitor Method
	def accept(self, visitor):
		return visitor.visit()

class If:
	#Constructor
	def __init__(self, condition,thenBranch,elseBranch):
		self.condition = condition
		self.thenBranch = thenBranch
		self.elseBranch = elseBranch

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

class Return:
	#Constructor
	def __init__(self, keyword,value):
		self.keyword = keyword
		self.value = value

	#Visitor Method
	def accept(self, visitor):
		return visitor.visit()

class While:
	#Constructor
	def __init__(self, condition,body):
		self.condition = condition
		self.body = body

	#Visitor Method
	def accept(self, visitor):
		return visitor.visit()

