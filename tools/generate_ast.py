import sys


def define_visitor(f):
    data = "\n\t#Visitor Method\n\tdef accept(self, visitor):\n\t\treturn visitor.visit()\n\n"
    f.write(data)

def comments(f):
    message = "{}Node classes(expression classes) definition{}\n{}This is a generated file, from tools/generate_ast.py script{}\n\n".format('"""', '"""', '"""', '"""')
    f.write(message)


def define_type(file, c_name, fields):
    # class definition with constructor
    _class = "class {}:\n\t#Constructor\n\tdef __init__(self, {}):\n{}".format(c_name, fields, "".join("\t\tself.{} = {}\n".format(i, i) for i in fields.split(",")))

    file.write(_class)

def generate_ast():
    if (len(sys.argv) != 3):
        raise SystemExit("Usage: python3 generate_ast.py <output directory> <file>")
    out_dir = sys.argv[1]
    file_name = sys.argv[2]
    path = "{}/{}.py".format(out_dir, file_name)

    print("Path", path)
    
    classes = {
        "Binary": "left,operator,right",
        "Grouping": "expression",
        "Literal": "value",
        "Unary": "operator,right"
    }
    f = open(path, "w")
    comments(f)
    
    for c_name,fields in classes.items():
        # fields = fields.split(",")
        # print(c_name, ":", fields)
        define_type(f, c_name, fields)
        define_visitor(f)
        
    

if __name__ == "__main__":
    generate_ast()