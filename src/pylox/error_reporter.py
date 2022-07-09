"""Error Reporters"""

from pylox.scanner.token_types import TOKEN_TYPES


def report(line, where, message, _type):
    if where: print("{}: [line: {}] {} : {}".format(_type, line, where, message))
    else: print("{}: [line: {}] {}".format(_type, line, message))
    