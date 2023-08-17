from tokens import IntegerToken, FloatToken, OperationToken, NameToken, KeywordToken, KEYWORDS, SemicolonToken, EOFToken, StringToken
import sys

class Lexer:
    digits = "0123456789"
    letters = "abcdefghijklmnopqrstuvwxyz"
    namechars = letters+letters.upper()+"_"
    allnamechars = namechars+digits
    operations = "+-/*^()|&!?[],{}.:"
    double_operations = "=><"
    stopwords = " \t\n"
    keywords = list(KEYWORDS.values())
    semicolon = ";"
    quotes = "\"'"

    def __init__(self, text):
        self.text = text
        self.idx = 0
        self.tokens = []
        self.char = self.text[self.idx]
        self.token = None

    def move(self):
        self.idx += 1
        if self.idx < len(self.text):
            self.char = self.text[self.idx]
        else:
            self.char = None

    def tokenize(self):
        while self.idx < len(self.text):
            self.token = None
            if self.char in self.digits:
                self.token = self.extract_number()
            elif self.char in self.operations:
                self.token = OperationToken(self.char)
                self.move()
            elif self.char in self.double_operations:
                if self.char == "=":
                    self.token = self.extract_double(["="])
                elif self.char == ">":
                    self.token = self.extract_double(["="])
                elif self.char == "<":
                    self.token = self.extract_double(["="])
            elif self.char in self.stopwords:
                self.move()
            elif self.char in self.namechars:
                self.token = self.extract_word()
            elif self.char in self.quotes:
                self.token = self.extract_string()
            elif self.char == self.semicolon:
                self.token = SemicolonToken()
                self.move()
            else:
                sys.exit(f"SyntaxError: Invalid Token '{self.char}'")
            if self.token:
                self.tokens.append(self.token)
        self.tokens.append(EOFToken())
        return self.tokens

    def extract_number(self):
        number = ""
        is_float = False
        while (self.char in self.digits or self.char == ".") and (self.idx < len(self.text)):
            if self.char == None: sys.exit(f"SyntaxError: Unexpected EOF while lexing number. Current value: '{number}'")
            if self.char == ".": is_float = True
            number += self.char
            self.move()
        return IntegerToken(number) if not is_float else FloatToken(number)
    
    def extract_string(self):
        quote = self.char
        string = ""
        self.move()
        while self.char != quote:
            if self.char == None: sys.exit(f"SyntaxError: Unexpected EOF while lexing string. Current value: '{string}'")
            string += self.char
            self.move()
        self.move()
        return StringToken(string)
    
    def extract_word(self):
        word = ""
        while self.char in self.allnamechars and self.idx < len(self.text):
            if self.char == None: sys.exit(f"SyntaxError: Unexpected EOF while lexing word. Current value: '{word}'")
            word += self.char
            self.move()
        return KeywordToken(word) if word in self.keywords else NameToken(word)
    
    def extract_double(self, possible_cases):
        value = self.char
        self.move()
        if self.char in possible_cases:
            value += self.char
            self.move()
        return OperationToken(value)
    
