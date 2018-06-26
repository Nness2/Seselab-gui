# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
import linecache
import os

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
        code = linecache.getline(file, line)
        code = code.split(';', 1)[0].strip()
        takeAll = self.split_infos(25, self.get_program(program[i][0])) + self.split_infos(25, code) + file + ':' + str(line)
        if len(program[i][1]) == 3:
            takeAll += ' (' + program[i][1][2] + ')'
        return takeAll

    def stack_infos(self, program):
        instrs = ['']
        for i in range(1, len(program)):
            instrs.append(self.get_infos(program,i))
        instrs.append("")
        return instrs

    def get_program (self, program):
        text = ''
        if not isinstance(program, str) is not isinstance(program, int):
            for i in range(len(program)):
                text = text + self.get_program(program[i])
        else :
            if program == 'reg':
                return ' r' + text
            elif program == 'imm':
                return ' #' + text
            elif program == 'mem':
                return ' @' + text
            elif program == 'ref':
                return ' !' + text
            else:
                return str(program)
        text = text.replace('! ','!')
        return text
