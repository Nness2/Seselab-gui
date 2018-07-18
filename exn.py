class ParseError (Exception):
    def __init__ (self, err):
        self.err = err

class DuplicateLabel (Exception):
    def __init__ (self, lbl):
        self.lbl = lbl

class LabelNotFound (Exception):
    def __init__ (self, lbl, file, line):
        self.lbl = lbl
        self.file = file
        self.line = line

class AddrError (Exception):
    def __init__ (self, addr):
        self.addr = addr

class WriteError (Exception):
    def __init__ (self):
        pass
