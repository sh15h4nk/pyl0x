
from shutil import ExecError
import sys
import readline
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
        readline.parse_and_bind('tab: complete')
        readline.parse_and_bind('set editing-mode vi')
        readline.parse_and_bind('C-x: "\x16\n"')
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
    run(src)

def run(src):
    try:
        scanner = Scanner(src)
        tokens = scanner.scan_tokens()
        
        parser = Parser(tokens)
        statements = parser.parse()
        
        resolve(statements)
        
        interpret(statements)
        
    except SyntaxError as e:
        error_report(e.line, e.char, e)
    except ParseError as e:
        error_report(e.token.line, e.token.lexeme, e)
    except RuntimeError as e:
        try:
            error_report(e.token.line, e.token.lexeme, e)
        except:
            error_report("#", None,e )
    except Exception as e:
        print(e)
    

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
	