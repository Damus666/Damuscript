from lexer import Lexer
from parse import Parser
from interpreter import Interpreter
from data import Data
from api import DSAPI
from ppd import PreProcessingDirectives
import sys
import mods

class Damuscript:
    def __init__(self, filename, show_tokens=False, show_tree=False):
        DSAPI.set_context(self)
        self.data = Data()

        text = ""
        with open(filename, "r") as file:
            text = file.read()
        if not text.strip(): quit()

        self.ppd = PreProcessingDirectives(filename, text)
        text = self.ppd.process()

        DSAPI.import_module("builtin")

        self.lexer = Lexer(text)
        tokens = self.lexer.tokenize()
        if show_tokens: print(tokens)

        self.parser = Parser(tokens)
        tree = self.parser.parse()
        if show_tree: print(tree)

        self.interpreter = Interpreter(self.data)
        self.interpreter.interpret(tree)

if __name__ == "__main__":
    #if len(sys.argv) < 2: sys.exit(f"ArgvError: file name expected")
    file_name = "scripts/script.ds"#sys.argv[1]
    show_tree, show_tokens = "--showtree" in sys.argv, "--showtok" in sys.argv
    ds = Damuscript(file_name, show_tokens, show_tree)