def report(line, where, message):
    print("Error:", "[line: "+str(line)+"]", where, ":", message)

def error(line, message):
    return report(line, "", message)