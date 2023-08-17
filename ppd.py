import sys

class PreProcessingDirectives:
    def __init__(self, filename, text):
        name, ext = filename.split(".")
        ppd_filename = name+".ppd."+ext
        try:
            with open(ppd_filename, "r") as file:
                self.ppd_text = file.read()
        except:
            self.ppd_text = ""
        self.text = text
        self.lines = self.ppd_text.split("\n")
        self.idx = 0

    def process(self):
        if not self.ppd_text.strip(): return self.text
        self.line = self.lines[self.idx]
        while self.line != None:
            self.process_line()
        return self.text

    def process_line(self):
        if self.line == None: return
        if not self.line.startswith("#"):
            sys.exit(f"PPDError: preprocessing directives must start with #")
        line = self.line.replace("#","").strip()
        ppd = line.split(" ",1)[0].strip()
        arg = line.replace(ppd, "").strip()
        getattr(self, ppd)(arg)

    def include(self, arg):
        try:
            with open(arg, "r") as file:
                content = file.read()
                self.text = content+self.text
        except:
            sys.exit(f"PPDError: Could not include '{arg}' script. Make sure it exists")
        self.move()

    def replace(self, arg):
        self.move()
        if self.line == None: return 
        replace_a = self.line
        self.move()
        if self.line == None: return
        replace_b = self.line
        self.move()
        self.text = self.text.replace(replace_a, replace_b)

    def move(self):
        if self.idx +1 < len(self.lines):
            self.idx += 1
            self.line = self.lines[self.idx]
            if self.line.strip() == "": self.move()
        else:
            self.line = None