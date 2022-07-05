"""Error Reporters"""

from pylox.scanner.token_types import TOKEN_TYPES


def report(line, where, message):
    if where: print("Error:", "[line: {}] {} : {}".format(line, where, message))
    else: print("Error: [line: {}] {}".format(line, message))
    