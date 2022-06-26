from glob import glob
from tempfile import tempdir
import pylox.parser.expr as EXP
import pylox.parser.stmt as STMT
from pylox.exceptions.runtime_error import runtime_error
from pylox.error_reporter import run_time_error
from pylox.environment.environment import Environment

env = Environment()

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
    env.assign(expr.name, value)
    return value

def visit_var_stmt(stmt):
    value = None
    if (stmt.initializer != None): value = evaluate(stmt.initializer)
    env.define(stmt.name, value)
    return None

def visit_variable_expression(expr):
    return env.get(expr.name)

def visit_expression_stmt(stmt):
    evaluate(stmt.expression)
    return None

def visit_print_stmt(stmt):
    value = evaluate(stmt.expression)
    print(stringify(value))
    return None


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
    
def visit_block_stmt(stmt):
    execute_block(stmt.statements, Environment(enclose=env))
    return None

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
    EXP.Binary.visit = visit_binary_expr
    EXP.Grouping.visit = visit_grouping_expr
    EXP.Literal.visit = visit_literal_expr
    EXP.Unary.visit = visit_unary_expr
    EXP.Variable.visit = visit_variable_expression
    EXP.Assign.visit = visit_assign_expr
    EXP.Logical.visit = visit_logical_expr
    
    STMT.Expression.visit = visit_expression_stmt
    STMT.Print.visit = visit_print_stmt
    STMT.Var.visit = visit_var_stmt
    STMT.Block.visit = visit_block_stmt
    STMT.If.visit = visit_if_stmt
    STMT.While.visit = visit_while_stmt
    
    
    try:
        for stmt in statements:
            execute(stmt)
    except runtime_error as e:
        run_time_error(e)


if __name__ == "__main__":
    pass