"""Error Reporters"""
import sys
from pylox.scanner.token_types import TOKEN_TYPES

had_error = False
had_runtime_error = False

def report(line, where, message):
    print("Error:", "[line: "+str(line)+"]", where, ":", message)
    print("It was repoterd here")
    sys.exit(1)

def error(token, message):
    if token.type == TOKEN_TYPES.EOF: return report(token.line, "at end", message)
    return report(token.line, "at '" + str(token.lexeme) + "' ", message)

def run_time_error(error):
    print("{} \t[line {} ]".format(error, error.token.line))
    print("its a run time here")
    sys.exit(1)