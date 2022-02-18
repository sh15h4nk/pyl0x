"""Error Reporters"""
from pylox.scanner.token_types import TOKEN_TYPES

def report(line, where, message):
    print("Error:", "[line: "+str(line)+"]", where, ":", message)

def error(token, message):
    if token.type == TOKEN_TYPES.EOF: return report(token.line, "at end", message)
    return report(token.line, "at '" + str(token.lexeme) + "' ", message)

def run_time_error(error):
    print("{} \n[line {} ]".format(error.getMessage(), error.token.line))