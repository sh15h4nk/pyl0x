from threading import local
import time
from pylox.interpreter.lox_function import Lox_function
from pylox.interpreter.lox_instance import LoxInstance
import pylox.parser.expr as EXP
import pylox.parser.stmt as STMT
from pylox.exceptions.runtime_error import runtime_error
from pylox.error_reporter import run_time_error
from pylox.environment.environment import Environment
from pylox.interpreter.lox_callable import Lox_callable
from pylox.interpreter.function_return import function_return
from pylox.scanner.token import token
from pylox.interpreter.lox_class import LoxClass

globals = Environment()
env = globals
locals = {}


def visit_while_stmt(stmt):
    while is_truthy(evaluate(stmt.condition)): execute(stmt.body)
    return None

def visit_logical_expr(expr):
    left = evaluate(expr.left)
    if expr.operator.type == "OR":
        if is_truthy(left): return left
    else:
        if not is_truthy(left): return left
    return evaluate(expr.right)

def visit_if_stmt(stmt):
    if is_truthy(evaluate(stmt.condition)):
        execute(stmt.thenBranch)
    elif stmt.elseBranch is not None:
        execute(stmt.elseBranch)
    return None

def visit_assign_expr(expr):
    value = evaluate(expr.value)
    
    dist = locals.get(expr)
    if dist: env.assign_at(dist, expr.name, value)
    else: globals.assign(expr.name, value)
    return value

def visit_var_stmt(stmt):
    value = None
    if stmt.initializer: value = evaluate(stmt.initializer)
    env.define(stmt.name, value)
    return None

def visit_variable_expr(expr):
    return look_up_variable(expr.name, expr)

def look_up_variable(name: token, expr: EXP):
    dist = locals.get(expr)
    if dist is not None:
        return env.get_at(dist, name)
    else:
        return globals.get(name)

def visit_expression_stmt(stmt):
    evaluate(stmt.expression)
    return None

def visit_function_stmt(stmt):
    function = Lox_function(stmt, env, False)
    env.define(stmt.name, function)
    return None

def visit_print_stmt(stmt):
    value = evaluate(stmt.expression)
    print(stringify(value))
    return None

def visit_return_stmt(stmt):
    value = None
    if stmt.value: value = evaluate(stmt.value)
    raise function_return(value)


def visit_binary_expr(expr):
    left = evaluate(expr.left)
    right = evaluate(expr.right)

    if expr.operator.type == "MINUS" and check_number_operands(expr.operator, left, right): return float(left) - float(right)
    elif expr.operator.type == "SLASH" and  check_number_operands(expr.operator, left, right): return float(left) / float(right)
    elif expr.operator.type == "STAR" and check_number_operands(expr.operator, left, right): return float(left) * float(right)

    elif (expr.operator.type == "PLUS"):
        if(is_float(left) and is_float(right)): return float(left) + float(right)
        if(type(left) is str and type(right) is str): return str(left+right)
        raise runtime_error(expr.operand, "Operands must be two numbers or two strings.")
    
    elif expr.operator.type == "GREATER" and check_number_operands(expr.operator, left, right): return float(left) > float(right)
    elif expr.operator.type == "GREATER_EQUAL" and check_number_operands(expr.operator, left, right): return float(left) >= float(right)
    elif expr.operator.type == "LESS" and check_number_operands(expr.operator, left, right): return float(left) < float(right)
    elif expr.operator.type == "LESS_EQUAL" and check_number_operands(expr.operator, left, right): return float(left) <= float(right)

    elif (expr.operator.type == "BANG_EQUAL"): return not is_equal(left, right)
    elif (expr.operator.type == "EQUAL_EQUAL"): return is_equal(left, right)

    return None

def visit_call_expr(expr):
    callee = evaluate(expr.callee)
    arguments = [evaluate(arg) for arg in expr.arguments]
    if not isinstance(callee, Lox_callable):
        raise runtime_error(expr.paren, "Can only call functions and classes.")
    function = callee
    if len(arguments) != function.arity():
        raise runtime_error(expr.paren, "Expected {} arguments but got {}.".format(function.arity(), len(arguments)))

    return function.call(globals, arguments)

def visit_get_expr(expr: EXP.Get):
    object = evaluate(expr.object)
    if type(object) is LoxInstance: return object.get(expr.name)
    raise runtime_error(expr.name, "Only instances have property")

