import sys
import argparse

from scanner.scanner import scanner

def repl():
	try:
		while True:
			cmd = input("> ")
			s = scanner(cmd)
			s.scan_tokens()
			print(s)
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