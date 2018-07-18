import sys
import os
from exn import *

class Compiler:

    def __init__ (self):
        self._ln = []
        self._files = []
        self._count = 0
        self._labels = {}
        self._code = []

    def arit (self, i, a):
        if len(i) != a + 1:
            raise ParseError('arity')

    def addr (self, a, noref = False):
        if a[0] == 'r':
            if a[1:].isdigit():
                return ('reg', int(a[1:]))
            else:
                raise ParseError('register')
        if a[0] == '@':
            if a[1:].isdigit():
                return ('mem', int(a[1:]))
            else:
                raise ParseError('memory')
        if a[0] == '!' and not noref:
            if ',' in a:
                r = a[1:].split(',', 1)
                return ('ref', self.val(r[0], True), self.val(r[1], True))
            else:
                return ('ref', self.val(a[1:], True))
        if noref:
            raise ParseError('reference')
        raise ParseError('address')

    def val (self, v, noref = False):
        if v[0] == '#':
            try:
                return ('imm', int(v[1:]))
            except:
                raise ParseError('immediate')
        else:
            return self.addr(v, noref)

    def lbl (self, l):
        if l.isidentifier():
            return ('lbl', l)
        else:
            return self.val(l)

    def instr (self, line):
        line = line.split(';', 1)[0].strip()
        if line == '':
            return None

        if ':' in line:
            line = line.split(':', 1)
            lbl = line[0].strip()
            if lbl in self._labels:
                raise DuplicateLabel(lbl)
            else:
                self._labels[lbl] = self._count, self._files[-1], self._ln[-1]
            line = line[1]

        line = line.split(';', 1)[0].strip()
        if line == '':
            return None

        i = line.split()

        if i[0] == 'nop':
            self.arit(i, 0)
            return [i[0]]

        if i[0] == 'ret':
            self.arit(i, 0)
            return [i[0]]

        if i[0] == 'cal':
            self.arit(i, 1)
            return [i[0], self.lbl(i[1])]

        if i[0] == 'jmp':
            self.arit(i, 1)
            return [i[0], self.lbl(i[1])]

        if i[0] == 'dbg':
            self.arit(i, 1)
            return [i[0], i[1]]

        if i[0] == 'prn':
            self.arit(i, 1)
            return [i[0], self.val(i[1])]

        if i[0] == 'prx':
            self.arit(i, 1)
            return [i[0], self.val(i[1])]

        if i[0] == 'prX':
            self.arit(i, 1)
            return [i[0], self.val(i[1])]

        if i[0] == 'prc':
            self.arit(i, 1)
            return [i[0], self.val(i[1])]

        if i[0] == 'prs':
            self.arit(i, 2)
            return [i[0], self.val(i[1]), self.val(i[2])]

        if i[0] == 'mov':
            self.arit(i, 2)
            return [i[0], self.addr(i[1]), self.val(i[2])]

        if i[0] == 'not':
            self.arit(i, 2)
            return [i[0], self.addr(i[1]), self.val(i[2])]

        if i[0] == 'beq':
            self.arit(i, 3)
            return [i[0], self.lbl(i[1]), self.val(i[2]), self.val(i[3])]

        if i[0] == 'bne':
            self.arit(i, 3)
            return [i[0], self.lbl(i[1]), self.val(i[2]), self.val(i[3])]

        if i[0] == 'and':
            self.arit(i, 3)
            return [i[0], self.addr(i[1]), self.val(i[2]), self.val(i[3])]

        if i[0] == 'orr':
            self.arit(i, 3)
            return [i[0], self.addr(i[1]), self.val(i[2]), self.val(i[3])]

        if i[0] == 'xor':
            self.arit(i, 3)
            return [i[0], self.addr(i[1]), self.val(i[2]), self.val(i[3])]

        if i[0] == 'lsl':
            self.arit(i, 3)
            return [i[0], self.addr(i[1]), self.val(i[2]), self.val(i[3])]

        if i[0] == 'lsr':
            self.arit(i, 3)
            return [i[0], self.addr(i[1]), self.val(i[2]), self.val(i[3])]

        if i[0] == 'min':
            self.arit(i, 3)
            return [i[0], self.addr(i[1]), self.val(i[2]), self.val(i[3])]

        if i[0] == 'max':
            self.arit(i, 3)
            return [i[0], self.addr(i[1]), self.val(i[2]), self.val(i[3])]

        if i[0] == 'add':
            self.arit(i, 3)
            return [i[0], self.addr(i[1]), self.val(i[2]), self.val(i[3])]

        if i[0] == 'sub':
            self.arit(i, 3)
            return [i[0], self.addr(i[1]), self.val(i[2]), self.val(i[3])]

        if i[0] == 'mul':
            self.arit(i, 3)
            return [i[0], self.addr(i[1]), self.val(i[2]), self.val(i[3])]

        if i[0] == 'div':
            self.arit(i, 3)
            return [i[0], self.addr(i[1]), self.val(i[2]), self.val(i[3])]

        if i[0] == 'mod':
            self.arit(i, 3)
            return [i[0], self.addr(i[1]), self.val(i[2]), self.val(i[3])]

        if i[0] == 'cmp':
            self.arit(i, 3)
            return [i[0], self.addr(i[1]), self.val(i[2]), self.val(i[3])]

        raise ParseError('opcode')

    def compile_file (self, path):
        inp = open(path, 'r')
        self._files.append(os.path.basename(path))
        self._ln.append(1)
        for l in inp:
            if '.include' in l:
                self.compile_file(os.path.dirname(path) + '/' +
                                  l.split('.include', 1)[1].strip())
            else:
                a = self.instr(l)
                if a is not None:
                    self._code.append([a, [self._files[-1], self._ln[-1]]])
                    self._count += 1
            self._ln[-1] += 1
        self._files.pop()
        self._ln.pop()
        inp.close()

    def compile (self, path):
        self._code.append([['jmp', ('lbl', 'main')], ['_', -1]])
        self._count += 1
        self.compile_file(os.path.abspath(path))
        for instr in self._code:
            if instr[0][0] in ('cal', 'jmp', 'beq', 'bne'):
                if instr[0][1][0] == 'lbl':
                    lbl = instr[0][1][1]
                    if lbl in self._labels:
                        instr[0][1] = 'imm', self._labels[lbl][0]
                        instr[1].append(lbl)
                    else:
                        raise LabelNotFound(lbl, instr[1][0], instr[1][1])
        for lbl in self._labels:
            instr = self._code[self._labels[lbl][0]]
            if len(instr[1]) == 2:
                instr[1].append(None)
            instr[1].append(lbl)
        return self._code

    def run (self, path):
        try:
            return self.compile(path)

        except ParseError as e:
            print('Parse error: ' + e.err +
                  ' in ' + self._files[-1] +
                  ' on line ' + str(self._ln[-1]),
                  file=sys.stderr)

        except DuplicateLabel as e:
            print('Duplicate label: ' + e.lbl +
                  ' in ' + self._files[-1] +
                  ' on line ' + str(self._ln[-1]) +
                  ' (first declared in ' + self._labels[e.lbl][1] +
                  ' on line ' + str(self._labels[e.lbl][2]) + ')',
                  file=sys.stderr)

        except LabelNotFound as e:
            print('Label not found: ' + e.lbl +
                  ' (called in ' + e.file +
                  ' on line ' + str(e.line) + ')',
                  file=sys.stderr)

        sys.exit(1)
