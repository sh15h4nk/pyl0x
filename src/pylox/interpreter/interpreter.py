"""Lox Intepreter which interprets the parsed statements"""
import time
from typing import List, Optional
from pylox.interpreter.lox_function import LoxFunction
from pylox.interpreter.lox_instance import LoxInstance
import pylox.parser.expr as EXPR
import pylox.parser.stmt as STMT
from pylox.exceptions.exceptions import RuntimeError
from pylox.environment.environment import Environment
from pylox.interpreter.lox_callable import LoxCallable
from pylox.interpreter.function_return import FunctionReturn
from pylox.scanner.token import Token
from pylox.interpreter.lox_class import LoxClass


# State of the interpreter
globals = Environment()
env = globals
locals = {}

def visit_while_stmt(stmt: STMT.While) -> None:
    """Evaluates the while statement.

    Args:
        stmt (STMT.While): While node.
    """
    while is_truthy(evaluate(stmt.condition)): execute(stmt.body)
    return None

def visit_if_stmt(stmt: STMT.If) -> None:
    """Evaluates the if statement with else clause.

    Args:
        stmt (STMT.If): If block node.
    """
    if is_truthy(evaluate(stmt.condition)):
        execute(stmt.thenBranch)
    elif stmt.elseBranch is not None:
        execute(stmt.elseBranch)
    return None

def visit_var_stmt(stmt: STMT.Var) -> None:
    """Evaluates the var statment.

    Args:
        stmt (STMT.Var): The Var node.
    """
    value = None
    if stmt.initializer: value = evaluate(stmt.initializer)
    env.define(stmt.name, value)
    return None

def visit_expression_stmt(stmt: STMT.Expression) -> None:
    """Evaluates an expression statement.

    Args:
        stmt (STMT.Expression): Expression node.
    """
    evaluate(stmt.expression)
    return None

def visit_function_stmt(stmt: STMT.Function) -> None:
    """Evaluates a function statement.

    Args:
        stmt (STMT.Function): Function node.
    """
    function = LoxFunction(stmt, env, False)
    env.define(stmt.name, function)
    return None

def visit_print_stmt(stmt: STMT.Print) -> None:
    """Evaluates a print statement and prints to console.

    Args:
        stmt (STMT.Print): print node.
    """
    value = evaluate(stmt.expression)
    print(stringify(value))
    return None

def visit_return_stmt(stmt: STMT.Return) -> None:
    """Evaluate a returns statement.

    Args:
        stmt (STMT.Return): Return node.
    """
    value = None
    if stmt.value: value = evaluate(stmt.value)
    raise FunctionReturn(value)

def visit_class_stmt(stmt: STMT.Class) -> None:
    """Evaluates a class statement.

    Args:
        stmt (STMT.Class): class node.
    """
    global env
    
    # super class evaluation.
    superclass = None
    if stmt.superclass:
        superclass = evaluate(stmt.superclass)
        if type(superclass) is not LoxClass: raise RuntimeError(stmt.superclass.name, "Superclass must be a class.")
    
    env.define(stmt.name, None)
    
    # super class assignment.
    if stmt.superclass:
        env = Environment(env)
        env.define("super", superclass)
    
    # Class methods evaluation.
    methods = {}
    for method in stmt.methods:
        function = LoxFunction(method, env, method.name.lexeme == "init")
        methods[method.name.lexeme] = function
    
    klass = LoxClass(stmt.name.lexeme, superclass, methods)
    
    if superclass:
        env = env.enclosing
    
    env.assign(stmt.name, klass)
    
def visit_block_stmt(stmt: STMT.Block) -> None:
    """Evaluates a block consisting of statements.

    Args:
        stmt (STMT.Block): Block node.
    """
    execute_block(stmt.statements, Environment(enclose=env))
    return None

def visit_logical_expr(expr: EXPR.Logical):
    """Evaluates a logical expression.

    Args:
        expr (EXPR.Logical): Logical expression node.
    """
    left = evaluate(expr.left)
    if expr.operator.type == "OR":
        if is_truthy(left): return left
    else:
        if not is_truthy(left): return left
    return evaluate(expr.right)

def visit_assign_expr(expr: EXPR.Assign):
    """Evaluates a assignment expression.

    Args:
        expr (EXPR.Assign): Expression node.
    """
    value = evaluate(expr.value)
    dist = locals.get(expr)
    if dist: env.assign_at(dist, expr.name, value)
    else: globals.assign(expr.name, value)
    return value

