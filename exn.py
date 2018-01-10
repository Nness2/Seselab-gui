class ParseError (Exception):
    def __init__ (self, err, file, line):
        self.err = err
        self.file = file
        self.line = line

class LabelError (Exception):
    def __init__ (self, lbl):
        self.lbl = lbl

class AddrError (Exception):
    def __init__ (self, addr):
        self.addr = addr

class ValError (Exception):
    def __init__ (self, val):
        self.val = val

class WriteError (Exception):
    def __init__ (self):
        pass
