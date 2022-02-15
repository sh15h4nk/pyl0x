# Token class defination
class token:
    def __init__(self, type, lexeme, literal, line) -> None:
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
    def __repr__(self) -> str:
        return "<TYPE:({}) LEXEME:({}) LITERAL:({})>".format(self.type, self.lexeme, self.literal)