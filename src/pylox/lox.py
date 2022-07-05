
import sys
import argparse
from pylox.scanner.scanner import Scanner
from pylox.parser.parser import Parser
from pylox.interpreter.interpreter import interpret
# from pylox.parser.ast_printer import ast_printer
from pylox.resolver.resolver import resolve
from pylox.exceptions.exceptions import SyntaxError, ParseError, RuntimeError
from pylox.error_reporter import report as error_report



def run_prompt():
    try:
        while True:
            cmd = input("> ")
            run(cmd)
    except (KeyboardInterrupt, EOFError) as e:
        print("Bye :)")
        sys.exit(0)
        
def run_file(file):
    src = file.read()
    if src == "":
        print("Your source file is empty :/")
        return

def run(src):
    try:
        scanner = Scanner(src)
        tokens = scanner.scan_tokens()
        
        parser = Parser(tokens)
        statements = parser.parse()
        print("THe statements", statements)
        
        resolve(statements)
        
        interpret(statements)
        
    except SyntaxError as e:
        error_report(e.line, e.char, e)
        sys.exit(0)
    except ParseError as e:
        print(e)
        sys.exit(0)
    except RuntimeError as e:
        error_report(e.token.line, e.token.lexeme, e)
        sys.exit(0)
    

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("infile", nargs="?", type=argparse.FileType('r'), default=None)

	args = parser.parse_args()

	if args.infile is None:
		run_prompt()
	else:
		run_file(args.infile)


if __name__ == "__main__":
	main()
	