from types import SimpleNamespace

# Single-Character tokens
single_char_token = {
    "LEFT_PAREN" : "(",
    "RIGHT_PAREN" : ")",
    "LEFT_BRACE" : "{",
    "RIGHT_BRACE": "}",
    "COMA" : ",",
    "DOT" : ".",
    "MINUS" : "-",
    "PLUS" : "+",
    "SEMICOLON" : ";",
    "STAR" : "*",
    "SLASH": "/"
}

# One or more character tokens
multi_char_token = {
    "BANG" : "!",
    "BANG_EQUAL" : "!=",
    "EQUAL" : "=",
    "EQUAL_EQUAL" : "==",
    "GREATER" : ">",
    "GREATER_EQUAL" : ">=",
    "LESS" : "<",
    "LESS_EQUAL" : "<="
}

# Literals
literals = {
    "IDENTIFIER" : "IDENTIFIER",
    "STRING" : "STRING",
    "NUMBER" : "NUMBER"
}

# keywords
keywords = {
    "AND" : "and",
    "CLASS" : "class",
    "ELSE" : "else",
    "FALSE" : "false",
    "FUN" : "fun",
    "FOR" : "for",
    "IF" : "if",
    "NIL" : "nil",
    "OR" : "or",
    "PRINT" : "print",
    "RETURN" : "return",
    "SUPER" : "super",
    "THIS" : "this",
    "TRUE" : "true",
    "VAR" : "var",
    "WHILE" : "while"
}

TOKEN_TYPES = SimpleNamespace(**single_char_token, **multi_char_token, **literals, **keywords, EOF="")