def visit_this_expr(expr: EXPR.This):
    """Evaluates this expression and looks up the variable"""
    return look_up_variable(expr.keyword, expr)

def visit_super_expr(expr: EXPR.Super):
    """Evaluates the super expression and binds the superclass"""
    dist = locals.get(expr)
    superclass = env.get_at(dist, "super")
    object = env.get_at(dist - 1, "this")
    
    method = superclass.find_method(expr.method.lexeme)
    if not method: raise RuntimeError(expr.method, "Undefined property '{}'.".format(expr.method.lexeme))
    return method.bind(object)

def visit_variable_expr(expr: EXPR.Variable):
    """Evaluates a variable expression"""
    return look_up_variable(expr.name, expr)

def look_up_variable(name: Token, expr: EXPR):
    """Resolves the variable from the locals and globals"""
    dist = locals.get(expr)
    print("-"*50)
    print("Dist", dist, "NAme", name, locals)
    if dist is not None:
        return env.get_at(dist, name)
    else:
        return globals.get(name)

def visit_binary_expr(expr: EXPR.Binary):
    """Evaluates a binary expression.

    Args:
        expr (EXPR.Binary): Binary expression node.

    Raises:
        RuntimeError: if failed to evaluate the binary expression.
    """
    left = evaluate(expr.left)
    right = evaluate(expr.right)

    if expr.operator.type == "MINUS" and check_number_operands(expr.operator, left, right): return float(left) - float(right)
    elif expr.operator.type == "SLASH" and  check_number_operands(expr.operator, left, right): return float(left) / float(right)
    elif expr.operator.type == "STAR" and check_number_operands(expr.operator, left, right): return float(left) * float(right)

    elif expr.operator.type == "PLUS":
        if is_float(left) and is_float(right): return float(left) + float(right)
        if type(left) is str and type(right) is str : return str(left+right)
        raise RuntimeError(expr.operand, "Operands must be two numbers or two strings.")
    
    elif expr.operator.type == "GREATER" and check_number_operands(expr.operator, left, right): return float(left) > float(right)
    elif expr.operator.type == "GREATER_EQUAL" and check_number_operands(expr.operator, left, right): return float(left) >= float(right)
    elif expr.operator.type == "LESS" and check_number_operands(expr.operator, left, right): return float(left) < float(right)
    elif expr.operator.type == "LESS_EQUAL" and check_number_operands(expr.operator, left, right): return float(left) <= float(right)

    elif expr.operator.type == "BANG_EQUAL": return not is_equal(left, right)
    elif expr.operator.type == "EQUAL_EQUAL": return is_equal(left, right)

    return None

def visit_call_expr(expr: EXPR.Call):
    """Evaluates a call expression.

    Args:
        expr (EXPR.Call): Call expression node.

    Raises:
        RuntimeError: if the expression is not callable.
        RuntimeError: if the length of args mismatch.
    """
    callee = evaluate(expr.callee)
    arguments = [evaluate(arg) for arg in expr.arguments]
    if not isinstance(callee, LoxCallable):
        raise RuntimeError(expr.paren, "Can only call functions and classes.")
    function = callee
    if len(arguments) != function.arity():
        raise RuntimeError(expr.paren, "Expected {} arguments but got {}.".format(function.arity(), len(arguments)))

    return function.call(globals, arguments)

def visit_get_expr(expr: EXPR.Get):
    """Evaluates a Get expression.

    Args:
        expr (EXPR.Get): Get expression node.

    Raises:
        RuntimeError: if the object is not an instance.
    """
    object = evaluate(expr.object)
    if type(object) is LoxInstance: return object.get(expr.name)
    raise RuntimeError(expr.name, "Only instances have property")

def visit_set_expr(expr: EXPR.Set):
    """Evaluates a Set expression.

    Args:
        expr (EXPR.Set): Set expression node.

    Raises:
        RuntimeError: if the object is not an instance.
    """
    object = evaluate(expr.object)
    if type(object) is not LoxInstance: raise RuntimeError(expr.name, "Only instances have fields")
    
    value = evaluate(expr.value)
    object.set(expr.name, value)
    return value

