"""Error Reporters"""

from pylox.scanner.token_types import TOKEN_TYPES


def report(line, where, message, type):
    if where: print("{}:", "[line: {}] {} : {}".format(line, where, message, type))
    else: print("{}: [line: {}] {}".format(line, message, type))
    