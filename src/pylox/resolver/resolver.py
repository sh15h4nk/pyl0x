from enum import Enum
from pylox.error_reporter import error as Lox_error
import pylox.parser.expr as EXPR
import pylox.parser.stmt as STMT
from pylox.interpreter.interpreter import resolve as interpreter_resolve
from pylox.scanner.token import Token

class FUNCTION_TYPES(Enum):
    NONE = 0
    FUNCTION = 1
    INITIALIZER = 2
    METHOD = 3

class CLASS_TYPE(Enum):
    NONE = 0
    CLASS = 1
    SUBCLASS = 2

current_class = CLASS_TYPE.NONE
current_function = FUNCTION_TYPES.NONE
scopes = []


def visit_block_stmt(stmt: STMT.Block) -> None:
    begin_scope()
    resolve(stmt.statements)
    end_scope()
    return None

def visit_class_stmt(stmt: STMT.Class) -> None:
    global current_class
    enclosing_class = current_class
    current_class = CLASS_TYPE.CLASS
    
    declare(stmt.name)
    define(stmt.name)
    
    if stmt.superclass and stmt.name.lexeme == stmt.superclass.name.lexeme: Lox_error(stmt.superclass, "A class can't inherit from itself.")
    if stmt.superclass:
        current_class = CLASS_TYPE.SUBCLASS
        resolve(stmt.superclass)
    if stmt.superclass:
        begin_scope()
        scopes[-1] = {"super": True}
    
    begin_scope()
    scopes[-1] = {"this": True}
    
    for method in stmt.methods:
        declaration = FUNCTION_TYPES.METHOD
        if method.name.lexeme == "init": declaration = FUNCTION_TYPES.INITIALIZER
        resolve_function(method, declaration)
    end_scope()
    
    if stmt.superclass: end_scope()
    
    current_class = enclosing_class
    return None

def visit_this_expr(expr: EXPR.This) -> None:
    if current_class == CLASS_TYPE.NONE:
        Lox_error(expr.keyword, "Can't use 'this' keyword outside of a class")
    resolveLocal(expr, expr.keyword)
    return None

def visit_super_expr(expr: EXPR.Super) -> None:
    if current_class is CLASS_TYPE.NONE: Lox_error(expr.keyword, "Can't use 'super' outside of a class")
    elif current_class is not CLASS_TYPE.SUBCLASS: Lox_error(expr.keyword, "Can't use 'super' in a class with no superclass.")
    resolveLocal(expr, expr.keyword)
    return None

def visit_expression_stmt(stmt: STMT.Expression) -> None:
    resolve(stmt.expression)
    return None

def visit_var_stmt(stmt: STMT.Var) -> None:
    declare(stmt.name)
    if stmt.initializer:
        resolve(stmt.initializer)
    define(stmt.name)
    return None

def visit_variable_expr(expr: EXPR.Variable) -> None:
    if len(scopes) and scopes[-1].get(expr.name.lexeme) == False:
       Lox_error(expr.name, "Can't read local variable in its own initializer.")
    resolveLocal(expr, expr.name)
    return None

def visit_assign_expr(expr: EXPR.Assign) -> None:
    resolve(expr.value)
    resolveLocal(expr, expr.name)
    return None

def visit_function_stmt(stmt: STMT.Function) -> None:
    declare(stmt.name)
    define(stmt.name)
    
    resolve_function(stmt, FUNCTION_TYPES.FUNCTION)
    return None


def visit_if_stmt(stmt: STMT.If) -> None:
    resolve(stmt.condition)
    resolve(stmt.thenBranch)
    if stmt.elseBranch: resolve(stmt.elseBranch)
    return None

def visit_print_stmt(stmt: STMT.Print) -> None:
    resolve(stmt.expression)
    return None

def visit_return_stmt(stmt: STMT.Return) -> None:
    if current_function == FUNCTION_TYPES.NONE:
        Lox_error(stmt.keyword, "Can't return from top level code.")
    if stmt.value: resolve(stmt.value)
    if current_function == FUNCTION_TYPES.INITIALIZER:
        Lox_error(stmt.keyword, "Can't return a value from an initializer.")
    return None

def visit_while_stmt(stmt: STMT.While) -> None:
    resolve(stmt.condition)
    resolve(stmt.body)
    return None

def visit_binary_expr(expr: EXPR.Binary) -> None:
    resolve(expr.left)
    resolve(expr.right)
    return None

def visit_call_expr(expr: EXPR.Call) -> None:
    resolve(expr.callee)
    for arg in expr.arguments:
        resolve(arg)
    return None

def visit_get_expr(expr: EXPR.Get) -> None:
    resolve(expr.object)
    return None

def visit_set_expr(expr: EXPR.Set) -> None:
    resolve(expr.value)
    resolve(expr.object)
    return None

def visit_grouping_expr(expr: EXPR.Grouping) -> None:
    resolve(expr.expression)
    return None

def visit_literal_expr(expr: EXPR.Literal) -> None:
    return None

def visit_logical_expr(expr: EXPR.Logical) -> None:
    resolve(expr.left)
    resolve(expr.right)
    return None

def visit_unary_expr(expr: EXPR.Unary) -> None:
    resolve(expr.right)
    return None

def resolve(handler) -> None:
    if type(handler) is list:
        for stmt in handler:
            resolve(stmt)
    else:
        handler.accept(handler)


def resolve_function(function: STMT.Function, type: FUNCTION_TYPES) -> None:
    global current_function
    enclosing_function = current_function
    current_function = type
    begin_scope()
    for param in function.params:
        declare(param)
        define(param)
    resolve(function.body)
    end_scope()
    current_function = enclosing_function

def begin_scope() -> None:
    scopes.append({})
    
def end_scope() -> None:
    scopes.pop()

def declare(name: Token) -> None:
    if not len(scopes):
        return None
    if name.lexeme in scopes[-1]:
        Lox_error(name, "Already a variable with this name exists in the scope.")
    scopes[-1] = {name.lexeme: False}

def define(name: Token) -> None:
    if not len(scopes):
        return None
    scopes[-1] = {name.lexeme: True}

def resolveLocal(expr: EXPR, name: Token):
    for i in range(len(scopes) -1 ,-1, -1):
        if name.lexeme in scopes[i]:
            interpreter_resolve(expr, len(scopes)-1-i)
            return
        

 # assigning visitor method to the classes
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