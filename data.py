import sys

class Data:
    def __init__(self, parent=None):
        self.variables = {}
        self.parent = parent

    def read(self, name):
        value = self.variables.get(name, None)
        if value is None:
            if self.parent:
                return self.parent.read(name)
            sys.exit(f"NameError: Name '{name}' was not defined")
        return value
    
    def write(self, name, value):
        self.variables[name] = value

    def write_all(self, **vars):
        for name, val in vars.items():
            self.write(name, val)

    def __getitem__(self, name):
        value = self.variables.get(name, None)
        if value is None:
            if self.parent:
                return self.parent.read(name)
            sys.exit(f"NameError: Name '{name}' was not defined")
        return value