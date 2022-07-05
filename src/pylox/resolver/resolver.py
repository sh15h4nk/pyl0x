"""Resolver for static analysis of the source"""

from enum import Enum
from pylox.exceptions.exceptions import RuntimeError
import pylox.parser.expr as EXPR
import pylox.parser.stmt as STMT
from pylox.interpreter.interpreter import resolve as interpreter_resolve
from pylox.scanner.token import Token


# Types of the functions
class FUNCTION_TYPES(Enum):
    NONE = 0
    FUNCTION = 1
    INITIALIZER = 2
    METHOD = 3

# Types of the classes
class CLASS_TYPE(Enum):
    NONE = 0
    CLASS = 1
    SUBCLASS = 2

# State
current_class = CLASS_TYPE.NONE
current_function = FUNCTION_TYPES.NONE
scopes = []


def visit_block_stmt(stmt: STMT.Block) -> None:
    """Resolves a block of statements.

    Args:
        stmt (STMT.Block): statement block node.
    """
    begin_scope()
    resolve(stmt.statements)
    end_scope()
    return None

def visit_class_stmt(stmt: STMT.Class) -> None:
    """Resolves a class statement.

    Args:
        stmt (STMT.Class): class node.
    """
    global current_class
    enclosing_class = current_class
    current_class = CLASS_TYPE.CLASS
    
    declare(stmt.name)
    define(stmt.name)
    
    # superclass analysis
    if stmt.superclass and stmt.name.lexeme == stmt.superclass.name.lexeme: raise RuntimeError(stmt.superclass, "A class can't inherit from itself.")
    if stmt.superclass:
        current_class = CLASS_TYPE.SUBCLASS
        resolve(stmt.superclass)
    if stmt.superclass:
        begin_scope()
        scopes[-1] = {"super": True}
    
    begin_scope()
    scopes[-1] = {"this": True}
    
    # methods analysis
    for method in stmt.methods:
        declaration = FUNCTION_TYPES.METHOD
        if method.name.lexeme == "init": declaration = FUNCTION_TYPES.INITIALIZER
        resolve_function(method, declaration)
    end_scope()
    
    if stmt.superclass: end_scope()
    current_class = enclosing_class
    return None

def visit_this_expr(expr: EXPR.This) -> None:
    """Resolves this expression.

    Args:
        expr (EXPR.This): This node.
    """
    if current_class == CLASS_TYPE.NONE:
        raise RuntimeError(expr.keyword, "Can't use 'this' keyword outside of a class")
    resolveLocal(expr, expr.keyword)
    return None

def visit_super_expr(expr: EXPR.Super) -> None:
    """Resolves the super expression.

    Args:
        expr (EXPR.Super): super expression.
    """
    if current_class is CLASS_TYPE.NONE: raise RuntimeError(expr.keyword, "Can't use 'super' outside of a class")
    elif current_class is not CLASS_TYPE.SUBCLASS: raise RuntimeError(expr.keyword, "Can't use 'super' in a class with no superclass.")
    resolveLocal(expr, expr.keyword)
    return None

def visit_expression_stmt(stmt: STMT.Expression) -> None:
    """Resolves expression statement.

    Args:
        stmt (STMT.Expression): statement expression node.
    """
    resolve(stmt.expression)
    return None

def visit_var_stmt(stmt: STMT.Var) -> None:
    """Resolves variable statement.

    Args:
        stmt (STMT.Var): variable statement node.
    """
    declare(stmt.name)
    if stmt.initializer:
        resolve(stmt.initializer)
    define(stmt.name)
    return None

def visit_variable_expr(expr: EXPR.Variable) -> None:
    """Resolves variable expression.

    Args:
        expr (EXPR.Variable): variable expression node.
    """
    if len(scopes) and scopes[-1].get(expr.name.lexeme) == False:
       raise RuntimeError(expr.name, "Can't read local variable in its own initializer.")
    resolveLocal(expr, expr.name)
    return None

def visit_assign_expr(expr: EXPR.Assign) -> None:
    """Resolves assignment expression.

    Args:
        expr (EXPR.Assign): assignment expression node.
    """
    resolve(expr.value)
    resolveLocal(expr, expr.name)
    return None

def visit_function_stmt(stmt: STMT.Function) -> None:
    """Resolves function statement.

    Args:
        stmt (STMT.Function): function statement node.
    """
    declare(stmt.name)
    define(stmt.name)
    
    resolve_function(stmt, FUNCTION_TYPES.FUNCTION)
    return None