def visit_set_expr(expr: EXP.Set):
    object = evaluate(expr.object)
    if type(object) is not LoxInstance: raise runtime_error(expr.name, "Only instances have fields")
    
    value = evaluate(expr.value)
    object.set(expr.name, value)
    return value

def check_number_operands(operator, left, right):
    if is_float(left) and is_float(right): return True
    raise runtime_error(operator, "Operands must be numbers.")

def visit_unary_expr(expr):
    right = evaluate(expr.right)
    if expr.operator.type == "MINUS" and check_number_operand(expr.operator, right): return -right
    elif expr.operator.type == "BANG": return not is_truthy(right)

    return None

def check_number_operand(operator, operand):
    if operand.isdigit(): return True
    raise runtime_error(operator, "Operand must be a number.")


def visit_grouping_expr(expr):
    return evaluate(expr)

def evaluate(expr):
    return expr.accept(expr)


def visit_literal_expr(expr):
    return expr.value

def is_truthy(obj):
    if obj is None: return False
    return bool(obj)

def is_equal(a, b):
    if a is None and b is None: return True
    if a is None: return False
    return a == b

def is_float(n):
    try:
        f = float(n)
        return True
    except:
        return False

def stringify(obj):
    if obj is None: return "nil"
    if is_float(obj) and str(obj).endswith(".0"): return str(obj)[:-2]
    return str(obj)

def execute(stmt):
    stmt.accept(stmt)
    
def resolve(expr: EXP, depth: int):
    locals[expr] = depth
    
def visit_block_stmt(stmt):
    execute_block(stmt.statements, Environment(enclose=env))
    return None

def visit_class_stmt(stmt: STMT.Class):
    global env
    superclass = None
    if stmt.superclass:
        superclass = evaluate(stmt.superclass)
        if type(superclass) is not LoxClass: raise runtime_error(stmt.superclass.name, "Superclass must be a class.")
    env.define(stmt.name, None)
    
    if stmt.superclass:
        env = Environment(env)
        env.define("super", superclass)
    
    methods = {}
    for method in stmt.methods:
        function = Lox_function(method, env, method.name.lexeme == "init")
        methods[method.name.lexeme] = function
    
    klass = LoxClass(stmt.name.lexeme, superclass, methods)
    
    if superclass:
        env = env.enclosing
    
    env.assign(stmt.name, klass)
    
def visit_this_expr(expr: EXP.This):
    return look_up_variable(expr.keyword, expr)
    
def visit_super_expr(expr: EXP.Super):
    dist = locals.get(expr)
    superclass = env.get_at(dist, "super")
    object = env.get_at(dist - 1, "this")
    
    method = superclass.find_method(expr.method.lexeme)
    if not method: raise runtime_error(expr.method, "Undefined property '{}'.".format(expr.method.lexeme))
    return method.bind(object)

def execute_block(statements, _env):
    global env
    previous_env = env
    env = _env
    try:
        for stmt in statements:
            execute(stmt)
            
    finally:    
        env = previous_env

def interpret(statements):
    # assigning visitor method to the classes
    EXP.Assign.visit = visit_assign_expr
    EXP.Binary.visit = visit_binary_expr
    EXP.Call.visit = visit_call_expr
    EXP.Get.visit = visit_get_expr
    EXP.Grouping.visit = visit_grouping_expr
    EXP.Literal.visit = visit_literal_expr
    EXP.Set.visit = visit_set_expr
    EXP.Super.visit = visit_super_expr
    EXP.This.visit = visit_this_expr
    EXP.Unary.visit = visit_unary_expr
    EXP.Variable.visit = visit_variable_expr
    EXP.Logical.visit = visit_logical_expr

    STMT.Expression.visit = visit_expression_stmt
    STMT.Class.visit = visit_class_stmt
    STMT.Return.visit = visit_return_stmt
    STMT.Function.visit = visit_function_stmt
    STMT.Print.visit = visit_print_stmt
    STMT.Var.visit = visit_var_stmt
    STMT.Block.visit = visit_block_stmt
    STMT.If.visit = visit_if_stmt
    STMT.While.visit = visit_while_stmt
    
    # def c_arity():
    #     return 0
    # def c_call(interepreter, globals):
    #     return time.time()
        
    # clock_object = Lox_callable()
    # clock_object.arity = c_arity
    # clock_object.call = c_call
    # globals.define("clock",clock_object)
    
    
    
    try:
        for stmt in statements:
            execute(stmt)
    except runtime_error as e:
        run_time_error(e)
        


if __name__ == "__main__":
    pass