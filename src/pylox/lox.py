import sys
import argparse

from pylox.scanner.scanner import scanner
from pylox.parser.parser import parser
from pylox.parser.ast_printer import ast_printer

def repl():
	try:
		while True:
			cmd = input("> ")
			s = scanner(cmd)
			tokens = s.scan_tokens()
			# print("The tokens", tokens)
			p = parser(tokens)
			expression = p.parse()
			print("The AST:")
			ast_printer(expression)
	except (KeyboardInterrupt, EOFError) as e:
		print(" Bye :)")
		sys.exit(0)

def run_file(file):
	src = file.read()
	if src == "":
		print("Your source file is empty :/")
		return
	print(type(file), src)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("infile", nargs="?", type=argparse.FileType('r'), default=None)

	args = parser.parse_args()

	if args.infile is None:
		repl()
	else:
		run_file(args.infile)


if __name__ == "__main__":
	main()
	