
import argparse
from pylox.scanner.scanner import scanner
from pylox.parser.parser import parser
from pylox.interpreter.interpreter import interpret
from pylox.parser.ast_printer import ast_printer
from pylox.resolver.resolver import resolve

def run_prompt():
	try:
		while True:
			cmd = input("> ")
			run(cmd)
	except (KeyboardInterrupt, EOFError) as e:
		print(" Bye :)")
		exit(0)

def run_file(file):
	src = file.read()
	if src == "":
		print("Your source file is empty :/")
		return

def run(src):
	try:
		s = scanner(src)
		tokens = s.scan_tokens()
		p = parser(tokens)
		statements = p.parse()
		resolve(statements)
		i = interpret(statements)
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
	