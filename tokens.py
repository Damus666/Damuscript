class Token:
    def __init__(self, t_type, value):
        self.type = t_type
        self.value = value

    def __repr__(self):
        return f"{self.value}"

class IntegerToken(Token):
    def __init__(self, value): super().__init__("INT", int(value))

class StringToken(Token):
    def __init__(self, value): super().__init__("STR", str(value))

class FloatToken(Token):
    def __init__(self, value): super().__init__("FLOAT", float(value))

class OperationToken(Token):
    def __init__(self, value): super().__init__("OP", value)

class KeywordToken(Token):
    def __init__(self, value): super().__init__("KW", value)

class NameToken(Token):
    def __init__(self, value): super().__init__("NAME", value)

class SemicolonToken(Token):
    def __init__(self): super().__init__("SEMIC", ";")

class EOFToken(Token):
    def __init__(self): super().__init__("EOF", "EOF")

KEYWORDS = {
    "function":"fun",
    "return": "ret",
    "import": "use",
    "while": "while",
    "break":"stop",
    "continue": "skip",
    "for": "repeat",
    "foreach": "for",
    "to":"to",
    "step":"step",
    "in":"in",
    "if":"if",
    "else":"else",
}