def visit_unary_expr(expr: EXPR.Unary):
    """Evaluates a unary expression.

    Args:
        expr (EXPR.Unary): Unary expression node.
    """
    right = evaluate(expr.right)
    if expr.operator.type == "MINUS" and check_number_operand(expr.operator, right): return -right
    elif expr.operator.type == "BANG": return not is_truthy(right)

    return None

def check_number_operands(operator, left, right) -> Optional[bool]:
    """Checks if the operands are float points.

    Args:
        operator (_type_): The operator of the binary expression.
        left: left operand.
        right: right operand.

    Raises:
        RuntimeError: if the operands aren't float points.

    Returns:
        Optional[bool]: returns true if both the operands can be converted to float.
    """
    if is_float(left) and is_float(right): return True
    raise RuntimeError(operator, "Operands must be numbers.")

def check_number_operand(operator, operand) -> bool:
    """Checks if the operand is number.

    Args:
        operator: The opeartor.
        operand: and the operand which is operating on.

    Raises:
        RuntimeError: if the operand is not a digit.
    """
    if operand.isdigit(): return True
    raise RuntimeError(operator, "Operand must be a number.")

def visit_grouping_expr(expr: EXPR.Grouping):
    """Evaluates a Grouping expression"""
    return evaluate(expr.expression)

def visit_literal_expr(expr: EXPR.Literal):
    """Evaluates a literal"""
    return expr.value

def is_truthy(obj) -> bool:
    """Checks the truth value of an object"""
    if obj is None: return False
    return bool(obj)

def is_equal(a, b) -> bool:
    """Checks if a and b are equal or not"""
    if a is None and b is None: return True
    if a is None: return False
    return a == b

def is_float(n) -> bool:
    """Checks if n is float or not"""
    try:
        f = float(n)
        return True
    except:
        return False

def stringify(obj) -> str:
    """Converts the object into string and returns"""
    if obj is None: return "nil"
    if is_float(obj) and str(obj).endswith(".0"): return str(obj)[:-2]
    return str(obj)

def evaluate(expr):
    """Evaluates an expression"""
    # calls the accept method on the visitor's class.
    return expr.accept(expr)

def execute(stmt):
    """Executes a statement"""
    stmt.accept(stmt)
    
def resolve(expr: EXPR, depth: int) -> None:
    """Resolves a local, global objects and assigns a depth.

    Args:
        expr (EXPR): object expession.
        depth (int): depth of the expression.
    """
    locals[expr] = depth

def execute_block(statements: List, _env: Environment):
    """Executes a block of statements with the provided environment.

    Args:
        statements (List): statements to execute.
        _env (Environment): the binded environment.
    """
    global env
    
    # storing the current env
    previous_env = env
    env = _env
    try:
        for stmt in statements:
            execute(stmt)
    finally:
        # restoring the previous env
        env = previous_env

def interpret(statements: List):
    # assigning visitor method to the visitor's classes
    EXPR.Assign.visit = visit_assign_expr
    EXPR.Binary.visit = visit_binary_expr
    EXPR.Call.visit = visit_call_expr
    EXPR.Get.visit = visit_get_expr
    EXPR.Grouping.visit = visit_grouping_expr
    EXPR.Literal.visit = visit_literal_expr
    EXPR.Set.visit = visit_set_expr
    EXPR.Super.visit = visit_super_expr
    EXPR.This.visit = visit_this_expr
    EXPR.Unary.visit = visit_unary_expr
    EXPR.Variable.visit = visit_variable_expr
    EXPR.Logical.visit = visit_logical_expr

    STMT.Expression.visit = visit_expression_stmt
    STMT.Class.visit = visit_class_stmt
    STMT.Return.visit = visit_return_stmt
    STMT.Function.visit = visit_function_stmt
    STMT.Print.visit = visit_print_stmt
    STMT.Var.visit = visit_var_stmt
    STMT.Block.visit = visit_block_stmt
    STMT.If.visit = visit_if_stmt
    STMT.While.visit = visit_while_stmt
    
    def c_arity():
        return 0
    def c_call(interepreter, globals):
        return time.time()
        
    clock_object = LoxCallable()
    clock_object.arity = c_arity
    clock_object.call = c_call
    globals.define("clock",clock_object)
    
    print("locc", locals)
    
    
    
    # Executing statement by statement
    for stmt in statements:
        execute(stmt)
    