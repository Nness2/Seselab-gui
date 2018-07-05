# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
import linecache
import os
import sys

class Instr:

    def split_infos(self, space, contents):
        text = contents
        size = len(text)
        while size < space:
            text = text + ' '
            size += 1
        return text

    def get_infos (self, program, i):
        takeAll = ''
        file = os.path.basename(program[i][1][0])
        line = program[i][1][1]
        code = linecache.getline(program[i][1][0], line)
        code = code.split(';', 1)[0].strip()
        takeAll = self.split_infos(25, self.format_instr(program[i][0])) + self.split_infos(25, code) + file + ':' + str(line)
        if len(program[i][1]) == 4:
            takeAll += ' (' + program[i][1][3] + ')'
        return takeAll

    def stack_infos(self, program):
        instrs = ['']
        for i in range(1, len(program)):
            instrs.append(self.get_infos(program,i))
        instrs.append("")
        return instrs

    def format_instr (self, instr):
        fmt = instr[0]
        for i in range(1, len(instr)):
            fmt += ' ' + self.format_arg(instr[i])
        return fmt

    def format_arg (self, arg):
        if arg[0] == 'imm':
            return '#' + str(arg[1])
        elif arg[0] == 'reg':
            return 'r' + str(arg[1])
        elif arg[0] == 'mem':
            return '@' + str(arg[1])
        elif arg[0] == 'ref':
            fmt = '!' + self.format_arg(arg[1])
            if len(arg) == 3:
                fmt += ',' + self.format_arg(arg[2])
            return fmt
