
import expr as EXP
from pylox.scanner.token import token
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
    EXP.Binary.visit = visit_binary_expr
    EXP.Grouping.visit = visit_grouping_expr
    EXP.Literal.visit = visit_literal_expr
    EXP.Unary.visit = visit_unary_expr
    print(expr.accept(expr))




if __name__ == "__main__":
    expression = EXP.Binary(EXP.Unary(token(TOKEN_TYPES.MINUS, "-", None, 1), EXP.Literal(123)), token(TOKEN_TYPES.STAR, "*", None, 1), EXP.Grouping(EXP.Literal(45.67)))
    ast_printer(expression)