def visit_if_stmt(stmt: STMT.If) -> None:
    """Resolves if statement.

    Args:
        stmt (STMT.If): if statement node.
    """
    resolve(stmt.condition)
    resolve(stmt.thenBranch)
    if stmt.elseBranch: resolve(stmt.elseBranch)
    return None

def visit_print_stmt(stmt: STMT.Print) -> None:
    """Resolve print statement.

    Args:
        stmt (STMT.Print): print statement node.
    """
    resolve(stmt.expression)
    return None

def visit_return_stmt(stmt: STMT.Return) -> None:
    """Resolves return statement.

    Args:
        stmt (STMT.Return): return statement node.
    """
    if current_function == FUNCTION_TYPES.NONE:
        raise RuntimeError(stmt.keyword, "Can't return from top level code.")
    if stmt.value: resolve(stmt.value)
    if current_function == FUNCTION_TYPES.INITIALIZER:
        raise RuntimeError(stmt.keyword, "Can't return a value from an initializer.")
    return None

def visit_while_stmt(stmt: STMT.While) -> None:
    """Resolves while loop statement.

    Args:
        stmt (STMT.While): while statement node.
    """
    resolve(stmt.condition)
    resolve(stmt.body)
    return None

def visit_binary_expr(expr: EXPR.Binary) -> None:
    """Resolves binary expression.

    Args:
        expr (EXPR.Binary): binary expression node.
    """
    resolve(expr.left)
    resolve(expr.right)
    return None

def visit_call_expr(expr: EXPR.Call) -> None:
    """Resolves a call expression.

    Args:
        expr (EXPR.Call): call expression node.
    """
    resolve(expr.callee)
    for arg in expr.arguments:
        resolve(arg)
    return None

def visit_get_expr(expr: EXPR.Get) -> None:
    """Resolves get expression.

    Args:
        expr (EXPR.Get): get expression node.
    """
    resolve(expr.object)
    return None

def visit_set_expr(expr: EXPR.Set) -> None:
    """Resolves set expression.

    Args:
        expr (EXPR.Set): set expression node.
    """
    resolve(expr.value)
    resolve(expr.object)
    return None

def visit_grouping_expr(expr: EXPR.Grouping) -> None:
    """Resolve grouping expression

    Args:
        expr (EXPR.Grouping): group expression node.
    """
    resolve(expr.expression)
    return None

def visit_literal_expr(expr: EXPR.Literal) -> None:
    """Resolves a literal expression.

    Args:
        expr (EXPR.Literal): literal expression node.
    """
    return None

def visit_logical_expr(expr: EXPR.Logical) -> None:
    """Resolves a logical expression.

    Args:
        expr (EXPR.Logical): logical expression node.
    """
    resolve(expr.left)
    resolve(expr.right)
    return None

def visit_unary_expr(expr: EXPR.Unary) -> None:
    """Resolves unary expression.

    Args:
        expr (EXPR.Unary): unary expression node.
    """
    resolve(expr.right)
    return None

def resolve(handler) -> None:
    """Resolves a handler

    Args:
        handler: list of statements or a single statement either expression or statement.
    """
    if type(handler) is list:
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
        for stmt in handler:
            resolve(stmt)
    else:
        handler.accept(handler)


def resolve_function(function: STMT.Function, type: FUNCTION_TYPES) -> None:
    """Resolves a function

    Args:
        function (STMT.Function): function node.
        type (FUNCTION_TYPES): type of the function.
    """
    global current_function
    enclosing_function = current_function
    current_function = type
    
    begin_scope()
    # params
    for param in function.params:
        declare(param)
        define(param)
    resolve(function.body)
    end_scope()
    
    current_function = enclosing_function

def begin_scope() -> None:
    """Begins a scope"""
    scopes.append({})
    
def end_scope() -> None:
    """Ends a scope"""
    scopes.pop()

def declare(name: Token) -> None:
    """Declares an identifier in the scope.

    Args:
        name (Token): token of the identifier.
    """
    if not len(scopes):
        return None
    if name.lexeme in scopes[-1]:
        raise RuntimeError(name, "Already a variable with this name exists in the scope.")
    scopes[-1] = {name.lexeme: False}

def define(name: Token) -> None:
    """Defines an identifier in the scope.

    Args:
        name (Token): token of the identifier.
    """
    if not len(scopes):
        return None
    scopes[-1] = {name.lexeme: True}

def resolveLocal(expr: EXPR, name: Token) -> None:
    """Resolves local identifiers to the interpreter state.

    Args:
        expr (EXPR): expression to be resolved.
        name (Token): token of the identifier.
    """
    for i in range(len(scopes) -1 ,-1, -1):
        if name.lexeme in scopes[i]:
            interpreter_resolve(expr, len(scopes)-1-i)
            return
        
        