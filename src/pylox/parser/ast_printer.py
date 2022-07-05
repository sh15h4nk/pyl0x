"""A Tool kit which prints the parsed AST after parsing tokens"""

import pylox.parser.expr as EXPR
from pylox.scanner.token import Token
from pylox.scanner.token_types import TOKEN_TYPES


def parenthesize(name, *arg):
    builder = "({}".format(name)
    for expr in arg:
        builder += " {}".format(expr.accept(expr))
    builder += ")"

    return builder

def visit_binary_expr(self):
    return parenthesize(self.operator.lexeme, self.left, self.right)

def visit_grouping_expr(expr):
    return parenthesize("group", expr.expression)

def visit_literal_expr(expr):
    if (expr.value == None): return "nil"
    return str(expr.value)

def visit_unary_expr(expr):
    return parenthesize(expr.operator.lexeme, expr.right)

def ast_printer(expr):
    EXPR.Binary.visit = visit_binary_expr
    EXPR.Grouping.visit = visit_grouping_expr
    EXPR.Literal.visit = visit_literal_expr
    EXPR.Unary.visit = visit_unary_expr
    print(expr.accept(expr))


if __name__ == "__main__":
    # Usage
    expression = EXPR.Binary(EXPR.Unary(Token(TOKEN_TYPES.MINUS, "-", None, 1), EXPR.Literal(123)), Token(TOKEN_TYPES.STAR, "*", None, 1), EXPR.Grouping(EXPR.Literal(45.67)))
    ast_printer(expression)

