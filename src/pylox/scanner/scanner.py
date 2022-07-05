"""This is scanner, which scans the source and segegrates into tokens"""

from typing import List, Type
from pylox.scanner.token_types import TOKEN_TYPES, single_char_token, multi_char_token, keywords
from pylox.scanner.token import Token
from pylox.exceptions.exceptions import SyntaxError
from decimal import Decimal

class Scanner:
    """Scanner class"""
    def __init__(self, source) -> None:
        """Initializing the scanner with source.

        Args:
            source (string): source code input.
        """
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.source = source
    
    def __repr__(self) -> str:
        """To represent a class object.

        Returns:
            str: outputs the source and tokens.
        """
        return "source: {} tokens: {}".format(self.source, self.tokens)

    def scan_tokens(self) -> List[Type[Token]]:
        """Scans all the tokens from the source.

        Returns:
            List: tokens list.
        """
        while(not self.is_at_end()):
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token("EOF", "", None, self.line))
        return self.tokens

    def is_at_end(self) -> bool:
        """Checks if the scanner has reached the end of the source.

        Returns:
            bool: returns True if the scanner reached the end.
        """
        return self.current >= len(self.source)
    
    def scan_token(self) -> None:
        """scans a single char from the source and identifies token,
            Also reports error if any unexpected char is found.
        """
        c = self.advance()
        if c in list(single_char_token.values()) and c != "/":
            type = list(single_char_token.keys())[list(single_char_token.values()).index(c)]
            self.add_token(type, None)
        elif c in list(multi_char_token.values()):
            type = list(multi_char_token.keys())[list(multi_char_token.values()).index(c)]
            if self.match("="):
                type += "_EQUAL"
            self.add_token(type, None)
        elif c == "/":
            if self.match("/"):
                while (self.peek() != "\n" and not self.is_at_end()):   self.advance()
            else:
                self.add_token("SLASH", None)
        elif c in [" ", "\r", "\t"]:
            pass
        elif c == "\n":
            self.line += 1
        elif c == '"':
            self.string()
        elif c.isdigit():
            self.number()
        elif c.isalpha() or c == "_":
            self.identifier()
        else:
            raise SyntaxError(self.line, c, "Unexpected character")
    
    def identifier(self) -> None:
        """Identifies identifiers from the source and adds to tokens.
        """
        while (self.peek().isalnum()): self.advance()
        lexeme = self.source[self.start: self.current]
        type = TOKEN_TYPES.IDENTIFIER
        if lexeme in list(keywords.values()):
            type = list(keywords.keys())[list(keywords.values()).index(lexeme)]
        self.add_token(type, None)
    
    def number(self) -> None:
        """Identifies number from the source and adds to tokens.
        """
        while (self.peek().isdigit()): self.advance()
        if (self.peek() == "." and self.peek_next().isdigit()):
            self.advance()
            while self.peek().isdigit(): self.advance()
        self.add_token(TOKEN_TYPES.NUMBER, Decimal(self.source[self.start: self.current]))
    
    def string(self) -> None:
        """Identifies string from the source (double quoted) and adds to tokens.
        """
        while(self.peek() != '"' and not self.is_at_end()):
            if (self.peek() == "\n"): self.line += 1
            self.advance()
        if (self.is_at_end()):
            raise SyntaxError(self.line, None, "Undeterminated string")
        self.advance()
        lexeme = self.source[self.start +1 : self.current -1]
        self.add_token(TOKEN_TYPES.STRING, lexeme)
    
    def peek(self) -> str:
        """looks the current position of the scanner. 

        Returns:
            str: returns null byte when the scanner reaches the end of source,
                else it will return the pointing element from the source.
        """
        if (self.is_at_end()): return "\0"
        return self.source[self.current]
    
    def peek_next(self) -> str:
        """one look ahead of the scanner

        Returns:
            str: returns null byte if it reachs the before last one in the source,
                else it will return one look ahead of the scanner pointer.
        """
        if (self.current + 1 >= len(self.source)): return "\0"
        return self.source[self.current +1]
    
    def match(self, expected: Token) -> bool:
        """To match the current token with the expected.

        Args:
            expected (token): token to be matched.

        Returns:
            bool: returns True if the current token matched, else False
        """
        if(self.is_at_end()):
            return False
            
        if (self.source[self.current] != expected):
            return False

        self.current += 1
        return True


    def advance(self) -> str:
        """Advances the scanner pointer

        Returns:
            str: the next char from the source
        """
        c = self.source[self.current]
        self.current += 1
        return c
    
    def add_token(self, type: TOKEN_TYPES, literal: str) -> None:
        """Adds the recognized tokens to the tokens list.

        Args:
            type (TOKEN_TYPES): Identified type
            literal (str): string literal of the token (source)
        """
        lexeme = self.source[self.start: self.current]
        self.tokens.append(Token(type, lexeme, literal, self.line))
