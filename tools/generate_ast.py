import sys

DEFAULT_PATH = "../src/pylox/parser"


def define_visitor(f):
    data = "\n\t#Visitor Method\n\tdef accept(self, visitor):\n\t\treturn visitor.visit()\n\n"
    f.write(data)

def comments(f, c):
    message = "{}Node classes({} classes) definition{}\n{}This is a generated file, from tools/generate_ast.py script{}\n\n".format('"""', c, '"""', '"""', '"""')
    f.write(message)


def define_type(file, c_name, fields):
    # class definition with constructor
    _class = "class {}:\n\t#Constructor\n\tdef __init__(self, {}):\n{}".format(c_name, fields, "".join("\t\tself.{} = {}\n".format(i, i) for i in fields.split(",")))

    file.write(_class)

def generate_ast(filename, path = DEFAULT_PATH):
    out_dir = path
    file_name = filename
    path = "{}/{}.py".format(out_dir, file_name)

    print("Path", path)
    
    if file_name == "expr":
        classes = {
            "Assign":"name,value",
            "Binary": "left,operator,right",
            "Grouping": "expression",
            "Literal": "value",
            "Unary": "operator,right",
            "Variable": "name"
        }
    elif file_name == "stmt":
        classes = {
            "Block" : "statements",
            "Expression": "expression",
            "If": "condition,thenBranch,elseBranch",
            "Print": "expression",
            "Var": "name,initializer"
        }
    else:
        raise SystemExit("Invalid filename")
    f = open(path, "w")
    comments(f, file_name)
    
    for c_name,fields in classes.items():
        # fields = fields.split(",")
        # print(c_name, ":", fields)
        define_type(f, c_name, fields)
        define_visitor(f)
        
    

if __name__ == "__main__":
    c = int(input("__MENU__\n1. Expr\n2. Stmt\nEnter the class: "))
    if (c == 1):
        generate_ast("expr")
    elif (c == 2):
        generate_ast("stmt")
    else:
        raise SystemExit("Invalid option")